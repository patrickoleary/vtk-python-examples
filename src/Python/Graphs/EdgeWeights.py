#!/usr/bin/env python

# Display edge weights on a fully connected directed graph. The
# force-directed layout uses the weight values to influence spacing.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkCommonCore import vtkDoubleArray
from vtkmodules.vtkCommonDataModel import vtkMutableDirectedGraph
from vtkmodules.vtkInfovisLayout import vtkForceDirectedLayoutStrategy
from vtkmodules.vtkViewsInfovis import vtkGraphLayoutView

# Colors (normalized RGB)
navy_rgb = (0.0, 0.0, 0.502)
midnight_blue_rgb = (0.098, 0.098, 0.439)

# Graph: three vertices, fully connected
graph = vtkMutableDirectedGraph()
v1 = graph.AddVertex()
v2 = graph.AddVertex()
v3 = graph.AddVertex()

graph.AddGraphEdge(v1, v2)
graph.AddGraphEdge(v2, v3)
graph.AddGraphEdge(v1, v3)

# Edge weight array
weights = vtkDoubleArray()
weights.SetNumberOfComponents(1)
weights.SetName("Weights")
weights.InsertNextValue(1.0)
weights.InsertNextValue(1.0)
weights.InsertNextValue(2.0)
graph.GetEdgeData().AddArray(weights)

print("Number of edges:", graph.GetNumberOfEdges())

# View: display the graph with a force-directed layout weighted by edges
view = vtkGraphLayoutView()
view.AddRepresentationFromInput(graph)
layout_strategy = vtkForceDirectedLayoutStrategy()
layout_strategy.SetEdgeWeightField("Weights")
layout_strategy.SetWeightEdges(True)
view.SetLayoutStrategy(layout_strategy)
view.SetEdgeLabelArrayName("Weights")
view.EdgeLabelVisibilityOn()
view.GetRenderer().SetBackground(navy_rgb)
view.GetRenderer().SetBackground2(midnight_blue_rgb)
render_window = view.GetRenderWindow()
render_window.SetWindowName("EdgeWeights")
view.ResetCamera()

# Launch the interactive visualization
view.GetInteractor().Initialize()
view.GetInteractor().Start()
