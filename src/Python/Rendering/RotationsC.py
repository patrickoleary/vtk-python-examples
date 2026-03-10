#!/usr/bin/env python

# Six incremental rotations of the cow model about the Z axis,
# rendered with EraseOff so all orientations overlap (VTK Textbook
# figure 3-31c).

import os
from pathlib import Path

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkFiltersGeneral import vtkAxes
from vtkmodules.vtkIOGeometry import vtkBYUReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
wheat = (0.961, 0.871, 0.702)
background = (0.102, 0.200, 0.400)

# Data directory
data_dir = Path(os.environ.get("VPE_DATA_DIR", Path(__file__).parent))

# Reader: load the cow geometry
reader = vtkBYUReader()
reader.SetGeometryFileName(str(data_dir / "cow.g"))

# Mapper: map cow polygon data
cow_mapper = vtkPolyDataMapper()
cow_mapper.SetInputConnection(reader.GetOutputPort())
cow_mapper.ScalarVisibilityOff()

# Actor: the cow model
cow_actor = vtkActor()
cow_actor.SetMapper(cow_mapper)
cow_actor.GetProperty().SetColor(wheat)

# Source: axes for orientation reference
axes_source = vtkAxes()
axes_source.SetScaleFactor(10)
axes_source.SetOrigin(0, 0, 0)

axes_mapper = vtkPolyDataMapper()
axes_mapper.SetInputConnection(axes_source.GetOutputPort())

axes_actor = vtkActor()
axes_actor.SetMapper(axes_mapper)

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.AddActor(cow_actor)
renderer.AddActor(axes_actor)
renderer.SetBackground(background)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(640, 480)
render_window.SetWindowName("RotationsC")

# Interactor: handle mouse and keyboard events
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Camera: front view along Z to show Z-axis rotation
renderer.ResetCamera()
bounds = cow_actor.GetBounds()
fp = [(bounds[i * 2 + 1] + bounds[i * 2]) / 2.0 for i in range(3)]
renderer.GetActiveCamera().SetPosition(2, 0, 25)
renderer.GetActiveCamera().SetFocalPoint(fp)
renderer.GetActiveCamera().SetViewUp(0, 1, 0)
renderer.ResetCameraClippingRange()

# Animation: six 60° rotations about Z with EraseOff overlay
render_window.Render()
render_window.Render()
render_window.EraseOff()
for _ in range(6):
    cow_actor.RotateZ(60)
    render_window.Render()
    render_window.Render()
render_window.EraseOn()

# Launch the interactive visualization
render_window.EraseOff()
interactor.Start()
