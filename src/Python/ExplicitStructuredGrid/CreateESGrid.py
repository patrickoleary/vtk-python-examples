#!/usr/bin/env python

# Create an explicit structured grid, convert it to an unstructured grid
# and back, demonstrating the round-trip conversion workflow.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
import numpy as np
from vtkmodules.vtkCommonCore import vtkPoints
from vtkmodules.vtkCommonDataModel import (
    vtkCellArray,
    vtkExplicitStructuredGrid,
)
from vtkmodules.vtkFiltersCore import (
    vtkExplicitStructuredGridToUnstructuredGrid,
    vtkUnstructuredGridToExplicitStructuredGrid,
)
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkDataSetMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
seashell_rgb = (1.0, 0.961, 0.933)
background_rgb = (0.184, 0.310, 0.310)

# Grid dimensions and spacing
ni, nj, nk = 5, 6, 7
si, sj, sk = 20, 10, 1

# Points: generate grid vertices
points = vtkPoints()
for z in range(0, nk * sk, sk):
    for y in range(0, nj * sj, sj):
        for x in range(0, ni * si, si):
            points.InsertNextPoint((x, y, z))

# Cells: define hexahedral cells using multi-index mapping
cells = vtkCellArray()
for k in range(nk - 1):
    for j in range(nj - 1):
        for i in range(ni - 1):
            multi_index = ([i, i + 1, i + 1, i, i, i + 1, i + 1, i],
                           [j, j, j + 1, j + 1, j, j, j + 1, j + 1],
                           [k, k, k, k, k + 1, k + 1, k + 1, k + 1])
            pts = np.ravel_multi_index(multi_index, (ni, nj, nk), order='F')
            cells.InsertNextCell(8, pts)

# Explicit structured grid: assemble the grid
grid = vtkExplicitStructuredGrid()
grid.SetDimensions(ni, nj, nk)
grid.SetPoints(points)
grid.SetCells(cells)

# Convert: explicit structured grid → unstructured grid
to_unstructured = vtkExplicitStructuredGridToUnstructuredGrid()
to_unstructured.SetInputData(grid)
to_unstructured.Update()

# Convert: unstructured grid → explicit structured grid (round-trip)
to_explicit = vtkUnstructuredGridToExplicitStructuredGrid()
to_explicit.SetInputData(to_unstructured.GetOutput())
to_explicit.SetInputArrayToProcess(0, 0, 0, 1, "BLOCK_I")
to_explicit.SetInputArrayToProcess(1, 0, 0, 1, "BLOCK_J")
to_explicit.SetInputArrayToProcess(2, 0, 0, 1, "BLOCK_K")
to_explicit.Update()
result_grid = to_explicit.GetOutput()

# Mapper: map the grid to graphics primitives
mapper = vtkDataSetMapper()
mapper.SetInputData(result_grid)

# Actor: assign the mapped geometry with visible edges
actor = vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().EdgeVisibilityOn()
actor.GetProperty().LightingOff()
actor.GetProperty().SetColor(seashell_rgb)

# Renderer: assemble the scene and configure the camera
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(background_rgb)
camera = renderer.GetActiveCamera()
camera.SetPosition(8.383354, -72.468670, 94.262605)
camera.SetFocalPoint(42.295234, 21.111537, -0.863606)
camera.SetViewUp(0.152863, 0.676710, 0.720206)
camera.SetDistance(137.681759)
camera.SetClippingRange(78.173985, 211.583658)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(640, 480)
render_window.SetWindowName("CreateESGrid")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
