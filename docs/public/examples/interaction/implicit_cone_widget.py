#!/usr/bin/env python
# Demonstrate vtkImplicitConeWidget clipping a mace geometry.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonDataModel import vtkCone
from vtkmodules.vtkFiltersCore import vtkAppendPolyData, vtkClipPolyData, vtkGlyph3D
from vtkmodules.vtkFiltersSources import vtkConeSource, vtkSphereSource
from vtkmodules.vtkInteractionWidgets import (
    vtkImplicitConeRepresentation,
    vtkImplicitConeWidget,
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
cone_source = vtkConeSource()

# Filters
glyph = vtkGlyph3D()
glyph.SetInputConnection(sphere.GetOutputPort())
glyph.SetSourceConnection(cone_source.GetOutputPort())
glyph.SetVectorModeToUseNormal()
glyph.SetScaleModeToScaleByVector()
glyph.SetScaleFactor(0.25)
glyph.Update()

append_filter = vtkAppendPolyData()
append_filter.AddInputConnection(glyph.GetOutputPort())
append_filter.AddInputConnection(sphere.GetOutputPort())

cone = vtkCone()
cone.SetIsDoubleCone(False)

clipper = vtkClipPolyData()
clipper.SetInputConnection(append_filter.GetOutputPort())
clipper.SetClipFunction(cone)
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
render_window.SetWindowName("implicit cone widget")
render_window.SetMultiSamples(0)
render_window.SetSize(300, 300)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)


# Callback updates the cone implicit function on interaction
def cone_callback(caller, event_string):
    widget_rep = caller.GetRepresentation()
    widget_rep.GetCone(cone)
    select_actor.VisibilityOn()


# Widget
cone_rep = vtkImplicitConeRepresentation()
cone_rep.SetPlaceFactor(1.25)
cone_rep.PlaceWidget(glyph.GetOutput().GetBounds())

cone_widget = vtkImplicitConeWidget()
cone_widget.SetInteractor(interactor)
cone_widget.SetRepresentation(cone_rep)
cone_widget.AddObserver("InteractionEvent", cone_callback)
cone_widget.SetEnabled(True)

# Scene
renderer.ResetCamera()

interactor.Initialize()
interactor.Start()
