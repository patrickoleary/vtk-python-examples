#!/usr/bin/env python

# World point picking using vtkWorldPointPicker. Left-click anywhere in the
# scene to get the world XYZ coordinates at that pixel (z-buffer depth).
# A crosshair marker is placed at the picked location.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkFiltersSources import (
    vtkConeSource,
    vtkCubeSource,
    vtkCylinderSource,
    vtkSphereSource,
)
from vtkmodules.vtkInteractionStyle import vtkInteractorStyleTrackballCamera
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
    vtkWorldPointPicker,
)

# Colors (normalized RGB)
yellow_rgb = (1.0, 1.0, 0.0)
cornflower_blue_rgb = (0.392, 0.584, 0.929)
salmon_rgb = (0.980, 0.502, 0.447)
medium_sea_green_rgb = (0.235, 0.702, 0.443)
medium_orchid_rgb = (0.729, 0.333, 0.827)
dim_gray_rgb = (0.412, 0.412, 0.412)



class MouseInteractorStyle(vtkInteractorStyleTrackballCamera):
    """Custom interactor that picks world coordinates on left-click."""

    def __init__(self):
        self.AddObserver("LeftButtonPressEvent", self.left_button_press_event)
        self.marker_actor = None

    def left_button_press_event(self, obj, event):
        pos = self.GetInteractor().GetEventPosition()

        picker = vtkWorldPointPicker()
        picker.Pick(pos[0], pos[1], 0, self.GetDefaultRenderer())

        world_pos = picker.GetPickPosition()
        print(
            f"World position: ({world_pos[0]:.4f}, {world_pos[1]:.4f}, {world_pos[2]:.4f})"
        )

        # Place a small yellow sphere marker at the picked world position
        if self.marker_actor is not None:
            self.GetDefaultRenderer().RemoveActor(self.marker_actor)

        marker_source = vtkSphereSource()
        marker_source.SetRadius(0.05)
        marker_source.SetCenter(world_pos)
        marker_source.SetPhiResolution(12)
        marker_source.SetThetaResolution(12)

        marker_mapper = vtkPolyDataMapper()
        marker_mapper.SetInputConnection(marker_source.GetOutputPort())

        self.marker_actor = vtkActor()
        self.marker_actor.SetMapper(marker_mapper)
        self.marker_actor.GetProperty().SetColor(yellow_rgb)

        self.GetDefaultRenderer().AddActor(self.marker_actor)
        self.GetInteractor().GetRenderWindow().Render()

        self.OnLeftButtonDown()


# Source: sphere at left
sphere_source = vtkSphereSource()
sphere_source.SetRadius(0.5)
sphere_source.SetCenter(-1.5, 0, 0)

# Source: cone at center
cone_source = vtkConeSource()
cone_source.SetRadius(0.4)
cone_source.SetHeight(0.8)
cone_source.SetCenter(0, 0, 0)

# Source: cube at right
cube_source = vtkCubeSource()
cube_source.SetXLength(0.7)
cube_source.SetYLength(0.7)
cube_source.SetZLength(0.7)
cube_source.SetCenter(1.5, 0, 0)

# Source: cylinder above center
cylinder_source = vtkCylinderSource()
cylinder_source.SetRadius(0.3)
cylinder_source.SetHeight(0.8)

# Mapper: sphere
sphere_mapper = vtkPolyDataMapper()
sphere_mapper.SetInputConnection(sphere_source.GetOutputPort())

sphere_actor = vtkActor()
sphere_actor.SetMapper(sphere_mapper)
sphere_actor.GetProperty().SetColor(cornflower_blue_rgb)

# Mapper: cone
cone_mapper = vtkPolyDataMapper()
cone_mapper.SetInputConnection(cone_source.GetOutputPort())

cone_actor = vtkActor()
cone_actor.SetMapper(cone_mapper)
cone_actor.GetProperty().SetColor(salmon_rgb)

# Mapper: cube
cube_mapper = vtkPolyDataMapper()
cube_mapper.SetInputConnection(cube_source.GetOutputPort())

cube_actor = vtkActor()
cube_actor.SetMapper(cube_mapper)
cube_actor.GetProperty().SetColor(medium_sea_green_rgb)

# Mapper: cylinder
cylinder_mapper = vtkPolyDataMapper()
cylinder_mapper.SetInputConnection(cylinder_source.GetOutputPort())

cylinder_actor = vtkActor()
cylinder_actor.SetMapper(cylinder_mapper)
cylinder_actor.GetProperty().SetColor(medium_orchid_rgb)
cylinder_actor.SetPosition(0, 1.2, 0)

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.AddActor(sphere_actor)
renderer.AddActor(cone_actor)
renderer.AddActor(cube_actor)
renderer.AddActor(cylinder_actor)
renderer.SetBackground(dim_gray_rgb)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("world point picking")
render_window.SetMultiSamples(0)
render_window.SetSize(640, 480)

# Interactor: handle mouse and keyboard events with custom picking style
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

style = MouseInteractorStyle()
style.SetDefaultRenderer(renderer)
render_window_interactor.SetInteractorStyle(style)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
