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
from vtkmodules.vtkFiltersSources import vtkGraphToPolyData
from vtkmodules.vtkInfovisLayout import (
    vtkGraphLayout,
    vtkSimple2DLayoutStrategy,
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

# Filter: layout the graph vertices in 2D
layout_strategy = vtkSimple2DLayoutStrategy()
layout_strategy.SetRandomSeed(0)
graph_layout = vtkGraphLayout()
graph_layout.SetInputData(graph)
graph_layout.SetLayoutStrategy(layout_strategy)

# Filter: convert graph to polydata for rendering
graph_to_polydata = vtkGraphToPolyData()
graph_to_polydata.SetInputConnection(graph_layout.GetOutputPort())

# Mapper: map edge lines with color from the lookup table
edge_mapper = vtkPolyDataMapper()
edge_mapper.SetInputConnection(graph_to_polydata.GetOutputPort())
edge_mapper.SetScalarModeToUseCellFieldData()
edge_mapper.SelectColorArray("Color")
edge_mapper.SetLookupTable(lookup_table)
edge_mapper.SetScalarRange(0, 1)

# Actor: assign the colored edge geometry
edge_actor = vtkActor()
edge_actor.SetMapper(edge_mapper)

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.AddActor(edge_actor)

# Render window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("color edges")
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
