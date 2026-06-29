#!/usr/bin/env python

# Smooth aliased polylines using vtkWindowedSincPolyDataFilter applied
# to discrete contour edges extracted from a rasterized cross shape,
# displayed in two viewports (original vs smoothed).

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import vtkPoints
from vtkmodules.vtkCommonDataModel import (
    vtkCellArray,
    vtkImageData,
    vtkPolyData,
)
from vtkmodules.vtkCommonTransforms import vtkTransform
from vtkmodules.vtkFiltersCore import (
    vtkStripper,
    vtkWindowedSincPolyDataFilter,
)
from vtkmodules.vtkFiltersGeneral import (
    vtkDiscreteFlyingEdges2D,
    vtkTransformPolyDataFilter,
)
from vtkmodules.vtkFiltersModeling import vtkContourLoopExtraction
from vtkmodules.vtkImagingColor import vtkImageQuantizeRGBToIndex
from vtkmodules.vtkImagingCore import vtkImageExtractComponents
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
    vtkWindowToImageFilter,
)

# Create synthetic aliased cross shape
cross_polydata = vtkPolyData()
cross_points = vtkPoints()
polys = vtkCellArray()

cross_points.SetNumberOfPoints(12)
cross_points.SetPoint(0, 1, -4, 0)
cross_points.SetPoint(1, 1, -1, 0)
cross_points.SetPoint(2, 4, -1, 0)
cross_points.SetPoint(3, 4, 1, 0)
cross_points.SetPoint(4, 1, 1, 0)
cross_points.SetPoint(5, 1, 4, 0)
cross_points.SetPoint(6, -1, 4, 0)
cross_points.SetPoint(7, -1, 1, 0)
cross_points.SetPoint(8, -4, 1, 0)
cross_points.SetPoint(9, -4, -1, 0)
cross_points.SetPoint(10, -1, -1, 0)
cross_points.SetPoint(11, -1, -4, 0)

polys.InsertNextCell(4)
polys.InsertCellPoint(1)
polys.InsertCellPoint(4)
polys.InsertCellPoint(7)
polys.InsertCellPoint(10)

polys.InsertNextCell(4)
polys.InsertCellPoint(11)
polys.InsertCellPoint(0)
polys.InsertCellPoint(1)
polys.InsertCellPoint(10)

polys.InsertNextCell(4)
polys.InsertCellPoint(1)
polys.InsertCellPoint(2)
polys.InsertCellPoint(3)
polys.InsertCellPoint(4)

polys.InsertNextCell(4)
polys.InsertCellPoint(4)
polys.InsertCellPoint(5)
polys.InsertCellPoint(6)
polys.InsertCellPoint(7)

polys.InsertNextCell(4)
polys.InsertCellPoint(7)
polys.InsertCellPoint(8)
polys.InsertCellPoint(9)
polys.InsertCellPoint(10)

cross_polydata.SetPoints(cross_points)
cross_polydata.SetPolys(polys)

# Rotate cross to enhance aliasing
transform = vtkTransform()
transform.RotateZ(17)
transform.Translate(0.1, 0, 0)

transform_filter = vtkTransformPolyDataFilter()
transform_filter.SetInputData(cross_polydata)
transform_filter.SetTransform(transform)

# Rasterize the cross through a temporary renderer/window
cross_mapper = vtkPolyDataMapper()
cross_mapper.SetInputConnection(transform_filter.GetOutputPort())

cross_actor = vtkActor()
cross_actor.SetMapper(cross_mapper)
cross_actor.GetProperty().SetColor(1, 0, 0)

raster_renderer = vtkRenderer()
raster_renderer.SetBackground(1, 1, 1)
raster_renderer.AddActor(cross_actor)

raster_window = vtkRenderWindow()
raster_window.AddRenderer(raster_renderer)
raster_window.SetMultiSamples(0)
raster_window.SetSize(50, 50)
raster_window.Render()

# Capture rasterized image
ren_source = vtkWindowToImageFilter()
ren_source.SetInput(raster_window)
ren_source.Update()

# Decouple pipeline
output = ren_source.GetOutput()
rasterized_image = vtkImageData()
rasterized_image.DeepCopy(output)

# Extract RGB components
extract = vtkImageExtractComponents()
extract.SetInputData(rasterized_image)
extract.SetComponents(0, 1, 2)

# Quantize to index
quantize = vtkImageQuantizeRGBToIndex()
quantize.SetInputConnection(extract.GetOutputPort())
quantize.SetNumberOfColors(3)

# Create discrete polylines from quantized image
discrete = vtkDiscreteFlyingEdges2D()
discrete.SetInputConnection(quantize.GetOutputPort())
discrete.SetValue(0, 2)

# Create contour loops (polylines)
poly_loops = vtkContourLoopExtraction()
poly_loops.SetInputConnection(discrete.GetOutputPort())
poly_loops.SetOutputModeToPolylines()

# Display original polylines
poly_mapper = vtkPolyDataMapper()
poly_mapper.SetInputConnection(poly_loops.GetOutputPort())

poly_actor = vtkActor()
poly_actor.SetMapper(poly_mapper)
poly_actor.GetProperty().SetColor(0, 1, 0)

# Smooth the discrete polylines
line_strip = vtkStripper()
line_strip.SetInputConnection(discrete.GetOutputPort())

smoother = vtkWindowedSincPolyDataFilter()
smoother.SetInputConnection(line_strip.GetOutputPort())
smoother.SetNumberOfIterations(50)
smoother.SetEdgeAngle(90)
smoother.SetWindowFunctionToHamming()

smooth_mapper = vtkPolyDataMapper()
smooth_mapper.SetInputConnection(smoother.GetOutputPort())

smooth_actor = vtkActor()
smooth_actor.SetMapper(smooth_mapper)
smooth_actor.GetProperty().SetColor(0, 1, 0)

# Renderers
renderer_0 = vtkRenderer()
renderer_0.SetViewport(0, 0, 0.5, 1.0)
renderer_0.SetBackground(1, 1, 1)
renderer_0.AddActor(poly_actor)

renderer_1 = vtkRenderer()
renderer_1.SetViewport(0.5, 0, 1.0, 1.0)
renderer_1.SetBackground(1, 1, 1)
renderer_1.AddActor(smooth_actor)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer_0)
render_window.AddRenderer(renderer_1)
render_window.SetMultiSamples(0)
render_window.SetSize(300, 150)
render_window.SetWindowName("windowed sinc polyline smoothing")

# Scene
renderer_1.SetActiveCamera(renderer_0.GetActiveCamera())
renderer_0.ResetCamera()

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
