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
from vtkmodules.vtkFiltersSources import vtkGraphToPolyData
from vtkmodules.vtkInfovisLayout import (
    vtkGraphLayout,
    vtkPassThroughLayoutStrategy,
)
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

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

# Filter: pass-through layout (positions already set via vtkPoints)
pass_through_layout_strategy = vtkPassThroughLayoutStrategy()
graph_layout = vtkGraphLayout()
graph_layout.SetInputData(graph)
graph_layout.SetLayoutStrategy(pass_through_layout_strategy)

# Filter: convert graph to polydata for rendering
graph_to_polydata = vtkGraphToPolyData()
graph_to_polydata.SetInputConnection(graph_layout.GetOutputPort())

# Mapper: map vertices with color from the lookup table
vertex_mapper = vtkPolyDataMapper()
vertex_mapper.SetInputConnection(graph_to_polydata.GetOutputPort())
vertex_mapper.SetScalarModeToUsePointFieldData()
vertex_mapper.SelectColorArray("Color")
vertex_mapper.SetLookupTable(lookup_table)
vertex_mapper.SetScalarRange(0, 2)

# Actor: assign the colored vertex/edge geometry
vertex_actor = vtkActor()
vertex_actor.SetMapper(vertex_mapper)
vertex_actor.GetProperty().SetPointSize(10)

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.AddActor(vertex_actor)

# Render window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("color vertices lookup table")
render_window.SetMultiSamples(0)
render_window.SetSize(640, 480)

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Scene: reset camera and zoom
renderer.ResetCamera()
renderer.GetActiveCamera().Zoom(0.8)

# Start: launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
