#!/usr/bin/env python

# Demonstrate vtkCookieCutter with point and cell data processing by
# cutting a volume plane with a cylinder-derived trim loop, showing
# three renderers for cell data, mesh-edge interpolation, and loop-edge
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
    vtkCookieCutter,
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
normal = [0.1, 1, 0.8]

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
build_loops.Update()

# Cookie cutter 0: cell data
cookie_0 = vtkCookieCutter()
cookie_0.SetInputConnection(point_to_cell.GetOutputPort())
cookie_0.SetLoopsConnection(build_loops.GetOutputPort())
cookie_0.PassCellDataOn()
cookie_0.PassPointDataOff()
cookie_0.Update()

cookie_0_mapper = vtkPolyDataMapper()
cookie_0_mapper.SetInputConnection(cookie_0.GetOutputPort())
cookie_0_mapper.SetScalarRange(0, 0.1)

cookie_0_actor = vtkActor()
cookie_0_actor.SetMapper(cookie_0_mapper)

# Cookie cutter 1: point data with mesh edge interpolation
cookie_1 = vtkCookieCutter()
cookie_1.SetInputConnection(point_to_cell.GetOutputPort())
cookie_1.SetLoopsConnection(build_loops.GetOutputPort())
cookie_1.PassCellDataOff()
cookie_1.PassPointDataOn()
cookie_1.SetPointInterpolationToMeshEdges()
cookie_1.Update()

cookie_1_mapper = vtkPolyDataMapper()
cookie_1_mapper.SetInputConnection(cookie_1.GetOutputPort())
cookie_1_mapper.SetScalarRange(0, 0.1)
cookie_1_mapper.SetScalarModeToUsePointFieldData()
cookie_1_mapper.SelectColorArray("scalars")

cookie_1_actor = vtkActor()
cookie_1_actor.SetMapper(cookie_1_mapper)

# Cookie cutter 2: point data with loop edge interpolation
cookie_2 = vtkCookieCutter()
cookie_2.SetInputConnection(point_to_cell.GetOutputPort())
cookie_2.SetLoopsConnection(build_loops.GetOutputPort())
cookie_2.PassCellDataOff()
cookie_2.PassPointDataOn()
cookie_2.SetPointInterpolationToLoopEdges()
cookie_2.Update()

cookie_2_mapper = vtkPolyDataMapper()
cookie_2_mapper.SetInputConnection(cookie_2.GetOutputPort())
cookie_2_mapper.SetScalarRange(0, 0.1)
cookie_2_mapper.SetScalarModeToUsePointFieldData()
cookie_2_mapper.SelectColorArray("scalars")

cookie_2_actor = vtkActor()
cookie_2_actor.SetMapper(cookie_2_mapper)

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

renderer_1 = vtkRenderer()
renderer_1.SetActiveCamera(renderer_0.GetActiveCamera())
renderer_1.SetViewport(0.333, 0, 0.667, 1.0)

renderer_2 = vtkRenderer()
renderer_2.SetActiveCamera(renderer_0.GetActiveCamera())
renderer_2.SetViewport(0.667, 0, 1.0, 1.0)

renderer_0.AddActor(outline_actor)
renderer_0.AddActor(cookie_0_actor)

renderer_1.AddActor(outline_actor)
renderer_1.AddActor(cookie_1_actor)

renderer_2.AddActor(outline_actor)
renderer_2.AddActor(cookie_2_actor)


# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer_0)
render_window.AddRenderer(renderer_1)
render_window.AddRenderer(renderer_2)
render_window.SetSize(600, 200)
render_window.SetWindowName("cookie cutter with data")

# Scene
renderer_0.ResetCamera()

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
