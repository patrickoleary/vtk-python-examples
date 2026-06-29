#!/usr/bin/env python

# Visualize combustor flow using ribbon streamlines from a PLOT3D
# dataset with Runge-Kutta 4 integration.

import os

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
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

# Data file path (relative to this script)
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

resolution = 4

# Read PLOT3D combustor dataset
pl3d = vtkMultiBlockPLOT3DReader()
pl3d.SetXYZFileName(os.path.join(data_dir, "combxyz.bin"))
pl3d.SetQFileName(os.path.join(data_dir, "combq.bin"))
pl3d.SetScalarFunctionNumber(100)
pl3d.SetVectorFunctionNumber(202)
pl3d.Update()
output = pl3d.GetOutput().GetBlock(0)

# Seed plane for streamlines
ps = vtkPlaneSource()
ps.SetXResolution(resolution)
ps.SetYResolution(resolution)
ps.SetOrigin(2, -2, 26)
ps.SetPoint1(2, 2, 26)
ps.SetPoint2(2, -2, 32)

ps_mapper = vtkPolyDataMapper()
ps_mapper.SetInputConnection(ps.GetOutputPort())

ps_actor = vtkActor()
ps_actor.SetMapper(ps_mapper)
ps_actor.GetProperty().SetRepresentationToWireframe()

# Stream tracer with RK4 integration
rk4 = vtkRungeKutta4()

streamer = vtkStreamTracer()
streamer.SetInputData(output)
streamer.SetSourceData(ps.GetOutput())
streamer.SetMaximumPropagation(100)
streamer.SetInitialIntegrationStep(0.2)
streamer.SetIntegrationDirectionToForward()
streamer.SetComputeVorticity(1)
streamer.SetIntegrator(rk4)

# Ribbon filter for streamline visualization
rf = vtkRibbonFilter()
rf.SetInputConnection(streamer.GetOutputPort())
rf.SetInputArrayToProcess(1, 0, 0, vtkDataObject.FIELD_ASSOCIATION_POINTS, "Normals")
rf.SetWidth(0.1)
rf.SetWidthFactor(5)

stream_mapper = vtkPolyDataMapper()
stream_mapper.SetInputConnection(rf.GetOutputPort())
stream_mapper.SetScalarRange(output.GetScalarRange())

streamline = vtkActor()
streamline.SetMapper(stream_mapper)

# Outline of structured grid
outline = vtkStructuredGridOutlineFilter()
outline.SetInputData(output)

outline_mapper = vtkPolyDataMapper()
outline_mapper.SetInputConnection(outline.GetOutputPort())

outline_actor = vtkActor()
outline_actor.SetMapper(outline_mapper)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(ps_actor)
renderer.AddActor(outline_actor)
renderer.AddActor(streamline)
renderer.SetBackground(0.1, 0.2, 0.4)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(300, 300)
render_window.SetWindowName("comb streamers")

# Scene
camera = renderer.GetActiveCamera()
camera.SetClippingRange(3.95297, 50)
camera.SetFocalPoint(9.71821, 0.458166, 29.3999)
camera.SetPosition(2.7439, -37.3196, 38.7167)
camera.SetViewUp(-0.16123, 0.264271, 0.950876)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
