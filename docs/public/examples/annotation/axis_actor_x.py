#!/usr/bin/env python

# Test vtkAxisActor configured as an X axis with custom labels and properties.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import vtkStringArray
from vtkmodules.vtkRenderingAnnotation import vtkAxisActor
from vtkmodules.vtkRenderingCore import (
    vtkProperty,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
    vtkTextProperty,
)

# Create and configure X axis
axis = vtkAxisActor()
axis.SetPoint1(0, 0, 0)
axis.SetPoint2(10, 0, 0)
axis.SetTitle("X Axis")
axis.SetBounds(0, 10, 0, 0, 0, 0)
axis.SetTickLocationToBoth()
axis.SetAxisTypeToX()
axis.SetRange(0, 10)
axis.SetLabelOffset(5)
axis.SetDeltaRangeMajor(2)
axis.SetDeltaRangeMinor(0.5)
axis.SetExponent("+00")
axis.SetExponentVisibility(True)
axis.SetExponentOffset(30)
axis.SetTitleOffset(0, 30)
axis.SetTitleScale(0.8)
axis.SetLabelScale(0.5)

# Custom labels
labels = vtkStringArray()
labels.SetNumberOfTuples(6)
labels.SetValue(0, "0")
labels.SetValue(1, "2")
labels.SetValue(2, "4")
labels.SetValue(3, "6")
labels.SetValue(4, "8")
labels.SetValue(5, "10")
axis.SetLabels(labels)

# Title text property
title_text_prop = vtkTextProperty()
title_text_prop.SetColor(0.0, 0.0, 1.0)
title_text_prop.SetOpacity(0.9)
title_text_prop.SetFontSize(24)
axis.SetTitleTextProperty(title_text_prop)

# Label text property
label_text_prop = vtkTextProperty()
label_text_prop.SetColor(1.0, 0.0, 0.0)
label_text_prop.SetOpacity(0.6)
label_text_prop.SetFontSize(18)
axis.SetLabelTextProperty(label_text_prop)

# Axis line properties
main_line_prop = vtkProperty()
main_line_prop.SetColor(1.0, 0.0, 1.0)
axis.SetAxisMainLineProperty(main_line_prop)

major_tick_prop = vtkProperty()
major_tick_prop.SetColor(1.0, 1.0, 0.0)
axis.SetAxisMajorTicksProperty(major_tick_prop)

minor_tick_prop = vtkProperty()
minor_tick_prop.SetColor(0.0, 1.0, 1.0)
axis.SetAxisMinorTicksProperty(minor_tick_prop)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(axis)
renderer.SetBackground(0.5, 0.5, 0.5)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("axis actor x")
render_window.SetMultiSamples(0)
render_window.SetSize(300, 300)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
axis.SetCamera(renderer.GetActiveCamera())
render_window.Render()
renderer.ResetCameraScreenSpace(0.8)

interactor.Initialize()
interactor.Start()
