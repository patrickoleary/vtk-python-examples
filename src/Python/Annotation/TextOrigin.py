#!/usr/bin/env python

# Demonstrate 3D text annotation using vtkVectorText and vtkFollower
# to label the origin of a coordinate axes display.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkFiltersGeneral import vtkAxes
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkFollower,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)
from vtkmodules.vtkRenderingFreeType import vtkVectorText

# Colors (normalized RGB)
peacock_rgb = (0.2, 0.631, 0.788)
background_rgb = (0.753, 0.753, 0.753)

# Source: generate XYZ axes at the origin
axes = vtkAxes()
axes.SetOrigin(0, 0, 0)

# Mapper: map axes polydata to graphics primitives
axes_mapper = vtkPolyDataMapper()
axes_mapper.SetInputConnection(axes.GetOutputPort())

# Actor: assign the axes geometry
axes_actor = vtkActor()
axes_actor.SetMapper(axes_mapper)

# Text source: create 3D vector text spelling "Origin"
text_source = vtkVectorText()
text_source.SetText("Origin")

# Mapper: map the text polydata to graphics primitives
text_mapper = vtkPolyDataMapper()
text_mapper.SetInputConnection(text_source.GetOutputPort())

# Follower: position the 3D text so it always faces the active camera
text_actor = vtkFollower()
text_actor.SetMapper(text_mapper)
text_actor.SetScale(0.2, 0.2, 0.2)
text_actor.AddPosition(0, -0.1, 0)
text_actor.GetProperty().SetColor(peacock_rgb)

# Renderer: assemble the scene and configure the camera
renderer = vtkRenderer()
renderer.AddActor(axes_actor)
renderer.AddActor(text_actor)
renderer.SetBackground(background_rgb)
renderer.ResetCamera()
renderer.GetActiveCamera().Zoom(1.6)
renderer.ResetCameraClippingRange()
text_actor.SetCamera(renderer.GetActiveCamera())

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(640, 480)
render_window.SetWindowName("TextOrigin")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
