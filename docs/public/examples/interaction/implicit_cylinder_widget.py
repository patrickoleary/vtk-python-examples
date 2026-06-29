#!/usr/bin/env python
# Demonstrate vtkImplicitCylinderWidget clipping a mace geometry.

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
render_window.SetWindowName("implicit cylinder widget")
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
cylinder_rep.SetRadius(0.25)
cylinder_rep.GetCylinderProperty().SetOpacity(0.1)

cylinder_widget = vtkImplicitCylinderWidget()
cylinder_widget.SetInteractor(interactor)
cylinder_widget.SetRepresentation(cylinder_rep)
cylinder_widget.AddObserver("InteractionEvent", cylinder_callback)
cylinder_widget.SetEnabled(True)

# Scene
renderer.ResetCamera()

interactor.Initialize()
interactor.Start()
