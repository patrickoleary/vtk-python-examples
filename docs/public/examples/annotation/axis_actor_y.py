#!/usr/bin/env python

# Test vtkAxisActor configured as a Y axis with log scale and custom properties.

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

# Create and configure Y axis
axis = vtkAxisActor()
axis.SetPoint1(0, 0, 0)
axis.SetPoint2(0, 10, 0)
axis.SetTitle("Y Axis")
axis.SetBounds(0, 0, 0, 10, 0, 0)
axis.SetTickLocationToInside()
axis.SetAxisTypeToY()
axis.SetRange(0.1, 4000)
axis.SetMajorRangeStart(0.1)
axis.SetMinorRangeStart(0.1)
axis.SetMinorTicksVisible(True)
axis.SetTitleAlignLocation(vtkAxisActor.VTK_ALIGN_TOP)
axis.SetTitleOffset(0, 3)
axis.SetExponentLocation(vtkAxisActor.VTK_ALIGN_TOP)
axis.SetExponent("+00")
axis.SetExponentVisibility(True)
axis.SetExponentOffset(20)
axis.SetLog(True)
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
title_text_prop.SetColor(1.0, 0.0, 0.0)
title_text_prop.SetOpacity(0.6)
axis.SetTitleTextProperty(title_text_prop)

# Axis lines property
lines_prop = vtkProperty()
lines_prop.SetColor(1.0, 0.0, 1.0)
axis.SetAxisLinesProperty(lines_prop)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(axis)
renderer.SetBackground(0.5, 0.5, 0.5)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("axis actor y")
render_window.SetMultiSamples(0)
render_window.SetSize(300, 300)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.GetActiveCamera().SetViewUp(1, 0, 0)
axis.SetCamera(renderer.GetActiveCamera())
render_window.Render()
renderer.ResetCameraScreenSpace(0.8)

interactor.Initialize()
interactor.Start()
