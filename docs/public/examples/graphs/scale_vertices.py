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
from vtkmodules.vtkFiltersCore import vtkGlyph3D
from vtkmodules.vtkFiltersSources import (
    vtkGlyphSource2D,
    vtkGraphToPolyData,
)
from vtkmodules.vtkInfovisLayout import (
    vtkForceDirectedLayoutStrategy,
    vtkGraphLayout,
)
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
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

# Filter: layout the graph vertices in 2D
force_directed_layout_strategy = vtkForceDirectedLayoutStrategy()
graph_layout = vtkGraphLayout()
graph_layout.SetInputData(graph)
graph_layout.SetLayoutStrategy(force_directed_layout_strategy)

# Filter: convert graph to polydata for rendering
graph_to_polydata = vtkGraphToPolyData()
graph_to_polydata.SetInputConnection(graph_layout.GetOutputPort())

# Glyph source: circle glyph for vertices
circle_source = vtkGlyphSource2D()
circle_source.SetGlyphTypeToCircle()
circle_source.SetScale(0.1)
circle_source.FilledOn()
circle_source.Update()

# Glyph filter: place scaled circles at each vertex
vertex_glyph = vtkGlyph3D()
vertex_glyph.SetInputConnection(graph_to_polydata.GetOutputPort())
vertex_glyph.SetSourceConnection(circle_source.GetOutputPort())
vertex_glyph.SetScaleModeToScaleByScalar()
vertex_glyph.SetInputArrayToProcess(0, 0, 0, 0, "Scales")

# Mapper: map vertex glyphs with color from the lookup table
vertex_mapper = vtkPolyDataMapper()
vertex_mapper.SetInputConnection(vertex_glyph.GetOutputPort())
vertex_mapper.SetScalarModeToUsePointFieldData()
vertex_mapper.SelectColorArray("Color")
vertex_mapper.SetLookupTable(lookup_table)
vertex_mapper.SetScalarRange(0, 1)

# Actor: assign the vertex glyphs
vertex_actor = vtkActor()
vertex_actor.SetMapper(vertex_mapper)

# Mapper: map edge lines to graphics primitives
edge_mapper = vtkPolyDataMapper()
edge_mapper.SetInputConnection(graph_to_polydata.GetOutputPort())
edge_mapper.ScalarVisibilityOff()

# Actor: assign the edge geometry
edge_actor = vtkActor()
edge_actor.SetMapper(edge_mapper)

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.AddActor(edge_actor)
renderer.AddActor(vertex_actor)
renderer.SetBackground(navy_rgb)
renderer.SetBackground2(midnight_blue_rgb)
renderer.GradientBackgroundOn()

# Render window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("scale vertices")
render_window.SetMultiSamples(0)
render_window.SetSize(640, 480)

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Scene: reset camera
renderer.ResetCamera()

# Start: launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
