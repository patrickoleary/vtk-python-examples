#!/usr/bin/env python

# Color edges of a directed graph using a lookup table. Each edge is assigned
# an integer index that maps to a color in a two-entry lookup table.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkCommonCore import (
    vtkIntArray,
    vtkLookupTable,
)
from vtkmodules.vtkCommonDataModel import vtkMutableDirectedGraph
from vtkmodules.vtkViewsCore import vtkViewTheme
from vtkmodules.vtkInfovisLayout import vtkSimple2DLayoutStrategy
from vtkmodules.vtkViewsInfovis import vtkGraphLayoutView

# Colors (normalized RGBA)
red_rgba = (1.0, 0.0, 0.0, 1.0)
green_rgba = (0.0, 1.0, 0.0, 1.0)

# Graph: three vertices with two directed edges
graph = vtkMutableDirectedGraph()
v1 = graph.AddVertex()
v2 = graph.AddVertex()
v3 = graph.AddVertex()

graph.AddGraphEdge(v1, v2)
graph.AddGraphEdge(v2, v3)

# Edge color array: integer index per edge into the lookup table
edge_colors = vtkIntArray()
edge_colors.SetNumberOfComponents(1)
edge_colors.SetName("Color")
edge_colors.InsertNextValue(0)
edge_colors.InsertNextValue(1)
graph.GetEdgeData().AddArray(edge_colors)

# LookupTable: map edge color indices to actual colors
lookup_table = vtkLookupTable()
lookup_table.SetNumberOfTableValues(2)
lookup_table.SetTableValue(0, red_rgba)
lookup_table.SetTableValue(1, green_rgba)
lookup_table.Build()

# Theme: apply the lookup table to cell (edge) colors
theme = vtkViewTheme()
theme.SetCellLookupTable(lookup_table)

# View: display the graph with colored edges
view = vtkGraphLayoutView()
view.AddRepresentationFromInput(graph)
layout_strategy = vtkSimple2DLayoutStrategy()
layout_strategy.SetRandomSeed(0)
view.SetLayoutStrategy(layout_strategy)
view.SetEdgeColorArrayName("Color")
view.SetEdgeLabelVisibility(True)
view.ColorEdgesOn()
view.ApplyViewTheme(theme)
view.ResetCamera()
view.GetRenderer().GetActiveCamera().Zoom(0.8)
render_window = view.GetRenderWindow()
render_window.SetWindowName("ColorEdges")

# Launch the interactive visualization
view.GetInteractor().Initialize()
view.GetInteractor().Start()
