#!/usr/bin/env python

# Select vertices and edges interactively on a random graph. Click on
# vertices or edges in the view; the pick callback prints the selected
# point or cell ID to the console.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkFiltersSources import vtkGraphToPolyData
from vtkmodules.vtkInfovisCore import vtkRandomGraphSource
from vtkmodules.vtkInfovisLayout import (
    vtkForceDirectedLayoutStrategy,
    vtkGraphLayout,
)
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkCellPicker,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Source: generate a random graph
source = vtkRandomGraphSource()
source.SetNumberOfVertices(10)
source.SetNumberOfEdges(12)
source.SetSeed(42)

# Filter: layout the graph vertices in 2D
layout_strategy = vtkForceDirectedLayoutStrategy()
graph_layout = vtkGraphLayout()
graph_layout.SetInputConnection(source.GetOutputPort())
graph_layout.SetLayoutStrategy(layout_strategy)

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
edge_actor.GetProperty().SetPointSize(8)

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.AddActor(edge_actor)

# Render window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("selected vertices and edges")
render_window.SetMultiSamples(0)
render_window.SetSize(600, 600)

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Picker: cell picker for selecting edges/vertices
cell_picker = vtkCellPicker()
cell_picker.SetTolerance(0.01)
render_window_interactor.SetPicker(cell_picker)


def pick_callback(caller, event):
    """Print the IDs of picked points and cells."""
    click_pos = caller.GetEventPosition()
    cell_picker.Pick(click_pos[0], click_pos[1], 0, renderer)

    point_id = cell_picker.GetPointId()
    cell_id = cell_picker.GetCellId()

    if point_id >= 0:
        print(f"Vertex Selected: {point_id}")
    if cell_id >= 0:
        print(f"Edge Selected: {cell_id}")
    if point_id >= 0 or cell_id >= 0:
        print("- - -")


render_window_interactor.AddObserver("LeftButtonPressEvent", pick_callback)

# Scene: reset camera
renderer.ResetCamera()

# Start: launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
