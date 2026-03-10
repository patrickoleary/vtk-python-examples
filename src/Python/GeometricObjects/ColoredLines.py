#!/usr/bin/env python

# Display two lines from a common origin, each with a different color,
# using per-cell scalar coloring on a vtkPolyData.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkCommonCore import (
    vtkPoints,
    vtkUnsignedCharArray,
)
from vtkmodules.vtkCommonDataModel import (
    vtkCellArray,
    vtkLine,
    vtkPolyData,
)
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB and unsigned char)
slate_gray_background_rgb = (0.439, 0.502, 0.565)
tomato_uc = (255, 99, 71)
mint_uc = (189, 252, 201)

# Data: define three points — an origin and two endpoints
points = vtkPoints()
points.InsertNextPoint(0.0, 0.0, 0.0)
points.InsertNextPoint(1.0, 0.0, 0.0)
points.InsertNextPoint(0.0, 1.0, 0.0)

# Create the first line (origin to p0)
line0 = vtkLine()
line0.GetPointIds().SetId(0, 0)
line0.GetPointIds().SetId(1, 1)

# Create the second line (origin to p1)
line1 = vtkLine()
line1.GetPointIds().SetId(0, 0)
line1.GetPointIds().SetId(1, 2)

# Store lines in a cell array
lines = vtkCellArray()
lines.InsertNextCell(line0)
lines.InsertNextCell(line1)

# Per-cell colors: one RGB tuple per line
cell_colors = vtkUnsignedCharArray()
cell_colors.SetNumberOfComponents(3)
cell_colors.InsertNextTypedTuple(tomato_uc)
cell_colors.InsertNextTypedTuple(mint_uc)

# Assemble polydata with points, lines, and per-cell colors
lines_poly_data = vtkPolyData()
lines_poly_data.SetPoints(points)
lines_poly_data.SetLines(lines)
lines_poly_data.GetCellData().SetScalars(cell_colors)

# Mapper: map polydata to graphics primitives
mapper = vtkPolyDataMapper()
mapper.SetInputData(lines_poly_data)

# Actor: set line width for visibility
actor = vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetLineWidth(4)

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(slate_gray_background_rgb)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("ColoredLines")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
