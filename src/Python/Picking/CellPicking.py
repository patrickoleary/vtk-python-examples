#!/usr/bin/env python

# Cell picking on a triangulated plane. Left-click to pick a cell; the
# selected cell is highlighted in red with visible edges.

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
from vtkmodules.vtkFiltersCore import vtkTriangleFilter
from vtkmodules.vtkFiltersExtraction import vtkExtractSelection
from vtkmodules.vtkFiltersSources import vtkPlaneSource
from vtkmodules.vtkInteractionStyle import vtkInteractorStyleTrackballCamera
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkCellPicker,
    vtkDataSetMapper,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
tomato_rgb = (1.0, 0.388, 0.278)
sea_green_rgb = (0.180, 0.545, 0.341)
pale_turquoise_rgb = (0.686, 0.933, 0.933)


class MouseInteractorStyle(vtkInteractorStyleTrackballCamera):
    """Custom interactor that picks cells on left-click and highlights them."""

    def __init__(self, data):
        self.AddObserver("LeftButtonPressEvent", self.left_button_press_event)
        self.data = data
        self.selected_mapper = vtkDataSetMapper()
        self.selected_actor = vtkActor()

    def left_button_press_event(self, obj, event):
        pos = self.GetInteractor().GetEventPosition()

        picker = vtkCellPicker()
        picker.SetTolerance(0.0005)
        picker.Pick(pos[0], pos[1], 0, self.GetDefaultRenderer())

        world_position = picker.GetPickPosition()
        print(f"Cell id is: {picker.GetCellId()}")

        if picker.GetCellId() != -1:
            print(
                f"Pick position is: ({world_position[0]:.6g},"
                f" {world_position[1]:.6g}, {world_position[2]:.6g})"
            )

            ids = vtkIdTypeArray()
            ids.SetNumberOfComponents(1)
            ids.InsertNextValue(picker.GetCellId())

            selection_node = vtkSelectionNode()
            selection_node.SetFieldType(vtkSelectionNode.CELL)
            selection_node.SetContentType(vtkSelectionNode.INDICES)
            selection_node.SetSelectionList(ids)

            selection = vtkSelection()
            selection.AddNode(selection_node)

            extract_selection = vtkExtractSelection()
            extract_selection.SetInputData(0, self.data)
            extract_selection.SetInputData(1, selection)
            extract_selection.Update()

            selected = vtkUnstructuredGrid()
            selected.ShallowCopy(extract_selection.GetOutput())

            print(f"Number of points in the selection: {selected.GetNumberOfPoints()}")
            print(f"Number of cells in the selection : {selected.GetNumberOfCells()}")

            self.selected_mapper.SetInputData(selected)
            self.selected_actor.SetMapper(self.selected_mapper)
            self.selected_actor.GetProperty().EdgeVisibilityOn()
            self.selected_actor.GetProperty().SetColor(tomato_rgb)
            self.selected_actor.GetProperty().SetLineWidth(3)

            self.GetInteractor().GetRenderWindow().GetRenderers().GetFirstRenderer().AddActor(
                self.selected_actor
            )

        self.OnLeftButtonDown()


# Source: a triangulated plane
plane_source = vtkPlaneSource()
plane_source.Update()

triangle_filter = vtkTriangleFilter()
triangle_filter.SetInputConnection(plane_source.GetOutputPort())
triangle_filter.Update()

# Mapper and actor for the plane
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(triangle_filter.GetOutputPort())

actor = vtkActor()
actor.GetProperty().SetColor(sea_green_rgb)
actor.SetMapper(mapper)

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(pale_turquoise_rgb)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(640, 480)
render_window.SetWindowName("CellPicking")

# Interactor: handle mouse and keyboard events with custom picking style
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

style = MouseInteractorStyle(triangle_filter.GetOutput())
style.SetDefaultRenderer(renderer)
render_window_interactor.SetInteractorStyle(style)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
