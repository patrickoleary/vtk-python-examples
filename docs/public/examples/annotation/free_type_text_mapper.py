#!/usr/bin/env python

# Test vtkTextMapper with various fonts, alignments, math text, and UTF-8.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

import os

from vtkmodules.vtkCommonCore import VTK_FONT_FILE
from vtkmodules.vtkRenderingCore import (
    vtkActor2D,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
    vtkTextMapper,
)

data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))
font_file = os.path.join(data_dir, "DejaVuSans.ttf")

text = "Sample multiline\ntext rendered\nusing FreeTypeTools."

# Mapper/actor 1: Times, red, left-top
mapper_1 = vtkTextMapper()
actor_1 = vtkActor2D()
actor_1.SetMapper(mapper_1)
mapper_1.GetTextProperty().SetFontSize(20)
mapper_1.GetTextProperty().SetColor(1.0, 0.0, 0.0)
mapper_1.GetTextProperty().SetJustificationToLeft()
mapper_1.GetTextProperty().SetVerticalJustificationToTop()
mapper_1.GetTextProperty().SetFontFamilyToTimes()
mapper_1.SetInput(text)
actor_1.SetPosition(10, 590)

# Mapper/actor 2: Courier, green, right-top
mapper_2 = vtkTextMapper()
actor_2 = vtkActor2D()
actor_2.SetMapper(mapper_2)
mapper_2.GetTextProperty().SetFontSize(20)
mapper_2.GetTextProperty().SetColor(0.0, 1.0, 0.0)
mapper_2.GetTextProperty().SetJustificationToRight()
mapper_2.GetTextProperty().SetVerticalJustificationToTop()
mapper_2.GetTextProperty().SetFontFamilyToCourier()
mapper_2.SetInput(text)
actor_2.SetPosition(590, 590)

# Mapper/actor 3: italic, blue, left-bottom
mapper_3 = vtkTextMapper()
actor_3 = vtkActor2D()
actor_3.SetMapper(mapper_3)
mapper_3.GetTextProperty().SetFontSize(20)
mapper_3.GetTextProperty().SetColor(0.0, 0.0, 1.0)
mapper_3.GetTextProperty().SetJustificationToLeft()
mapper_3.GetTextProperty().SetVerticalJustificationToBottom()
mapper_3.GetTextProperty().SetItalic(1)
mapper_3.SetInput(text)
actor_3.SetPosition(10, 10)

# Mapper/actor 4: bold with shadow, right-bottom
mapper_4 = vtkTextMapper()
actor_4 = vtkActor2D()
actor_4.SetMapper(mapper_4)
mapper_4.GetTextProperty().SetFontSize(20)
mapper_4.GetTextProperty().SetColor(0.3, 0.4, 0.5)
mapper_4.GetTextProperty().SetJustificationToRight()
mapper_4.GetTextProperty().SetVerticalJustificationToBottom()
mapper_4.GetTextProperty().SetBold(1)
mapper_4.GetTextProperty().SetShadow(1)
mapper_4.GetTextProperty().SetShadowOffset(-3, 2)
mapper_4.SetInput(text)
actor_4.SetPosition(590, 10)

# Mapper/actor 5: bold+italic with shadow, centered
mapper_5 = vtkTextMapper()
actor_5 = vtkActor2D()
actor_5.SetMapper(mapper_5)
mapper_5.GetTextProperty().SetFontSize(20)
mapper_5.GetTextProperty().SetColor(1.0, 1.0, 0.0)
mapper_5.GetTextProperty().SetJustificationToCentered()
mapper_5.GetTextProperty().SetVerticalJustificationToCentered()
mapper_5.GetTextProperty().SetBold(1)
mapper_5.GetTextProperty().SetItalic(1)
mapper_5.GetTextProperty().SetShadow(1)
mapper_5.GetTextProperty().SetShadowOffset(5, -8)
mapper_5.SetInput(text)
actor_5.SetPosition(300, 300)

# Mapper/actor 6: oriented 45, centered
mapper_6 = vtkTextMapper()
actor_6 = vtkActor2D()
actor_6.SetMapper(mapper_6)
mapper_6.GetTextProperty().SetFontSize(16)
mapper_6.GetTextProperty().SetColor(1.0, 0.5, 0.2)
mapper_6.GetTextProperty().SetJustificationToCentered()
mapper_6.GetTextProperty().SetVerticalJustificationToCentered()
mapper_6.GetTextProperty().SetOrientation(45)
mapper_6.SetInput(text)
actor_6.SetPosition(300, 450)

# Mapper/actor 7: oriented 45, left-center
mapper_7 = vtkTextMapper()
actor_7 = vtkActor2D()
actor_7.SetMapper(mapper_7)
mapper_7.GetTextProperty().SetFontSize(16)
mapper_7.GetTextProperty().SetColor(0.5, 0.2, 1.0)
mapper_7.GetTextProperty().SetJustificationToLeft()
mapper_7.GetTextProperty().SetVerticalJustificationToCentered()
mapper_7.GetTextProperty().SetOrientation(45)
mapper_7.SetInput(text)
actor_7.SetPosition(100, 200)

# Mapper/actor 8: oriented 45, right-center
mapper_8 = vtkTextMapper()
actor_8 = vtkActor2D()
actor_8.SetMapper(mapper_8)
mapper_8.GetTextProperty().SetFontSize(16)
mapper_8.GetTextProperty().SetColor(0.8, 1.0, 0.3)
mapper_8.GetTextProperty().SetJustificationToRight()
mapper_8.GetTextProperty().SetVerticalJustificationToCentered()
mapper_8.GetTextProperty().SetOrientation(45)
mapper_8.SetInput(text)
actor_8.SetPosition(500, 200)

# Mapper/actor 9: escaped dollar signs
mapper_9 = vtkTextMapper()
actor_9 = vtkActor2D()
actor_9.SetMapper(mapper_9)
mapper_9.GetTextProperty().SetFontSize(12)
mapper_9.GetTextProperty().SetColor(0.2, 0.5, 1.0)
mapper_9.SetInput("Escaped dollar signs:\n\\$10, \\$20")
actor_9.SetPosition(100, 450)

# Mapper/actor 10: math text, oriented
mapper_10 = vtkTextMapper()
actor_10 = vtkActor2D()
actor_10.SetMapper(mapper_10)
mapper_10.GetTextProperty().SetFontSize(16)
mapper_10.GetTextProperty().SetColor(0.5, 0.2, 1.0)
mapper_10.GetTextProperty().SetJustificationToRight()
mapper_10.GetTextProperty().SetOrientation(45)
mapper_10.SetInput("Test MathText $\\int_0^\\infty\\frac{2\\pi}{x - \\frac{z}{4}}\\,dx$")
actor_10.SetPosition(590, 300)

# Mapper/actor 11: invalid latex (fallback)
mapper_11 = vtkTextMapper()
actor_11 = vtkActor2D()
actor_11.SetMapper(mapper_11)
mapper_11.GetTextProperty().SetFontSize(15)
mapper_11.GetTextProperty().SetColor(1.0, 0.5, 0.2)
mapper_11.SetInput("Test FreeType fallback:\n$\\asdf$")
actor_11.SetPosition(10, 350)

# Mapper/actor 12: mixed escaped and math text
mapper_12 = vtkTextMapper()
actor_12 = vtkActor2D()
actor_12.SetMapper(mapper_12)
mapper_12.GetTextProperty().SetFontSize(18)
mapper_12.GetTextProperty().SetColor(0.0, 1.0, 0.7)
mapper_12.SetInput("Test MathText '\\$' $\\$\\sqrt[3]{8}$")
actor_12.SetPosition(10, 300)

# Mapper/actor 13: pure math text
mapper_13 = vtkTextMapper()
actor_13 = vtkActor2D()
actor_13.SetMapper(mapper_13)
mapper_13.GetTextProperty().SetFontSize(18)
mapper_13.GetTextProperty().SetColor(0.2, 1.0, 1.0)
mapper_13.SetInput("$A = \\pi r^2$")
actor_13.SetPosition(10, 250)

# Mapper/actor 14: courier bold italic number
mapper_14 = vtkTextMapper()
actor_14 = vtkActor2D()
actor_14.SetMapper(mapper_14)
mapper_14.GetTextProperty().SetFontSize(21)
mapper_14.GetTextProperty().SetColor(1.0, 0.0, 0.0)
mapper_14.GetTextProperty().SetJustificationToCentered()
mapper_14.GetTextProperty().SetVerticalJustificationToCentered()
mapper_14.GetTextProperty().SetBold(1)
mapper_14.GetTextProperty().SetItalic(1)
mapper_14.GetTextProperty().SetFontFamilyToCourier()
mapper_14.SetInput("4.0")
actor_14.SetPosition(500, 400)

# Mapper/actor 15: UTF-8 with custom font
mapper_15 = vtkTextMapper()
actor_15 = vtkActor2D()
actor_15.SetMapper(mapper_15)
mapper_15.GetTextProperty().SetFontFile(font_file)
mapper_15.GetTextProperty().SetFontFamily(VTK_FONT_FILE)
mapper_15.GetTextProperty().SetJustificationToCentered()
mapper_15.GetTextProperty().SetVerticalJustificationToCentered()
mapper_15.GetTextProperty().SetFontSize(18)
mapper_15.GetTextProperty().SetColor(0.0, 1.0, 0.7)
mapper_15.SetInput("UTF-8 FreeType: \u03a8\u0494\u0496\u0444\u04be")
actor_15.SetPosition(300, 110)

# Mapper/actor 16: rotated kerning test
mapper_16 = vtkTextMapper()
actor_16 = vtkActor2D()
actor_16.SetMapper(mapper_16)
mapper_16.GetTextProperty().SetFontFile(font_file)
mapper_16.GetTextProperty().SetFontFamily(VTK_FONT_FILE)
mapper_16.GetTextProperty().SetJustificationToCentered()
mapper_16.GetTextProperty().SetVerticalJustificationToCentered()
mapper_16.GetTextProperty().SetFontSize(18)
mapper_16.GetTextProperty().SetOrientation(90)
mapper_16.GetTextProperty().SetColor(0.0, 1.0, 0.7)
mapper_16.SetInput("oTeVaVoVAW")
actor_16.SetPosition(300, 200)

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
renderer.AddActor(actor_11)
renderer.AddActor(actor_12)
renderer.AddActor(actor_13)
renderer.AddActor(actor_14)
renderer.AddActor(actor_15)
renderer.AddActor(actor_16)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("free type text mapper")
render_window.SetMultiSamples(0)
render_window.SetSize(600, 600)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
