#!/usr/bin/env python

# Visualize combustor flow with streamlines seeded from a plane.

import os
from pathlib import Path

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkFiltersCore import vtkStructuredGridOutlineFilter
from vtkmodules.vtkFiltersFlowPaths import vtkStreamTracer
from vtkmodules.vtkFiltersSources import vtkPlaneSource
from vtkmodules.vtkIOParallel import vtkMultiBlockPLOT3DReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
midnight_blue = (0.098, 0.098, 0.439)
white = (1.0, 1.0, 1.0)

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

# Source: planar seed grid for streamlines
seeds = vtkPlaneSource()
seeds.SetXResolution(4)
seeds.SetYResolution(4)
seeds.SetOrigin(2, -2, 26)
seeds.SetPoint1(2, 2, 26)
seeds.SetPoint2(2, -2, 32)

# Filter: trace streamlines forward through the flow field
streamline = vtkStreamTracer()
streamline.SetInputData(sg)
streamline.SetSourceConnection(seeds.GetOutputPort())
streamline.SetMaximumPropagation(200)
streamline.SetInitialIntegrationStep(0.2)
streamline.SetIntegrationDirectionToForward()

streamline_mapper = vtkPolyDataMapper()
streamline_mapper.SetInputConnection(streamline.GetOutputPort())

streamline_actor = vtkActor()
streamline_actor.SetMapper(streamline_mapper)

# Filter: outline around the data
outline = vtkStructuredGridOutlineFilter()
outline.SetInputData(sg)

outline_mapper = vtkPolyDataMapper()
outline_mapper.SetInputConnection(outline.GetOutputPort())

outline_actor = vtkActor()
outline_actor.SetMapper(outline_mapper)
outline_actor.GetProperty().SetColor(white)

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.AddActor(streamline_actor)
renderer.AddActor(outline_actor)
renderer.SetBackground(midnight_blue)
renderer.GetActiveCamera().SetPosition(-32.8, -12.3, 46.3)
renderer.GetActiveCamera().SetFocalPoint(8.3, 0.03, 29.8)
renderer.GetActiveCamera().SetViewUp(0.2, 0.5, 0.9)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("StreamLines")
render_window.SetSize(640, 480)

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Start()
