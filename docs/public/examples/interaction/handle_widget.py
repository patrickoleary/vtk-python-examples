#!/usr/bin/env python
# Demonstrate vtkHandleWidget constrained to an implicit plane on a mace geometry.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonDataModel import vtkPlane
from vtkmodules.vtkFiltersCore import vtkAppendPolyData, vtkCutter, vtkGlyph3D
from vtkmodules.vtkFiltersModeling import vtkOutlineFilter
from vtkmodules.vtkFiltersSources import vtkConeSource, vtkSphereSource
from vtkmodules.vtkInteractionWidgets import (
    vtkHandleWidget,
    vtkImplicitPlaneRepresentation,
    vtkImplicitPlaneWidget2,
    vtkPointHandleRepresentation3D,
)
from vtkmodules.vtkRenderingCore import (
    vtkActor,
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

apd = vtkAppendPolyData()
apd.AddInputConnection(glyph.GetOutputPort())
apd.AddInputConnection(sphere.GetOutputPort())

cut_plane = vtkPlane()

cutter = vtkCutter()
cutter.SetInputConnection(apd.GetOutputPort())
cutter.SetCutFunction(cut_plane)

outline = vtkOutlineFilter()
outline.SetInputConnection(apd.GetOutputPort())

# Mapper + Actor: cut selection
select_mapper = vtkPolyDataMapper()
select_mapper.SetInputConnection(cutter.GetOutputPort())

select_actor = vtkLODActor()
select_actor.SetMapper(select_mapper)
select_actor.GetProperty().SetColor(0, 1, 0)
select_actor.VisibilityOff()
select_actor.SetScale(1.01, 1.01, 1.01)

# Mapper + Actor: outline
outline_mapper = vtkPolyDataMapper()
outline_mapper.SetInputConnection(outline.GetOutputPort())

outline_actor = vtkActor()
outline_actor.SetMapper(outline_mapper)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(select_actor)
renderer.AddActor(outline_actor)
renderer.SetBackground(0.1, 0.2, 0.4)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("handle widget")
render_window.SetMultiSamples(0)
render_window.SetSize(300, 300)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)


# Callback updates cutting plane from the implicit plane widget
def plane_callback(caller, event_string):
    widget_rep = caller.GetRepresentation()
    widget_rep.GetPlane(cut_plane)
    select_actor.VisibilityOn()


# Widget: implicit plane
plane_rep = vtkImplicitPlaneRepresentation()
plane_rep.SetPlaceFactor(1.0)
plane_rep.GetPlaneProperty().SetAmbientColor(0.0, 0.5, 0.5)
plane_rep.GetPlaneProperty().SetOpacity(0.3)
plane_rep.PlaceWidget([-0.7, 0.7, -0.7, 0.7, -0.7, 0.7])
plane_rep.SetNormal(0.942174, 0.25322, 0.219519)
plane_rep.GetPlane(cut_plane)

plane_widget = vtkImplicitPlaneWidget2()
plane_widget.SetRepresentation(plane_rep)
plane_widget.SetInteractor(interactor)
plane_widget.AddObserver("InteractionEvent", plane_callback)
plane_widget.EnabledOn()

# Widget: handle
handle_rep = vtkPointHandleRepresentation3D()
handle_rep.SetPlaceFactor(2.5)
handle_rep.PlaceWidget(outline_actor.GetBounds())
handle_rep.SetHandleSize(30)
handle_rep.SetWorldPosition([-0.0417953, 0.202206, -0.0538641])

handle_widget = vtkHandleWidget()
handle_widget.SetInteractor(interactor)
handle_widget.SetRepresentation(handle_rep)
handle_widget.EnabledOn()

# Scene
renderer.ResetCamera()
renderer.ResetCameraClippingRange()

interactor.Initialize()
interactor.Start()
