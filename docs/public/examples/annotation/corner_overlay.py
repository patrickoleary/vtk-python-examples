#!/usr/bin/env python

# Test vtkCornerAnnotation with image actor and window/level display.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkImagingColor import vtkImageMapToWindowLevelColors
from vtkmodules.vtkImagingCore import vtkImageShiftScale
from vtkmodules.vtkImagingSources import vtkImageMandelbrotSource
from vtkmodules.vtkRenderingAnnotation import vtkCornerAnnotation
from vtkmodules.vtkRenderingCore import (
    vtkImageActor,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Source
mandelbrot_source = vtkImageMandelbrotSource()

# Filter
shift_scale_filter = vtkImageShiftScale()
shift_scale_filter.SetInputConnection(mandelbrot_source.GetOutputPort())
shift_scale_filter.SetScale(100)
shift_scale_filter.SetShift(0)
shift_scale_filter.SetOutputScalarTypeToShort()
shift_scale_filter.Update()

# Window/level mapping
window_level_colors = vtkImageMapToWindowLevelColors()
window_level_colors.SetInputConnection(shift_scale_filter.GetOutputPort())
window_level_colors.SetWindow(10000)
window_level_colors.SetLevel(5000)

# Image actor
image_actor = vtkImageActor()
image_actor.GetMapper().SetInputConnection(window_level_colors.GetOutputPort())

# Corner annotation
corner_annotation = vtkCornerAnnotation()
corner_annotation.SetImageActor(image_actor)
corner_annotation.SetWindowLevel(window_level_colors)
corner_annotation.SetLinearFontScaleFactor(2)
corner_annotation.SetNonlinearFontScaleFactor(1)
corner_annotation.SetMaximumFontSize(20)

corner_annotation.SetText(vtkCornerAnnotation.LowerLeft, "LL (<image>)")
corner_annotation.SetText(vtkCornerAnnotation.LowerRight, "LR (<image_and_max>)")
corner_annotation.SetText(vtkCornerAnnotation.UpperLeft, "UL (<slice>)")
corner_annotation.SetText(vtkCornerAnnotation.UpperRight, "UR (<slice_and_max>)")
corner_annotation.SetText(vtkCornerAnnotation.UpperEdge, "T (<window_level>)")
corner_annotation.SetText(vtkCornerAnnotation.LowerEdge, "B (<slice_pos>)")
corner_annotation.SetText(vtkCornerAnnotation.LeftEdge, "L (<window>)")
corner_annotation.SetText(vtkCornerAnnotation.RightEdge, "R (<level>)")

corner_annotation.GetTextProperty().SetColor(1, 0, 0)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(image_actor)
renderer.AddViewProp(corner_annotation)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("corner overlay")
render_window.SetMultiSamples(0)
render_window.SetSize(800, 600)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
