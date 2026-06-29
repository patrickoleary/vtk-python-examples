#!/usr/bin/env python

# Test vtkAxisActor configured as a Z axis with custom tick sizes and offsets.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import vtkStringArray
from vtkmodules.vtkRenderingAnnotation import vtkAxisActor
from vtkmodules.vtkRenderingCore import (
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
    vtkTextProperty,
)

# Create and configure Z axis
axis = vtkAxisActor()
axis.SetPoint1(0, 0, 0)
axis.SetPoint2(0, 0, 10)
axis.SetTitle("Z Axis")
axis.SetBounds(0, 0, 0, 0, 0, 10)
axis.SetTickLocationToOutside()
axis.SetAxisTypeToZ()
axis.SetRange(0, 10)
axis.SetTitleAlignLocation(vtkAxisActor.VTK_ALIGN_POINT2)
axis.SetExponentLocation(vtkAxisActor.VTK_ALIGN_POINT1)
axis.SetTitleOffset(-80, -150)
axis.SetExponent("+00")
axis.SetExponentVisibility(True)
axis.SetExponentOffset(-150)
axis.SetMajorTickSize(3)
axis.SetMinorTickSize(1)
axis.SetDeltaRangeMajor(2)
axis.SetDeltaRangeMinor(0.5)
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
title_text_prop.SetColor(0.0, 1.0, 0.0)
title_text_prop.SetOpacity(1.0)
axis.SetTitleTextProperty(title_text_prop)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(axis)
renderer.SetBackground(0.5, 0.5, 0.5)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("axis actor z")
render_window.SetMultiSamples(0)
render_window.SetSize(300, 300)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.GetActiveCamera().SetPosition(0, 10, 0)
renderer.GetActiveCamera().SetViewUp(1, 0, 0)
axis.SetCamera(renderer.GetActiveCamera())
render_window.Render()
renderer.ResetCameraScreenSpace(0.8)

interactor.Initialize()
interactor.Start()
