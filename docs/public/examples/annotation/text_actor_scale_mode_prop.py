#!/usr/bin/env python

# Test vtkTextActor with PROP scale mode and pre-instantiated text property.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import VTK_ARIAL, VTK_TEXT_BOTTOM, VTK_TEXT_LEFT
from vtkmodules.vtkRenderingCore import (
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
    vtkTextActor,
    vtkTextProperty,
)

# Pre-instantiated text property (VTK bug 15412)
text_property = vtkTextProperty()
text_property.SetBold(1)
text_property.SetItalic(1)
text_property.SetShadow(0)
text_property.SetFontFamily(VTK_ARIAL)
text_property.SetJustification(VTK_TEXT_LEFT)
text_property.SetVerticalJustification(VTK_TEXT_BOTTOM)

# Text actor with PROP scale mode
text_actor = vtkTextActor()
text_actor.GetPositionCoordinate().SetCoordinateSystemToDisplay()
text_actor.GetPositionCoordinate().SetReferenceCoordinate(None)
text_actor.GetPosition2Coordinate().SetCoordinateSystemToDisplay()
text_actor.GetPosition2Coordinate().SetReferenceCoordinate(None)
text_actor.SetTextScaleModeToProp()
text_actor.SetTextProperty(text_property)
text_actor.SetInput("15412")
text_actor.GetPositionCoordinate().SetValue(20.0, 20.0, 0.0)
text_actor.GetPosition2Coordinate().SetValue(280.0, 80.0, 0.0)

# Renderer
renderer = vtkRenderer()
renderer.SetBackground(0.1, 0.1, 0.1)
renderer.AddViewProp(text_actor)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("text actor scale mode prop")
render_window.SetMultiSamples(0)
render_window.SetSize(300, 300)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
