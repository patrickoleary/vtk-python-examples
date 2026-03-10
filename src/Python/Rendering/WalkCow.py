#!/usr/bin/env python

# The cow 'walking' around the global origin by composing incremental
# rotations and translations, rendered with EraseOff overlay
# (VTK Textbook figure 3-32).

import os
from pathlib import Path

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkCommonTransforms import vtkTransform
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
reader.Update()

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
render_window.SetWindowName("WalkCow")

# Interactor: handle mouse and keyboard events
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Camera: top-down view for walking animation
bounds = cow_actor.GetBounds()
fp = [(bounds[i * 2 + 1] + bounds[i * 2]) / 2.0 for i in range(3)]
cow_actor.SetOrientation(0, 0, 0)
cow_actor.SetOrigin(0, 0, 0)

cow_transform = vtkTransform()
cow_transform.Identity()
cow_transform.Translate(0, 0, 5)
cow_actor.SetUserMatrix(cow_transform.GetMatrix())

renderer.GetActiveCamera().SetPosition(1, 24, 16)
renderer.GetActiveCamera().SetFocalPoint(fp)
renderer.GetActiveCamera().SetViewUp(0, 0, -1)
renderer.ResetCameraClippingRange()

# Animation: the cow walks around the origin (rotate then translate)
render_window.Render()
render_window.Render()
render_window.EraseOff()
for i in range(1, 7):
    cow_transform.Identity()
    cow_transform.RotateY(i * 60)
    cow_transform.Translate(0, 0, 5)
    cow_actor.SetUserMatrix(cow_transform.GetMatrix())
    render_window.Render()
    render_window.Render()
render_window.EraseOn()

# Launch the interactive visualization
render_window.EraseOff()
interactor.Start()
