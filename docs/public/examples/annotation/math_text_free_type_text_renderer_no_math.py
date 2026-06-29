#!/usr/bin/env python

# Test vtkTextActor with MathText FreeType renderer, no math text, and UTF-8.

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

text = "Sample multiline\ntext rendered\nusing FreeTypeTools."

# Actor 1: Times, red, left-top
actor_1 = vtkTextActor()
actor_1.GetTextProperty().SetFontSize(20)
actor_1.GetTextProperty().SetColor(1.0, 0.0, 0.0)
actor_1.GetTextProperty().SetJustificationToLeft()
actor_1.GetTextProperty().SetVerticalJustificationToTop()
actor_1.GetTextProperty().SetFontFamilyToTimes()
actor_1.SetInput(text)
actor_1.SetPosition(10, 590)

# Actor 2: Courier, green, right-top
actor_2 = vtkTextActor()
actor_2.GetTextProperty().SetFontSize(20)
actor_2.GetTextProperty().SetColor(0.0, 1.0, 0.0)
actor_2.GetTextProperty().SetJustificationToRight()
actor_2.GetTextProperty().SetVerticalJustificationToTop()
actor_2.GetTextProperty().SetFontFamilyToCourier()
actor_2.SetInput(text)
actor_2.SetPosition(590, 590)

# Actor 3: italic, blue, left-bottom
actor_3 = vtkTextActor()
actor_3.GetTextProperty().SetFontSize(20)
actor_3.GetTextProperty().SetColor(0.0, 0.0, 1.0)
actor_3.GetTextProperty().SetJustificationToLeft()
actor_3.GetTextProperty().SetVerticalJustificationToBottom()
actor_3.GetTextProperty().SetItalic(1)
actor_3.SetInput(text)
actor_3.SetPosition(10, 10)

# Actor 4: bold with shadow, right-bottom
actor_4 = vtkTextActor()
actor_4.GetTextProperty().SetFontSize(20)
actor_4.GetTextProperty().SetColor(0.3, 0.4, 0.5)
actor_4.GetTextProperty().SetJustificationToRight()
actor_4.GetTextProperty().SetVerticalJustificationToBottom()
actor_4.GetTextProperty().SetBold(1)
actor_4.GetTextProperty().SetShadow(1)
actor_4.GetTextProperty().SetShadowOffset(-3, 2)
actor_4.SetInput(text)
actor_4.SetPosition(590, 10)

# Actor 5: bold+italic with shadow, centered
actor_5 = vtkTextActor()
actor_5.GetTextProperty().SetFontSize(20)
actor_5.GetTextProperty().SetColor(1.0, 1.0, 0.0)
actor_5.GetTextProperty().SetJustificationToCentered()
actor_5.GetTextProperty().SetVerticalJustificationToCentered()
actor_5.GetTextProperty().SetBold(1)
actor_5.GetTextProperty().SetItalic(1)
actor_5.GetTextProperty().SetShadow(1)
actor_5.GetTextProperty().SetShadowOffset(5, -8)
actor_5.SetInput(text)
actor_5.SetPosition(300, 300)

# Actor 6: oriented 45, centered
actor_6 = vtkTextActor()
actor_6.GetTextProperty().SetFontSize(16)
actor_6.GetTextProperty().SetColor(1.0, 0.5, 0.2)
actor_6.GetTextProperty().SetJustificationToCentered()
actor_6.GetTextProperty().SetVerticalJustificationToCentered()
actor_6.GetTextProperty().SetOrientation(45)
actor_6.SetInput(text)
actor_6.SetPosition(300, 450)

# Actor 7: oriented 45, left-center
actor_7 = vtkTextActor()
actor_7.GetTextProperty().SetFontSize(16)
actor_7.GetTextProperty().SetColor(0.5, 0.2, 1.0)
actor_7.GetTextProperty().SetJustificationToLeft()
actor_7.GetTextProperty().SetVerticalJustificationToCentered()
actor_7.GetTextProperty().SetOrientation(45)
actor_7.SetInput(text)
actor_7.SetPosition(100, 156)

# Actor 8: oriented 45, right-center
actor_8 = vtkTextActor()
actor_8.GetTextProperty().SetFontSize(16)
actor_8.GetTextProperty().SetColor(0.8, 1.0, 0.3)
actor_8.GetTextProperty().SetJustificationToRight()
actor_8.GetTextProperty().SetVerticalJustificationToCentered()
actor_8.GetTextProperty().SetOrientation(45)
actor_8.SetInput(text)
actor_8.SetPosition(500, 249)

# Actor 9: courier bold italic number
actor_9 = vtkTextActor()
actor_9.GetTextProperty().SetFontSize(21)
actor_9.GetTextProperty().SetColor(1.0, 0.0, 0.0)
actor_9.GetTextProperty().SetJustificationToCentered()
actor_9.GetTextProperty().SetVerticalJustificationToCentered()
actor_9.GetTextProperty().SetBold(1)
actor_9.GetTextProperty().SetItalic(1)
actor_9.GetTextProperty().SetFontFamilyToCourier()
actor_9.SetInput("4.0")
actor_9.SetPosition(500, 400)

# Actor 10: UTF-8 with custom font
actor_10 = vtkTextActor()
actor_10.GetTextProperty().SetFontFamily(VTK_FONT_FILE)
actor_10.GetTextProperty().SetFontFile(font_file)
actor_10.GetTextProperty().SetJustificationToCentered()
actor_10.GetTextProperty().SetVerticalJustificationToCentered()
actor_10.GetTextProperty().SetFontSize(18)
actor_10.GetTextProperty().SetColor(0.0, 1.0, 0.7)
actor_10.SetInput("UTF-8 FreeType: \u03a8\u0494\u0496\u0444\u04be")
actor_10.SetPosition(300, 110)

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
renderer.AddActor(actor_9)
renderer.AddActor(actor_10)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("math text free type text renderer no math")
render_window.SetMultiSamples(0)
render_window.SetSize(600, 600)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
