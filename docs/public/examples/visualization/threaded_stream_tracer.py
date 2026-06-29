#!/usr/bin/env python

# Demonstrate vtkStreamTracer with vtkRungeKutta4 integrator on
# PLOT3D combustor data, rendering streamlines as ribbons with
# scalar coloring.

import os

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonDataModel import vtkDataObject
from vtkmodules.vtkCommonMath import vtkRungeKutta4
from vtkmodules.vtkFiltersCore import vtkStructuredGridOutlineFilter
from vtkmodules.vtkFiltersFlowPaths import vtkStreamTracer
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

resolution = 2

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
seed_plane.SetXResolution(resolution)
seed_plane.SetYResolution(resolution)
seed_plane.SetOrigin(2, -2, 26)
seed_plane.SetPoint1(2, 2, 26)
seed_plane.SetPoint2(2, -2, 32)
seed_plane.Update()

seed_plane_mapper = vtkPolyDataMapper()
seed_plane_mapper.SetInputConnection(seed_plane.GetOutputPort())

seed_plane_actor = vtkActor()
seed_plane_actor.SetMapper(seed_plane_mapper)
seed_plane_actor.GetProperty().SetRepresentationToWireframe()

# Stream tracer
rk4 = vtkRungeKutta4()
streamer = vtkStreamTracer()
streamer.SetInputData(output)
streamer.SetSourceData(seed_plane.GetOutput())
streamer.SetMaximumPropagation(100)
streamer.SetInitialIntegrationStep(0.2)
streamer.SetIntegrationDirectionToForward()
streamer.SetComputeVorticity(1)
streamer.SetIntegrator(rk4)
streamer.Update()

# Ribbon filter
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

# Outline
outline = vtkStructuredGridOutlineFilter()
outline.SetInputData(output)

outline_mapper = vtkPolyDataMapper()
outline_mapper.SetInputConnection(outline.GetOutputPort())

outline_actor = vtkActor()
outline_actor.SetMapper(outline_mapper)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(seed_plane_actor)
renderer.AddActor(outline_actor)
renderer.AddActor(streamline)
renderer.SetBackground(0.1, 0.2, 0.4)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(300, 300)
render_window.SetWindowName("threaded stream tracer")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
camera = renderer.GetActiveCamera()
camera.SetClippingRange(3.95297, 50)
camera.SetFocalPoint(9.71821, 0.458166, 29.3999)
camera.SetPosition(2.7439, -37.3196, 38.7167)
camera.SetViewUp(-0.16123, 0.264271, 0.950876)

interactor.Initialize()
interactor.Start()
