#!/usr/bin/env python

# Demonstrate keypress event handling with a custom interactor style.
# Press 's' to toggle wireframe, 'c' to toggle color, and 'q' to quit.
# The current key is printed to the console.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkFiltersSources import vtkConeSource
from vtkmodules.vtkInteractionStyle import vtkInteractorStyleTrackballCamera
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
tomato_rgb = (1.0, 0.388, 0.278)
steel_blue_rgb = (0.275, 0.510, 0.706)
gold_rgb = (1.0, 0.843, 0.0)
medium_sea_green_rgb = (0.235, 0.702, 0.443)
orchid_rgb = (0.855, 0.439, 0.839)
dark_slate_gray_rgb = (0.184, 0.310, 0.310)

# Source: generate a cone
cone = vtkConeSource()
cone.SetResolution(64)

# Mapper: map cone polygon data to graphics primitives
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(cone.GetOutputPort())

# Actor: assign the mapped geometry
actor = vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetColor(tomato_rgb)

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(dark_slate_gray_rgb)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(640, 480)
render_window.SetWindowName("KeypressEvents")

# Interactor: handle mouse and keyboard events
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)
interactor.SetInteractorStyle(vtkInteractorStyleTrackballCamera())

# Alternate color list
color_list = [tomato_rgb, steel_blue_rgb, gold_rgb, medium_sea_green_rgb, orchid_rgb]
color_index = [0]


# Keypress callback: toggle wireframe with 's', cycle color with 'c'
def on_keypress(obj, event):
    key = obj.GetKeySym()
    print(f"Key pressed: {key}")
    if key == "s":
        rep = actor.GetProperty().GetRepresentation()
        if rep == 1:
            actor.GetProperty().SetRepresentationToSurface()
        else:
            actor.GetProperty().SetRepresentationToWireframe()
        render_window.Render()
    elif key == "c":
        color_index[0] = (color_index[0] + 1) % len(color_list)
        actor.GetProperty().SetColor(color_list[color_index[0]])
        render_window.Render()


interactor.AddObserver("KeyPressEvent", on_keypress)

# Launch the interactive visualization
interactor.Initialize()
interactor.Start()
