#!/usr/bin/env python

# Demonstrate vtkTextActor with MathText rendering via matplotlib backend.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
import vtkmodules.vtkRenderingMatplotlib  # noqa: F401

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

# Renderer
renderer = vtkRenderer()
renderer.SetBackground(0.0, 0.0, 0.0)

width = 600
height = 600
x = (100, 300, 500)
y = (100, 300, 500)

# Anchor points polydata for alignment reference
anchors = vtkPolyData()
points = vtkPoints()
anchors.SetPoints(points)
verts = vtkCellArray()
anchors.SetVerts(verts)
colors = vtkUnsignedCharArray()
colors.SetNumberOfComponents(4)
anchors.GetCellData().SetScalars(colors)

# row=0,col=0: Right/Bottom, orientation=0, frame=True
actor_0_0 = vtkTextActor()
actor_0_0.GetTextProperty().SetJustificationToRight()
actor_0_0.GetTextProperty().SetVerticalJustificationToBottom()
actor_0_0.GetTextProperty().SetFontSize(22)
actor_0_0.GetTextProperty().SetOrientation(0.0)
actor_0_0.GetTextProperty().SetColor(0.75, 0.2, 0.2)
actor_0_0.GetTextProperty().SetBackgroundColor(0.0, 1.0, 1.0)
actor_0_0.GetTextProperty().SetBackgroundOpacity(0.25)
actor_0_0.GetTextProperty().SetFrame(True)
actor_0_0.GetTextProperty().SetFrameColor(0.0, 0.0, 1.0)
actor_0_0.GetTextProperty().SetFrameWidth(1)
actor_0_0.SetPosition(100, 100)
actor_0_0.SetInput("BR $\\theta = 0$")
pt_id = points.InsertNextPoint(100, 100, 0.0)
verts.InsertNextCell(1, [pt_id])
colors.InsertNextTuple4(191, 51, 51, 255)
renderer.AddActor(actor_0_0)

# row=0,col=1: Right/Centered, orientation=45, frame=False
actor_0_1 = vtkTextActor()
actor_0_1.GetTextProperty().SetJustificationToRight()
actor_0_1.GetTextProperty().SetVerticalJustificationToCentered()
actor_0_1.GetTextProperty().SetFontSize(22)
actor_0_1.GetTextProperty().SetOrientation(45.0)
actor_0_1.GetTextProperty().SetColor(0.75, 0.46, 0.2)
actor_0_1.GetTextProperty().SetBackgroundColor(0.0, 0.74, 1.0)
actor_0_1.GetTextProperty().SetBackgroundOpacity(0.25)
actor_0_1.GetTextProperty().SetFrame(False)
actor_0_1.GetTextProperty().SetFrameColor(1.0, 1.0, 1.0)
actor_0_1.GetTextProperty().SetFrameWidth(1)
actor_0_1.SetPosition(300, 100)
actor_0_1.SetInput("CR $\\theta = 45$")
pt_id = points.InsertNextPoint(300, 100, 0.0)
verts.InsertNextCell(1, [pt_id])
colors.InsertNextTuple4(191, 117, 51, 255)
renderer.AddActor(actor_0_1)

# row=0,col=2: Right/Top, orientation=90, frame=False
actor_0_2 = vtkTextActor()
actor_0_2.GetTextProperty().SetJustificationToRight()
actor_0_2.GetTextProperty().SetVerticalJustificationToTop()
actor_0_2.GetTextProperty().SetFontSize(22)
actor_0_2.GetTextProperty().SetOrientation(90.0)
actor_0_2.GetTextProperty().SetColor(0.75, 0.72, 0.2)
actor_0_2.GetTextProperty().SetBackgroundColor(0.0, 0.48, 1.0)
actor_0_2.GetTextProperty().SetBackgroundOpacity(0.25)
actor_0_2.GetTextProperty().SetFrame(False)
actor_0_2.GetTextProperty().SetFrameColor(1.0, 0.0, 0.0)
actor_0_2.GetTextProperty().SetFrameWidth(1)
actor_0_2.SetPosition(500, 100)
actor_0_2.SetInput("TR $\\theta = 90$")
pt_id = points.InsertNextPoint(500, 100, 0.0)
verts.InsertNextCell(1, [pt_id])
colors.InsertNextTuple4(191, 183, 51, 255)
renderer.AddActor(actor_0_2)

# row=1,col=0: Centered/Bottom, orientation=135, frame=False
actor_1_0 = vtkTextActor()
actor_1_0.GetTextProperty().SetJustificationToCentered()
actor_1_0.GetTextProperty().SetVerticalJustificationToBottom()
actor_1_0.GetTextProperty().SetFontSize(22)
actor_1_0.GetTextProperty().SetOrientation(135.0)
actor_1_0.GetTextProperty().SetColor(0.75, 0.2, 0.46)
actor_1_0.GetTextProperty().SetBackgroundColor(0.0, 1.0, 0.74)
actor_1_0.GetTextProperty().SetBackgroundOpacity(0.25)
actor_1_0.GetTextProperty().SetFrame(False)
actor_1_0.GetTextProperty().SetFrameColor(0.0, 0.0, 1.0)
actor_1_0.GetTextProperty().SetFrameWidth(1)
actor_1_0.SetPosition(100, 300)
actor_1_0.SetInput("BC $\\theta = 135$")
pt_id = points.InsertNextPoint(100, 300, 0.0)
verts.InsertNextCell(1, [pt_id])
colors.InsertNextTuple4(191, 51, 117, 255)
renderer.AddActor(actor_1_0)

# row=1,col=1: Centered/Centered, orientation=180, frame=False
actor_1_1 = vtkTextActor()
actor_1_1.GetTextProperty().SetJustificationToCentered()
actor_1_1.GetTextProperty().SetVerticalJustificationToCentered()
actor_1_1.GetTextProperty().SetFontSize(22)
actor_1_1.GetTextProperty().SetOrientation(180.0)
actor_1_1.GetTextProperty().SetColor(0.75, 0.46, 0.46)
actor_1_1.GetTextProperty().SetBackgroundColor(0.0, 0.74, 0.74)
actor_1_1.GetTextProperty().SetBackgroundOpacity(0.25)
actor_1_1.GetTextProperty().SetFrame(False)
actor_1_1.GetTextProperty().SetFrameColor(1.0, 1.0, 1.0)
actor_1_1.GetTextProperty().SetFrameWidth(1)
actor_1_1.SetPosition(300, 300)
actor_1_1.SetInput("CC $\\theta = 180$")
pt_id = points.InsertNextPoint(300, 300, 0.0)
verts.InsertNextCell(1, [pt_id])
colors.InsertNextTuple4(191, 117, 117, 255)
renderer.AddActor(actor_1_1)

# row=1,col=2: Centered/Top, orientation=225, frame=False
actor_1_2 = vtkTextActor()
actor_1_2.GetTextProperty().SetJustificationToCentered()
actor_1_2.GetTextProperty().SetVerticalJustificationToTop()
actor_1_2.GetTextProperty().SetFontSize(22)
actor_1_2.GetTextProperty().SetOrientation(225.0)
actor_1_2.GetTextProperty().SetColor(0.75, 0.72, 0.46)
actor_1_2.GetTextProperty().SetBackgroundColor(0.0, 0.48, 0.74)
actor_1_2.GetTextProperty().SetBackgroundOpacity(0.25)
actor_1_2.GetTextProperty().SetFrame(False)
actor_1_2.GetTextProperty().SetFrameColor(1.0, 0.0, 0.0)
actor_1_2.GetTextProperty().SetFrameWidth(1)
actor_1_2.SetPosition(500, 300)
actor_1_2.SetInput("TC $\\theta = 225$")
pt_id = points.InsertNextPoint(500, 300, 0.0)
verts.InsertNextCell(1, [pt_id])
colors.InsertNextTuple4(191, 183, 117, 255)
renderer.AddActor(actor_1_2)

# row=2,col=0: Left/Bottom, orientation=270, frame=False
actor_2_0 = vtkTextActor()
actor_2_0.GetTextProperty().SetJustificationToLeft()
actor_2_0.GetTextProperty().SetVerticalJustificationToBottom()
actor_2_0.GetTextProperty().SetFontSize(22)
actor_2_0.GetTextProperty().SetOrientation(270.0)
actor_2_0.GetTextProperty().SetColor(0.75, 0.2, 0.72)
actor_2_0.GetTextProperty().SetBackgroundColor(0.0, 1.0, 0.48)
actor_2_0.GetTextProperty().SetBackgroundOpacity(0.25)
actor_2_0.GetTextProperty().SetFrame(False)
actor_2_0.GetTextProperty().SetFrameColor(0.0, 0.0, 1.0)
actor_2_0.GetTextProperty().SetFrameWidth(1)
actor_2_0.SetPosition(100, 500)
actor_2_0.SetInput("BL $\\theta = 270$")
pt_id = points.InsertNextPoint(100, 500, 0.0)
verts.InsertNextCell(1, [pt_id])
colors.InsertNextTuple4(191, 51, 183, 255)
renderer.AddActor(actor_2_0)

# row=2,col=1: Left/Centered, orientation=315, frame=False
actor_2_1 = vtkTextActor()
actor_2_1.GetTextProperty().SetJustificationToLeft()
actor_2_1.GetTextProperty().SetVerticalJustificationToCentered()
actor_2_1.GetTextProperty().SetFontSize(22)
actor_2_1.GetTextProperty().SetOrientation(315.0)
actor_2_1.GetTextProperty().SetColor(0.75, 0.46, 0.72)
actor_2_1.GetTextProperty().SetBackgroundColor(0.0, 0.74, 0.48)
actor_2_1.GetTextProperty().SetBackgroundOpacity(0.25)
actor_2_1.GetTextProperty().SetFrame(False)
actor_2_1.GetTextProperty().SetFrameColor(1.0, 1.0, 1.0)
actor_2_1.GetTextProperty().SetFrameWidth(1)
actor_2_1.SetPosition(300, 500)
actor_2_1.SetInput("CL $\\theta = 315$")
pt_id = points.InsertNextPoint(300, 500, 0.0)
verts.InsertNextCell(1, [pt_id])
colors.InsertNextTuple4(191, 117, 183, 255)
renderer.AddActor(actor_2_1)

# row=2,col=2: Left/Top, orientation=360, frame=False
actor_2_2 = vtkTextActor()
actor_2_2.GetTextProperty().SetJustificationToLeft()
actor_2_2.GetTextProperty().SetVerticalJustificationToTop()
actor_2_2.GetTextProperty().SetFontSize(22)
actor_2_2.GetTextProperty().SetOrientation(360.0)
actor_2_2.GetTextProperty().SetColor(0.75, 0.72, 0.72)
actor_2_2.GetTextProperty().SetBackgroundColor(0.0, 0.48, 0.48)
actor_2_2.GetTextProperty().SetBackgroundOpacity(0.25)
actor_2_2.GetTextProperty().SetFrame(False)
actor_2_2.GetTextProperty().SetFrameColor(1.0, 0.0, 0.0)
actor_2_2.GetTextProperty().SetFrameWidth(1)
actor_2_2.SetPosition(500, 500)
actor_2_2.SetInput("TL $\\theta = 360$")
pt_id = points.InsertNextPoint(500, 500, 0.0)
verts.InsertNextCell(1, [pt_id])
colors.InsertNextTuple4(191, 183, 183, 255)
renderer.AddActor(actor_2_2)

# Anchor point overlay
anchor_mapper = vtkPolyDataMapper2D()
anchor_mapper.SetInputData(anchors)
anchor_actor = vtkActor2D()
anchor_actor.SetMapper(anchor_mapper)
anchor_actor.GetProperty().SetPointSize(5)
renderer.AddActor(anchor_actor)

# Render window
render_window = vtkRenderWindow()
render_window.SetSize(width, height)
render_window.AddRenderer(renderer)
render_window.SetMultiSamples(0)
render_window.SetWindowName("math text actor")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
