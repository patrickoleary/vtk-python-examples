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
from vtkmodules.vtkFiltersSources import vtkGraphToPolyData
from vtkmodules.vtkInfovisLayout import (
    vtkGraphLayout,
    vtkSimple2DLayoutStrategy,
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

# Filter: layout the graph vertices in 2D
simple_2_d_layout_strategy = vtkSimple2DLayoutStrategy()
graph_layout = vtkGraphLayout()
graph_layout.SetInputData(graph)
graph_layout.SetLayoutStrategy(simple_2_d_layout_strategy)

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

# Vertex labels: display VertexIDs array as red text at each vertex
label_mapper = vtkLabeledDataMapper()
label_mapper.SetInputConnection(graph_to_polydata.GetOutputPort())
label_mapper.SetLabelModeToLabelFieldData()
label_mapper.SetFieldDataName("VertexIDs")
label_mapper.GetLabelTextProperty().SetColor(red_rgb)

label_actor = vtkActor2D()
label_actor.SetMapper(label_mapper)

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.AddActor(edge_actor)
renderer.AddActor(label_actor)

# Render window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("color vertex labels")
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
