#!/usr/bin/env python

# Test vtkTextMapper with various alignments and orientations.

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
    vtkTextMapper,
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

# Row 0, Col 0: Right/Bottom, orientation=0
mapper_0_0 = vtkTextMapper()
mapper_0_0.GetTextProperty().SetJustificationToRight()
mapper_0_0.GetTextProperty().SetVerticalJustificationToBottom()
mapper_0_0.GetTextProperty().SetOrientation(0.0)
mapper_0_0.GetTextProperty().SetColor(0.75, 0.20, 0.20)
mapper_0_0.SetInput("TProp Angle: 0.0\nHAlign: Right\nVAlign: Bottom")
actor_0_0 = vtkActor2D()
actor_0_0.SetPosition(100, 100)
actor_0_0.SetMapper(mapper_0_0)
pt_id = anchor_points.InsertNextPoint(100, 100, 0.0)
anchor_verts.InsertNextCell(1, [pt_id])
anchor_colors.InsertNextTuple4(191, 51, 51, 255)

# Row 0, Col 1: Right/Centered, orientation=45
mapper_0_1 = vtkTextMapper()
mapper_0_1.GetTextProperty().SetJustificationToRight()
mapper_0_1.GetTextProperty().SetVerticalJustificationToCentered()
mapper_0_1.GetTextProperty().SetOrientation(45.0)
mapper_0_1.GetTextProperty().SetColor(0.75, 0.46, 0.20)
mapper_0_1.SetInput("TProp Angle: 45.0\nHAlign: Right\nVAlign: Centered")
actor_0_1 = vtkActor2D()
actor_0_1.SetPosition(300, 100)
actor_0_1.SetMapper(mapper_0_1)
pt_id = anchor_points.InsertNextPoint(300, 100, 0.0)
anchor_verts.InsertNextCell(1, [pt_id])
anchor_colors.InsertNextTuple4(191, 117, 51, 255)

# Row 0, Col 2: Right/Top, orientation=90
mapper_0_2 = vtkTextMapper()
mapper_0_2.GetTextProperty().SetJustificationToRight()
mapper_0_2.GetTextProperty().SetVerticalJustificationToTop()
mapper_0_2.GetTextProperty().SetOrientation(90.0)
mapper_0_2.GetTextProperty().SetColor(0.75, 0.72, 0.20)
mapper_0_2.SetInput("TProp Angle: 90.0\nHAlign: Right\nVAlign: Top")
actor_0_2 = vtkActor2D()
actor_0_2.SetPosition(500, 100)
actor_0_2.SetMapper(mapper_0_2)
pt_id = anchor_points.InsertNextPoint(500, 100, 0.0)
anchor_verts.InsertNextCell(1, [pt_id])
anchor_colors.InsertNextTuple4(191, 183, 51, 255)

# Row 1, Col 0: Centered/Bottom, orientation=135
mapper_1_0 = vtkTextMapper()
mapper_1_0.GetTextProperty().SetJustificationToCentered()
mapper_1_0.GetTextProperty().SetVerticalJustificationToBottom()
mapper_1_0.GetTextProperty().SetOrientation(135.0)
mapper_1_0.GetTextProperty().SetColor(0.75, 0.20, 0.40)
mapper_1_0.SetInput("TProp Angle: 135.0\nHAlign: Centered\nVAlign: Bottom")
actor_1_0 = vtkActor2D()
actor_1_0.SetPosition(100, 300)
actor_1_0.SetMapper(mapper_1_0)
pt_id = anchor_points.InsertNextPoint(100, 300, 0.0)
anchor_verts.InsertNextCell(1, [pt_id])
anchor_colors.InsertNextTuple4(191, 51, 102, 255)

# Row 1, Col 1: Centered/Centered, orientation=180
mapper_1_1 = vtkTextMapper()
mapper_1_1.GetTextProperty().SetJustificationToCentered()
mapper_1_1.GetTextProperty().SetVerticalJustificationToCentered()
mapper_1_1.GetTextProperty().SetOrientation(180.0)
mapper_1_1.GetTextProperty().SetColor(0.75, 0.46, 0.40)
mapper_1_1.SetInput("TProp Angle: 180.0\nHAlign: Centered\nVAlign: Centered")
actor_1_1 = vtkActor2D()
actor_1_1.SetPosition(300, 300)
actor_1_1.SetMapper(mapper_1_1)
pt_id = anchor_points.InsertNextPoint(300, 300, 0.0)
anchor_verts.InsertNextCell(1, [pt_id])
anchor_colors.InsertNextTuple4(191, 117, 102, 255)

# Row 1, Col 2: Centered/Top, orientation=225
mapper_1_2 = vtkTextMapper()
mapper_1_2.GetTextProperty().SetJustificationToCentered()
mapper_1_2.GetTextProperty().SetVerticalJustificationToTop()
mapper_1_2.GetTextProperty().SetOrientation(225.0)
mapper_1_2.GetTextProperty().SetColor(0.75, 0.72, 0.40)
mapper_1_2.SetInput("TProp Angle: 225.0\nHAlign: Centered\nVAlign: Top")
actor_1_2 = vtkActor2D()
actor_1_2.SetPosition(500, 300)
actor_1_2.SetMapper(mapper_1_2)
pt_id = anchor_points.InsertNextPoint(500, 300, 0.0)
anchor_verts.InsertNextCell(1, [pt_id])
anchor_colors.InsertNextTuple4(191, 183, 102, 255)

# Row 2, Col 0: Left/Bottom, orientation=270
mapper_2_0 = vtkTextMapper()
mapper_2_0.GetTextProperty().SetJustificationToLeft()
mapper_2_0.GetTextProperty().SetVerticalJustificationToBottom()
mapper_2_0.GetTextProperty().SetOrientation(270.0)
mapper_2_0.GetTextProperty().SetColor(0.75, 0.20, 0.60)
mapper_2_0.SetInput("TProp Angle: 270.0\nHAlign: Left\nVAlign: Bottom")
actor_2_0 = vtkActor2D()
actor_2_0.SetPosition(100, 500)
actor_2_0.SetMapper(mapper_2_0)
pt_id = anchor_points.InsertNextPoint(100, 500, 0.0)
anchor_verts.InsertNextCell(1, [pt_id])
anchor_colors.InsertNextTuple4(191, 51, 153, 255)

# Row 2, Col 1: Left/Centered, orientation=315
mapper_2_1 = vtkTextMapper()
mapper_2_1.GetTextProperty().SetJustificationToLeft()
mapper_2_1.GetTextProperty().SetVerticalJustificationToCentered()
mapper_2_1.GetTextProperty().SetOrientation(315.0)
mapper_2_1.GetTextProperty().SetColor(0.75, 0.46, 0.60)
mapper_2_1.SetInput("TProp Angle: 315.0\nHAlign: Left\nVAlign: Centered")
actor_2_1 = vtkActor2D()
actor_2_1.SetPosition(300, 500)
actor_2_1.SetMapper(mapper_2_1)
pt_id = anchor_points.InsertNextPoint(300, 500, 0.0)
anchor_verts.InsertNextCell(1, [pt_id])
anchor_colors.InsertNextTuple4(191, 117, 153, 255)

# Row 2, Col 2: Left/Top, orientation=360
mapper_2_2 = vtkTextMapper()
mapper_2_2.GetTextProperty().SetJustificationToLeft()
mapper_2_2.GetTextProperty().SetVerticalJustificationToTop()
mapper_2_2.GetTextProperty().SetOrientation(360.0)
mapper_2_2.GetTextProperty().SetColor(0.75, 0.72, 0.60)
mapper_2_2.SetInput("TProp Angle: 360.0\nHAlign: Left\nVAlign: Top")
actor_2_2 = vtkActor2D()
actor_2_2.SetPosition(500, 500)
actor_2_2.SetMapper(mapper_2_2)
pt_id = anchor_points.InsertNextPoint(500, 500, 0.0)
anchor_verts.InsertNextCell(1, [pt_id])
anchor_colors.InsertNextTuple4(191, 183, 153, 255)

# Anchor actor
anchor_mapper = vtkPolyDataMapper2D()
anchor_mapper.SetInputData(anchors)
anchor_actor = vtkActor2D()
anchor_actor.SetMapper(anchor_mapper)
anchor_actor.GetProperty().SetPointSize(5)

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
renderer.AddViewProp(anchor_actor)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("text mapper")
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
