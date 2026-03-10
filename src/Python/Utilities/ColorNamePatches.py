#!/usr/bin/env python

# Visualize a grid of named VTK colors as flat colored squares.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkCommonColor import vtkNamedColors
from vtkmodules.vtkCommonCore import vtkPoints
from vtkmodules.vtkCommonDataModel import (
    vtkCellArray,
    vtkPolyData,
)
from vtkmodules.vtkCommonCore import vtkUnsignedCharArray
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
colors = vtkNamedColors()

# Collect all named colors, sorted alphabetically.
# GetColorNames() returns a newline-separated string of all color names.
color_names = sorted(colors.GetColorNames().split("\n"))

# Grid layout parameters
cols = 20
rows = (len(color_names) + cols - 1) // cols
pad = 0.05
cell_w = 1.0
cell_h = 1.0

# Build a polydata with one quad per color
points = vtkPoints()
cells = vtkCellArray()
cell_colors = vtkUnsignedCharArray()
cell_colors.SetNumberOfComponents(3)
cell_colors.SetName("Colors")

for idx, name in enumerate(color_names):
    col = idx % cols
    row = rows - 1 - idx // cols

    x0 = col * (cell_w + pad)
    y0 = row * (cell_h + pad)
    x1 = x0 + cell_w
    y1 = y0 + cell_h

    pid = points.GetNumberOfPoints()
    points.InsertNextPoint(x0, y0, 0.0)
    points.InsertNextPoint(x1, y0, 0.0)
    points.InsertNextPoint(x1, y1, 0.0)
    points.InsertNextPoint(x0, y1, 0.0)

    cells.InsertNextCell(4)
    cells.InsertCellPoint(pid)
    cells.InsertCellPoint(pid + 1)
    cells.InsertCellPoint(pid + 2)
    cells.InsertCellPoint(pid + 3)

    rgba = [0, 0, 0, 0]
    colors.GetColor(name, rgba)
    cell_colors.InsertNextTuple3(rgba[0], rgba[1], rgba[2])

poly_data = vtkPolyData()
poly_data.SetPoints(points)
poly_data.SetPolys(cells)
poly_data.GetCellData().SetScalars(cell_colors)

# Mapper: map the colored quads to graphics primitives
mapper = vtkPolyDataMapper()
mapper.SetInputData(poly_data)
mapper.SetScalarModeToUseCellData()

# Actor: display the color patch grid
actor = vtkActor()
actor.SetMapper(mapper)

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(0.2, 0.2, 0.2)
renderer.ResetCamera()

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(1200, 800)
render_window.SetWindowName("ColorNamePatches")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
