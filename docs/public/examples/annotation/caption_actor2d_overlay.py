#!/usr/bin/env python

# Test vtkCaptionActor2D with an arrow leader glyph.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersSources import vtkArrowSource
from vtkmodules.vtkRenderingAnnotation import vtkCaptionActor2D
from vtkmodules.vtkRenderingCore import (
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Caption actor
caption_actor = vtkCaptionActor2D()
caption_actor.SetAttachmentPoint(0, 0, 0)
caption_actor.SetCaption("(2) 2.27")
caption_actor.BorderOff()

# Arrow leader glyph
leader_glyph = vtkArrowSource()
leader_glyph.SetShaftRadius(0.2)
leader_glyph.SetTipRadius(0.5)
leader_glyph.SetTipLength(0.6)
leader_glyph.Update()

caption_actor.SetLeaderGlyphConnection(leader_glyph.GetOutputPort())
caption_actor.SetLeaderGlyphSize(0.05)
caption_actor.SetMaximumLeaderGlyphSize(30)

caption_actor.SetPadding(0)
caption_actor.GetCaptionTextProperty().SetJustificationToLeft()
caption_actor.GetCaptionTextProperty().ShadowOff()
caption_actor.GetCaptionTextProperty().ItalicOff()
caption_actor.GetCaptionTextProperty().SetFontFamilyToCourier()
caption_actor.GetCaptionTextProperty().SetFontSize(24)
caption_actor.GetTextActor().SetTextScaleModeToNone()
caption_actor.SetPosition(0.0, 50.0)

# Renderer
renderer = vtkRenderer()
renderer.SetBackground(0, 0, 0)
renderer.AddActor(caption_actor)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("caption actor2d overlay")
render_window.SetMultiSamples(0)
render_window.SetSize(300, 300)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
