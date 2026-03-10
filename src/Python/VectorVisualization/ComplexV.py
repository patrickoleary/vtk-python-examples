#!/usr/bin/env python

# Visualize the carotid artery vector field using a hedgehog plot.

import os
from pathlib import Path

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkCommonCore import vtkLookupTable
from vtkmodules.vtkFiltersCore import vtkHedgeHog
from vtkmodules.vtkFiltersModeling import vtkOutlineFilter
from vtkmodules.vtkIOLegacy import vtkStructuredPointsReader
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

# Data directory
data_dir = Path(os.environ.get("VPE_DATA_DIR", Path(__file__).parent))

# Reader: load carotid artery velocity field
reader = vtkStructuredPointsReader()
reader.SetFileName(str(data_dir / "carotid.vtk"))

# Filter: hedgehog plot — oriented and scaled lines at each point
hhog = vtkHedgeHog()
hhog.SetInputConnection(reader.GetOutputPort())
hhog.SetScaleFactor(0.3)

# Lookup table: default color mapping
lut = vtkLookupTable()
lut.Build()

# Mapper: color hedgehog lines by scalar
hhog_mapper = vtkPolyDataMapper()
hhog_mapper.SetInputConnection(hhog.GetOutputPort())
hhog_mapper.SetScalarRange(50, 550)
hhog_mapper.SetLookupTable(lut)

# Actor: display the hedgehog
hhog_actor = vtkActor()
hhog_actor.SetMapper(hhog_mapper)

# Filter: outline around the data
outline = vtkOutlineFilter()
outline.SetInputConnection(reader.GetOutputPort())

outline_mapper = vtkPolyDataMapper()
outline_mapper.SetInputConnection(outline.GetOutputPort())

outline_actor = vtkActor()
outline_actor.SetMapper(outline_mapper)
outline_actor.GetProperty().SetColor(black)

# Renderer: assemble the scene and configure the camera
renderer = vtkRenderer()
renderer.AddActor(outline_actor)
renderer.AddActor(hhog_actor)
renderer.SetBackground(slate_gray)
renderer.GetActiveCamera().SetFocalPoint(0, 0, 0)
renderer.GetActiveCamera().SetPosition(1, 0, 0)
renderer.GetActiveCamera().SetViewUp(0, 0, 1)
renderer.ResetCamera()
renderer.GetActiveCamera().Azimuth(60)
renderer.GetActiveCamera().Elevation(30)
renderer.GetActiveCamera().Dolly(1.1)
renderer.ResetCameraClippingRange()

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("ComplexV")
render_window.SetSize(640, 480)

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Start()
