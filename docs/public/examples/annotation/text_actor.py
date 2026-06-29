#!/usr/bin/env python

# Test vtkTextActor with various alignments, orientations, frames, and edge cases.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import vtkPoints, vtkUnsignedCharArray
from vtkmodules.vtkCommonDataModel import vtkCellArray, vtkPolyData
from vtkmodules.vtkRenderingCore import (
    vtkActor2D,
    vtkPolyDataMapper2D,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
    vtkTextActor,
)

width = 600
height = 600

# Anchor points polydata
anchors = vtkPolyData()
anchor_points = vtkPoints()
anchors.SetPoints(anchor_points)
anchor_verts = vtkCellArray()
anchors.SetVerts(anchor_verts)
anchor_colors = vtkUnsignedCharArray()
anchor_colors.SetNumberOfComponents(4)
anchors.GetCellData().SetScalars(anchor_colors)

# Row 0, Col 0: TProp orientation=45, Right/Top
actor_0_0 = vtkTextActor()
actor_0_0.GetTextProperty().SetOrientation(45)
actor_0_0.GetTextProperty().SetJustificationToRight()
actor_0_0.GetTextProperty().SetVerticalJustificationToTop()
actor_0_0.GetTextProperty().SetColor(0.75, 0.20, 0.20)
actor_0_0.GetTextProperty().SetBackgroundColor(0.25, 0.40, 0.50)
actor_0_0.GetTextProperty().SetBackgroundOpacity(1.0)
actor_0_0.SetPosition(100, 100)
actor_0_0.GetTextProperty().SetFrame(True)
actor_0_0.GetTextProperty().SetFrameColor(0.0, 0.0, 1.0)
actor_0_0.GetTextProperty().SetFrameWidth(1)
actor_0_0.SetInput("TProp Angle: 45.0\nActor Angle: 0.0\nHAlign: Right\nVAlign: Top")
pt_id = anchor_points.InsertNextPoint(100, 100, 0.0)
anchor_verts.InsertNextCell(1, [pt_id])
anchor_colors.InsertNextTuple4(191, 51, 51, 255)

# Row 0, Col 1: TProp orientation=45, Centered/Centered
actor_0_1 = vtkTextActor()
actor_0_1.GetTextProperty().SetOrientation(45)
actor_0_1.GetTextProperty().SetJustificationToCentered()
actor_0_1.GetTextProperty().SetVerticalJustificationToCentered()
actor_0_1.GetTextProperty().SetColor(0.75, 0.46, 0.20)
actor_0_1.GetTextProperty().SetBackgroundColor(0.25, 0.27, 0.50)
actor_0_1.GetTextProperty().SetBackgroundOpacity(1.0)
actor_0_1.SetPosition(300, 100)
actor_0_1.GetTextProperty().SetFrame(False)
actor_0_1.GetTextProperty().SetFrameColor(1.0, 1.0, 1.0)
actor_0_1.GetTextProperty().SetFrameWidth(1)
actor_0_1.SetInput("TProp Angle: 45.0\nActor Angle: 0.0\nHAlign: Centered\nVAlign: Centered")
pt_id = anchor_points.InsertNextPoint(300, 100, 0.0)
anchor_verts.InsertNextCell(1, [pt_id])
anchor_colors.InsertNextTuple4(191, 117, 51, 255)

# Row 0, Col 2: TProp orientation=45, Left/Bottom
actor_0_2 = vtkTextActor()
actor_0_2.GetTextProperty().SetOrientation(45)
actor_0_2.GetTextProperty().SetJustificationToLeft()
actor_0_2.GetTextProperty().SetVerticalJustificationToBottom()
actor_0_2.GetTextProperty().SetColor(0.75, 0.72, 0.20)
actor_0_2.GetTextProperty().SetBackgroundColor(0.25, 0.14, 0.50)
actor_0_2.GetTextProperty().SetBackgroundOpacity(1.0)
actor_0_2.SetPosition(500, 100)
actor_0_2.GetTextProperty().SetFrame(True)
actor_0_2.GetTextProperty().SetFrameColor(1.0, 0.0, 0.0)
actor_0_2.GetTextProperty().SetFrameWidth(1)
actor_0_2.SetInput("TProp Angle: 45.0\nActor Angle: 0.0\nHAlign: Left\nVAlign: Bottom")
pt_id = anchor_points.InsertNextPoint(500, 100, 0.0)
anchor_verts.InsertNextCell(1, [pt_id])
anchor_colors.InsertNextTuple4(191, 183, 51, 255)

# Row 1, Col 0: Actor orientation=-45, Right/Top
actor_1_0 = vtkTextActor()
actor_1_0.SetOrientation(-45)
actor_1_0.GetTextProperty().SetJustificationToRight()
actor_1_0.GetTextProperty().SetVerticalJustificationToTop()
actor_1_0.GetTextProperty().SetColor(0.75, 0.20, 0.40)
actor_1_0.GetTextProperty().SetBackgroundColor(0.25, 0.40, 0.40)
actor_1_0.GetTextProperty().SetBackgroundOpacity(1.0)
actor_1_0.SetPosition(100, 233)
actor_1_0.GetTextProperty().SetFrame(False)
actor_1_0.GetTextProperty().SetFrameColor(0.0, 0.0, 1.0)
actor_1_0.GetTextProperty().SetFrameWidth(2)
actor_1_0.SetInput("TProp Angle: 0.0\nActor Angle: -45.0\nHAlign: Right\nVAlign: Top")
pt_id = anchor_points.InsertNextPoint(100, 233, 0.0)
anchor_verts.InsertNextCell(1, [pt_id])
anchor_colors.InsertNextTuple4(191, 51, 102, 255)

# Row 1, Col 1: Actor orientation=-45, Centered/Centered
actor_1_1 = vtkTextActor()
actor_1_1.SetOrientation(-45)
actor_1_1.GetTextProperty().SetJustificationToCentered()
actor_1_1.GetTextProperty().SetVerticalJustificationToCentered()
actor_1_1.GetTextProperty().SetColor(0.75, 0.46, 0.40)
actor_1_1.GetTextProperty().SetBackgroundColor(0.25, 0.27, 0.40)
actor_1_1.GetTextProperty().SetBackgroundOpacity(1.0)
actor_1_1.SetPosition(300, 233)
actor_1_1.GetTextProperty().SetFrame(True)
actor_1_1.GetTextProperty().SetFrameColor(1.0, 1.0, 1.0)
actor_1_1.GetTextProperty().SetFrameWidth(2)
actor_1_1.SetInput("TProp Angle: 0.0\nActor Angle: -45.0\nHAlign: Centered\nVAlign: Centered")
pt_id = anchor_points.InsertNextPoint(300, 233, 0.0)
anchor_verts.InsertNextCell(1, [pt_id])
anchor_colors.InsertNextTuple4(191, 117, 102, 255)

# Row 1, Col 2: Actor orientation=-45, Left/Bottom
actor_1_2 = vtkTextActor()
actor_1_2.SetOrientation(-45)
actor_1_2.GetTextProperty().SetJustificationToLeft()
actor_1_2.GetTextProperty().SetVerticalJustificationToBottom()
actor_1_2.GetTextProperty().SetColor(0.75, 0.72, 0.40)
actor_1_2.GetTextProperty().SetBackgroundColor(0.25, 0.14, 0.40)
actor_1_2.GetTextProperty().SetBackgroundOpacity(1.0)
actor_1_2.SetPosition(500, 233)
actor_1_2.GetTextProperty().SetFrame(False)
actor_1_2.GetTextProperty().SetFrameColor(1.0, 0.0, 0.0)
actor_1_2.GetTextProperty().SetFrameWidth(2)
actor_1_2.SetInput("TProp Angle: 0.0\nActor Angle: -45.0\nHAlign: Left\nVAlign: Bottom")
pt_id = anchor_points.InsertNextPoint(500, 233, 0.0)
anchor_verts.InsertNextCell(1, [pt_id])
anchor_colors.InsertNextTuple4(191, 183, 102, 255)

# Row 2, Col 0: No orientation, Right/Top
actor_2_0 = vtkTextActor()
actor_2_0.GetTextProperty().SetJustificationToRight()
actor_2_0.GetTextProperty().SetVerticalJustificationToTop()
actor_2_0.GetTextProperty().SetColor(0.75, 0.20, 0.60)
actor_2_0.GetTextProperty().SetBackgroundColor(0.25, 0.40, 0.30)
actor_2_0.GetTextProperty().SetBackgroundOpacity(1.0)
actor_2_0.SetPosition(100, 366)
actor_2_0.GetTextProperty().SetFrame(True)
actor_2_0.GetTextProperty().SetFrameColor(0.0, 0.0, 1.0)
actor_2_0.GetTextProperty().SetFrameWidth(3)
actor_2_0.SetInput("TProp Angle: 0.0\nActor Angle: 0.0\nHAlign: Right\nVAlign: Top")
pt_id = anchor_points.InsertNextPoint(100, 366, 0.0)
anchor_verts.InsertNextCell(1, [pt_id])
anchor_colors.InsertNextTuple4(191, 51, 153, 255)

# Row 2, Col 1: No orientation, Centered/Centered
actor_2_1 = vtkTextActor()
actor_2_1.GetTextProperty().SetJustificationToCentered()
actor_2_1.GetTextProperty().SetVerticalJustificationToCentered()
actor_2_1.GetTextProperty().SetColor(0.75, 0.46, 0.60)
actor_2_1.GetTextProperty().SetBackgroundColor(0.25, 0.27, 0.30)
actor_2_1.GetTextProperty().SetBackgroundOpacity(1.0)
actor_2_1.SetPosition(300, 366)
actor_2_1.GetTextProperty().SetFrame(False)
actor_2_1.GetTextProperty().SetFrameColor(1.0, 1.0, 1.0)
actor_2_1.GetTextProperty().SetFrameWidth(3)
actor_2_1.SetInput("TProp Angle: 0.0\nActor Angle: 0.0\nHAlign: Centered\nVAlign: Centered")
pt_id = anchor_points.InsertNextPoint(300, 366, 0.0)
anchor_verts.InsertNextCell(1, [pt_id])
anchor_colors.InsertNextTuple4(191, 117, 153, 255)

# Row 2, Col 2: No orientation, Left/Bottom
actor_2_2 = vtkTextActor()
actor_2_2.GetTextProperty().SetJustificationToLeft()
actor_2_2.GetTextProperty().SetVerticalJustificationToBottom()
actor_2_2.GetTextProperty().SetColor(0.75, 0.72, 0.60)
actor_2_2.GetTextProperty().SetBackgroundColor(0.25, 0.14, 0.30)
actor_2_2.GetTextProperty().SetBackgroundOpacity(1.0)
actor_2_2.SetPosition(500, 366)
actor_2_2.GetTextProperty().SetFrame(True)
actor_2_2.GetTextProperty().SetFrameColor(1.0, 0.0, 0.0)
actor_2_2.GetTextProperty().SetFrameWidth(3)
actor_2_2.SetInput("TProp Angle: 0.0\nActor Angle: 0.0\nHAlign: Left\nVAlign: Bottom")
pt_id = anchor_points.InsertNextPoint(500, 366, 0.0)
anchor_verts.InsertNextCell(1, [pt_id])
anchor_colors.InsertNextTuple4(191, 183, 153, 255)

# Row 3, Col 0: TProp orientation=45 + Actor orientation=45, Right/Top
actor_3_0 = vtkTextActor()
actor_3_0.GetTextProperty().SetOrientation(45)
actor_3_0.SetOrientation(45)
actor_3_0.GetTextProperty().SetJustificationToRight()
actor_3_0.GetTextProperty().SetVerticalJustificationToTop()
actor_3_0.GetTextProperty().SetColor(0.75, 0.20, 0.80)
actor_3_0.GetTextProperty().SetBackgroundColor(0.25, 0.40, 0.20)
actor_3_0.GetTextProperty().SetBackgroundOpacity(1.0)
actor_3_0.SetPosition(100, 500)
actor_3_0.GetTextProperty().SetFrame(False)
actor_3_0.GetTextProperty().SetFrameColor(0.0, 0.0, 1.0)
actor_3_0.GetTextProperty().SetFrameWidth(1)
actor_3_0.SetInput("TProp Angle: 45.0\nActor Angle: 45.0\nHAlign: Right\nVAlign: Top")
pt_id = anchor_points.InsertNextPoint(100, 500, 0.0)
anchor_verts.InsertNextCell(1, [pt_id])
anchor_colors.InsertNextTuple4(191, 51, 204, 255)

# Row 3, Col 1: TProp orientation=45 + Actor orientation=45, Centered/Centered
actor_3_1 = vtkTextActor()
actor_3_1.GetTextProperty().SetOrientation(45)
actor_3_1.SetOrientation(45)
actor_3_1.GetTextProperty().SetJustificationToCentered()
actor_3_1.GetTextProperty().SetVerticalJustificationToCentered()
actor_3_1.GetTextProperty().SetColor(0.75, 0.46, 0.80)
actor_3_1.GetTextProperty().SetBackgroundColor(0.25, 0.27, 0.20)
actor_3_1.GetTextProperty().SetBackgroundOpacity(1.0)
actor_3_1.SetPosition(300, 500)
actor_3_1.GetTextProperty().SetFrame(True)
actor_3_1.GetTextProperty().SetFrameColor(1.0, 1.0, 1.0)
actor_3_1.GetTextProperty().SetFrameWidth(1)
actor_3_1.SetInput("TProp Angle: 45.0\nActor Angle: 45.0\nHAlign: Centered\nVAlign: Centered")
pt_id = anchor_points.InsertNextPoint(300, 500, 0.0)
anchor_verts.InsertNextCell(1, [pt_id])
anchor_colors.InsertNextTuple4(191, 117, 204, 255)

# Row 3, Col 2: TProp orientation=45 + Actor orientation=45, Left/Bottom
actor_3_2 = vtkTextActor()
actor_3_2.GetTextProperty().SetOrientation(45)
actor_3_2.SetOrientation(45)
actor_3_2.GetTextProperty().SetJustificationToLeft()
actor_3_2.GetTextProperty().SetVerticalJustificationToBottom()
actor_3_2.GetTextProperty().SetColor(0.75, 0.72, 0.80)
actor_3_2.GetTextProperty().SetBackgroundColor(0.25, 0.14, 0.20)
actor_3_2.GetTextProperty().SetBackgroundOpacity(1.0)
actor_3_2.SetPosition(500, 500)
actor_3_2.GetTextProperty().SetFrame(False)
actor_3_2.GetTextProperty().SetFrameColor(1.0, 0.0, 0.0)
actor_3_2.GetTextProperty().SetFrameWidth(1)
actor_3_2.SetInput("TProp Angle: 45.0\nActor Angle: 45.0\nHAlign: Left\nVAlign: Bottom")
pt_id = anchor_points.InsertNextPoint(500, 500, 0.0)
anchor_verts.InsertNextCell(1, [pt_id])
anchor_colors.InsertNextTuple4(191, 183, 204, 255)

# Anchor actor
anchor_mapper = vtkPolyDataMapper2D()
anchor_mapper.SetInputData(anchors)
anchor_actor = vtkActor2D()
anchor_actor.SetMapper(anchor_mapper)
anchor_actor.GetProperty().SetPointSize(5)

# Empty text actors (edge cases)
null_input_actor = vtkTextActor()
null_input_actor.SetInput(None)

empty_input_actor = vtkTextActor()
empty_input_actor.SetInput("")

space_actor = vtkTextActor()
space_actor.SetInput(" ")

tab_actor = vtkTextActor()
tab_actor.SetInput("\t")

newline_actor = vtkTextActor()
newline_actor.SetInput("\n")

# Renderer
renderer = vtkRenderer()
renderer.SetBackground(0.0, 0.0, 0.0)
renderer.AddViewProp(actor_0_0)
renderer.AddViewProp(actor_0_1)
renderer.AddViewProp(actor_0_2)
renderer.AddViewProp(actor_1_0)
renderer.AddViewProp(actor_1_1)
renderer.AddViewProp(actor_1_2)
renderer.AddViewProp(actor_2_0)
renderer.AddViewProp(actor_2_1)
renderer.AddViewProp(actor_2_2)
renderer.AddViewProp(actor_3_0)
renderer.AddViewProp(actor_3_1)
renderer.AddViewProp(actor_3_2)
renderer.AddViewProp(anchor_actor)
renderer.AddViewProp(null_input_actor)
renderer.AddViewProp(empty_input_actor)
renderer.AddViewProp(space_actor)
renderer.AddViewProp(tab_actor)
renderer.AddViewProp(newline_actor)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("text actor")
render_window.SetMultiSamples(0)
render_window.SetSize(width, height)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.GetActiveCamera().SetPosition(0, 0, 400)
renderer.GetActiveCamera().SetFocalPoint(0, 0, 0)
renderer.GetActiveCamera().SetViewUp(0, 1, 0)
renderer.ResetCameraClippingRange()

interactor.Initialize()
interactor.Start()
