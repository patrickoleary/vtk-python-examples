#!/usr/bin/env python

# Demonstrate vtkExtractTensorComponents extracting scalar, vector,
# and texture coordinate components from a point load tensor field,
# with contour visualization and context plane.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersCore import (
    vtkContourFilter,
    vtkProbeFilter,
)
from vtkmodules.vtkFiltersExtraction import vtkExtractTensorComponents
from vtkmodules.vtkFiltersGeometry import vtkImageDataGeometryFilter
from vtkmodules.vtkFiltersModeling import vtkOutlineFilter
from vtkmodules.vtkFiltersSources import vtkConeSource
from vtkmodules.vtkImagingHybrid import vtkPointLoad
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkCamera,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Point load source
pt_load = vtkPointLoad()
pt_load.SetLoadValue(100.0)
pt_load.SetSampleDimensions(30, 30, 30)
pt_load.ComputeEffectiveStressOn()
pt_load.SetModelBounds(-10, 10, -10, 10, -10, 10)

# Extract tensor components
extract_tensor = vtkExtractTensorComponents()
extract_tensor.SetInputConnection(pt_load.GetOutputPort())
extract_tensor.ScalarIsEffectiveStress()
extract_tensor.ScalarIsComponent()
extract_tensor.ExtractScalarsOn()
extract_tensor.ExtractVectorsOn()
extract_tensor.ExtractNormalsOff()
extract_tensor.ExtractTCoordsOn()

# Contour at zero
contour = vtkContourFilter()
contour.SetInputConnection(extract_tensor.GetOutputPort())
contour.SetValue(0, 0)

# Probe contour with original tensor field
probe = vtkProbeFilter()
probe.SetInputConnection(contour.GetOutputPort())
probe.SetSourceConnection(pt_load.GetOutputPort())

s1_mapper = vtkPolyDataMapper()
s1_mapper.SetInputConnection(probe.GetOutputPort())

s1_actor = vtkActor()
s1_actor.SetMapper(s1_mapper)

# Context plane from image data geometry
geometry_filter = vtkImageDataGeometryFilter()
geometry_filter.SetInputConnection(pt_load.GetOutputPort())
geometry_filter.SetExtent(0, 100, 0, 100, 0, 0)
geometry_filter.Update()

geometry_mapper = vtkPolyDataMapper()
geometry_mapper.SetInputConnection(geometry_filter.GetOutputPort())
geometry_mapper.SetScalarRange(geometry_filter.GetOutput().GetScalarRange())

geometry_actor = vtkActor()
geometry_actor.SetMapper(geometry_mapper)

s1_mapper.SetScalarRange(geometry_filter.GetOutput().GetScalarRange())

# Outline
outline = vtkOutlineFilter()
outline.SetInputConnection(pt_load.GetOutputPort())

outline_mapper = vtkPolyDataMapper()
outline_mapper.SetInputConnection(outline.GetOutputPort())

outline_actor = vtkActor()
outline_actor.SetMapper(outline_mapper)
outline_actor.GetProperty().SetColor(0, 0, 0)

# Cone indicating load application
cone_source = vtkConeSource()
cone_source.SetRadius(0.5)
cone_source.SetHeight(2)

cone_mapper = vtkPolyDataMapper()
cone_mapper.SetInputConnection(cone_source.GetOutputPort())

cone_actor = vtkActor()
cone_actor.SetMapper(cone_mapper)
cone_actor.SetPosition(0, 0, 11)
cone_actor.RotateY(90)
cone_actor.GetProperty().SetColor(1, 0, 0)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(s1_actor)
renderer.AddActor(outline_actor)
renderer.AddActor(cone_actor)
renderer.AddActor(geometry_actor)
renderer.SetBackground(1.0, 1.0, 1.0)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(300, 300)
render_window.SetWindowName("extract tensors")

# Scene
camera = vtkCamera()
camera.SetFocalPoint(0.113766, -1.13665, -1.01919)
camera.SetPosition(-29.4886, -63.1488, 26.5807)
camera.SetViewAngle(24.4617)
camera.SetViewUp(0.17138, 0.331163, 0.927879)
camera.SetClippingRange(1, 100)
renderer.SetActiveCamera(camera)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
