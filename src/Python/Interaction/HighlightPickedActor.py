#!/usr/bin/env python

# Demonstrate actor picking with vtkCellPicker.  Click on any of the three
# objects to highlight it in yellow; the previously highlighted actor reverts
# to its original color.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkFiltersSources import (
    vtkConeSource,
    vtkCubeSource,
    vtkSphereSource,
)
from vtkmodules.vtkInteractionStyle import vtkInteractorStyleTrackballCamera
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkCellPicker,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
tomato_rgb = (1.0, 0.388, 0.278)
steel_blue_rgb = (0.275, 0.510, 0.706)
medium_sea_green_rgb = (0.235, 0.702, 0.443)
yellow_rgb = (1.0, 1.0, 0.0)
slate_gray_rgb = (0.439, 0.502, 0.565)

# Source: sphere on the left
sphere = vtkSphereSource()
sphere.SetCenter(-2, 0, 0)

sphere_mapper = vtkPolyDataMapper()
sphere_mapper.SetInputConnection(sphere.GetOutputPort())

sphere_actor = vtkActor()
sphere_actor.SetMapper(sphere_mapper)
sphere_actor.GetProperty().SetColor(tomato_rgb)

# Source: cube in the center
cube = vtkCubeSource()
cube.SetCenter(0, 0, 0)

cube_mapper = vtkPolyDataMapper()
cube_mapper.SetInputConnection(cube.GetOutputPort())

cube_actor = vtkActor()
cube_actor.SetMapper(cube_mapper)
cube_actor.GetProperty().SetColor(steel_blue_rgb)

# Source: cone on the right
cone = vtkConeSource()
cone.SetCenter(2, 0, 0)
cone.SetResolution(64)

cone_mapper = vtkPolyDataMapper()
cone_mapper.SetInputConnection(cone.GetOutputPort())

cone_actor = vtkActor()
cone_actor.SetMapper(cone_mapper)
cone_actor.GetProperty().SetColor(medium_sea_green_rgb)

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.AddActor(sphere_actor)
renderer.AddActor(cube_actor)
renderer.AddActor(cone_actor)
renderer.SetBackground(slate_gray_rgb)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(640, 480)
render_window.SetWindowName("HighlightPickedActor")

# Interactor: handle mouse and keyboard events
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)
interactor.SetInteractorStyle(vtkInteractorStyleTrackballCamera())

# Picker: cell-level picking
picker = vtkCellPicker()
interactor.SetPicker(picker)

# State: track the previously highlighted actor and its original color
last_actor = [None]
last_color = [None]


# Pick callback: highlight the picked actor in yellow
def on_left_button_press(obj, event):
    click_pos = obj.GetEventPosition()
    picker.Pick(click_pos[0], click_pos[1], 0, renderer)
    picked_actor = picker.GetActor()

    if last_actor[0] is not None and last_actor[0] is not picked_actor:
        last_actor[0].GetProperty().SetColor(last_color[0])

    if picked_actor is not None:
        last_color[0] = picked_actor.GetProperty().GetColor()
        last_actor[0] = picked_actor
        picked_actor.GetProperty().SetColor(yellow_rgb)
        render_window.Render()


interactor.AddObserver("LeftButtonPressEvent", on_left_button_press)

# Launch the interactive visualization
interactor.Initialize()
interactor.Start()
