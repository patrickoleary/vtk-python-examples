#!/usr/bin/env python

# Highlight a picked actor by changing its color. Left-click on a sphere to
# highlight it in red with visible edges; the previous highlight is restored.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
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


# Source: 10 randomly placed spheres
source_0 = vtkSphereSource()
source_0.SetRadius(0.5936)
source_0.SetCenter(0.9463, -4.8686, 3.0200)
source_0.SetPhiResolution(11)
source_0.SetThetaResolution(21)

source_1 = vtkSphereSource()
source_1.SetRadius(0.5399)
source_1.SetCenter(0.9038, 0.7512, -4.7596)
source_1.SetPhiResolution(11)
source_1.SetThetaResolution(21)

source_2 = vtkSphereSource()
source_2.SetRadius(0.6566)
source_2.SetCenter(3.2573, -3.7712, -3.2553)
source_2.SetPhiResolution(11)
source_2.SetThetaResolution(21)

source_3 = vtkSphereSource()
source_3.SetRadius(0.6770)
source_3.SetCenter(-1.2821, 1.9590, 4.0833)
source_3.SetPhiResolution(11)
source_3.SetThetaResolution(21)

source_4 = vtkSphereSource()
source_4.SetRadius(0.7152)
source_4.SetCenter(-4.9000, -3.4790, -1.0889)
source_4.SetPhiResolution(11)
source_4.SetThetaResolution(21)

source_5 = vtkSphereSource()
source_5.SetRadius(0.7569)
source_5.SetCenter(4.6296, -0.6932, -0.9068)
source_5.SetPhiResolution(11)
source_5.SetThetaResolution(21)

source_6 = vtkSphereSource()
source_6.SetRadius(0.9914)
source_6.SetCenter(-4.0024, 2.1089, 3.6577)
source_6.SetPhiResolution(11)
source_6.SetThetaResolution(21)

source_7 = vtkSphereSource()
source_7.SetRadius(0.6710)
source_7.SetCenter(1.7914, -2.0026, 2.6714)
source_7.SetPhiResolution(11)
source_7.SetThetaResolution(21)

source_8 = vtkSphereSource()
source_8.SetRadius(0.8590)
source_8.SetCenter(2.3649, -2.8627, -2.8903)
source_8.SetPhiResolution(11)
source_8.SetThetaResolution(21)

source_9 = vtkSphereSource()
source_9.SetRadius(0.8184)
source_9.SetCenter(4.8909, 1.8100, 0.0388)
source_9.SetPhiResolution(11)
source_9.SetThetaResolution(21)

# Mapper: sphere 0
mapper_0 = vtkPolyDataMapper()
mapper_0.SetInputConnection(source_0.GetOutputPort())
actor_0 = vtkActor()
actor_0.SetMapper(mapper_0)
actor_0.GetProperty().SetDiffuseColor(0.880, 0.647, 0.707)
actor_0.GetProperty().SetDiffuse(0.8)
actor_0.GetProperty().SetSpecular(0.5)
actor_0.GetProperty().SetSpecularColor(white_rgb)
actor_0.GetProperty().SetSpecularPower(30.0)

# Mapper: sphere 1
mapper_1 = vtkPolyDataMapper()
mapper_1.SetInputConnection(source_1.GetOutputPort())
actor_1 = vtkActor()
actor_1.SetMapper(mapper_1)
actor_1.GetProperty().SetDiffuseColor(0.814, 0.754, 0.565)
actor_1.GetProperty().SetDiffuse(0.8)
actor_1.GetProperty().SetSpecular(0.5)
actor_1.GetProperty().SetSpecularColor(white_rgb)
actor_1.GetProperty().SetSpecularPower(30.0)

# Mapper: sphere 2
mapper_2 = vtkPolyDataMapper()
mapper_2.SetInputConnection(source_2.GetOutputPort())
actor_2 = vtkActor()
actor_2.SetMapper(mapper_2)
actor_2.GetProperty().SetDiffuseColor(0.790, 0.775, 0.562)
actor_2.GetProperty().SetDiffuse(0.8)
actor_2.GetProperty().SetSpecular(0.5)
actor_2.GetProperty().SetSpecularColor(white_rgb)
actor_2.GetProperty().SetSpecularPower(30.0)

# Mapper: sphere 3
mapper_3 = vtkPolyDataMapper()
mapper_3.SetInputConnection(source_3.GetOutputPort())
actor_3 = vtkActor()
actor_3.SetMapper(mapper_3)
actor_3.GetProperty().SetDiffuseColor(0.801, 0.686, 0.730)
actor_3.GetProperty().SetDiffuse(0.8)
actor_3.GetProperty().SetSpecular(0.5)
actor_3.GetProperty().SetSpecularColor(white_rgb)
actor_3.GetProperty().SetSpecularPower(30.0)

# Mapper: sphere 4
mapper_4 = vtkPolyDataMapper()
mapper_4.SetInputConnection(source_4.GetOutputPort())
actor_4 = vtkActor()
actor_4.SetMapper(mapper_4)
actor_4.GetProperty().SetDiffuseColor(0.438, 0.586, 0.831)
actor_4.GetProperty().SetDiffuse(0.8)
actor_4.GetProperty().SetSpecular(0.5)
actor_4.GetProperty().SetSpecularColor(white_rgb)
actor_4.GetProperty().SetSpecularPower(30.0)

# Mapper: sphere 5
mapper_5 = vtkPolyDataMapper()
mapper_5.SetInputConnection(source_5.GetOutputPort())
actor_5 = vtkActor()
actor_5.SetMapper(mapper_5)
actor_5.GetProperty().SetDiffuseColor(0.724, 0.762, 0.512)
actor_5.GetProperty().SetDiffuse(0.8)
actor_5.GetProperty().SetSpecular(0.5)
actor_5.GetProperty().SetSpecularColor(white_rgb)
actor_5.GetProperty().SetSpecularPower(30.0)

# Mapper: sphere 6
mapper_6 = vtkPolyDataMapper()
mapper_6.SetInputConnection(source_6.GetOutputPort())
actor_6 = vtkActor()
actor_6.SetMapper(mapper_6)
actor_6.GetProperty().SetDiffuseColor(0.429, 0.780, 0.598)
actor_6.GetProperty().SetDiffuse(0.8)
actor_6.GetProperty().SetSpecular(0.5)
actor_6.GetProperty().SetSpecularColor(white_rgb)
actor_6.GetProperty().SetSpecularPower(30.0)

# Mapper: sphere 7
mapper_7 = vtkPolyDataMapper()
mapper_7.SetInputConnection(source_7.GetOutputPort())
actor_7 = vtkActor()
actor_7.SetMapper(mapper_7)
actor_7.GetProperty().SetDiffuseColor(0.603, 0.455, 0.850)
actor_7.GetProperty().SetDiffuse(0.8)
actor_7.GetProperty().SetSpecular(0.5)
actor_7.GetProperty().SetSpecularColor(white_rgb)
actor_7.GetProperty().SetSpecularPower(30.0)

# Mapper: sphere 8
mapper_8 = vtkPolyDataMapper()
mapper_8.SetInputConnection(source_8.GetOutputPort())
actor_8 = vtkActor()
actor_8.SetMapper(mapper_8)
actor_8.GetProperty().SetDiffuseColor(0.473, 0.635, 0.759)
actor_8.GetProperty().SetDiffuse(0.8)
actor_8.GetProperty().SetSpecular(0.5)
actor_8.GetProperty().SetSpecularColor(white_rgb)
actor_8.GetProperty().SetSpecularPower(30.0)

# Mapper: sphere 9
mapper_9 = vtkPolyDataMapper()
mapper_9.SetInputConnection(source_9.GetOutputPort())
actor_9 = vtkActor()
actor_9.SetMapper(mapper_9)
actor_9.GetProperty().SetDiffuseColor(0.578, 0.884, 0.543)
actor_9.GetProperty().SetDiffuse(0.8)
actor_9.GetProperty().SetSpecular(0.5)
actor_9.GetProperty().SetSpecularColor(white_rgb)
actor_9.GetProperty().SetSpecularPower(30.0)

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.AddActor(actor_0)
renderer.AddActor(actor_1)
renderer.AddActor(actor_2)
renderer.AddActor(actor_3)
renderer.AddActor(actor_4)
renderer.AddActor(actor_5)
renderer.AddActor(actor_6)
renderer.AddActor(actor_7)
renderer.AddActor(actor_8)
renderer.AddActor(actor_9)
renderer.SetBackground(steel_blue_rgb)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("highlight picked actor spheres")
render_window.SetMultiSamples(0)
render_window.SetSize(640, 480)

# Interactor: handle mouse and keyboard events with custom picking style
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

style = MouseInteractorHighLightActor()
style.SetDefaultRenderer(renderer)
render_window_interactor.SetInteractorStyle(style)

render_window_interactor.Initialize()
render_window_interactor.Start()
