#!/usr/bin/env python

# Draw an interactive contour on the screen using a contour widget.

import math

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
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

# Colors (normalized RGB)
midnight_blue_rgb = (0.098, 0.098, 0.439)
red_rgb = (1.0, 0.0, 0.0)

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.SetBackground(midnight_blue_rgb)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.SetSize(600, 600)
render_window.SetWindowName("ContourWidget")
render_window.AddRenderer(renderer)

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# ContourWidget: interactive contour drawing
contour_rep = vtkOrientedGlyphContourRepresentation()
contour_rep.GetLinesProperty().SetColor(red_rgb)

contour_widget = vtkContourWidget()
contour_widget.SetInteractor(render_window_interactor)
contour_widget.SetRepresentation(contour_rep)
contour_widget.On()

# Build a circular contour as initial data
num_pts = 21
points = vtkPoints()
for i in range(num_pts):
    angle = 2.0 * math.pi * i / 20.0
    points.InsertPoint(i, 0.1 * math.cos(angle), 0.1 * math.sin(angle), 0.0)

vertex_indices = list(range(num_pts))
vertex_indices.append(0)
lines = vtkCellArray()
lines.InsertNextCell(num_pts + 1, vertex_indices)

pd = vtkPolyData()
pd.SetPoints(points)
pd.SetLines(lines)

contour_widget.Initialize(pd, 1)
contour_widget.Render()
renderer.ResetCamera()

# Launch the interactive visualization
render_window.Render()
render_window_interactor.Initialize()
render_window_interactor.Start()
