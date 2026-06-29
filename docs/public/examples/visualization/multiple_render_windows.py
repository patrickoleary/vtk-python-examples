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

# Window layout parameters
width, height = 300, 300
dx, dy = 20, 40
w, h = width + dx, height + dy

# Mapper: sphere
mapper_0 = vtkPolyDataMapper()
mapper_0.SetInputConnection(sphere.GetOutputPort())

# Actor: sphere
actor_0 = vtkActor()
actor_0.SetMapper(mapper_0)
actor_0.GetProperty().SetColor(bisque)

# Mapper: cone
mapper_1 = vtkPolyDataMapper()
mapper_1.SetInputConnection(cone.GetOutputPort())

# Actor: cone
actor_1 = vtkActor()
actor_1.SetMapper(mapper_1)
actor_1.GetProperty().SetColor(rosy_brown)

# Mapper: cube
mapper_2 = vtkPolyDataMapper()
mapper_2.SetInputConnection(cube.GetOutputPort())

# Actor: cube
actor_2 = vtkActor()
actor_2.SetMapper(mapper_2)
actor_2.GetProperty().SetColor(goldenrod)

# Mapper: cylinder
mapper_3 = vtkPolyDataMapper()
mapper_3.SetInputConnection(cylinder.GetOutputPort())

# Actor: cylinder
actor_3 = vtkActor()
actor_3.SetMapper(mapper_3)
actor_3.GetProperty().SetColor(chocolate)

# Renderer 0: sphere
renderer_0 = vtkRenderer()
renderer_0.AddActor(actor_0)
renderer_0.SetBackground(alice_blue)
renderer_0.ResetCamera()

camera = renderer_0.GetActiveCamera()
camera.Azimuth(30)
camera.Elevation(30)

# Renderer 1: cone
renderer_1 = vtkRenderer()
renderer_1.SetActiveCamera(camera)
renderer_1.AddActor(actor_1)
renderer_1.SetBackground(ghost_white)
renderer_1.ResetCamera()

# Renderer 2: cube
renderer_2 = vtkRenderer()
renderer_2.SetActiveCamera(camera)
renderer_2.AddActor(actor_2)
renderer_2.SetBackground(white_smoke)
renderer_2.ResetCamera()

# Renderer 3: cylinder
renderer_3 = vtkRenderer()
renderer_3.SetActiveCamera(camera)
renderer_3.AddActor(actor_3)
renderer_3.SetBackground(seashell)
renderer_3.ResetCamera()

# Window 0: sphere
render_window_0 = vtkRenderWindow()
render_window_0.AddRenderer(renderer_0)
render_window_0.SetWindowName("MultipleRenderWindows 0")
render_window_0.SetMultiSamples(0)
render_window_0.SetSize(width, height)
render_window_0.SetPosition(0 * w, h - 0 * h)

# Window 1: cone
render_window_1 = vtkRenderWindow()
render_window_1.AddRenderer(renderer_1)
render_window_1.SetWindowName("MultipleRenderWindows 1")
render_window_1.SetMultiSamples(0)
render_window_1.SetSize(width, height)
render_window_1.SetPosition(1 * w, h - 0 * h)

# Window 2: cube
render_window_2 = vtkRenderWindow()
render_window_2.AddRenderer(renderer_2)
render_window_2.SetWindowName("MultipleRenderWindows 2")
render_window_2.SetMultiSamples(0)
render_window_2.SetSize(width, height)
render_window_2.SetPosition(0 * w, h - 1 * h)

# Window 3: cylinder
render_window_3 = vtkRenderWindow()
render_window_3.AddRenderer(renderer_3)
render_window_3.SetWindowName("MultipleRenderWindows 3")
render_window_3.SetMultiSamples(0)
render_window_3.SetSize(width, height)
render_window_3.SetPosition(1 * w, h - 1 * h)

# Interactor 0: sphere
interactor_0 = vtkRenderWindowInteractor()
interactor_0.SetRenderWindow(render_window_0)

# Interactor 1: cone
interactor_1 = vtkRenderWindowInteractor()
interactor_1.SetRenderWindow(render_window_1)

# Interactor 2: cube
interactor_2 = vtkRenderWindowInteractor()
interactor_2.SetRenderWindow(render_window_2)

# Interactor 3: cylinder
interactor_3 = vtkRenderWindowInteractor()
interactor_3.SetRenderWindow(render_window_3)

# Launch the interactive visualization
interactor_0.Initialize()
interactor_0.Start()
