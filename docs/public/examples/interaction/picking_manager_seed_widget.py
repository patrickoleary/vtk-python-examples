#!/usr/bin/env python
# Demonstrate vtkPickingManager with a cube of seed widgets.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkInteractionStyle import vtkInteractorStyleTrackballCamera
from vtkmodules.vtkInteractionWidgets import (
    vtkSeedRepresentation,
    vtkSeedWidget,
    vtkSphereHandleRepresentation,
)
from vtkmodules.vtkRenderingCore import (
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Renderer
renderer = vtkRenderer()
renderer.SetBackground(0.1, 0.2, 0.4)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("picking manager seed widget")
render_window.SetMultiSamples(0)
render_window.SetSize(600, 600)

# Interactor
interactor_style = vtkInteractorStyleTrackballCamera()

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)
interactor.SetInteractorStyle(interactor_style)


# Callback to toggle picking manager with Ctrl key
def picking_manager_callback(caller, event_string):
    key_sym = caller.GetKeySym()
    if key_sym in ("Control_L", "Control_R") and caller.GetPickingManager():
        pm = caller.GetPickingManager()
        if not pm.GetEnabled():
            print("PickingManager ON !")
            pm.EnabledOn()
        else:
            print("PickingManager OFF !")
            pm.EnabledOff()
    elif key_sym == "o" and caller.GetPickingManager():
        pm = caller.GetPickingManager()
        if not pm.GetOptimizeOnInteractorEvents():
            print("Optimization on Interactor events ON !")
            pm.SetOptimizeOnInteractorEvents(True)
        else:
            print("Optimization on Interactor events OFF !")
            pm.SetOptimizeOnInteractorEvents(False)


interactor.AddObserver("KeyPressEvent", picking_manager_callback)

# Widget
handle = vtkSphereHandleRepresentation()
handle.GetProperty().SetRepresentationToWireframe()
handle.GetProperty().SetColor(1, 1, 1)

seed_rep = vtkSeedRepresentation()
seed_rep.SetHandleRepresentation(handle)

seed_widget = vtkSeedWidget()
seed_widget.SetRepresentation(seed_rep)
seed_widget.SetInteractor(interactor)
seed_widget.EnabledOn()

# Create a cube of seeds: (2*base_cube)^3 = 64 seeds
base_cube = 2
seeds = []
for i in range(-base_cube, base_cube):
    for j in range(-base_cube, base_cube):
        for k in range(-base_cube, base_cube):
            new_handle = seed_widget.CreateNewHandle()
            new_handle.SetEnabled(1)
            new_handle_rep = new_handle.GetRepresentation()
            new_handle_rep.GetProperty().SetRepresentationToWireframe()
            new_handle_rep.GetProperty().SetColor(1, 1, 1)
            new_handle_rep.SetWorldPosition((float(i), float(j), float(k)))
            seeds.append(new_handle)

seed_widget.CompleteInteraction()


# Callback to reorganize the cube when space is pressed
def reorganize_callback(caller, event_string):
    if caller.GetKeySym() == "space":
        base = int(round(len(seeds) ** (1.0 / 3.0) / 2))
        idx = 0
        for i in range(-base, base):
            for j in range(-base, base):
                for k in range(-base, base):
                    handle_rep = seeds[idx].GetRepresentation()
                    handle_rep.SetWorldPosition((float(i), float(j), float(k)))
                    idx += 1


interactor.AddObserver("KeyPressEvent", reorganize_callback)

# Scene
renderer.ResetCamera((-7, 7, -7, 7, -1, 1))

interactor.Initialize()
interactor.Start()
