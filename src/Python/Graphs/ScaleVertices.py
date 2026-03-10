#!/usr/bin/env python

# Scale vertex glyphs by a data array. Two vertices are drawn as circles
# whose size reflects a "Scales" array, and whose color is driven by a
# lookup table.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkCommonCore import (
    vtkFloatArray,
    vtkIntArray,
    vtkLookupTable,
)
from vtkmodules.vtkCommonDataModel import vtkMutableUndirectedGraph
from vtkmodules.vtkRenderingCore import vtkGraphToGlyphs
from vtkmodules.vtkViewsCore import vtkViewTheme
from vtkmodules.vtkViewsInfovis import (
    vtkGraphLayoutView,
    vtkRenderedGraphRepresentation,
)

# Colors (normalized RGBA for LUT, RGB for scene)
yellow_rgba = (1.0, 1.0, 0.0, 1.0)
green_rgba = (0.0, 1.0, 0.0, 1.0)
navy_rgb = (0.0, 0.0, 0.502)
midnight_blue_rgb = (0.098, 0.098, 0.439)

# Graph: two vertices with two parallel edges
graph = vtkMutableUndirectedGraph()
v1 = graph.AddVertex()
v2 = graph.AddVertex()
graph.AddEdge(v1, v2)
graph.AddEdge(v1, v2)

# Scale array: controls the size of vertex glyphs
scales = vtkFloatArray()
scales.SetNumberOfComponents(1)
scales.SetName("Scales")
scales.InsertNextValue(2.0)
scales.InsertNextValue(5.0)
graph.GetVertexData().AddArray(scales)

# Vertex color array: integer index per vertex into the lookup table
vertex_colors = vtkIntArray()
vertex_colors.SetNumberOfComponents(1)
vertex_colors.SetName("Color")
vertex_colors.InsertNextValue(0)
vertex_colors.InsertNextValue(1)
graph.GetVertexData().AddArray(vertex_colors)

# LookupTable: map vertex color indices to actual colors
lookup_table = vtkLookupTable()
lookup_table.SetNumberOfTableValues(2)
lookup_table.SetTableValue(0, yellow_rgba)
lookup_table.SetTableValue(1, green_rgba)
lookup_table.Build()

# Theme: apply the lookup table to point (vertex) colors
theme = vtkViewTheme()
theme.SetPointLookupTable(lookup_table)

# View: display the graph with scaled vertex glyphs
view = vtkGraphLayoutView()
view.SetLayoutStrategyToForceDirected()
view.AddRepresentationFromInput(graph)
view.ApplyViewTheme(theme)
view.ScaledGlyphsOn()
view.SetScalingArrayName("Scales")
view.SetVertexColorArrayName("Color")
view.ColorVerticesOn()

# Representation: set glyph type to circle
vtkRenderedGraphRepresentation.SafeDownCast(
    view.GetRepresentation()
).SetGlyphType(vtkGraphToGlyphs.CIRCLE)

view.ResetCamera()
view.GetRenderer().SetBackground(navy_rgb)
view.GetRenderer().SetBackground2(midnight_blue_rgb)
render_window = view.GetRenderWindow()
render_window.SetWindowName("ScaleVertices")

# Launch the interactive visualization
view.GetInteractor().Initialize()
view.GetInteractor().Start()
