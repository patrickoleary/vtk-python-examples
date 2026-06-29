#!/usr/bin/env python
# Demonstrate vtkContourWidget initialized from a circular polydata contour.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

import math

from vtkmodules.vtkCommonCore import vtkPoints
from vtkmodules.vtkCommonDataModel import (
    vtkCellArray,
    vtkPolyData,
)
from vtkmodules.vtkInteractionWidgets import (
    vtkContourWidget,
    vtkOrientedGlyphContourRepresentation,
)
from vtkmodules.vtkRenderingCore import (
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Build a closed circular contour as polydata
num_pts = 20
contour_points = vtkPoints()
contour_lines = vtkCellArray()

line_indices = list(range(num_pts)) + [0]
for i in range(num_pts):
    angle = 2.0 * math.pi * i / num_pts
    contour_points.InsertPoint(i, 0.1 * math.cos(angle), 0.1 * math.sin(angle), 0.0)

contour_lines.InsertNextCell(num_pts + 1, line_indices)

contour_pd = vtkPolyData()
contour_pd.SetPoints(contour_points)
contour_pd.SetLines(contour_lines)

# Renderer
renderer = vtkRenderer()
renderer.SetBackground(0.1, 0.2, 0.4)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("contour widget circular")
render_window.SetSize(600, 600)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Widget
contour_rep = vtkOrientedGlyphContourRepresentation()

contour_widget = vtkContourWidget()
contour_widget.SetInteractor(interactor)
contour_widget.SetRepresentation(contour_rep)
contour_widget.On()
contour_widget.Initialize(contour_pd)
contour_widget.Render()

# Scene
renderer.ResetCamera()

interactor.Initialize()
interactor.Start()
