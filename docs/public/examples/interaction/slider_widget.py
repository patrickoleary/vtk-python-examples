#!/usr/bin/env python
# Demonstrate vtkSliderWidget with a 3D representation controlling glyph scale on a mace geometry.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersCore import vtkAppendPolyData, vtkGlyph3D
from vtkmodules.vtkFiltersSources import (
    vtkConeSource,
    vtkSphereSource,
)
from vtkmodules.vtkInteractionWidgets import (
    vtkSliderRepresentation3D,
    vtkSliderWidget,
)
from vtkmodules.vtkRenderingCore import (
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)
from vtkmodules.vtkRenderingLOD import vtkLODActor

# Sources
sphere_source = vtkSphereSource()

cone_source = vtkConeSource()

# Filters
glyph = vtkGlyph3D()
glyph.SetInputConnection(sphere_source.GetOutputPort())
glyph.SetSourceConnection(cone_source.GetOutputPort())
glyph.SetVectorModeToUseNormal()
glyph.SetScaleModeToScaleByVector()
glyph.SetScaleFactor(0.25)

append_filter = vtkAppendPolyData()
append_filter.AddInputConnection(glyph.GetOutputPort())
append_filter.AddInputConnection(sphere_source.GetOutputPort())

# Mapper + Actor
mace_mapper = vtkPolyDataMapper()
mace_mapper.SetInputConnection(append_filter.GetOutputPort())

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
render_window.SetWindowName("slider widget")
render_window.SetMultiSamples(0)
render_window.SetSize(300, 300)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)


# Callback updates glyph scale factor from slider value
def slider_callback(caller, event_string):
    value = caller.GetRepresentation().GetValue()
    glyph.SetScaleFactor(value)


# Widget
slider_rep = vtkSliderRepresentation3D()
slider_rep.SetValue(0.25)
slider_rep.SetTitleText("Spike Size")
slider_rep.GetPoint1Coordinate().SetCoordinateSystemToWorld()
slider_rep.GetPoint1Coordinate().SetValue(0, 0, 0)
slider_rep.GetPoint2Coordinate().SetCoordinateSystemToWorld()
slider_rep.GetPoint2Coordinate().SetValue(2, 0, 0)
slider_rep.SetSliderLength(0.075)
slider_rep.SetSliderWidth(0.05)
slider_rep.SetEndCapLength(0.05)

slider_widget = vtkSliderWidget()
slider_widget.SetInteractor(interactor)
slider_widget.SetRepresentation(slider_rep)
slider_widget.SetAnimationModeToAnimate()
slider_widget.AddObserver("InteractionEvent", slider_callback)
slider_widget.EnabledOn()

# Scene
renderer.ResetCamera()

interactor.Initialize()
interactor.Start()
