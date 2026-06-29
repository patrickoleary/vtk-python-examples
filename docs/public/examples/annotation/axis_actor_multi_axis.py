#!/usr/bin/env python

# Test vtkAxisActor with X, Y, and Z axes displayed together.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import vtkStringArray
from vtkmodules.vtkRenderingAnnotation import vtkAxisActor
from vtkmodules.vtkRenderingCore import (
    vtkCamera,
    vtkProperty,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
    vtkTextProperty,
)

# Shared labels
labels = vtkStringArray()
labels.SetNumberOfTuples(6)
labels.SetValue(0, "0")
labels.SetValue(1, "2")
labels.SetValue(2, "4")
labels.SetValue(3, "6")
labels.SetValue(4, "8")
labels.SetValue(5, "10")

# X axis
x_axis = vtkAxisActor()
x_axis.SetPoint1(0, 0, 0)
x_axis.SetPoint2(10, 0, 0)
x_axis.SetTitle("X Axis")
x_axis.SetBounds(0, 10, 0, 0, 0, 0)
x_axis.SetTickLocationToBoth()
x_axis.SetAxisTypeToX()
x_axis.SetRange(0, 10)
x_axis.SetLabelOffset(5)
x_axis.SetDeltaRangeMajor(2)
x_axis.SetDeltaRangeMinor(0.5)
x_axis.SetExponent("+00")
x_axis.SetExponentVisibility(True)
x_axis.SetExponentOffset(30)
x_axis.SetTitleOffset(0, 30)
x_axis.SetTitleScale(0.8)
x_axis.SetLabelScale(0.5)
x_axis.SetLabels(labels)

x_title_prop = vtkTextProperty()
x_title_prop.SetColor(0.0, 0.0, 1.0)
x_title_prop.SetOpacity(0.9)
x_title_prop.SetFontSize(24)
x_axis.SetTitleTextProperty(x_title_prop)

x_label_prop = vtkTextProperty()
x_label_prop.SetColor(1.0, 0.0, 0.0)
x_label_prop.SetOpacity(0.6)
x_label_prop.SetFontSize(18)
x_axis.SetLabelTextProperty(x_label_prop)

x_main_prop = vtkProperty()
x_main_prop.SetColor(1.0, 0.0, 1.0)
x_axis.SetAxisMainLineProperty(x_main_prop)

x_major_prop = vtkProperty()
x_major_prop.SetColor(1.0, 1.0, 0.0)
x_axis.SetAxisMajorTicksProperty(x_major_prop)

x_minor_prop = vtkProperty()
x_minor_prop.SetColor(0.0, 1.0, 1.0)
x_axis.SetAxisMinorTicksProperty(x_minor_prop)

# Y axis
y_axis = vtkAxisActor()
y_axis.SetPoint1(0, 0, 0)
y_axis.SetPoint2(0, 10, 0)
y_axis.SetTitle("Y Axis")
y_axis.SetBounds(0, 0, 0, 10, 0, 0)
y_axis.SetTickLocationToInside()
y_axis.SetAxisTypeToY()
y_axis.SetRange(0.1, 4000)
y_axis.SetMajorRangeStart(0.1)
y_axis.SetMinorRangeStart(0.1)
y_axis.SetMinorTicksVisible(True)
y_axis.SetTitleAlignLocation(vtkAxisActor.VTK_ALIGN_TOP)
y_axis.SetTitleOffset(0, 3)
y_axis.SetExponentLocation(vtkAxisActor.VTK_ALIGN_TOP)
y_axis.SetExponent("+00")
y_axis.SetExponentVisibility(True)
y_axis.SetExponentOffset(20)
y_axis.SetLog(True)
y_axis.SetTitleScale(0.8)
y_axis.SetLabelScale(0.5)
y_axis.SetLabels(labels)

y_title_prop = vtkTextProperty()
y_title_prop.SetColor(1.0, 0.0, 0.0)
y_title_prop.SetOpacity(0.6)
y_axis.SetTitleTextProperty(y_title_prop)

y_lines_prop = vtkProperty()
y_lines_prop.SetColor(1.0, 0.0, 1.0)
y_axis.SetAxisLinesProperty(y_lines_prop)

# Z axis
z_axis = vtkAxisActor()
z_axis.SetPoint1(0, 0, 0)
z_axis.SetPoint2(0, 0, 10)
z_axis.SetTitle("Z Axis")
z_axis.SetBounds(0, 0, 0, 0, 0, 10)
z_axis.SetTickLocationToOutside()
z_axis.SetAxisTypeToZ()
z_axis.SetRange(0, 10)
z_axis.SetTitleAlignLocation(vtkAxisActor.VTK_ALIGN_POINT2)
z_axis.SetExponentLocation(vtkAxisActor.VTK_ALIGN_POINT1)
z_axis.SetTitleOffset(-80, -150)
z_axis.SetExponent("+00")
z_axis.SetExponentVisibility(True)
z_axis.SetExponentOffset(-150)
z_axis.SetMajorTickSize(3)
z_axis.SetMinorTickSize(1)
z_axis.SetDeltaRangeMajor(2)
z_axis.SetDeltaRangeMinor(0.5)
z_axis.SetTitleScale(0.8)
z_axis.SetLabelScale(0.5)
z_axis.SetLabels(labels)

z_title_prop = vtkTextProperty()
z_title_prop.SetColor(0.0, 1.0, 0.0)
z_title_prop.SetOpacity(1.0)
z_axis.SetTitleTextProperty(z_title_prop)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(x_axis)
renderer.AddActor(y_axis)
renderer.AddActor(z_axis)
renderer.SetBackground(0.5, 0.5, 0.5)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("axis actor multi axis")
render_window.SetMultiSamples(0)
render_window.SetSize(500, 500)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
x_axis.SetCamera(renderer.GetActiveCamera())
y_axis.SetCamera(renderer.GetActiveCamera())
z_axis.SetCamera(renderer.GetActiveCamera())
render_window.Render()
renderer.GetActiveCamera().Azimuth(45)
renderer.GetActiveCamera().Elevation(45)
renderer.ResetCameraScreenSpace()

interactor.Initialize()
interactor.Start()
