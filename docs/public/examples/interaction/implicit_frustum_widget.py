#!/usr/bin/env python
# Demonstrate vtkImplicitFrustumWidget clipping a mace geometry.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonDataModel import vtkFrustum
from vtkmodules.vtkFiltersCore import vtkAppendPolyData, vtkClipPolyData, vtkGlyph3D
from vtkmodules.vtkFiltersSources import vtkConeSource, vtkSphereSource
from vtkmodules.vtkInteractionWidgets import (
    vtkImplicitFrustumRepresentation,
    vtkImplicitFrustumWidget,
)
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

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

frustum = vtkFrustum()

clipper = vtkClipPolyData()
clipper.SetInputConnection(append_filter.GetOutputPort())
clipper.SetClipFunction(frustum)
clipper.InsideOutOn()

# Mapper + Actor: mace
mace_mapper = vtkPolyDataMapper()
mace_mapper.SetInputConnection(append_filter.GetOutputPort())

mace_actor = vtkActor()
mace_actor.SetMapper(mace_mapper)
mace_actor.VisibilityOn()

# Mapper + Actor: clipped selection
select_mapper = vtkPolyDataMapper()
select_mapper.SetInputConnection(clipper.GetOutputPort())

select_actor = vtkActor()
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
render_window.SetWindowName("implicit frustum widget")
render_window.SetMultiSamples(0)
render_window.SetSize(300, 300)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)


# Callback updates the frustum implicit function on interaction
def frustum_callback(caller, event_string):
    widget_rep = caller.GetRepresentation()
    widget_rep.GetFrustum(frustum)
    select_actor.VisibilityOn()


# Widget
frustum_rep = vtkImplicitFrustumRepresentation()
frustum_rep.SetPlaceFactor(1.25)
frustum_rep.PlaceWidget(glyph.GetOutput().GetBounds())
frustum_rep.SetOrigin(-0.8, -0.8, 0)
frustum_rep.SetOrientation(0, 0, -45)

frustum_widget = vtkImplicitFrustumWidget()
frustum_widget.SetInteractor(interactor)
frustum_widget.SetRepresentation(frustum_rep)
frustum_widget.AddObserver("InteractionEvent", frustum_callback)
frustum_widget.SetEnabled(True)

# Scene
renderer.ResetCamera()

interactor.Initialize()
interactor.Start()
