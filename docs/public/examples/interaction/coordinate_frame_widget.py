#!/usr/bin/env python
# Demonstrate vtkCoordinateFrameWidget clipping a mace geometry.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonDataModel import vtkPlane
from vtkmodules.vtkFiltersCore import vtkAppendPolyData, vtkClipPolyData, vtkGlyph3D
from vtkmodules.vtkFiltersSources import vtkConeSource, vtkSphereSource
from vtkmodules.vtkInteractionWidgets import (
    vtkCoordinateFrameRepresentation,
    vtkCoordinateFrameWidget,
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

apd = vtkAppendPolyData()
apd.AddInputConnection(glyph.GetOutputPort())
apd.AddInputConnection(sphere.GetOutputPort())

plane = vtkPlane()
clipper = vtkClipPolyData()
clipper.SetInputConnection(apd.GetOutputPort())
clipper.SetClipFunction(plane)
clipper.InsideOutOn()

# Mapper + Actor
select_mapper = vtkPolyDataMapper()
select_mapper.SetInputConnection(clipper.GetOutputPort())

select_actor = vtkLODActor()
select_actor.SetMapper(select_mapper)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(select_actor)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("coordinate frame widget")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Widget
frame_rep = vtkCoordinateFrameRepresentation()
frame_rep.SetPlaceFactor(1.25)
frame_rep.PlaceWidget(select_actor.GetBounds())
frame_rep.SetNormal(plane.GetNormal())

frame_widget = vtkCoordinateFrameWidget()
frame_widget.SetInteractor(interactor)
frame_widget.SetRepresentation(frame_rep)
frame_widget.On()

interactor.Initialize()
interactor.Start()
