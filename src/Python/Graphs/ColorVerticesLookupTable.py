#!/usr/bin/env python

# Color vertices of a directed graph using a lookup table. Each vertex is
# assigned an integer index that maps to a color in a three-entry lookup table.
# Vertex positions are set explicitly via vtkPoints.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkCommonCore import (
    vtkIntArray,
    vtkLookupTable,
    vtkPoints,
)
from vtkmodules.vtkCommonDataModel import vtkMutableDirectedGraph
from vtkmodules.vtkViewsCore import vtkViewTheme
from vtkmodules.vtkViewsInfovis import vtkGraphLayoutView

# Colors (normalized RGBA)
red_rgba = (1.0, 0.0, 0.0, 1.0)
white_rgba = (1.0, 1.0, 1.0, 1.0)
green_rgba = (0.0, 1.0, 0.0, 1.0)

# Graph: three vertices with two directed edges
graph = vtkMutableDirectedGraph()
v1 = graph.AddVertex()
v2 = graph.AddVertex()
v3 = graph.AddVertex()
graph.AddEdge(v1, v2)
graph.AddEdge(v2, v3)

# Points: manually position the vertices along the x-axis
points = vtkPoints()
points.InsertNextPoint(0, 0, 0)
points.InsertNextPoint(1, 0, 0)
points.InsertNextPoint(2, 0, 0)
graph.SetPoints(points)

# Vertex color array: integer index per vertex into the lookup table
vertex_colors = vtkIntArray()
vertex_colors.SetNumberOfComponents(1)
vertex_colors.SetName("Color")
vertex_colors.InsertNextValue(0)
vertex_colors.InsertNextValue(1)
vertex_colors.InsertNextValue(2)
graph.GetVertexData().AddArray(vertex_colors)

# LookupTable: map vertex color indices to actual colors
lookup_table = vtkLookupTable()
lookup_table.SetNumberOfTableValues(3)
lookup_table.SetTableValue(0, red_rgba)
lookup_table.SetTableValue(1, white_rgba)
lookup_table.SetTableValue(2, green_rgba)
lookup_table.Build()

# Theme: apply the lookup table to point (vertex) colors
theme = vtkViewTheme()
theme.SetPointLookupTable(lookup_table)

# View: display the graph with colored vertices
view = vtkGraphLayoutView()
view.AddRepresentationFromInput(graph)
view.SetLayoutStrategyToPassThrough()
view.SetVertexColorArrayName("Color")
view.ColorVerticesOn()
view.ApplyViewTheme(theme)
view.ResetCamera()
view.GetRenderer().GetActiveCamera().Zoom(0.8)
render_window = view.GetRenderWindow()
render_window.SetWindowName("ColorVerticesLookupTable")

# Launch the interactive visualization
view.GetInteractor().Initialize()
view.GetInteractor().Start()
