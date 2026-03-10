#!/usr/bin/env python

# Highlight a picked actor by changing its color. Left-click on a sphere to
# highlight it in red with visible edges; the previous highlight is restored.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkCommonCore import vtkMinimalStandardRandomSequence
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkInteractionStyle import vtkInteractorStyleTrackballCamera
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkPropPicker,
    vtkProperty,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
red_rgb = (1.0, 0.0, 0.0)
steel_blue_rgb = (0.275, 0.510, 0.706)
white_rgb = (1.0, 1.0, 1.0)

NUM_SPHERES = 10


class MouseInteractorHighLightActor(vtkInteractorStyleTrackballCamera):
    """Custom interactor that highlights the picked actor on left-click."""

    def __init__(self):
        self.AddObserver("LeftButtonPressEvent", self.left_button_press_event)
        self.last_picked_actor = None
        self.last_picked_property = vtkProperty()

    def left_button_press_event(self, obj, event):
        click_pos = self.GetInteractor().GetEventPosition()

        picker = vtkPropPicker()
        picker.Pick(click_pos[0], click_pos[1], 0, self.GetDefaultRenderer())

        new_picked_actor = picker.GetActor()

        if new_picked_actor:
            if self.last_picked_actor:
                self.last_picked_actor.GetProperty().DeepCopy(self.last_picked_property)

            self.last_picked_property.DeepCopy(new_picked_actor.GetProperty())
            new_picked_actor.GetProperty().SetColor(red_rgb)
            new_picked_actor.GetProperty().SetDiffuse(1.0)
            new_picked_actor.GetProperty().SetSpecular(0.0)
            new_picked_actor.GetProperty().EdgeVisibilityOn()

            self.last_picked_actor = new_picked_actor

        self.OnLeftButtonDown()


# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.SetBackground(steel_blue_rgb)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(640, 480)
render_window.SetWindowName("HighlightPickedActor")

# Interactor: handle mouse and keyboard events with custom picking style
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

style = MouseInteractorHighLightActor()
style.SetDefaultRenderer(renderer)
render_window_interactor.SetInteractorStyle(style)

# Generate random spheres to pick from
rand_seq = vtkMinimalStandardRandomSequence()
rand_seq.SetSeed(8775070)

for i in range(NUM_SPHERES):
    source = vtkSphereSource()

    x = rand_seq.GetRangeValue(-5.0, 5.0)
    rand_seq.Next()
    y = rand_seq.GetRangeValue(-5.0, 5.0)
    rand_seq.Next()
    z = rand_seq.GetRangeValue(-5.0, 5.0)
    rand_seq.Next()
    radius = rand_seq.GetRangeValue(0.5, 1.0)
    rand_seq.Next()

    source.SetRadius(radius)
    source.SetCenter(x, y, z)
    source.SetPhiResolution(11)
    source.SetThetaResolution(21)

    mapper = vtkPolyDataMapper()
    mapper.SetInputConnection(source.GetOutputPort())
    actor = vtkActor()
    actor.SetMapper(mapper)

    r = rand_seq.GetRangeValue(0.4, 1.0)
    rand_seq.Next()
    g = rand_seq.GetRangeValue(0.4, 1.0)
    rand_seq.Next()
    b = rand_seq.GetRangeValue(0.4, 1.0)
    rand_seq.Next()

    actor.GetProperty().SetDiffuseColor(r, g, b)
    actor.GetProperty().SetDiffuse(0.8)
    actor.GetProperty().SetSpecular(0.5)
    actor.GetProperty().SetSpecularColor(white_rgb)
    actor.GetProperty().SetSpecularPower(30.0)

    renderer.AddActor(actor)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
