#!/usr/bin/env python

# Use vtkHardwareSelector to identify visible cells in the scene.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkCommonDataModel import vtkDataObject
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkInteractionStyle import vtkInteractorStyleTrackballCamera
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkHardwareSelector,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
bisque = (1.000, 0.894, 0.769)
navy = (0.000, 0.000, 0.502)

# Source: generate sphere polygon data
source = vtkSphereSource()
source.SetCenter(0.0, 0.0, 0.0)
source.SetRadius(5.0)

# Mapper: map polygon data to graphics primitives
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(source.GetOutputPort())

# Actor: assign the mapped geometry
actor = vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetColor(bisque)

# Renderer: assemble the scene and configure the camera
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.GetActiveCamera().ParallelProjectionOn()
renderer.SetBackground(navy)
renderer.ResetCamera()

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("HardwareSelector")
render_window.SetSize(640, 480)

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

style = vtkInteractorStyleTrackballCamera()
render_window_interactor.SetInteractorStyle(style)


# Callback: use hardware selection to report visible cell IDs
def selection_callback(caller, event_id):
    selector = vtkHardwareSelector()
    selector.SetFieldAssociation(vtkDataObject.FIELD_ASSOCIATION_CELLS)
    selector.SetRenderer(renderer)
    x, y = caller.GetRenderWindow().GetSize()
    selector.SetArea(0, 0, x, y)
    result = selector.Select()
    if result.GetNumberOfNodes() < 1:
        print("No visible cells")
    else:
        node = result.GetNode(0)
        selection_list = node.GetSelectionList()
        ids = [int(selection_list.GetValue(i)) for i in range(selection_list.GetNumberOfTuples())]
        print("Visible cell IDs:", ids)


render_window_interactor.AddObserver("UserEvent", selection_callback)

# Launch the interactive visualization
render_window_interactor.Start()
