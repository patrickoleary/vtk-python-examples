#!/usr/bin/env python
# Demonstrate vtkBoxWidget2 with vtkBoxRepresentation and transform callback on mace geometry.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonTransforms import vtkTransform
from vtkmodules.vtkFiltersCore import (
    vtkAppendPolyData,
    vtkGlyph3D,
)
from vtkmodules.vtkFiltersSources import (
    vtkConeSource,
    vtkSphereSource,
)
from vtkmodules.vtkInteractionWidgets import (
    vtkBoxRepresentation,
    vtkBoxWidget2,
)
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Create mace geometry (sphere with cone glyphs)
cone = vtkConeSource()
cone.SetResolution(6)

sphere = vtkSphereSource()
sphere.SetThetaResolution(8)
sphere.SetPhiResolution(8)

glyph = vtkGlyph3D()
glyph.SetInputConnection(sphere.GetOutputPort())
glyph.SetSourceConnection(cone.GetOutputPort())
glyph.SetVectorModeToUseNormal()
glyph.SetScaleModeToScaleByVector()
glyph.SetScaleFactor(0.25)
glyph.Update()

append = vtkAppendPolyData()
append.AddInputConnection(glyph.GetOutputPort())
append.AddInputConnection(sphere.GetOutputPort())

mace_mapper = vtkPolyDataMapper()
mace_mapper.SetInputConnection(append.GetOutputPort())

mace_actor = vtkActor()
mace_actor.SetMapper(mace_mapper)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(mace_actor)
renderer.SetBackground(0, 0, 0)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("box widget transform callback")
render_window.SetSize(300, 300)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Callback
transform = vtkTransform()


def box_callback(widget, event_string):
    box_rep = widget.GetRepresentation()
    box_rep.GetTransform(transform)
    mace_actor.SetUserTransform(transform)


# Widget
box_rep = vtkBoxRepresentation()
box_rep.SetPlaceFactor(1.25)
box_rep.PlaceWidget(glyph.GetOutput().GetBounds())

box_widget = vtkBoxWidget2()
box_widget.SetInteractor(interactor)
box_widget.SetRepresentation(box_rep)
box_widget.AddObserver("InteractionEvent", box_callback)
box_widget.SetPriority(1)

interactor.Initialize()
interactor.Start()
