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
from vtkmodules.vtkInfovisLayout import vtkCircularLayoutStrategy
from vtkmodules.vtkViewsInfovis import vtkGraphLayoutView

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

# View: display the graph with a circular layout and labels on both
view = vtkGraphLayoutView()
view.AddRepresentationFromInput(graph)
view.SetLayoutStrategy(vtkCircularLayoutStrategy())
view.SetVertexLabelArrayName("VertexIDs")
view.SetVertexLabelVisibility(True)
view.SetEdgeLabelArrayName("Weights")
view.SetEdgeLabelVisibility(True)
view.GetRepresentation().GetVertexLabelTextProperty().SetColor(yellow_rgb)
view.GetRepresentation().GetEdgeLabelTextProperty().SetColor(green_rgb)
view.ResetCamera()
render_window = view.GetRenderWindow()
render_window.SetWindowName("LabelVerticesAndEdges")

# Launch the interactive visualization
view.GetInteractor().Initialize()
view.GetInteractor().Start()
