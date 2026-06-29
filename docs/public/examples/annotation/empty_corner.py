#!/usr/bin/env python

# Test vtkCornerAnnotation with an emptied text slot to verify no artifact box.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkRenderingAnnotation import vtkCornerAnnotation
from vtkmodules.vtkRenderingCore import (
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Renderer
renderer = vtkRenderer()
renderer.SetBackground(0.5, 0.5, 0.5)

# Corner annotation
corner_annotation = vtkCornerAnnotation()
corner_annotation.SetLinearFontScaleFactor(2)
corner_annotation.SetNonlinearFontScaleFactor(1)
corner_annotation.SetMaximumFontSize(20)
corner_annotation.SetText(0, "normal text")
corner_annotation.SetText(1, "1234567890")
corner_annotation.SetText(2, "~`!@#$%^&*()_-+=")
corner_annotation.SetText(3, "text to remove")
corner_annotation.GetTextProperty().SetColor(1, 0, 0)

renderer.AddViewProp(corner_annotation)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("empty corner")
render_window.SetMultiSamples(0)
render_window.SetSize(300, 300)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# First render with all text
render_window.Render()

# Empty annotation #3 — should not display a black or white box
corner_annotation.SetText(3, "")

interactor.Initialize()
interactor.Start()
