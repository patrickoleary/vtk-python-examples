#!/usr/bin/env python

# Demonstrate the four gradient background modes available in VTK:
# vertical, horizontal, radial farthest-side, and radial farthest-corner.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkFiltersSources import vtkConeSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
    vtkViewport,
)

# Colors (normalized RGB)
honeydew = (0.941, 1.0, 0.941)
gold = (1.0, 0.843, 0.0)
orange_red = (1.0, 0.271, 0.0)

# Source: generate a cone used in all four viewports
cone = vtkConeSource()
cone.SetResolution(25)
cone.SetDirection(0, 1, 0)
cone.SetHeight(1)

# Mapper: map cone polygon data
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(cone.GetOutputPort())

# Actor: shared cone geometry with a light specular highlight
actor = vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetColor(honeydew)
actor.GetProperty().SetSpecular(0.3)
actor.GetProperty().SetSpecularPower(60.0)

# Gradient modes and viewport layout (2 x 2 grid)
modes = [
    vtkViewport.GradientModes.VTK_GRADIENT_VERTICAL,
    vtkViewport.GradientModes.VTK_GRADIENT_HORIZONTAL,
    vtkViewport.GradientModes.VTK_GRADIENT_RADIAL_VIEWPORT_FARTHEST_SIDE,
    vtkViewport.GradientModes.VTK_GRADIENT_RADIAL_VIEWPORT_FARTHEST_CORNER,
]
viewports = [
    (0.0, 0.0, 0.5, 0.5),
    (0.5, 0.0, 1.0, 0.5),
    (0.0, 0.5, 0.5, 1.0),
    (0.5, 0.5, 1.0, 1.0),
]

# Renderers: one per gradient mode
renderers = []
for i in range(4):
    ren = vtkRenderer()
    ren.AddActor(actor)
    ren.GradientBackgroundOn()
    ren.SetGradientMode(modes[i])
    ren.SetBackground(gold)
    ren.SetBackground2(orange_red)
    ren.SetViewport(viewports[i])
    ren.GetActiveCamera().Azimuth(20)
    ren.GetActiveCamera().Elevation(30)
    ren.ResetCamera()
    renderers.append(ren)

# Window: display the rendered scene
render_window = vtkRenderWindow()
for ren in renderers:
    render_window.AddRenderer(ren)
render_window.SetSize(1024, 1024)
render_window.SetWindowName("GradientBackground")

# Interactor: handle mouse and keyboard events
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window.Render()
interactor.Start()
