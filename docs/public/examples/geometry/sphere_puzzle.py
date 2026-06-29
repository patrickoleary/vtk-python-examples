#!/usr/bin/env python

# Demonstrate vtkSpherePuzzle and vtkSpherePuzzleArrows by creating a sphere
# puzzle, performing horizontal and vertical moves, and rendering with arrows.

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
render_window.SetWindowName("sphere puzzle")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
camera = renderer.GetActiveCamera()
camera.Elevation(-40)

# Functional render and puzzle moves
render_window.Render()

puzzle.MoveHorizontal(0, 100, 0)
puzzle.MoveHorizontal(1, 100, 1)
puzzle.MoveHorizontal(2, 100, 0)
puzzle.MoveVertical(2, 100, 0)
puzzle.MoveVertical(1, 100, 0)

interactor.Initialize()
interactor.Start()
