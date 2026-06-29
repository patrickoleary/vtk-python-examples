#!/usr/bin/env python

# Demonstrate vtkImprintFilter with point and cell data processing by
# imprinting a cylinder-derived trim loop onto a volume plane, showing
# three renderers for cell data, target-edge interpolation, and imprint-edge
# interpolation of point data.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonDataModel import vtkCylinder, vtkPlane
from vtkmodules.vtkFiltersCore import (
    vtkFlyingEdgesPlaneCutter,
    vtkPointDataToCellData,
    vtkPolyDataPlaneClipper,
)
from vtkmodules.vtkFiltersGeneral import vtkSampleImplicitFunctionFilter
from vtkmodules.vtkFiltersModeling import (
    vtkContourLoopExtraction,
    vtkImprintFilter,
    vtkOutlineFilter,
)
from vtkmodules.vtkFiltersSources import vtkCylinderSource
from vtkmodules.vtkImagingHybrid import vtkSampleFunction
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Control parameters
resolution = 101
cylinder_resolution = 20
coloring = 1
normal = [0, 1.01, 1]

# Sample a cylinder implicit function across a volume
cylinder = vtkCylinder()
cylinder.SetCenter(0.0, 0.0, 0.0)
cylinder.SetRadius(0.25)
cylinder.SetAxis(0, 1, 0)

sample = vtkSampleFunction()
sample.SetImplicitFunction(cylinder)
sample.SetModelBounds(-0.75, 0.75, -1, 1, -0.5, 0.5)
sample.SetSampleDimensions(resolution, resolution, resolution)
sample.ComputeNormalsOff()
sample.SetOutputScalarTypeToFloat()
sample.Update()

# Cut plane
plane = vtkPlane()
plane.SetOrigin(0, 0, 0)
plane.SetNormal(normal)

# Flying edges plane cutter
cut = vtkFlyingEdgesPlaneCutter()
cut.SetInputConnection(sample.GetOutputPort())
cut.SetPlane(plane)
cut.ComputeNormalsOff()
cut.Update()

# Create cell data from point data
point_to_cell = vtkPointDataToCellData()
point_to_cell.SetInputConnection(cut.GetOutputPort())
point_to_cell.PassPointDataOn()
point_to_cell.Update()

# Cylinder shell for trim loop
shell = vtkCylinderSource()
shell.SetCenter(0, 0, 0)
shell.SetResolution(cylinder_resolution)
shell.SetHeight(5)
shell.CappingOff()
shell.Update()

# Clip shell with the plane to get trim loop
clipped_shell = vtkPolyDataPlaneClipper()
clipped_shell.SetInputConnection(shell.GetOutputPort())
clipped_shell.SetPlane(plane)
clipped_shell.ClippingLoopsOn()
clipped_shell.CappingOff()
clipped_shell.Update()

# Sample implicit function on clipping loops
sample_implicit = vtkSampleImplicitFunctionFilter()
sample_implicit.SetInputConnection(clipped_shell.GetOutputPort(1))
sample_implicit.SetImplicitFunction(plane)
sample_implicit.ComputeGradientsOff()
sample_implicit.SetScalarArrayName("scalars")
sample_implicit.Update()

# Build loops from clipping output
build_loops = vtkContourLoopExtraction()
build_loops.SetInputConnection(sample_implicit.GetOutputPort(0))
build_loops.CleanPointsOn()
build_loops.Update()

# Imprint 0: cell data
imprint_0 = vtkImprintFilter()
imprint_0.SetTargetConnection(point_to_cell.GetOutputPort())
imprint_0.SetImprintConnection(build_loops.GetOutputPort())
imprint_0.SetOutputTypeToImprintedRegion()
imprint_0.BoundaryEdgeInsertionOn()
imprint_0.SetTolerance(0.0001)
imprint_0.SetMergeTolerance(0.0005)
imprint_0.PassCellDataOn()
imprint_0.PassPointDataOff()
imprint_0.Update()

imprint_0_mapper = vtkPolyDataMapper()
imprint_0_mapper.SetInputConnection(imprint_0.GetOutputPort())
imprint_0_mapper.SetScalarRange(0, 0.1)

imprint_0_actor = vtkActor()
imprint_0_actor.SetMapper(imprint_0_mapper)

# Imprint 1: point data with target edge interpolation
imprint_1 = vtkImprintFilter()
imprint_1.SetTargetConnection(point_to_cell.GetOutputPort())
imprint_1.SetImprintConnection(build_loops.GetOutputPort())
imprint_1.SetOutputTypeToImprintedRegion()
imprint_1.BoundaryEdgeInsertionOn()
imprint_1.SetTolerance(0.0001)
imprint_1.SetMergeTolerance(0.0005)
imprint_1.PassCellDataOff()
imprint_1.PassPointDataOn()
imprint_1.SetPointInterpolationToTargetEdges()
imprint_1.Update()

imprint_1_mapper = vtkPolyDataMapper()
imprint_1_mapper.SetInputConnection(imprint_1.GetOutputPort())
imprint_1_mapper.SetScalarRange(0, 0.1)
imprint_1_mapper.SetScalarModeToUsePointFieldData()
imprint_1_mapper.SelectColorArray("scalars")

imprint_1_actor = vtkActor()
imprint_1_actor.SetMapper(imprint_1_mapper)

# Imprint 2: point data with imprint edge interpolation
imprint_2 = vtkImprintFilter()
imprint_2.SetTargetConnection(point_to_cell.GetOutputPort())
imprint_2.SetImprintConnection(build_loops.GetOutputPort())
imprint_2.SetOutputTypeToImprintedRegion()
imprint_2.BoundaryEdgeInsertionOn()
imprint_2.SetTolerance(0.0001)
imprint_2.SetMergeTolerance(0.0005)
imprint_2.PassCellDataOff()
imprint_2.PassPointDataOn()
imprint_2.SetPointInterpolationToImprintEdges()
imprint_2.Update()

imprint_2_mapper = vtkPolyDataMapper()
imprint_2_mapper.SetInputConnection(imprint_2.GetOutputPort())
imprint_2_mapper.SetScalarRange(0, 0.1)
imprint_2_mapper.SetScalarModeToUsePointFieldData()
imprint_2_mapper.SelectColorArray("scalars")

imprint_2_actor = vtkActor()
imprint_2_actor.SetMapper(imprint_2_mapper)

# Outline around volume
outline = vtkOutlineFilter()
outline.SetInputConnection(sample.GetOutputPort())

outline_mapper = vtkPolyDataMapper()
outline_mapper.SetInputConnection(outline.GetOutputPort())

outline_actor = vtkActor()
outline_actor.SetMapper(outline_mapper)

# Three renderers sharing a camera
renderer_0 = vtkRenderer()
renderer_0.GetActiveCamera().SetPosition(normal)
renderer_0.SetViewport(0, 0, 0.333, 1.0)
renderer_0.AddActor(outline_actor)
renderer_0.AddActor(imprint_0_actor)

renderer_1 = vtkRenderer()
renderer_1.SetActiveCamera(renderer_0.GetActiveCamera())
renderer_1.SetViewport(0.333, 0, 0.667, 1.0)
renderer_1.AddActor(outline_actor)
renderer_1.AddActor(imprint_1_actor)

renderer_2 = vtkRenderer()
renderer_2.SetActiveCamera(renderer_0.GetActiveCamera())
renderer_2.SetViewport(0.667, 0, 1.0, 1.0)
renderer_2.AddActor(outline_actor)
renderer_2.AddActor(imprint_2_actor)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer_0)
render_window.AddRenderer(renderer_1)
render_window.AddRenderer(renderer_2)
render_window.SetSize(600, 200)
render_window.SetWindowName("imprint with data")

# Scene
renderer_0.ResetCamera()

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
