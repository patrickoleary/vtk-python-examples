#!/usr/bin/env python

# Construct and render two tetrahedra using vtkTetra in separate
# vtkUnstructuredGrids that share the same point set.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkCommonCore import vtkPoints
from vtkmodules.vtkCommonDataModel import (
    VTK_TETRA,
    vtkCellArray,
    vtkTetra,
    vtkUnstructuredGrid,
)
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkDataSetMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
cyan_rgb = (0.0, 1.0, 1.0)
yellow_rgb = (1.0, 1.0, 0.0)
dark_green_background_rgb = (0.0, 0.392, 0.0)

# Data: eight points shared by both tetrahedra
points = vtkPoints()
points.InsertNextPoint(0, 0, 0)
points.InsertNextPoint(1, 0, 0)
points.InsertNextPoint(1, 1, 0)
points.InsertNextPoint(0, 1, 1)
points.InsertNextPoint(2, 2, 2)
points.InsertNextPoint(3, 2, 2)
points.InsertNextPoint(3, 3, 2)
points.InsertNextPoint(2, 3, 3)

# First tetrahedron: points 0-3
tetra1 = vtkTetra()
tetra1.GetPointIds().SetId(0, 0)
tetra1.GetPointIds().SetId(1, 1)
tetra1.GetPointIds().SetId(2, 2)
tetra1.GetPointIds().SetId(3, 3)

cell_array1 = vtkCellArray()
cell_array1.InsertNextCell(tetra1)

unstructured_grid1 = vtkUnstructuredGrid()
unstructured_grid1.SetPoints(points)
unstructured_grid1.SetCells(VTK_TETRA, cell_array1)

# Second tetrahedron: points 4-7
tetra2 = vtkTetra()
tetra2.GetPointIds().SetId(0, 4)
tetra2.GetPointIds().SetId(1, 5)
tetra2.GetPointIds().SetId(2, 6)
tetra2.GetPointIds().SetId(3, 7)

cell_array2 = vtkCellArray()
cell_array2.InsertNextCell(tetra2)

unstructured_grid2 = vtkUnstructuredGrid()
unstructured_grid2.SetPoints(points)
unstructured_grid2.SetCells(VTK_TETRA, cell_array2)

# Mapper and actor: first tetrahedron (cyan)
mapper1 = vtkDataSetMapper()
mapper1.SetInputData(unstructured_grid1)

actor1 = vtkActor()
actor1.SetMapper(mapper1)
actor1.GetProperty().SetColor(cyan_rgb)

# Mapper and actor: second tetrahedron (yellow)
mapper2 = vtkDataSetMapper()
mapper2.SetInputData(unstructured_grid2)

actor2 = vtkActor()
actor2.SetMapper(mapper2)
actor2.GetProperty().SetColor(yellow_rgb)

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.AddActor(actor1)
renderer.AddActor(actor2)
renderer.SetBackground(dark_green_background_rgb)
renderer.ResetCamera()
renderer.GetActiveCamera().Azimuth(-10)
renderer.GetActiveCamera().Elevation(-20)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("Tetrahedron")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
