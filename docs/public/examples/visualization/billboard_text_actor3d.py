#!/usr/bin/env python

# Place billboard text labels at random 3D positions next to sphere glyphs.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkBillboardTextActor3D,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
dark_slate_gray = (0.184, 0.310, 0.310)
peacock = (0.200, 0.631, 0.788)
misty_rose = (1.000, 0.894, 0.882)
gold = (1.000, 0.843, 0.000)

# Source: generate sphere polygon data used for each glyph
sphere_source = vtkSphereSource()
sphere_source.SetCenter(0.0, 0.0, 0.0)
sphere_source.SetRadius(1.0)

# Origin marker: a sphere at (0, 0, 0)
origin_mapper = vtkPolyDataMapper()
origin_mapper.SetInputConnection(sphere_source.GetOutputPort())

origin_actor = vtkActor()
origin_actor.SetMapper(origin_mapper)
origin_actor.SetPosition(0.0, 0.0, 0.0)
origin_actor.GetProperty().SetColor(peacock)

# Labeled sphere 0
mapper_0 = vtkPolyDataMapper()
mapper_0.SetInputConnection(sphere_source.GetOutputPort())

actor_0 = vtkActor()
actor_0.SetMapper(mapper_0)
actor_0.SetPosition(9.769738, -0.015473, -0.047476)
actor_0.GetProperty().SetColor(misty_rose)

text_actor_0 = vtkBillboardTextActor3D()
text_actor_0.SetInput("9.77, -0.0155, -0.0475")
text_actor_0.SetPosition(9.769738, -0.015473, -0.047476)
text_actor_0.GetTextProperty().SetFontSize(12)
text_actor_0.GetTextProperty().SetColor(gold)
text_actor_0.GetTextProperty().SetJustificationToCentered()

# Labeled sphere 1
mapper_1 = vtkPolyDataMapper()
mapper_1.SetInputConnection(sphere_source.GetOutputPort())

actor_1 = vtkActor()
actor_1.SetMapper(mapper_1)
actor_1.SetPosition(2.074966, -6.045053, 0.788068)
actor_1.GetProperty().SetColor(misty_rose)

text_actor_1 = vtkBillboardTextActor3D()
text_actor_1.SetInput("2.07, -6.05, 0.788")
text_actor_1.SetPosition(2.074966, -6.045053, 0.788068)
text_actor_1.GetTextProperty().SetFontSize(12)
text_actor_1.GetTextProperty().SetColor(gold)
text_actor_1.GetTextProperty().SetJustificationToCentered()

# Labeled sphere 2
mapper_2 = vtkPolyDataMapper()
mapper_2.SetInputConnection(sphere_source.GetOutputPort())

actor_2 = vtkActor()
actor_2.SetMapper(mapper_2)
actor_2.SetPosition(5.053454, -6.590450, -5.696974)
actor_2.GetProperty().SetColor(misty_rose)

text_actor_2 = vtkBillboardTextActor3D()
text_actor_2.SetInput("5.05, -6.59, -5.7")
text_actor_2.SetPosition(5.053454, -6.590450, -5.696974)
text_actor_2.GetTextProperty().SetFontSize(12)
text_actor_2.GetTextProperty().SetColor(gold)
text_actor_2.GetTextProperty().SetJustificationToCentered()

# Labeled sphere 3
mapper_3 = vtkPolyDataMapper()
mapper_3.SetInputConnection(sphere_source.GetOutputPort())

actor_3 = vtkActor()
actor_3.SetMapper(mapper_3)
actor_3.SetPosition(-9.045208, -2.813410, -4.975787)
actor_3.GetProperty().SetColor(misty_rose)

text_actor_3 = vtkBillboardTextActor3D()
text_actor_3.SetInput("-9.05, -2.81, -4.98")
text_actor_3.SetPosition(-9.045208, -2.813410, -4.975787)
text_actor_3.GetTextProperty().SetFontSize(12)
text_actor_3.GetTextProperty().SetColor(gold)
text_actor_3.GetTextProperty().SetJustificationToCentered()

# Labeled sphere 4
mapper_4 = vtkPolyDataMapper()
mapper_4.SetInputConnection(sphere_source.GetOutputPort())

actor_4 = vtkActor()
actor_4.SetMapper(mapper_4)
actor_4.SetPosition(-8.043943, 5.457825, 9.657843)
actor_4.GetProperty().SetColor(misty_rose)

text_actor_4 = vtkBillboardTextActor3D()
text_actor_4.SetInput("-8.04, 5.46, 9.66")
text_actor_4.SetPosition(-8.043943, 5.457825, 9.657843)
text_actor_4.GetTextProperty().SetFontSize(12)
text_actor_4.GetTextProperty().SetColor(gold)
text_actor_4.GetTextProperty().SetJustificationToCentered()

# Labeled sphere 5
mapper_5 = vtkPolyDataMapper()
mapper_5.SetInputConnection(sphere_source.GetOutputPort())

actor_5 = vtkActor()
actor_5.SetMapper(mapper_5)
actor_5.SetPosition(-0.627986, 5.440828, 4.003035)
actor_5.GetProperty().SetColor(misty_rose)

text_actor_5 = vtkBillboardTextActor3D()
text_actor_5.SetInput("-0.628, 5.44, 4")
text_actor_5.SetPosition(-0.627986, 5.440828, 4.003035)
text_actor_5.GetTextProperty().SetFontSize(12)
text_actor_5.GetTextProperty().SetColor(gold)
text_actor_5.GetTextProperty().SetJustificationToCentered()

# Labeled sphere 6
mapper_6 = vtkPolyDataMapper()
mapper_6.SetInputConnection(sphere_source.GetOutputPort())

actor_6 = vtkActor()
actor_6.SetMapper(mapper_6)
actor_6.SetPosition(-0.988179, -8.326075, 3.664959)
actor_6.GetProperty().SetColor(misty_rose)

text_actor_6 = vtkBillboardTextActor3D()
text_actor_6.SetInput("-0.988, -8.33, 3.66")
text_actor_6.SetPosition(-0.988179, -8.326075, 3.664959)
text_actor_6.GetTextProperty().SetFontSize(12)
text_actor_6.GetTextProperty().SetColor(gold)
text_actor_6.GetTextProperty().SetJustificationToCentered()

# Labeled sphere 7
mapper_7 = vtkPolyDataMapper()
mapper_7.SetInputConnection(sphere_source.GetOutputPort())

actor_7 = vtkActor()
actor_7.SetMapper(mapper_7)
actor_7.SetPosition(-3.041831, -4.047047, 1.276854)
actor_7.GetProperty().SetColor(misty_rose)

text_actor_7 = vtkBillboardTextActor3D()
text_actor_7.SetInput("-3.04, -4.05, 1.28")
text_actor_7.SetPosition(-3.041831, -4.047047, 1.276854)
text_actor_7.GetTextProperty().SetFontSize(12)
text_actor_7.GetTextProperty().SetColor(gold)
text_actor_7.GetTextProperty().SetJustificationToCentered()

# Labeled sphere 8
mapper_8 = vtkPolyDataMapper()
mapper_8.SetInputConnection(sphere_source.GetOutputPort())

actor_8 = vtkActor()
actor_8.SetMapper(mapper_8)
actor_8.SetPosition(0.079898, 2.850394, 6.574051)
actor_8.GetProperty().SetColor(misty_rose)

text_actor_8 = vtkBillboardTextActor3D()
text_actor_8.SetInput("0.0799, 2.85, 6.57")
text_actor_8.SetPosition(0.079898, 2.850394, 6.574051)
text_actor_8.GetTextProperty().SetFontSize(12)
text_actor_8.GetTextProperty().SetColor(gold)
text_actor_8.GetTextProperty().SetJustificationToCentered()

# Labeled sphere 9
mapper_9 = vtkPolyDataMapper()
mapper_9.SetInputConnection(sphere_source.GetOutputPort())

actor_9 = vtkActor()
actor_9.SetMapper(mapper_9)
actor_9.SetPosition(-9.916446, -5.702042, 5.786989)
actor_9.GetProperty().SetColor(misty_rose)

text_actor_9 = vtkBillboardTextActor3D()
text_actor_9.SetInput("-9.92, -5.7, 5.79")
text_actor_9.SetPosition(-9.916446, -5.702042, 5.786989)
text_actor_9.GetTextProperty().SetFontSize(12)
text_actor_9.GetTextProperty().SetColor(gold)
text_actor_9.GetTextProperty().SetJustificationToCentered()

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.AddActor(origin_actor)
renderer.AddActor(actor_0)
renderer.AddActor(text_actor_0)
renderer.AddActor(actor_1)
renderer.AddActor(text_actor_1)
renderer.AddActor(actor_2)
renderer.AddActor(text_actor_2)
renderer.AddActor(actor_3)
renderer.AddActor(text_actor_3)
renderer.AddActor(actor_4)
renderer.AddActor(text_actor_4)
renderer.AddActor(actor_5)
renderer.AddActor(text_actor_5)
renderer.AddActor(actor_6)
renderer.AddActor(text_actor_6)
renderer.AddActor(actor_7)
renderer.AddActor(text_actor_7)
renderer.AddActor(actor_8)
renderer.AddActor(text_actor_8)
renderer.AddActor(actor_9)
renderer.AddActor(text_actor_9)
renderer.SetBackground(dark_slate_gray)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("billboard text actor3d")
render_window.SetMultiSamples(0)
render_window.SetSize(640, 480)

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
