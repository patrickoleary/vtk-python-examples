#!/usr/bin/env python

# Demonstrate vtkGL2PSExporter with font DPI scaling and MathText via matplotlib.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
import vtkmodules.vtkRenderingMatplotlib  # noqa: F401

import os
import tempfile

from vtkmodules.vtkIOExportGL2PS import vtkGL2PSExporter
from vtkmodules.vtkRenderingCore import (
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
    vtkTextActor,
)

# Font file path (DejaVuSans.ttf from FreeType test data)
font_dir = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "FreeType", "data"
)
unicode_font_file = os.path.join(font_dir, "DejaVuSans.ttf")

text = "Sample multiline\ntext rendered\nusing FreeTypeTools."

# Actor 1: Times, red, top-left
actor_1 = vtkTextActor()
actor_1.GetTextProperty().SetFontSize(20)
actor_1.GetTextProperty().SetColor(1.0, 0.0, 0.0)
actor_1.GetTextProperty().SetJustificationToLeft()
actor_1.GetTextProperty().SetVerticalJustificationToTop()
actor_1.GetTextProperty().SetFontFamilyToTimes()
actor_1.SetInput(text)
actor_1.SetPosition(10, 590)

# Actor 2: Courier, green, top-right
actor_2 = vtkTextActor()
actor_2.GetTextProperty().SetFontSize(20)
actor_2.GetTextProperty().SetColor(0.0, 1.0, 0.0)
actor_2.GetTextProperty().SetJustificationToRight()
actor_2.GetTextProperty().SetVerticalJustificationToTop()
actor_2.GetTextProperty().SetFontFamilyToCourier()
actor_2.SetInput(text)
actor_2.SetPosition(590, 590)

# Actor 3: italic, blue, bottom-left
actor_3 = vtkTextActor()
actor_3.GetTextProperty().SetFontSize(20)
actor_3.GetTextProperty().SetColor(0.0, 0.0, 1.0)
actor_3.GetTextProperty().SetJustificationToLeft()
actor_3.GetTextProperty().SetVerticalJustificationToBottom()
actor_3.GetTextProperty().SetItalic(1)
actor_3.SetInput(text)
actor_3.SetPosition(10, 10)

# Actor 4: bold with shadow, bottom-right
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

# Actor 5: bold italic with shadow, center
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

# Actor 6: rotated 45 degrees, center
actor_6 = vtkTextActor()
actor_6.GetTextProperty().SetFontSize(16)
actor_6.GetTextProperty().SetColor(1.0, 0.5, 0.2)
actor_6.GetTextProperty().SetJustificationToCentered()
actor_6.GetTextProperty().SetVerticalJustificationToCentered()
actor_6.GetTextProperty().SetOrientation(45)
actor_6.SetInput(text)
actor_6.SetPosition(300, 450)

# Actor 7: rotated 45 degrees, left-justified
actor_7 = vtkTextActor()
actor_7.GetTextProperty().SetFontSize(16)
actor_7.GetTextProperty().SetColor(0.5, 0.2, 1.0)
actor_7.GetTextProperty().SetJustificationToLeft()
actor_7.GetTextProperty().SetVerticalJustificationToCentered()
actor_7.GetTextProperty().SetOrientation(45)
actor_7.SetInput(text)
actor_7.SetPosition(100, 156)

# Actor 8: rotated 45 degrees, right-justified
actor_8 = vtkTextActor()
actor_8.GetTextProperty().SetFontSize(16)
actor_8.GetTextProperty().SetColor(0.8, 1.0, 0.3)
actor_8.GetTextProperty().SetJustificationToRight()
actor_8.GetTextProperty().SetVerticalJustificationToCentered()
actor_8.GetTextProperty().SetOrientation(45)
actor_8.SetInput(text)
actor_8.SetPosition(500, 249)

# Actor 9: escaped dollar signs
actor_9 = vtkTextActor()
actor_9.GetTextProperty().SetFontSize(12)
actor_9.GetTextProperty().SetColor(0.2, 0.5, 1.0)
actor_9.SetInput("Escaped dollar signs:\n\\$10, \\$20")
actor_9.SetPosition(100, 450)

# Actor 10: MathText integral
actor_10 = vtkTextActor()
actor_10.GetTextProperty().SetFontSize(16)
actor_10.GetTextProperty().SetColor(0.5, 0.2, 1.0)
actor_10.GetTextProperty().SetJustificationToRight()
actor_10.GetTextProperty().SetOrientation(45)
actor_10.SetInput(
    "Test MathText $\\int_0^\\infty\\frac{2\\pi}{x - \\frac{z}{4}}\\,dx$"
)
actor_10.SetPosition(588, 433)

# Actor 11: invalid LaTeX (fallback to freetype)
actor_11 = vtkTextActor()
actor_11.GetTextProperty().SetFontSize(15)
actor_11.GetTextProperty().SetColor(1.0, 0.5, 0.2)
actor_11.SetInput("Test FreeType fallback:\n$\\asdf$")
actor_11.SetPosition(10, 350)

# Actor 12: mixed $...$ and escaped $
actor_12 = vtkTextActor()
actor_12.GetTextProperty().SetFontSize(18)
actor_12.GetTextProperty().SetColor(0.0, 1.0, 0.7)
actor_12.SetInput("Test MathText '\\$' $\\$\\sqrt[3]{8}$")
actor_12.SetPosition(10, 300)

# Actor 13: MathText only
actor_13 = vtkTextActor()
actor_13.GetTextProperty().SetFontSize(18)
actor_13.GetTextProperty().SetColor(0.2, 1.0, 1.0)
actor_13.SetInput("$A = \\pi r^2$")
actor_13.SetPosition(10, 250)

# Actor 14: courier bold italic numbers
actor_14 = vtkTextActor()
actor_14.GetTextProperty().SetFontSize(21)
actor_14.GetTextProperty().SetColor(1.0, 0.0, 0.0)
actor_14.GetTextProperty().SetJustificationToCentered()
actor_14.GetTextProperty().SetVerticalJustificationToCentered()
actor_14.GetTextProperty().SetBold(1)
actor_14.GetTextProperty().SetItalic(1)
actor_14.GetTextProperty().SetFontFamilyToCourier()
actor_14.SetInput("4.0")
actor_14.SetPosition(500, 400)

# Actor 15: UTF-8 with custom font
actor_15 = vtkTextActor()
VTK_FONT_FILE = 4
actor_15.GetTextProperty().SetFontFamily(VTK_FONT_FILE)
actor_15.GetTextProperty().SetFontFile(unicode_font_file)
actor_15.GetTextProperty().SetJustificationToCentered()
actor_15.GetTextProperty().SetVerticalJustificationToCentered()
actor_15.GetTextProperty().SetFontSize(18)
actor_15.GetTextProperty().SetColor(0.0, 1.0, 0.7)
actor_15.SetInput("UTF-8 FreeType: \u03a8\u0494\u0496\u0444\u04be")
actor_15.SetPosition(300, 110)

# Actor 16: rotated kerning test
actor_16 = vtkTextActor()
actor_16.GetTextProperty().SetFontFile(unicode_font_file)
actor_16.GetTextProperty().SetFontFamily(VTK_FONT_FILE)
actor_16.GetTextProperty().SetJustificationToCentered()
actor_16.GetTextProperty().SetVerticalJustificationToCentered()
actor_16.GetTextProperty().SetFontSize(18)
actor_16.GetTextProperty().SetOrientation(90)
actor_16.GetTextProperty().SetColor(0.0, 1.0, 0.7)
actor_16.SetInput("oTeVaVoVAW")
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

# Render window
render_window = vtkRenderWindow()
render_window.SetMultiSamples(0)
render_window.SetDPI(96)
render_window.AddRenderer(renderer)
render_window.SetSize(600, 600)
render_window.SetWindowName("gl2 ps font dpi scaling")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

render_window.Render()

# GL2PS export
exporter = vtkGL2PSExporter()
exporter.SetRenderWindow(render_window)
exporter.SetFileFormatToPS()
exporter.CompressOff()
exporter.SetSortToSimple()
exporter.TextAsPathOn()
exporter.DrawBackgroundOn()
exporter.SetFilePrefix(tempfile.mktemp(prefix="GL2PSFontDPIScaling"))
exporter.Write()

interactor.Initialize()
interactor.Start()
