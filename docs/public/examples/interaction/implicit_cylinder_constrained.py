#!/usr/bin/env python
# Demonstrate vtkImplicitCylinderWidget with constraint and bounds testing.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonDataModel import vtkCylinder
from vtkmodules.vtkFiltersCore import vtkAppendPolyData, vtkClipPolyData, vtkGlyph3D
from vtkmodules.vtkFiltersSources import vtkConeSource, vtkSphereSource
from vtkmodules.vtkInteractionWidgets import (
    vtkImplicitCylinderRepresentation,
    vtkImplicitCylinderWidget,
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

cylinder = vtkCylinder()
clipper = vtkClipPolyData()
clipper.SetInputConnection(append_filter.GetOutputPort())
clipper.SetClipFunction(cylinder)
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
render_window.SetWindowName("implicit cylinder constrained")
render_window.SetMultiSamples(0)
render_window.SetSize(300, 300)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)


# Callback updates the cylinder implicit function on interaction
def cylinder_callback(caller, event_string):
    widget_rep = caller.GetRepresentation()
    widget_rep.GetCylinder(cylinder)
    select_actor.VisibilityOn()


# Widget
cylinder_rep = vtkImplicitCylinderRepresentation()
cylinder_rep.SetPlaceFactor(1.25)
cylinder_rep.PlaceWidget(glyph.GetOutput().GetBounds())

cylinder_widget = vtkImplicitCylinderWidget()
cylinder_widget.SetInteractor(interactor)
cylinder_widget.SetRepresentation(cylinder_rep)
cylinder_widget.AddObserver("InteractionEvent", cylinder_callback)
cylinder_widget.SetEnabled(1)

# Constraint tests
center = cylinder_rep.GetCenter()

# Test 1: With ConstrainCenter on, center should not be settable outside widget bounds
cylinder_rep.ConstrainToWidgetBoundsOn()
wbounds = cylinder_rep.GetWidgetBounds()
cylinder_rep.SetCenter(wbounds[1] + 1.0, wbounds[3] + 1.0, wbounds[5] + 1.0)
center1 = cylinder_rep.GetCenter()

# Test 2: With ConstrainCenter off, center should be settable outside current widget bounds
cylinder_rep.ConstrainToWidgetBoundsOff()
cylinder_rep.SetCenter(wbounds[1] + 1.0, wbounds[3] + 1.0, wbounds[5] + 1.0)
center2 = cylinder_rep.GetCenter()

cylinder_rep.SetCenter(center)
cylinder_widget.SetEnabled(0)

# Test 3: With ConstrainCenter on and OutsideBounds off, translation limited
cylinder_rep.OutsideBoundsOff()
cylinder_rep.ConstrainToWidgetBoundsOn()

# Scene
renderer.ResetCamera()

interactor.Initialize()
interactor.Start()
