#!/usr/bin/env python
# Demonstrate vtkSliderWidget with 2D and 3D representations in multiple viewports.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersCore import vtkAppendPolyData, vtkGlyph3D
from vtkmodules.vtkFiltersSources import vtkConeSource, vtkSphereSource
from vtkmodules.vtkInteractionWidgets import (
    vtkSliderRepresentation2D,
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

# Renderers
renderer_0 = vtkRenderer()
renderer_0.SetViewport(0, 0, 0.5, 1.0)
renderer_0.SetBackground(0.1, 0.2, 0.4)
renderer_0.AddActor(mace_actor)

renderer_1 = vtkRenderer()
renderer_1.SetViewport(0.5, 0, 1.0, 1.0)
renderer_1.SetBackground(0.9, 0.4, 0.2)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer_0)
render_window.AddRenderer(renderer_1)
render_window.SetWindowName("slider widget multiple viewports")
render_window.SetMultiSamples(0)
render_window.SetSize(300, 300)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)


# Callback updates glyph scale factor from slider value
def slider_callback(caller, event_string):
    value = caller.GetRepresentation().GetValue()
    glyph.SetScaleFactor(value)


# Widgets
# 2D slider widget in the second viewport
slider_rep_2d = vtkSliderRepresentation2D()
slider_rep_2d.SetValue(0.25)
slider_rep_2d.SetTitleText("Spike Size")
slider_rep_2d.GetPoint1Coordinate().SetCoordinateSystemToNormalizedDisplay()
slider_rep_2d.GetPoint1Coordinate().SetValue(0.1, 0.1)
slider_rep_2d.GetPoint2Coordinate().SetCoordinateSystemToNormalizedDisplay()
slider_rep_2d.GetPoint2Coordinate().SetValue(0.4, 0.1)
slider_rep_2d.SetSliderLength(0.02)
slider_rep_2d.SetSliderWidth(0.03)
slider_rep_2d.SetEndCapLength(0.01)
slider_rep_2d.SetEndCapWidth(0.03)
slider_rep_2d.SetTubeWidth(0.005)

slider_widget_2d = vtkSliderWidget()
slider_widget_2d.SetInteractor(interactor)
slider_widget_2d.SetRepresentation(slider_rep_2d)
slider_widget_2d.SetCurrentRenderer(renderer_1)
slider_widget_2d.SetAnimationModeToAnimate()
slider_widget_2d.AddObserver("InteractionEvent", slider_callback)
slider_widget_2d.EnabledOn()

# 3D slider widget in the second viewport
slider_rep_3d = vtkSliderRepresentation3D()
slider_rep_3d.SetValue(0.25)
slider_rep_3d.SetTitleText("Spike Size")
slider_rep_3d.GetPoint1Coordinate().SetCoordinateSystemToWorld()
slider_rep_3d.GetPoint1Coordinate().SetValue(0, 0, 0)
slider_rep_3d.GetPoint2Coordinate().SetCoordinateSystemToWorld()
slider_rep_3d.GetPoint2Coordinate().SetValue(2, 0, 0)
slider_rep_3d.SetSliderLength(0.075)
slider_rep_3d.SetSliderWidth(0.05)
slider_rep_3d.SetEndCapLength(0.05)

slider_widget_3d = vtkSliderWidget()
slider_widget_3d.GetEventTranslator().SetTranslation(
    "RightButtonPressEvent", "SelectEvent"
)
slider_widget_3d.GetEventTranslator().SetTranslation(
    "RightButtonReleaseEvent", "EndSelectEvent"
)
slider_widget_3d.SetInteractor(interactor)
slider_widget_3d.SetRepresentation(slider_rep_3d)
slider_widget_3d.SetCurrentRenderer(renderer_1)
slider_widget_3d.SetAnimationModeToAnimate()
slider_widget_3d.AddObserver("InteractionEvent", slider_callback)
slider_widget_3d.EnabledOn()

# Scene
renderer_0.ResetCamera()

interactor.Initialize()
interactor.Start()
