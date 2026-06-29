#!/usr/bin/env python

# Test creating and resizing offscreen render windows.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Create offscreen render window
render_window = vtkRenderWindow()
render_window.SetShowWindow(False)
render_window.SetUseOffScreenBuffers(True)
render_window.SetSize(300, 300)

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

renderer = vtkRenderer()
renderer.SetBackground(0.3, 0.3, 0.3)
render_window.AddRenderer(renderer)

sphere = vtkSphereSource()

mapper = vtkPolyDataMapper()
mapper.SetInputConnection(sphere.GetOutputPort())

actor = vtkActor()
actor.SetMapper(mapper)
renderer.AddActor(actor)

# Scene
renderer.ResetCamera()

# Pipeline exception: initial offscreen render before resize
render_window.Render()

# Resize and render again
render_window.SetSize(400, 300)
render_window.SetWindowName("offscreen resize")

# Pipeline exception: re-render after resize
render_window.Render()

interactor.Initialize()
interactor.Start()
