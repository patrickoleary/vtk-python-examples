#!/usr/bin/env python

# Demonstrate vtkSpherePuzzle and vtkSpherePuzzleArrows with interactive
# button callback that moves a puzzle piece and updates arrow permutations.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersModeling import vtkSpherePuzzle, vtkSpherePuzzleArrows
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Create puzzle
puzzle = vtkSpherePuzzle()

mapper = vtkPolyDataMapper()
mapper.SetInputConnection(puzzle.GetOutputPort())

actor = vtkActor()
actor.SetMapper(mapper)

# Create arrows
arrows = vtkSpherePuzzleArrows()

mapper_2 = vtkPolyDataMapper()
mapper_2.SetInputConnection(arrows.GetOutputPort())

actor_2 = vtkActor()
actor_2.SetMapper(mapper_2)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.AddActor(actor_2)
renderer.SetBackground(0.1, 0.2, 0.4)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(400, 400)
render_window.SetWindowName("sphere puzzle arrows")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
camera = renderer.GetActiveCamera()
camera.Elevation(-40)

# Functional render needed for coordinate picking
render_window.Render()

# Simulate a button press at screen position (261, 272)
window_y = 400
x = 261
y = window_y - 272
z = renderer.GetZ(x, y)
renderer.SetDisplayPoint(x, y, z)
renderer.DisplayToWorld()
world_point = renderer.GetWorldPoint()
point_x = world_point[0]
point_y = world_point[1]
point_z = world_point[2]

# Animate the puzzle move
i = 0
while i <= 100:
    puzzle.SetPoint(point_x, point_y, point_z)
    puzzle.MovePoint(i)
    render_window.Render()
    i += 5

# Update arrow permutations
arrows.SetPermutation(puzzle)

interactor.Initialize()
interactor.Start()
