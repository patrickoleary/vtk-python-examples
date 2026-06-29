#!/usr/bin/env python
# Demonstrate vtkBoxWidget to define a clipping box on a mace geometry.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonDataModel import vtkPlanes
from vtkmodules.vtkFiltersCore import (
    vtkAppendPolyData,
    vtkClipPolyData,
    vtkGlyph3D,
)
from vtkmodules.vtkFiltersSources import (
    vtkConeSource,
    vtkSphereSource,
)
from vtkmodules.vtkInteractionWidgets import vtkBoxWidget
from vtkmodules.vtkRenderingCore import (
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)
from vtkmodules.vtkRenderingLOD import vtkLODActor

# Create a mace from a sphere with cone glyphs
sphere = vtkSphereSource()

cone = vtkConeSource()

glyph = vtkGlyph3D()
glyph.SetInputConnection(sphere.GetOutputPort())
glyph.SetSourceConnection(cone.GetOutputPort())
glyph.SetVectorModeToUseNormal()
glyph.SetScaleModeToScaleByVector()
glyph.SetScaleFactor(0.25)

# Append sphere and glyphs into a single polydata
apd = vtkAppendPolyData()
apd.AddInputConnection(glyph.GetOutputPort())
apd.AddInputConnection(sphere.GetOutputPort())

# Map and create the mace actor
mace_mapper = vtkPolyDataMapper()
mace_mapper.SetInputConnection(apd.GetOutputPort())

mace_actor = vtkLODActor()
mace_actor.SetMapper(mace_mapper)
mace_actor.VisibilityOn()

# Set up clipping with vtkPlanes
planes = vtkPlanes()

clipper = vtkClipPolyData()
clipper.SetInputConnection(apd.GetOutputPort())
clipper.SetClipFunction(planes)
clipper.InsideOutOn()

# Map and create the clipped region actor (green)
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
render_window.SetWindowName("box widget basic")
render_window.SetSize(300, 300)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)


# Callback to update clipping planes from box widget
def select_polygons(widget, event_string):
    box_widget.GetPlanes(planes)
    select_actor.VisibilityOn()


# Widget
box_widget = vtkBoxWidget()
box_widget.SetInteractor(interactor)
box_widget.SetInputConnection(glyph.GetOutputPort())
box_widget.PlaceWidget()
box_widget.AddObserver("EndInteractionEvent", select_polygons)

interactor.Initialize()
interactor.Start()
