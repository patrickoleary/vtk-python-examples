#!/usr/bin/env python
# Demonstrate vtkPickingManager with seed widgets and disabled seeds toggling.

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
render_window.SetWindowName("picking manager seed toggle")
render_window.SetMultiSamples(0)
render_window.SetSize(600, 600)

# Interactor
interactor_style = vtkInteractorStyleTrackballCamera()

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)
interactor.SetInteractorStyle(interactor_style)

# Enable picking manager
interactor.GetPickingManager().EnabledOn()

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


# Callback: space reorganizes cube, Alt toggles every other seed
def key_callback(caller, event_string):
    key_sym = caller.GetKeySym()
    if key_sym == "space":
        base = int(round(len(seeds) ** (1.0 / 3.0) / 2))
        idx = 0
        for i in range(-base, base):
            for j in range(-base, base):
                for k in range(-base, base):
                    handle_rep = seeds[idx].GetRepresentation()
                    handle_rep.SetWorldPosition((float(i), float(j), float(k)))
                    idx += 1
    elif key_sym in ("Alt_L", "Alt_R"):
        n_seeds = len(seeds)
        for n in range(n_seeds):
            if n % 2 == 0:
                seed_handle = seed_widget.GetSeed(n)
                seed_handle.SetEnabled(not seed_handle.GetEnabled())
        seed_widget.GetCurrentRenderer().Render()


interactor.AddObserver("KeyPressEvent", key_callback)

# Scene
renderer.ResetCamera((-7, 7, -7, 7, -1, 1))

interactor.Initialize()
interactor.Start()
