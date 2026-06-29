#!/usr/bin/env python

# Towers of Hanoi puzzle: animate the full solution from initial to final state.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkCommonCore import vtkMinimalStandardRandomSequence
from vtkmodules.vtkFiltersSources import (
    vtkCylinderSource,
    vtkPlaneSource,
)
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkCamera,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
papaya_whip_rgb = (1.0, 0.937, 0.835)
saddle_brown_rgb = (0.545, 0.271, 0.075)
lavender_rgb = (0.902, 0.902, 0.980)

# Puzzle parameters
num_pucks = 5
num_steps = 5
puck_resolution = 48
L = 1.0
R = 0.5
r_min = 4.0 * R
r_max = 12.0 * R
D = 1.1 * 1.25 * r_max
H = 1.1 * num_pucks * L
num_moves = 0
peg_stack = [[], [], []]

# Source/Mapper: peg geometry (thin cylinder)
peg_geometry = vtkCylinderSource()
peg_geometry.SetResolution(8)
peg_mapper = vtkPolyDataMapper()
peg_mapper.SetInputConnection(peg_geometry.GetOutputPort())

# Source/Mapper: puck geometry (wider cylinder)
puck_geometry = vtkCylinderSource()
puck_geometry.SetResolution(puck_resolution)
puck_mapper = vtkPolyDataMapper()
puck_mapper.SetInputConnection(puck_geometry.GetOutputPort())

# Source/Mapper: table geometry (plane)
table_geometry = vtkPlaneSource()
table_geometry.SetResolution(10, 10)
table_mapper = vtkPolyDataMapper()
table_mapper.SetInputConnection(table_geometry.GetOutputPort())

# Actor: table surface
table = vtkActor()
table.SetMapper(table_mapper)
table.GetProperty().SetColor(saddle_brown_rgb)
table.AddPosition(D, 0, 0)
table.SetScale(4 * D, 2 * D, 3 * D)
table.RotateX(90)

# Actor: peg 0
peg_0 = vtkActor()
peg_0.SetMapper(peg_mapper)
peg_0.GetProperty().SetColor(lavender_rgb)
peg_0.AddPosition(0 * D, H / 2, 0)
peg_0.SetScale(1, H, 1)

# Actor: peg 1
peg_1 = vtkActor()
peg_1.SetMapper(peg_mapper)
peg_1.GetProperty().SetColor(lavender_rgb)
peg_1.AddPosition(1 * D, H / 2, 0)
peg_1.SetScale(1, H, 1)

# Actor: peg 2
peg_2 = vtkActor()
peg_2.SetMapper(peg_mapper)
peg_2.GetProperty().SetColor(lavender_rgb)
peg_2.AddPosition(2 * D, H / 2, 0)
peg_2.SetScale(1, H, 1)

# Actors: pucks stacked on peg 0 with random colors
rng = vtkMinimalStandardRandomSequence()
rng.SetSeed(1)

puck_0_r = rng.GetValue(); rng.Next()
puck_0_g = rng.GetValue(); rng.Next()
puck_0_b = rng.GetValue(); rng.Next()
puck_0 = vtkActor()
puck_0.SetMapper(puck_mapper)
puck_0.GetProperty().SetColor(puck_0_r, puck_0_g, puck_0_b)
puck_0.AddPosition(0, 0 * L + L / 2, 0)
puck_0.SetScale(r_max - 0 * (r_max - r_min) / (num_pucks - 1), 1, r_max - 0 * (r_max - r_min) / (num_pucks - 1))

puck_1_r = rng.GetValue(); rng.Next()
puck_1_g = rng.GetValue(); rng.Next()
puck_1_b = rng.GetValue(); rng.Next()
puck_1 = vtkActor()
puck_1.SetMapper(puck_mapper)
puck_1.GetProperty().SetColor(puck_1_r, puck_1_g, puck_1_b)
puck_1.AddPosition(0, 1 * L + L / 2, 0)
puck_1.SetScale(r_max - 1 * (r_max - r_min) / (num_pucks - 1), 1, r_max - 1 * (r_max - r_min) / (num_pucks - 1))

puck_2_r = rng.GetValue(); rng.Next()
puck_2_g = rng.GetValue(); rng.Next()
puck_2_b = rng.GetValue(); rng.Next()
puck_2 = vtkActor()
puck_2.SetMapper(puck_mapper)
puck_2.GetProperty().SetColor(puck_2_r, puck_2_g, puck_2_b)
puck_2.AddPosition(0, 2 * L + L / 2, 0)
puck_2.SetScale(r_max - 2 * (r_max - r_min) / (num_pucks - 1), 1, r_max - 2 * (r_max - r_min) / (num_pucks - 1))

puck_3_r = rng.GetValue(); rng.Next()
puck_3_g = rng.GetValue(); rng.Next()
puck_3_b = rng.GetValue(); rng.Next()
puck_3 = vtkActor()
puck_3.SetMapper(puck_mapper)
puck_3.GetProperty().SetColor(puck_3_r, puck_3_g, puck_3_b)
puck_3.AddPosition(0, 3 * L + L / 2, 0)
puck_3.SetScale(r_max - 3 * (r_max - r_min) / (num_pucks - 1), 1, r_max - 3 * (r_max - r_min) / (num_pucks - 1))

puck_4_r = rng.GetValue(); rng.Next()
puck_4_g = rng.GetValue(); rng.Next()
puck_4_b = rng.GetValue(); rng.Next()
puck_4 = vtkActor()
puck_4.SetMapper(puck_mapper)
puck_4.GetProperty().SetColor(puck_4_r, puck_4_g, puck_4_b)
puck_4.AddPosition(0, 4 * L + L / 2, 0)
puck_4.SetScale(r_max - 4 * (r_max - r_min) / (num_pucks - 1), 1, r_max - 4 * (r_max - r_min) / (num_pucks - 1))

pucks = [puck_0, puck_1, puck_2, puck_3, puck_4]
peg_stack[0] = [puck_0, puck_1, puck_2, puck_3, puck_4]

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.AddActor(table)
renderer.AddActor(peg_0)
renderer.AddActor(peg_1)
renderer.AddActor(peg_2)
renderer.AddActor(puck_0)
renderer.AddActor(puck_1)
renderer.AddActor(puck_2)
renderer.AddActor(puck_3)
renderer.AddActor(puck_4)
renderer.SetBackground(papaya_whip_rgb)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("hanoi")
render_window.SetMultiSamples(0)
render_window.SetSize(1200, 750)

# Scene: configure camera
camera = vtkCamera()
camera.SetPosition(41.0433, 27.9637, 30.442)
camera.SetFocalPoint(11.5603, -1.51931, 0.95899)
camera.SetClippingRange(18.9599, 91.6042)
camera.SetViewUp(0, 1, 0)
renderer.SetActiveCamera(camera)

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

render_window.Render()


def move_puck(peg1, peg2):
    global num_moves
    num_moves += 1
    moving_actor = peg_stack[peg1].pop()
    dist_up = (H - (L * (len(peg_stack[peg1]) - 1)) + r_max) / num_steps
    for _i in range(num_steps):
        moving_actor.AddPosition(0, dist_up, 0)
        render_window.Render()
    dist_across = (peg2 - peg1) * D / num_steps
    flip_angle = 180.0 / num_steps
    for _i in range(num_steps):
        moving_actor.AddPosition(dist_across, 0, 0)
        moving_actor.RotateX(flip_angle)
        render_window.Render()
    dist_down = ((L * (len(peg_stack[peg2]) - 1)) - H - r_max) / num_steps
    for _i in range(num_steps):
        moving_actor.AddPosition(0, dist_down, 0)
        render_window.Render()
    peg_stack[peg2].append(moving_actor)


def hanoi(n, src, dst, aux):
    if n == 1:
        move_puck(src, dst)
    else:
        hanoi(n - 1, src, aux, dst)
        move_puck(src, dst)
        hanoi(n - 1, aux, dst, src)


# Animate: solve the full puzzle (peg 0 → peg 1)
hanoi(num_pucks, 0, 1, 2)
render_window.Render()

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
