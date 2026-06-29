#!/usr/bin/env python
# Demonstrate 2D context drawing primitives: lines, points, poly, rect, quad, ellipse, markers.

import math

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingContextOpenGL2  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import vtkPoints2D
from vtkmodules.vtkCommonTransforms import vtkTransform2D
from vtkmodules.vtkPythonContext2D import vtkPythonItem
from vtkmodules.vtkRenderingContext2D import vtkContextActor
from vtkmodules.vtkRenderingCore import (
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)


class ContextDrawing:
    """Python object for vtkPythonItem that draws various 2D primitives."""

    def Initialize(self, vtkSelf):
        return True

    def Paint(self, vtkSelf, painter):
        # Draw a title string.
        painter.GetTextProp().SetVerticalJustificationToCentered()
        painter.GetTextProp().SetJustificationToCentered()
        painter.GetTextProp().SetColor(0.0, 0.0, 0.0)
        painter.GetTextProp().SetFontSize(24)
        painter.GetTextProp().SetFontFamilyToArial()
        painter.GetPen().SetColor(0, 0, 0, 255)
        painter.GetBrush().SetColor(0, 0, 0, 255)
        painter.DrawString(400, 25, "OpenGL is used as a backend to the context.")

        # Draw individual lines of different thicknesses.
        for i in range(10):
            painter.GetPen().SetColor(255, int(float(i) * 25.0), 0)
            painter.GetPen().SetWidth(1.0 + float(i))
            painter.DrawLine(10, 50 + float(i) * 10, 60, 50 + float(i) * 10)

        # Use DrawPoly to draw a sine wave shape.
        points = vtkPoints2D()
        points.SetNumberOfPoints(30)
        for i in range(30):
            points.SetPoint(i, float(i) * 25.0 + 10.0, math.sin(float(i) / 5.0) * 100.0 + 200.0)
        painter.GetPen().SetColor(0, 255, 0)
        painter.GetPen().SetWidth(5.0)
        painter.DrawPoly(points)

        # Draw corner points.
        painter.GetPen().SetColor(0, 0, 255)
        painter.GetPen().SetWidth(5.0)
        painter.DrawPoint(10, 10)
        painter.DrawPoint(790, 10)
        painter.DrawPoint(10, 590)
        painter.DrawPoint(790, 590)

        # Draw individual points at different sizes.
        for i in range(10):
            painter.GetPen().SetColor(0, int(float(i) * 25.0), 255, 255)
            painter.GetPen().SetWidth(1.0 + float(i))
            painter.DrawPoint(75, 50 + float(i) * 10)

        # Draw points along the poly path.
        painter.GetPen().SetColor(0, 0, 255)
        painter.GetPen().SetWidth(3.0)
        painter.DrawPoints(points)

        # Draw a rectangle.
        painter.GetPen().SetColor(100, 200, 255)
        painter.GetPen().SetWidth(3.0)
        painter.GetBrush().SetColor(100, 255, 100)
        painter.DrawRect(100, 50, 200, 100)

        # Draw a quad.
        painter.GetPen().SetColor(159, 0, 255)
        painter.GetPen().SetWidth(1.0)
        painter.GetBrush().SetColor(100, 55, 0, 200)
        painter.DrawQuad(350, 50, 375, 150, 525, 199, 666, 45)

        # Test transforms.
        transform = vtkTransform2D()
        transform.Translate(20, 200)
        painter.GetDevice().SetMatrix(transform.GetMatrix())
        painter.GetPen().SetColor(255, 0, 0)
        painter.GetPen().SetWidth(6.0)
        painter.DrawPoly(points)

        transform.Translate(0, 10)
        painter.GetDevice().SetMatrix(transform.GetMatrix())
        painter.GetPen().SetColor(0, 0, 200)
        painter.GetPen().SetWidth(2.0)
        painter.DrawPoints(points)

        transform.Translate(0, -20)
        painter.GetDevice().SetMatrix(transform.GetMatrix())
        painter.GetPen().SetColor(100, 0, 200)
        painter.GetPen().SetWidth(5.0)
        painter.DrawPoints(points)

        # Draw an ellipse.
        painter.GetPen().SetColor(0, 0, 0)
        painter.GetPen().SetWidth(1.0)
        painter.GetBrush().SetColor(0, 0, 100, 69)
        painter.DrawEllipse(110.0, 89.0, 20, 100)
        painter.DrawEllipseWedge(250.0, 89.0, 100, 20, 50, 10, 0, 360)

        return True


# Create the vtkPythonItem and set the drawing object.
python_item = vtkPythonItem()
python_item.SetPythonObject(ContextDrawing())

# Context actor and scene wiring.
context_actor = vtkContextActor()
context_actor.GetScene().AddItem(python_item)

# Renderer
renderer = vtkRenderer()
renderer.SetBackground(1.0, 1.0, 1.0)
context_actor.GetScene().SetRenderer(renderer)
renderer.AddActor(context_actor)

# Window
render_window = vtkRenderWindow()
render_window.SetSize(800, 600)
render_window.SetMultiSamples(0)
render_window.AddRenderer(renderer)
render_window.SetWindowName("context")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
