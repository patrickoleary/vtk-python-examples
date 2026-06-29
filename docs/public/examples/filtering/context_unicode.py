#!/usr/bin/env python
# Demonstrate Unicode string rendering in a 2D context scene.

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


class ContextUnicodeItem:
    """Python object for vtkPythonItem that draws Unicode strings."""

    def Initialize(self, vtkSelf):
        return True

    def Paint(self, vtkSelf, painter):
        painter.GetTextProp().SetVerticalJustificationToCentered()
        painter.GetTextProp().SetJustificationToCentered()
        painter.GetTextProp().SetColor(0.0, 0.0, 0.0)
        painter.GetTextProp().SetFontSize(24)
        painter.GetTextProp().SetFontFamilyToArial()
        painter.DrawString(70, 20, "Angstrom")
        painter.DrawString(150, 20, "\u212b")       # Angstrom symbol
        painter.DrawString(100, 80, "a\u03b1")      # a + alpha
        painter.DrawString(100, 50, "\u03b1\u03b2\u03b3")  # alpha beta gamma
        return True


# Create the vtkPythonItem and set the drawing object.
python_item = vtkPythonItem()
python_item.SetPythonObject(ContextUnicodeItem())

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
render_window.SetSize(200, 100)
render_window.SetMultiSamples(0)
render_window.AddRenderer(renderer)
render_window.SetWindowName("context unicode")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
