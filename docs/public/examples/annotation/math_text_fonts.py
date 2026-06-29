#!/usr/bin/env python

# Test vtkTextActor with math text using various font families and styles.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

import os

from vtkmodules.vtkCommonCore import VTK_FONT_FILE
from vtkmodules.vtkRenderingCore import (
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
    vtkTextActor,
)

data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))
font_file = os.path.join(data_dir, "DejaVuSans.ttf")

math_str = "$TextMath=\\int_0^\\infty\\frac{2\\pi}{x - \\frac{z}{4}}\\,dx$"

# Actor 1: Times, red
actor_1 = vtkTextActor()
actor_1.GetTextProperty().SetFontSize(20)
actor_1.GetTextProperty().SetColor(1.0, 0.0, 0.0)
actor_1.GetTextProperty().SetFontFamilyToTimes()
actor_1.SetInput("Times " + math_str)
actor_1.SetPosition(10, 500)

# Actor 2: Courier, green
actor_2 = vtkTextActor()
actor_2.GetTextProperty().SetFontSize(20)
actor_2.GetTextProperty().SetColor(0.0, 1.0, 0.0)
actor_2.GetTextProperty().SetFontFamilyToCourier()
actor_2.SetInput("Courier " + math_str)
actor_2.SetPosition(10, 400)

# Actor 3: italic, blue
actor_3 = vtkTextActor()
actor_3.GetTextProperty().SetFontSize(20)
actor_3.GetTextProperty().SetColor(0.0, 0.0, 1.0)
actor_3.GetTextProperty().SetItalic(1)
actor_3.SetInput("Italic " + math_str)
actor_3.SetPosition(10, 10)

# Actor 4: bold
actor_4 = vtkTextActor()
actor_4.GetTextProperty().SetFontSize(20)
actor_4.GetTextProperty().SetColor(0.3, 0.4, 0.5)
actor_4.GetTextProperty().SetBold(1)
actor_4.SetInput("Bold " + math_str)
actor_4.SetPosition(10, 60)

# Actor 5: italic+bold, yellow
actor_5 = vtkTextActor()
actor_5.GetTextProperty().SetFontSize(20)
actor_5.GetTextProperty().SetColor(1.0, 1.0, 0.0)
actor_5.GetTextProperty().SetBold(1)
actor_5.GetTextProperty().SetItalic(1)
actor_5.SetInput("ItalicBold " + math_str)
actor_5.SetPosition(10, 300)

# Actor 6: oriented 45
actor_6 = vtkTextActor()
actor_6.GetTextProperty().SetFontSize(16)
actor_6.GetTextProperty().SetColor(1.0, 0.5, 0.2)
actor_6.GetTextProperty().SetOrientation(45)
actor_6.SetInput("Oriented " + math_str)
actor_6.SetPosition(400, 300)

# Actor 7: custom font file
actor_7 = vtkTextActor()
actor_7.GetTextProperty().SetFontFamily(VTK_FONT_FILE)
actor_7.GetTextProperty().SetFontFile(font_file)
actor_7.GetTextProperty().SetFontSize(16)
actor_7.GetTextProperty().SetColor(0.5, 0.2, 1.0)
actor_7.SetInput("FontFile " + math_str)
actor_7.SetPosition(10, 130)

# Actor 8: math text font variants
math_variants = (
    "$\\mathit{TextMathItalic}$ | $\\mathbf{TextMathBold}$\n"
    "$\\mathcal{TextMathCallihraphy}$ | $\\mathtt{TextMathTypewriter}$"
)
actor_8 = vtkTextActor()
actor_8.GetTextProperty().SetFontSize(20)
actor_8.GetTextProperty().SetColor(1.0, 0.5, 0.2)
actor_8.SetInput(math_variants)
actor_8.SetPosition(10, 200)

# Renderer
renderer = vtkRenderer()
renderer.SetBackground(0.1, 0.1, 0.1)

renderer.AddActor(actor_1)
renderer.AddActor(actor_2)
renderer.AddActor(actor_3)
renderer.AddActor(actor_4)
renderer.AddActor(actor_5)
renderer.AddActor(actor_6)
renderer.AddActor(actor_7)
renderer.AddActor(actor_8)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("math text fonts")
render_window.SetMultiSamples(0)
render_window.SetSize(600, 600)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
