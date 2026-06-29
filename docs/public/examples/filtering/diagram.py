#!/usr/bin/env python
# Demonstrate a 2D API diagram drawn with context drawing primitives.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingContextOpenGL2  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkPythonContext2D import vtkPythonItem
from vtkmodules.vtkRenderingContext2D import vtkContextActor
from vtkmodules.vtkRenderingCore import (
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)


class APIDiagram:
    """Python object for vtkPythonItem that draws an API diagram."""

    def Initialize(self, vtkSelf):
        return True

    def Paint(self, vtkSelf, painter):
        painter.GetTextProp().SetVerticalJustificationToCentered()
        painter.GetTextProp().SetJustificationToCentered()
        painter.GetTextProp().SetColor(0.0, 0.0, 0.0)
        painter.GetTextProp().SetFontSize(24)
        painter.GetPen().SetColor(0, 0, 0)

        painter.GetBrush().SetColor(100, 255, 100)
        painter.DrawRect(100, 50, 200, 100)
        painter.DrawString(200, 100, "OpenGL")

        painter.GetBrush().SetColor(255, 100, 0)
        painter.DrawRect(300, 50, 200, 100)
        painter.DrawString(400, 100, "Others?")

        painter.GetBrush().SetColor(100, 0, 255)
        painter.DrawRect(500, 50, 200, 100)
        painter.DrawString(600, 100, "Others?")

        painter.GetBrush().SetColor(180, 180, 255)
        painter.DrawRect(100, 150, 600, 100)
        painter.DrawString(400, 200, "2D API")

        painter.GetBrush().SetColor(255, 255, 180)
        painter.DrawRect(100, 250, 600, 200)
        painter.DrawString(400, 400, "Canvas API")

        painter.GetBrush().SetColor(180, 255, 180)
        painter.DrawRect(100, 250, 300, 100)
        painter.DrawString(250, 300, "Point Mark")

        painter.GetBrush().SetColor(255, 255, 255)
        painter.DrawRect(100, 450, 600, 100)
        painter.DrawString(400, 500, "Canvas View")

        return True


# Create the vtkPythonItem and set the drawing object.
python_item = vtkPythonItem()
python_item.SetPythonObject(APIDiagram())

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
render_window.SetWindowName("diagram")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
