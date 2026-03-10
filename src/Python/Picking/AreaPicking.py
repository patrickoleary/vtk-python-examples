#!/usr/bin/env python

# Area picking with rubber-band selection. Press 'r' to enter rubber-band
# mode, then drag a rectangle to select actors. Selected actors are
# highlighted in red; non-selected actors are restored to their original color.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkCommonCore import vtkMinimalStandardRandomSequence
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkInteractionStyle import vtkInteractorStyleRubberBandPick
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkAreaPicker,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
red_rgb = (1.0, 0.0, 0.0)
steel_blue_rgb = (0.275, 0.510, 0.706)
white_rgb = (1.0, 1.0, 1.0)

NUM_SPHERES = 20


def pick_callback(obj, event):
    """Callback invoked when an area pick completes."""
    picker = obj
    props = picker.GetProp3Ds()
    props.InitTraversal()

    # Reset all actors to original color first
    actors = renderer.GetActors()
    actors.InitTraversal()
    for _ in range(actors.GetNumberOfItems()):
        a = actors.GetNextActor()
        a.GetProperty().SetColor(a.GetProperty().GetDiffuseColor())

    # Highlight picked actors in red
    num_picked = props.GetNumberOfItems()
    for _ in range(num_picked):
        prop = props.GetNextProp3D()
        if prop:
            prop.GetProperty().SetColor(red_rgb)

    if num_picked > 0:
        print(f"Picked {num_picked} actor(s)")

    renderer.GetRenderWindow().Render()


# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.SetBackground(steel_blue_rgb)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(640, 480)
render_window.SetWindowName("AreaPicking")

# AreaPicker: select actors within a rectangular region
area_picker = vtkAreaPicker()
area_picker.AddObserver("EndPickEvent", pick_callback)

# Interactor: rubber-band selection style
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)
render_window_interactor.SetPicker(area_picker)

style = vtkInteractorStyleRubberBandPick()
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
    radius = rand_seq.GetRangeValue(0.3, 0.8)
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
