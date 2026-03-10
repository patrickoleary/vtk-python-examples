#!/usr/bin/env python

# Display an annotated cube orientation marker alongside a cube actor.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkFiltersSources import vtkCubeSource
from vtkmodules.vtkInteractionWidgets import vtkOrientationMarkerWidget
from vtkmodules.vtkRenderingAnnotation import vtkAnnotatedCubeActor
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
burlywood_rgb = (0.871, 0.722, 0.529)
red_rgb = (1.0, 0.0, 0.0)
cornflower_blue_rgb = (0.392, 0.584, 0.929)
yellow_rgb = (1.0, 1.0, 0.0)
blue_rgb = (0.0, 0.0, 1.0)

# Source: generate a large cube
cube = vtkCubeSource()
cube.SetXLength(200)
cube.SetYLength(200)
cube.SetZLength(200)
cube.Update()

# Mapper: map polygon data to graphics primitives
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(cube.GetOutputPort())

# Actor: assign the mapped geometry
actor = vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetColor(burlywood_rgb)
actor.GetProperty().EdgeVisibilityOn()
actor.GetProperty().SetEdgeColor(red_rgb)

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(cornflower_blue_rgb)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.SetSize(640, 480)
render_window.SetWindowName("OrientationMarkerWidget")
render_window.AddRenderer(renderer)

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# AnnotatedCubeActor: anatomical orientation labels
axes_actor = vtkAnnotatedCubeActor()
axes_actor.SetXPlusFaceText("L")
axes_actor.SetXMinusFaceText("R")
axes_actor.SetYMinusFaceText("I")
axes_actor.SetYPlusFaceText("S")
axes_actor.SetZMinusFaceText("P")
axes_actor.SetZPlusFaceText("A")
axes_actor.GetTextEdgesProperty().SetColor(yellow_rgb)
axes_actor.GetTextEdgesProperty().SetLineWidth(2)
axes_actor.GetCubeProperty().SetColor(blue_rgb)

# OrientationMarkerWidget: display the annotated cube in the viewport corner
om_widget = vtkOrientationMarkerWidget()
om_widget.SetOrientationMarker(axes_actor)
om_widget.SetInteractor(render_window_interactor)
om_widget.EnabledOn()
om_widget.InteractiveOn()
renderer.ResetCamera()

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window.Render()
renderer.GetActiveCamera().Azimuth(45)
renderer.GetActiveCamera().Elevation(30)
render_window.Render()
render_window_interactor.Start()
