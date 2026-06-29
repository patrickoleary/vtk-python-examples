#!/usr/bin/env python
# Demonstrate vtkCenteredSliderWidget controlling glyph scale on a mace geometry.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersCore import vtkAppendPolyData, vtkGlyph3D
from vtkmodules.vtkFiltersSources import (
    vtkConeSource,
    vtkSphereSource,
)
from vtkmodules.vtkInteractionWidgets import (
    vtkCenteredSliderWidget,
    vtkSliderRepresentation2D,
)
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)
from vtkmodules.vtkRenderingLOD import vtkLODActor

# Create a mace geometry (sphere + cone glyphs)
sphere = vtkSphereSource()

cone = vtkConeSource()

glyph = vtkGlyph3D()
glyph.SetInputConnection(sphere.GetOutputPort())
glyph.SetSourceConnection(cone.GetOutputPort())
glyph.SetVectorModeToUseNormal()
glyph.SetScaleModeToScaleByVector()
glyph.SetScaleFactor(0.25)

apd = vtkAppendPolyData()
apd.AddInputConnection(glyph.GetOutputPort())
apd.AddInputConnection(sphere.GetOutputPort())

mace_mapper = vtkPolyDataMapper()
mace_mapper.SetInputConnection(apd.GetOutputPort())

mace_actor = vtkLODActor()
mace_actor.SetMapper(mace_mapper)
mace_actor.VisibilityOn()
mace_actor.SetPosition(1, 1, 1)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(mace_actor)
renderer.SetBackground(0.1, 0.2, 0.4)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("centered slider widget2d")
render_window.SetSize(300, 300)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)


# Callback adjusts glyph scale factor based on slider value
def slider_callback(caller, event_string):
    value = caller.GetValue()
    glyph.SetScaleFactor(glyph.GetScaleFactor() * value)


# Widget
slider_rep = vtkSliderRepresentation2D()
slider_rep.SetMinimumValue(0.7)
slider_rep.SetMaximumValue(1.3)
slider_rep.SetValue(1.0)
slider_rep.SetTitleText("Spike Size")
slider_rep.GetPoint1Coordinate().SetCoordinateSystemToNormalizedDisplay()
slider_rep.GetPoint1Coordinate().SetValue(0.2, 0.1)
slider_rep.GetPoint2Coordinate().SetCoordinateSystemToNormalizedDisplay()
slider_rep.GetPoint2Coordinate().SetValue(0.8, 0.1)
slider_rep.SetSliderLength(0.02)
slider_rep.SetSliderWidth(0.03)
slider_rep.SetEndCapLength(0.03)
slider_rep.SetEndCapWidth(0.03)
slider_rep.SetTubeWidth(0.005)

slider_widget = vtkCenteredSliderWidget()
slider_widget.SetInteractor(interactor)
slider_widget.SetRepresentation(slider_rep)
slider_widget.AddObserver("InteractionEvent", slider_callback)
slider_widget.On()

interactor.Initialize()
interactor.Start()
