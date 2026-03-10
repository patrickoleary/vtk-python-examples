#!/usr/bin/env python

# Extract a subset of cells by index using vtkExtractSelection, showing
# all cells, selected cells, and non-selected cells in three viewports.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkCommonCore import vtkIdTypeArray
from vtkmodules.vtkCommonDataModel import (
    vtkSelection,
    vtkSelectionNode,
    vtkUnstructuredGrid,
)
from vtkmodules.vtkFiltersExtraction import vtkExtractSelection
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkCamera,
    vtkDataSetMapper,
    vtkProperty,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
misty_rose_rgb = (1.000, 0.894, 0.882)
gold_rgb = (1.000, 0.843, 0.000)
burlywood_rgb = (0.871, 0.722, 0.529)
orchid_dark_rgb = (0.600, 0.196, 0.800)
cornflower_blue_rgb = (0.392, 0.584, 0.929)

# Source: sphere
sphere_source = vtkSphereSource()
sphere_source.Update()

# Selection: cell indices 10 through 19
ids = vtkIdTypeArray()
ids.SetNumberOfComponents(1)
ids.InsertNextValue(10)
ids.InsertNextValue(11)
ids.InsertNextValue(12)
ids.InsertNextValue(13)
ids.InsertNextValue(14)
ids.InsertNextValue(15)
ids.InsertNextValue(16)
ids.InsertNextValue(17)
ids.InsertNextValue(18)
ids.InsertNextValue(19)

selection_node = vtkSelectionNode()
selection_node.SetFieldType(vtkSelectionNode.CELL)
selection_node.SetContentType(vtkSelectionNode.INDICES)
selection_node.SetSelectionList(ids)

selection = vtkSelection()
selection.AddNode(selection_node)

# Filter: extract cells IN the selection
extract_selection = vtkExtractSelection()
extract_selection.SetInputConnection(0, sphere_source.GetOutputPort())
extract_selection.SetInputData(1, selection)
extract_selection.Update()

selected = vtkUnstructuredGrid()
selected.ShallowCopy(extract_selection.GetOutput())

# Invert to get cells NOT in the selection
selection_node.GetProperties().Set(vtkSelectionNode.INVERSE(), 1)
extract_selection.Update()

not_selected = vtkUnstructuredGrid()
not_selected.ShallowCopy(extract_selection.GetOutput())

# Shared back-face property
backfaces = vtkProperty()
backfaces.SetColor(gold_rgb)

# Mapper & Actor: map all cells to graphics primitives
input_mapper = vtkDataSetMapper()
input_mapper.SetInputConnection(sphere_source.GetOutputPort())

input_actor = vtkActor()
input_actor.SetMapper(input_mapper)
input_actor.GetProperty().SetColor(misty_rose_rgb)
input_actor.SetBackfaceProperty(backfaces)

# Mapper & Actor: map selected cells to graphics primitives
selected_mapper = vtkDataSetMapper()
selected_mapper.SetInputData(selected)

selected_actor = vtkActor()
selected_actor.SetMapper(selected_mapper)
selected_actor.GetProperty().SetColor(misty_rose_rgb)
selected_actor.SetBackfaceProperty(backfaces)

# Mapper & Actor: map non-selected cells to graphics primitives
not_selected_mapper = vtkDataSetMapper()
not_selected_mapper.SetInputData(not_selected)

not_selected_actor = vtkActor()
not_selected_actor.SetMapper(not_selected_mapper)
not_selected_actor.GetProperty().SetColor(misty_rose_rgb)
not_selected_actor.SetBackfaceProperty(backfaces)

# Shared camera
camera = vtkCamera()

# Left renderer: all cells
left_renderer = vtkRenderer()
left_renderer.SetViewport(0.0, 0.0, 0.33, 1.0)
left_renderer.SetBackground(burlywood_rgb)
left_renderer.SetActiveCamera(camera)
left_renderer.AddActor(input_actor)

# Center renderer: selected cells
center_renderer = vtkRenderer()
center_renderer.SetViewport(0.33, 0.0, 0.66, 1.0)
center_renderer.SetBackground(orchid_dark_rgb)
center_renderer.SetActiveCamera(camera)
center_renderer.AddActor(selected_actor)

# Right renderer: non-selected cells
right_renderer = vtkRenderer()
right_renderer.SetViewport(0.66, 0.0, 1.0, 1.0)
right_renderer.SetBackground(cornflower_blue_rgb)
right_renderer.SetActiveCamera(camera)
right_renderer.AddActor(not_selected_actor)

left_renderer.ResetCamera()

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(left_renderer)
render_window.AddRenderer(center_renderer)
render_window.AddRenderer(right_renderer)
render_window.SetSize(900, 300)
render_window.SetWindowName("ExtractSelectionUsingCells")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window.Render()
render_window_interactor.Start()
