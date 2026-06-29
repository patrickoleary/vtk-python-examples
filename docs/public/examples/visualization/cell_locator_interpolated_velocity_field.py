#!/usr/bin/env python

# Demonstrate vtkStreamTracer with different cell locator strategies
# (vtkCellTreeLocator and vtkStaticCellLocator) for interpolated
# velocity field on PLOT3D combustor data, side by side.

import os

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonDataModel import (
    vtkCellLocatorStrategy,
    vtkCellTreeLocator,
    vtkDataObject,
    vtkStaticCellLocator,
)
from vtkmodules.vtkCommonMath import vtkRungeKutta4
from vtkmodules.vtkFiltersCore import vtkStructuredGridOutlineFilter
from vtkmodules.vtkFiltersFlowPaths import (
    vtkCompositeInterpolatedVelocityField,
    vtkStreamTracer,
)
from vtkmodules.vtkFiltersModeling import vtkRibbonFilter
from vtkmodules.vtkFiltersSources import vtkPlaneSource
from vtkmodules.vtkIOParallel import vtkMultiBlockPLOT3DReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Read PLOT3D data
plot3d_reader = vtkMultiBlockPLOT3DReader()
plot3d_reader.SetXYZFileName(os.path.join(data_dir, "combxyz.bin"))
plot3d_reader.SetQFileName(os.path.join(data_dir, "combq.bin"))
plot3d_reader.SetScalarFunctionNumber(100)
plot3d_reader.SetVectorFunctionNumber(202)
plot3d_reader.Update()
output = plot3d_reader.GetOutput().GetBlock(0)

# Seed plane
seed_plane = vtkPlaneSource()
seed_plane.SetXResolution(4)
seed_plane.SetYResolution(4)
seed_plane.SetOrigin(2, -2, 26)
seed_plane.SetPoint1(2, 2, 26)
seed_plane.SetPoint2(2, -2, 32)

seed_plane_mapper = vtkPolyDataMapper()
seed_plane_mapper.SetInputConnection(seed_plane.GetOutputPort())

seed_plane_actor = vtkActor()
seed_plane_actor.SetMapper(seed_plane_mapper)
seed_plane_actor.GetProperty().SetRepresentationToWireframe()

# Stream tracer with vtkCellTreeLocator
rk4 = vtkRungeKutta4()

tree_loc = vtkCellTreeLocator()
ivp = vtkCompositeInterpolatedVelocityField()
cell_locator_strategy = vtkCellLocatorStrategy()
ivp.SetFindCellStrategy(cell_locator_strategy)
cell_locator_strategy.SetCellLocator(tree_loc)

streamer = vtkStreamTracer()
streamer.SetInputData(output)
streamer.SetSourceData(seed_plane.GetOutput())
streamer.SetMaximumPropagation(100)
streamer.SetInitialIntegrationStep(0.2)
streamer.SetIntegrationDirectionToForward()
streamer.SetComputeVorticity(1)
streamer.SetIntegrator(rk4)
streamer.SetInterpolatorPrototype(ivp)

ribbon_filter = vtkRibbonFilter()
ribbon_filter.SetInputConnection(streamer.GetOutputPort())
ribbon_filter.SetInputArrayToProcess(
    1, 0, 0, vtkDataObject.FIELD_ASSOCIATION_POINTS, "Normals")
ribbon_filter.SetWidth(0.1)
ribbon_filter.SetWidthFactor(5)

stream_mapper = vtkPolyDataMapper()
stream_mapper.SetInputConnection(ribbon_filter.GetOutputPort())
stream_mapper.SetScalarRange(output.GetScalarRange())

streamline = vtkActor()
streamline.SetMapper(stream_mapper)

outline = vtkStructuredGridOutlineFilter()
outline.SetInputData(output)

outline_mapper = vtkPolyDataMapper()
outline_mapper.SetInputConnection(outline.GetOutputPort())

outline_actor = vtkActor()
outline_actor.SetMapper(outline_mapper)

# Stream tracer with vtkStaticCellLocator
static_loc = vtkStaticCellLocator()
ivp_2 = vtkCompositeInterpolatedVelocityField()
cell_locator_strategy_2 = vtkCellLocatorStrategy()
ivp_2.SetFindCellStrategy(cell_locator_strategy_2)
cell_locator_strategy_2.SetCellLocator(static_loc)

streamer_2 = vtkStreamTracer()
streamer_2.SetInputData(output)
streamer_2.SetSourceData(seed_plane.GetOutput())
streamer_2.SetMaximumPropagation(100)
streamer_2.SetInitialIntegrationStep(0.2)
streamer_2.SetIntegrationDirectionToForward()
streamer_2.SetComputeVorticity(1)
streamer_2.SetIntegrator(rk4)
streamer_2.SetInterpolatorPrototype(ivp_2)
streamer_2.Update()

ribbon_filter_2 = vtkRibbonFilter()
ribbon_filter_2.SetInputConnection(streamer_2.GetOutputPort())
ribbon_filter_2.SetInputArrayToProcess(
    1, 0, 0, vtkDataObject.FIELD_ASSOCIATION_POINTS, "Normals")
ribbon_filter_2.SetWidth(0.1)
ribbon_filter_2.SetWidthFactor(5)

stream_mapper_2 = vtkPolyDataMapper()
stream_mapper_2.SetInputConnection(ribbon_filter_2.GetOutputPort())
stream_mapper_2.SetScalarRange(output.GetScalarRange())

streamline_2 = vtkActor()
streamline_2.SetMapper(stream_mapper_2)

outline_2 = vtkStructuredGridOutlineFilter()
outline_2.SetInputData(output)

outline_mapper_2 = vtkPolyDataMapper()
outline_mapper_2.SetInputConnection(outline_2.GetOutputPort())

outline_actor_2 = vtkActor()
outline_actor_2.SetMapper(outline_mapper_2)

# Left renderer - CellTreeLocator
renderer_0 = vtkRenderer()
renderer_0.SetViewport(0, 0, 0.5, 1)
renderer_0.AddActor(seed_plane_actor)
renderer_0.AddActor(outline_actor)
renderer_0.AddActor(streamline)
renderer_0.SetBackground(0.1, 0.2, 0.4)

# Right renderer - StaticCellLocator
renderer_1 = vtkRenderer()
renderer_1.SetViewport(0.5, 0, 1, 1)
renderer_1.AddActor(seed_plane_actor)
renderer_1.AddActor(outline_actor_2)
renderer_1.AddActor(streamline_2)
renderer_1.SetBackground(0.1, 0.2, 0.4)

# Window
render_window = vtkRenderWindow()
render_window.SetSize(600, 300)
render_window.AddRenderer(renderer_0)
render_window.AddRenderer(renderer_1)
render_window.SetWindowName("cell locator interpolated velocity field")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
camera = renderer_0.GetActiveCamera()
camera.SetClippingRange(3.95297, 50)
camera.SetFocalPoint(9.71821, 0.458166, 29.3999)
camera.SetPosition(2.7439, -37.3196, 38.7167)
camera.SetViewUp(-0.16123, 0.264271, 0.950876)
renderer_1.SetActiveCamera(camera)

interactor.Initialize()
interactor.Start()
