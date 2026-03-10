#!/usr/bin/env python

# Share a single camera across four viewports showing different geometry.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkCommonColor import vtkColorSeries
from vtkmodules.vtkFiltersSources import (
    vtkConeSource,
    vtkCubeSource,
    vtkCylinderSource,
    vtkSphereSource,
)
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
tomato_rgb = (1.0, 0.388, 0.278)

# Background colors from a Brewer color series
color_series = vtkColorSeries()
color_series.SetColorSchemeByName("Brewer Qualitative Pastel2")

# Viewport layout: 2x2 grid
xmins = [0.0, 0.5, 0.0, 0.5]
xmaxs = [0.5, 1.0, 0.5, 1.0]
ymins = [0.0, 0.0, 0.5, 0.5]
ymaxs = [0.5, 0.5, 1.0, 1.0]

# Sources: four different geometric primitives
sources = [vtkSphereSource(), vtkConeSource(), vtkCubeSource(), vtkCylinderSource()]

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.SetSize(640, 480)
render_window.SetWindowName("ShareCamera")

# Shared camera reference
shared_camera = None

for i in range(4):
    sources[i].Update()

    mapper = vtkPolyDataMapper()
    mapper.SetInputConnection(sources[i].GetOutputPort())

    actor = vtkActor()
    actor.SetMapper(mapper)
    actor.GetProperty().SetColor(tomato_rgb)

    c = color_series.GetColor(i)
    bg = (c.GetRed() / 255.0, c.GetGreen() / 255.0, c.GetBlue() / 255.0)

    renderer = vtkRenderer()
    renderer.AddActor(actor)
    renderer.SetBackground(bg)
    renderer.SetViewport(xmins[i], ymins[i], xmaxs[i], ymaxs[i])

    if i == 0:
        shared_camera = renderer.GetActiveCamera()
        shared_camera.Azimuth(30)
        shared_camera.Elevation(30)
    else:
        renderer.SetActiveCamera(shared_camera)

    renderer.ResetCamera()
    render_window.AddRenderer(renderer)

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
