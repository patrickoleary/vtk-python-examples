#!/usr/bin/env python

# Demonstrate VTK observer callbacks using both a function and a callable
# class.  An orientation marker widget and an outline provide scene context.
# The camera orientation is printed to the console after each interaction.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkFiltersModeling import vtkOutlineFilter
from vtkmodules.vtkFiltersSources import vtkConeSource
from vtkmodules.vtkInteractionWidgets import vtkOrientationMarkerWidget
from vtkmodules.vtkRenderingAnnotation import vtkAxesActor
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkCamera,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
peacock_rgb = (0.200, 0.631, 0.788)
black_rgb = (0.0, 0.0, 0.0)
alice_blue_rgb = (0.941, 0.973, 1.0)

# Toggle between function callback and class callback
use_function_callback = True

# Source: generate a cone
cone = vtkConeSource()
cone.SetCenter(0, 0, 0)
cone.SetRadius(1)
cone.SetHeight(1.6180339887498948482)
cone.SetResolution(128)
cone.Update()

# Mapper: map cone polygon data to graphics primitives
cone_mapper = vtkPolyDataMapper()
cone_mapper.SetInputConnection(cone.GetOutputPort())

# Actor: assign the mapped geometry
cone_actor = vtkActor()
cone_actor.SetMapper(cone_mapper)
cone_actor.GetProperty().SetColor(peacock_rgb)
cone_actor.GetProperty().SetAmbient(0.3)
cone_actor.GetProperty().SetDiffuse(0.0)
cone_actor.GetProperty().SetSpecular(1.0)
cone_actor.GetProperty().SetSpecularPower(20.0)

# Outline: provide spatial context around the cone
outline = vtkOutlineFilter()
outline.SetInputData(cone.GetOutput())

outline_mapper = vtkPolyDataMapper()
outline_mapper.SetInputConnection(outline.GetOutputPort())

outline_actor = vtkActor()
outline_actor.GetProperty().SetColor(black_rgb)
outline_actor.SetMapper(outline_mapper)

# Camera: set up an initial view direction
camera = vtkCamera()
camera.SetPosition(4.6, -2.0, 3.8)
camera.SetFocalPoint(0.0, 0.0, 0.0)
camera.SetClippingRange(3.2, 10.2)
camera.SetViewUp(0.3, 1.0, 0.13)

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.AddActor(cone_actor)
renderer.AddActor(outline_actor)
renderer.SetActiveCamera(camera)
renderer.SetBackground(alice_blue_rgb)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(512, 512)
render_window.SetWindowName("CallBack")

# Interactor: handle mouse and keyboard events
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# OrientationMarker: axes widget in the lower-left corner
axes = vtkAxesActor()
axes.SetShaftTypeToCylinder()
axes.SetXAxisLabelText("X")
axes.SetYAxisLabelText("Y")
axes.SetZAxisLabelText("Z")
axes.SetTotalLength(1.0, 1.0, 1.0)
axes.SetCylinderRadius(0.5 * axes.GetCylinderRadius())
axes.SetConeRadius(1.025 * axes.GetConeRadius())
axes.SetSphereRadius(1.5 * axes.GetSphereRadius())

orientation_widget = vtkOrientationMarkerWidget()
orientation_widget.SetOrientationMarker(axes)
orientation_widget.SetViewport(0, 0, 0.2, 0.2)
orientation_widget.SetInteractor(interactor)
orientation_widget.EnabledOn()
orientation_widget.InteractiveOn()


# Callback function: print camera orientation after interaction
def get_orientation(caller, ev):
    cam = renderer.GetActiveCamera()
    fmt = "{:9.6g}"
    print(caller.GetClassName(), "Event Id:", ev)
    print("       Position:", ", ".join(map(fmt.format, cam.GetPosition())))
    print("    Focal point:", ", ".join(map(fmt.format, cam.GetFocalPoint())))
    print("  Clipping range:", ", ".join(map(fmt.format, cam.GetClippingRange())))
    print("        View up:", ", ".join(map(fmt.format, cam.GetViewUp())))
    print("       Distance:", fmt.format(cam.GetDistance()))


# Callback class: same behavior wrapped in a callable object
class OrientationObserver:
    def __init__(self, cam):
        self.cam = cam

    def __call__(self, caller, ev):
        fmt = "{:9.6g}"
        print(caller.GetClassName(), "Event Id:", ev)
        print("       Position:", ", ".join(map(fmt.format, self.cam.GetPosition())))
        print("    Focal point:", ", ".join(map(fmt.format, self.cam.GetFocalPoint())))
        print("  Clipping range:", ", ".join(map(fmt.format, self.cam.GetClippingRange())))
        print("        View up:", ", ".join(map(fmt.format, self.cam.GetViewUp())))
        print("       Distance:", fmt.format(self.cam.GetDistance()))


# Register the callback
if use_function_callback:
    interactor.AddObserver("EndInteractionEvent", get_orientation)
else:
    interactor.AddObserver("EndInteractionEvent", OrientationObserver(renderer.GetActiveCamera()))

# Launch the interactive visualization
interactor.Initialize()
interactor.Start()
