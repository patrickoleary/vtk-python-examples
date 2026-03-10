#!/usr/bin/env python

# Visualize combustor flow with a stream surface generated from a rake of seed points.

import os
from pathlib import Path

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkCommonMath import vtkRungeKutta4
from vtkmodules.vtkFiltersCore import vtkStructuredGridOutlineFilter
from vtkmodules.vtkFiltersFlowPaths import vtkStreamTracer
from vtkmodules.vtkFiltersModeling import vtkRuledSurfaceFilter
from vtkmodules.vtkFiltersSources import vtkLineSource
from vtkmodules.vtkIOParallel import vtkMultiBlockPLOT3DReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
slate_gray = (0.439, 0.502, 0.565)
black = (0.0, 0.0, 0.0)
tomato = (1.0, 0.388, 0.278)

# Data directory
data_dir = Path(os.environ.get("VPE_DATA_DIR", Path(__file__).parent))

# Reader: load PLOT3D combustor dataset
pl3d = vtkMultiBlockPLOT3DReader()
pl3d.SetXYZFileName(str(data_dir / "combxyz.bin"))
pl3d.SetQFileName(str(data_dir / "combq.bin"))
pl3d.SetScalarFunctionNumber(100)
pl3d.SetVectorFunctionNumber(202)
pl3d.Update()

sg = pl3d.GetOutput().GetBlock(0)

# Source: rake of seed points as a line across the inlet
rake = vtkLineSource()
rake.SetPoint1(2.0, -2.0, 28.0)
rake.SetPoint2(2.0, 2.0, 28.0)
rake.SetResolution(20)

# Filter: trace streamlines forward from the rake using RK4
rk4 = vtkRungeKutta4()

streamer = vtkStreamTracer()
streamer.SetInputData(sg)
streamer.SetSourceConnection(rake.GetOutputPort())
streamer.SetMaximumPropagation(200)
streamer.SetInitialIntegrationStep(0.2)
streamer.SetIntegrationDirectionToForward()
streamer.SetComputeVorticity(1)
streamer.SetIntegrator(rk4)

# Filter: ruled surface connecting adjacent streamlines
surface = vtkRuledSurfaceFilter()
surface.SetInputConnection(streamer.GetOutputPort())
surface.SetOffset(0)
surface.SetOnRatio(2)
surface.PassLinesOn()
surface.SetRuledModeToResample()
surface.SetResolution(50, 1)
surface.CloseSurfaceOff()

surface_mapper = vtkPolyDataMapper()
surface_mapper.SetInputConnection(surface.GetOutputPort())
surface_mapper.SetScalarRange(sg.GetScalarRange())

surface_actor = vtkActor()
surface_actor.SetMapper(surface_mapper)

# Filter: outline around the structured grid
outline = vtkStructuredGridOutlineFilter()
outline.SetInputData(sg)

outline_mapper = vtkPolyDataMapper()
outline_mapper.SetInputConnection(outline.GetOutputPort())

outline_actor = vtkActor()
outline_actor.SetMapper(outline_mapper)
outline_actor.GetProperty().SetColor(black)

# Rake actor for context
rake_mapper = vtkPolyDataMapper()
rake_mapper.SetInputConnection(rake.GetOutputPort())

rake_actor = vtkActor()
rake_actor.SetMapper(rake_mapper)
rake_actor.GetProperty().SetColor(tomato)
rake_actor.GetProperty().SetLineWidth(3.0)

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.AddActor(surface_actor)
renderer.AddActor(outline_actor)
renderer.AddActor(rake_actor)
renderer.SetBackground(slate_gray)
renderer.GetActiveCamera().SetClippingRange(3.95, 50)
renderer.GetActiveCamera().SetFocalPoint(8.9, 0.6, 29.3)
renderer.GetActiveCamera().SetPosition(-12.3, 31.7, 41.2)
renderer.GetActiveCamera().SetViewUp(0.06, -0.32, 0.95)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("StreamSurface")
render_window.SetSize(640, 480)

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Start()
