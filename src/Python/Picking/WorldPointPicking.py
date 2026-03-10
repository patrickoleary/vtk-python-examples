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

COLOR_MAP = {
    "CornflowerBlue": cornflower_blue_rgb,
    "Salmon": salmon_rgb,
    "MediumSeaGreen": medium_sea_green_rgb,
    "MediumOrchid": medium_orchid_rgb,
}


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


# Source objects: place several shapes in the scene
sources = [
    (vtkSphereSource, {"SetRadius": 0.5}, (-1.5, 0, 0), "CornflowerBlue"),
    (vtkConeSource, {"SetRadius": 0.4, "SetHeight": 0.8}, (0, 0, 0), "Salmon"),
    (vtkCubeSource, {"SetXLength": 0.7, "SetYLength": 0.7, "SetZLength": 0.7}, (1.5, 0, 0), "MediumSeaGreen"),
    (vtkCylinderSource, {"SetRadius": 0.3, "SetHeight": 0.8}, (0, 1.2, 0), "MediumOrchid"),
]

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.SetBackground(dim_gray_rgb)

for source_class, params, center, color_name in sources:
    source = source_class()
    for method, value in params.items():
        getattr(source, method)(value)
    source.SetCenter(center) if hasattr(source, "SetCenter") else None

    mapper = vtkPolyDataMapper()
    mapper.SetInputConnection(source.GetOutputPort())

    actor = vtkActor()
    actor.SetMapper(mapper)
    actor.GetProperty().SetColor(COLOR_MAP[color_name])
    if not hasattr(source, "SetCenter"):
        actor.SetPosition(center)

    renderer.AddActor(actor)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(640, 480)
render_window.SetWindowName("WorldPointPicking")

# Interactor: handle mouse and keyboard events with custom picking style
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

style = MouseInteractorStyle()
style.SetDefaultRenderer(renderer)
render_window_interactor.SetInteractorStyle(style)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
