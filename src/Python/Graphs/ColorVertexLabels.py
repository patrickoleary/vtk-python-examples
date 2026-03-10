#!/usr/bin/env python

# Color vertex labels of a directed graph. Each vertex is labelled with its
# integer ID and the label text is rendered in red.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkCommonCore import vtkIntArray
from vtkmodules.vtkCommonDataModel import vtkMutableDirectedGraph
from vtkmodules.vtkViewsInfovis import (
    vtkGraphLayoutView,
    vtkRenderedGraphRepresentation,
)

# Colors (normalized RGB)
red_rgb = (1.0, 0.0, 0.0)

# Graph: two vertices with one directed edge
graph = vtkMutableDirectedGraph()
v1 = graph.AddVertex()
v2 = graph.AddVertex()
graph.AddEdge(v1, v2)

# Vertex label array: integer ID per vertex
vertex_ids = vtkIntArray()
vertex_ids.SetNumberOfComponents(1)
vertex_ids.SetName("VertexIDs")
vertex_ids.InsertNextValue(0)
vertex_ids.InsertNextValue(1)
graph.GetVertexData().AddArray(vertex_ids)

# View: display the graph with colored vertex labels
view = vtkGraphLayoutView()
view.AddRepresentationFromInput(graph)
view.SetLayoutStrategyToSimple2D()
view.SetVertexLabelArrayName("VertexIDs")
view.SetVertexLabelVisibility(True)

# Representation: set vertex label text color to red
vtkRenderedGraphRepresentation.SafeDownCast(
    view.GetRepresentation()
).GetVertexLabelTextProperty().SetColor(red_rgb)

view.ResetCamera()
view.GetRenderer().GetActiveCamera().Zoom(0.8)
render_window = view.GetRenderWindow()
render_window.SetWindowName("ColorVertexLabels")

# Launch the interactive visualization
view.GetInteractor().Initialize()
view.GetInteractor().Start()
