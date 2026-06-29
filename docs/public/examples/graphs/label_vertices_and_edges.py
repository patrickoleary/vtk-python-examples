#!/usr/bin/env python

# Label both vertices and edges of an undirected graph. Vertices are labelled
# with integer IDs and edges with floating-point weights, using a circular
# layout strategy.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkCommonCore import (
    vtkDoubleArray,
    vtkIntArray,
)
from vtkmodules.vtkCommonDataModel import vtkMutableUndirectedGraph
from vtkmodules.vtkFiltersSources import vtkGraphToPolyData
from vtkmodules.vtkInfovisLayout import (
    vtkCircularLayoutStrategy,
    vtkGraphLayout,
)
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkActor2D,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)
from vtkmodules.vtkRenderingLabel import vtkLabeledDataMapper

# Colors (normalized RGB)
yellow_rgb = (1.0, 1.0, 0.0)
green_rgb = (0.0, 1.0, 0.0)

# Graph: three vertices, fully connected
graph = vtkMutableUndirectedGraph()
v1 = graph.AddVertex()
v2 = graph.AddVertex()
v3 = graph.AddVertex()

graph.AddEdge(v1, v2)
graph.AddEdge(v2, v3)
graph.AddEdge(v1, v3)

# Edge weight array
weights = vtkDoubleArray()
weights.SetNumberOfComponents(1)
weights.SetName("Weights")
weights.InsertNextValue(1.0)
weights.InsertNextValue(1.0)
weights.InsertNextValue(2.0)
graph.GetEdgeData().AddArray(weights)

# Vertex label array
vertex_ids = vtkIntArray()
vertex_ids.SetNumberOfComponents(1)
vertex_ids.SetName("VertexIDs")
vertex_ids.InsertNextValue(0)
vertex_ids.InsertNextValue(1)
vertex_ids.InsertNextValue(2)
graph.GetVertexData().AddArray(vertex_ids)

# Filter: layout the graph vertices in a circle
circular_layout_strategy = vtkCircularLayoutStrategy()
graph_layout = vtkGraphLayout()
graph_layout.SetInputData(graph)
graph_layout.SetLayoutStrategy(circular_layout_strategy)

# Filter: convert graph to polydata for rendering
graph_to_polydata = vtkGraphToPolyData()
graph_to_polydata.SetInputConnection(graph_layout.GetOutputPort())

# Mapper: map edge lines to graphics primitives
edge_mapper = vtkPolyDataMapper()
edge_mapper.SetInputConnection(graph_to_polydata.GetOutputPort())
edge_mapper.ScalarVisibilityOff()

# Actor: assign the edge geometry
edge_actor = vtkActor()
edge_actor.SetMapper(edge_mapper)

# Vertex labels: display VertexIDs as yellow text at each vertex
vertex_label_mapper = vtkLabeledDataMapper()
vertex_label_mapper.SetInputConnection(graph_to_polydata.GetOutputPort())
vertex_label_mapper.SetLabelModeToLabelFieldData()
vertex_label_mapper.SetFieldDataName("VertexIDs")
vertex_label_mapper.GetLabelTextProperty().SetColor(yellow_rgb)

vertex_label_actor = vtkActor2D()
vertex_label_actor.SetMapper(vertex_label_mapper)

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.AddActor(edge_actor)
renderer.AddActor(vertex_label_actor)

# Render window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("label vertices and edges")
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
