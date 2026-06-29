#!/usr/bin/env python
# Demonstrate vtkImplicitPlaneWidget2 with constraint and bounds testing.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonDataModel import vtkPlane
from vtkmodules.vtkFiltersCore import vtkAppendPolyData, vtkClipPolyData, vtkGlyph3D
from vtkmodules.vtkFiltersSources import vtkConeSource, vtkSphereSource
from vtkmodules.vtkInteractionWidgets import (
    vtkImplicitPlaneRepresentation,
    vtkImplicitPlaneWidget2,
)
from vtkmodules.vtkRenderingCore import (
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)
from vtkmodules.vtkRenderingLOD import vtkLODActor

# Sources
sphere = vtkSphereSource()
cone = vtkConeSource()

# Filters
glyph = vtkGlyph3D()
glyph.SetInputConnection(sphere.GetOutputPort())
glyph.SetSourceConnection(cone.GetOutputPort())
glyph.SetVectorModeToUseNormal()
glyph.SetScaleModeToScaleByVector()
glyph.SetScaleFactor(0.25)
glyph.Update()

append_filter = vtkAppendPolyData()
append_filter.AddInputConnection(glyph.GetOutputPort())
append_filter.AddInputConnection(sphere.GetOutputPort())

plane = vtkPlane()
clipper = vtkClipPolyData()
clipper.SetInputConnection(append_filter.GetOutputPort())
clipper.SetClipFunction(plane)
clipper.InsideOutOn()

# Mapper + Actor: mace
mace_mapper = vtkPolyDataMapper()
mace_mapper.SetInputConnection(append_filter.GetOutputPort())

mace_actor = vtkLODActor()
mace_actor.SetMapper(mace_mapper)
mace_actor.VisibilityOn()

# Mapper + Actor: clipped selection
select_mapper = vtkPolyDataMapper()
select_mapper.SetInputConnection(clipper.GetOutputPort())

select_actor = vtkLODActor()
select_actor.SetMapper(select_mapper)
select_actor.GetProperty().SetColor(0, 1, 0)
select_actor.VisibilityOff()
select_actor.SetScale(1.01, 1.01, 1.01)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(mace_actor)
renderer.AddActor(select_actor)
renderer.SetBackground(0.1, 0.2, 0.4)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("implicit plane constrained")
render_window.SetMultiSamples(0)
render_window.SetSize(300, 300)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)


# Callback updates the plane implicit function on interaction
def plane_callback(caller, event_string):
    widget_rep = caller.GetRepresentation()
    widget_rep.GetPlane(plane)
    select_actor.VisibilityOn()


# Widget
plane_rep = vtkImplicitPlaneRepresentation()
plane_rep.SetPlaceFactor(1.25)
plane_rep.PlaceWidget(glyph.GetOutput().GetBounds())

plane_widget = vtkImplicitPlaneWidget2()
plane_widget.SetInteractor(interactor)
plane_widget.SetRepresentation(plane_rep)
plane_widget.AddObserver("InteractionEvent", plane_callback)
plane_widget.SetEnabled(1)

# Constraint tests
origin = plane_rep.GetOrigin()

# Test 1: With ConstrainOrigin on, origin should not be settable outside widget bounds
plane_rep.ConstrainToWidgetBoundsOn()
wbounds = plane_rep.GetWidgetBounds()
plane_rep.SetOrigin(wbounds[1] + 1.0, wbounds[3] + 1.0, wbounds[5] + 1.0)

# Test 2: With ConstrainOrigin off, origin should be settable outside current widget bounds
plane_rep.ConstrainToWidgetBoundsOff()
plane_rep.SetOrigin(wbounds[1] + 1.0, wbounds[3] + 1.0, wbounds[5] + 1.0)

plane_rep.SetOrigin(origin)
plane_widget.SetEnabled(0)

# Test 3: With ConstrainOrigin on and OutsideBounds off, translation limited
plane_rep.OutsideBoundsOff()
plane_rep.ConstrainToWidgetBoundsOn()

# Scene
renderer.ResetCamera()

interactor.Initialize()
interactor.Start()
