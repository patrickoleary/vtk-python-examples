#!/usr/bin/env python

# Point picking on a sphere. Left-click to pick the nearest point; a small
# glyph sphere is placed at the picked point location and its ID is printed.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkInteractionStyle import vtkInteractorStyleTrackballCamera
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPointPicker,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
red_rgb = (1.0, 0.0, 0.0)
cornflower_blue_rgb = (0.392, 0.584, 0.929)
slate_gray_rgb = (0.439, 0.502, 0.565)


class MouseInteractorStyle(vtkInteractorStyleTrackballCamera):
    """Custom interactor that picks the nearest point on left-click."""

    def __init__(self, point_data):
        self.AddObserver("LeftButtonPressEvent", self.left_button_press_event)
        self.point_data = point_data
        self.glyph_actor = None

    def left_button_press_event(self, obj, event):
        pos = self.GetInteractor().GetEventPosition()

        picker = vtkPointPicker()
        picker.SetTolerance(0.01)
        picker.Pick(pos[0], pos[1], 0, self.GetDefaultRenderer())

        point_id = picker.GetPointId()

        if point_id != -1:
            world_pos = picker.GetPickPosition()
            print(
                f"Point id: {point_id}  Position: "
                f"({world_pos[0]:.4f}, {world_pos[1]:.4f}, {world_pos[2]:.4f})"
            )

            # Place a small red sphere at the picked point
            if self.glyph_actor is not None:
                self.GetDefaultRenderer().RemoveActor(self.glyph_actor)

            glyph_source = vtkSphereSource()
            glyph_source.SetRadius(0.02)
            glyph_source.SetCenter(world_pos)
            glyph_source.SetPhiResolution(12)
            glyph_source.SetThetaResolution(12)

            glyph_mapper = vtkPolyDataMapper()
            glyph_mapper.SetInputConnection(glyph_source.GetOutputPort())

            self.glyph_actor = vtkActor()
            self.glyph_actor.SetMapper(glyph_mapper)
            self.glyph_actor.GetProperty().SetColor(red_rgb)

            self.GetDefaultRenderer().AddActor(self.glyph_actor)
            self.GetInteractor().GetRenderWindow().Render()

        self.OnLeftButtonDown()


# Source: a high-resolution sphere to pick points on
sphere_source = vtkSphereSource()
sphere_source.SetRadius(1.0)
sphere_source.SetPhiResolution(30)
sphere_source.SetThetaResolution(30)
sphere_source.Update()

# Mapper and actor for the sphere
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(sphere_source.GetOutputPort())

actor = vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetColor(cornflower_blue_rgb)
actor.GetProperty().SetOpacity(0.8)

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(slate_gray_rgb)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(640, 480)
render_window.SetWindowName("PointPicking")

# Interactor: handle mouse and keyboard events with custom picking style
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

style = MouseInteractorStyle(sphere_source.GetOutput())
style.SetDefaultRenderer(renderer)
render_window_interactor.SetInteractorStyle(style)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
