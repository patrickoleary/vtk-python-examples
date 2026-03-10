#!/usr/bin/env python

# Create and label an annotated cube actor with anatomic orientation labels.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkRenderingAnnotation import vtkAnnotatedCubeActor
from vtkmodules.vtkRenderingCore import (
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
wheat = (0.961, 0.871, 0.702)
black = (0.000, 0.000, 0.000)
turquoise = (0.251, 0.878, 0.816)
mint = (0.741, 0.988, 0.788)
tomato = (1.000, 0.388, 0.278)

# Actor: create an annotated cube with anatomic face labels
cube = vtkAnnotatedCubeActor()
cube.SetFaceTextScale(2.0 / 3.0)
cube.SetXPlusFaceText("A")
cube.SetXMinusFaceText("P")
cube.SetYPlusFaceText("L")
cube.SetYMinusFaceText("R")
cube.SetZPlusFaceText("S")
cube.SetZMinusFaceText("I")

cube.GetTextEdgesProperty().SetColor(black)
cube.GetTextEdgesProperty().SetLineWidth(4)
cube.GetXPlusFaceProperty().SetColor(turquoise)
cube.GetXMinusFaceProperty().SetColor(turquoise)
cube.GetYPlusFaceProperty().SetColor(mint)
cube.GetYMinusFaceProperty().SetColor(mint)
cube.GetZPlusFaceProperty().SetColor(tomato)
cube.GetZMinusFaceProperty().SetColor(tomato)

# Renderer: assemble the scene and configure the camera
renderer = vtkRenderer()
renderer.AddActor(cube)
renderer.SetBackground(wheat)

camera = renderer.GetActiveCamera()
camera.SetViewUp(0, 0, 1)
camera.SetFocalPoint(0, 0, 0)
camera.SetPosition(4.5, 4.5, 2.5)
renderer.ResetCamera()
camera.Dolly(1.0)
renderer.ResetCameraClippingRange()

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("AnnotatedCubeActor")
render_window.SetSize(640, 480)

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Start()
