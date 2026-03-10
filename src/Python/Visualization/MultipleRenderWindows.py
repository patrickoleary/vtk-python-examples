#!/usr/bin/env python

# Display four geometric objects in separate render windows sharing one camera.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
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
alice_blue = (0.941, 0.973, 1.000)
ghost_white = (0.973, 0.973, 1.000)
white_smoke = (0.961, 0.961, 0.961)
seashell = (1.000, 0.961, 0.933)
bisque = (1.000, 0.894, 0.769)
rosy_brown = (0.737, 0.561, 0.561)
goldenrod = (0.855, 0.647, 0.125)
chocolate = (0.824, 0.412, 0.118)

# Sources: create four geometric objects
sphere = vtkSphereSource()
sphere.SetCenter(0.0, 0.0, 0.0)

cone = vtkConeSource()
cone.SetCenter(0.0, 0.0, 0.0)
cone.SetDirection(0, 1, 0)

cube = vtkCubeSource()
cube.SetCenter(0.0, 0.0, 0.0)

cylinder = vtkCylinderSource()
cylinder.SetCenter(0.0, 0.0, 0.0)

sources = [sphere, cone, cube, cylinder]
backgrounds = [alice_blue, ghost_white, white_smoke, seashell]
actor_colors = [bisque, rosy_brown, goldenrod, chocolate]

# Window layout parameters
width, height = 300, 300
dx, dy = 20, 40
w, h = width + dx, height + dy

camera = None
interactors = []

for i in range(4):
    # Renderer: each window gets its own renderer
    renderer = vtkRenderer()

    if i == 0:
        camera = renderer.GetActiveCamera()
        camera.Azimuth(30)
        camera.Elevation(30)
    else:
        renderer.SetActiveCamera(camera)

    # ---- Mapper: map polygon data to graphics primitives ----
    mapper = vtkPolyDataMapper()
    mapper.SetInputConnection(sources[i].GetOutputPort())

    # ---- Actor: assign the mapped geometry ----
    actor = vtkActor()
    actor.SetMapper(mapper)
    actor.GetProperty().SetColor(actor_colors[i])

    renderer.AddActor(actor)
    renderer.SetBackground(backgrounds[i])
    renderer.ResetCamera()

    # ---- Window: display the rendered scene ----
    render_window = vtkRenderWindow()
    render_window.AddRenderer(renderer)
    render_window.SetSize(width, height)
    render_window.SetWindowName(f"MultipleRenderWindows {i}")
    render_window.SetPosition((i % 2) * w, h - (i // 2) * h)

    # ---- Interactor: handle mouse and keyboard events ----
    render_window_interactor = vtkRenderWindowInteractor()
    render_window_interactor.SetRenderWindow(render_window)
    interactors.append(render_window_interactor)

# Launch the interactive visualization
interactors[0].Start()
