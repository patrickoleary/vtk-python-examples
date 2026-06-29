#!/usr/bin/env python

# Test vtkBillboardTextActor3D with various text alignments and orientations.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import vtkPoints, vtkUnsignedCharArray
from vtkmodules.vtkCommonDataModel import vtkCellArray, vtkPolyData
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)
from vtkmodules.vtkRenderingCore import vtkBillboardTextActor3D

width = 600
height = 600
x_pos = [100, 300, 500]
y_pos = [100, 300, 500]

# Anchor points polydata
anchors = vtkPolyData()
anchor_points = vtkPoints()
anchors.SetPoints(anchor_points)
anchor_verts = vtkCellArray()
anchors.SetVerts(anchor_verts)
anchor_colors = vtkUnsignedCharArray()
anchor_colors.SetNumberOfComponents(4)
anchors.GetCellData().SetScalars(anchor_colors)

# Row 0, Col 0: Right/Bottom, orientation=0, pos=(100,100,0)
billboard_0_0 = vtkBillboardTextActor3D()
billboard_0_0.GetTextProperty().SetJustificationToRight()
billboard_0_0.GetTextProperty().SetVerticalJustificationToBottom()
billboard_0_0.GetTextProperty().SetFontSize(20)
billboard_0_0.GetTextProperty().SetOrientation(0.0)
billboard_0_0.GetTextProperty().SetColor(0.75, 0.20, 0.20)
billboard_0_0.GetTextProperty().SetBackgroundColor(0.0, 1.0, 1.0)
billboard_0_0.GetTextProperty().SetBackgroundOpacity(0.85)
billboard_0_0.SetPosition(100, 100, 0.0)
billboard_0_0.SetInput("TProp Angle: 0.0\nHAlign: Right\nVAlign: Bottom")
pt_id = anchor_points.InsertNextPoint(100, 100, 0.0)
anchor_verts.InsertNextCell(1, [pt_id])
anchor_colors.InsertNextTuple4(191, 51, 51, 255)

# Row 0, Col 1: Right/Centered, orientation=45, pos=(300,100,0)
billboard_0_1 = vtkBillboardTextActor3D()
billboard_0_1.GetTextProperty().SetJustificationToRight()
billboard_0_1.GetTextProperty().SetVerticalJustificationToCentered()
billboard_0_1.GetTextProperty().SetFontSize(20)
billboard_0_1.GetTextProperty().SetOrientation(45.0)
billboard_0_1.GetTextProperty().SetColor(0.75, 0.46, 0.20)
billboard_0_1.GetTextProperty().SetBackgroundColor(0.0, 0.74, 1.0)
billboard_0_1.GetTextProperty().SetBackgroundOpacity(0.85)
billboard_0_1.SetPosition(300, 100, 0.0)
billboard_0_1.SetInput("TProp Angle: 45.0\nHAlign: Right\nVAlign: Centered")
pt_id = anchor_points.InsertNextPoint(300, 100, 0.0)
anchor_verts.InsertNextCell(1, [pt_id])
anchor_colors.InsertNextTuple4(191, 117, 51, 255)

# Row 0, Col 2: Right/Top, orientation=90, pos=(500,100,0)
billboard_0_2 = vtkBillboardTextActor3D()
billboard_0_2.GetTextProperty().SetJustificationToRight()
billboard_0_2.GetTextProperty().SetVerticalJustificationToTop()
billboard_0_2.GetTextProperty().SetFontSize(20)
billboard_0_2.GetTextProperty().SetOrientation(90.0)
billboard_0_2.GetTextProperty().SetColor(0.75, 0.72, 0.20)
billboard_0_2.GetTextProperty().SetBackgroundColor(0.0, 0.48, 1.0)
billboard_0_2.GetTextProperty().SetBackgroundOpacity(0.85)
billboard_0_2.SetPosition(500, 100, 0.0)
billboard_0_2.SetInput("TProp Angle: 90.0\nHAlign: Right\nVAlign: Top")
pt_id = anchor_points.InsertNextPoint(500, 100, 0.0)
anchor_verts.InsertNextCell(1, [pt_id])
anchor_colors.InsertNextTuple4(191, 183, 51, 255)

# Row 1, Col 0: Centered/Bottom, orientation=135, pos=(100,300,0)
billboard_1_0 = vtkBillboardTextActor3D()
billboard_1_0.GetTextProperty().SetJustificationToCentered()
billboard_1_0.GetTextProperty().SetVerticalJustificationToBottom()
billboard_1_0.GetTextProperty().SetFontSize(20)
billboard_1_0.GetTextProperty().SetOrientation(135.0)
billboard_1_0.GetTextProperty().SetColor(0.75, 0.20, 0.46)
billboard_1_0.GetTextProperty().SetBackgroundColor(0.0, 1.0, 0.74)
billboard_1_0.GetTextProperty().SetBackgroundOpacity(0.85)
billboard_1_0.SetPosition(100, 300, 0.0)
billboard_1_0.SetInput("TProp Angle: 135.0\nHAlign: Centered\nVAlign: Bottom")
pt_id = anchor_points.InsertNextPoint(100, 300, 0.0)
anchor_verts.InsertNextCell(1, [pt_id])
anchor_colors.InsertNextTuple4(191, 51, 117, 255)

# Row 1, Col 1: Centered/Centered, orientation=180, pos=(300,300,0)
billboard_1_1 = vtkBillboardTextActor3D()
billboard_1_1.GetTextProperty().SetJustificationToCentered()
billboard_1_1.GetTextProperty().SetVerticalJustificationToCentered()
billboard_1_1.GetTextProperty().SetFontSize(20)
billboard_1_1.GetTextProperty().SetOrientation(180.0)
billboard_1_1.GetTextProperty().SetColor(0.75, 0.46, 0.46)
billboard_1_1.GetTextProperty().SetBackgroundColor(0.0, 0.74, 0.74)
billboard_1_1.GetTextProperty().SetBackgroundOpacity(0.85)
billboard_1_1.SetPosition(300, 300, 0.0)
billboard_1_1.SetInput("TProp Angle: 180.0\nHAlign: Centered\nVAlign: Centered")
pt_id = anchor_points.InsertNextPoint(300, 300, 0.0)
anchor_verts.InsertNextCell(1, [pt_id])
anchor_colors.InsertNextTuple4(191, 117, 117, 255)

# Row 1, Col 2: Centered/Top, orientation=225, pos=(500,300,0)
billboard_1_2 = vtkBillboardTextActor3D()
billboard_1_2.GetTextProperty().SetJustificationToCentered()
billboard_1_2.GetTextProperty().SetVerticalJustificationToTop()
billboard_1_2.GetTextProperty().SetFontSize(20)
billboard_1_2.GetTextProperty().SetOrientation(225.0)
billboard_1_2.GetTextProperty().SetColor(0.75, 0.72, 0.46)
billboard_1_2.GetTextProperty().SetBackgroundColor(0.0, 0.48, 0.74)
billboard_1_2.GetTextProperty().SetBackgroundOpacity(0.85)
billboard_1_2.SetPosition(500, 300, 0.0)
billboard_1_2.SetInput("TProp Angle: 225.0\nHAlign: Centered\nVAlign: Top")
pt_id = anchor_points.InsertNextPoint(500, 300, 0.0)
anchor_verts.InsertNextCell(1, [pt_id])
anchor_colors.InsertNextTuple4(191, 183, 117, 255)

# Row 2, Col 0: Left/Bottom, orientation=270, pos=(100,500,0)
billboard_2_0 = vtkBillboardTextActor3D()
billboard_2_0.GetTextProperty().SetJustificationToLeft()
billboard_2_0.GetTextProperty().SetVerticalJustificationToBottom()
billboard_2_0.GetTextProperty().SetFontSize(20)
billboard_2_0.GetTextProperty().SetOrientation(270.0)
billboard_2_0.GetTextProperty().SetColor(0.75, 0.20, 0.72)
billboard_2_0.GetTextProperty().SetBackgroundColor(0.0, 1.0, 0.48)
billboard_2_0.GetTextProperty().SetBackgroundOpacity(0.85)
billboard_2_0.SetPosition(100, 500, 0.0)
billboard_2_0.SetInput("TProp Angle: 270.0\nHAlign: Left\nVAlign: Bottom")
pt_id = anchor_points.InsertNextPoint(100, 500, 0.0)
anchor_verts.InsertNextCell(1, [pt_id])
anchor_colors.InsertNextTuple4(191, 51, 183, 255)

# Row 2, Col 1: Left/Centered, orientation=315, pos=(300,500,0)
billboard_2_1 = vtkBillboardTextActor3D()
billboard_2_1.GetTextProperty().SetJustificationToLeft()
billboard_2_1.GetTextProperty().SetVerticalJustificationToCentered()
billboard_2_1.GetTextProperty().SetFontSize(20)
billboard_2_1.GetTextProperty().SetOrientation(315.0)
billboard_2_1.GetTextProperty().SetColor(0.75, 0.46, 0.72)
billboard_2_1.GetTextProperty().SetBackgroundColor(0.0, 0.74, 0.48)
billboard_2_1.GetTextProperty().SetBackgroundOpacity(0.85)
billboard_2_1.SetPosition(300, 500, 0.0)
billboard_2_1.SetInput("TProp Angle: 315.0\nHAlign: Left\nVAlign: Centered")
pt_id = anchor_points.InsertNextPoint(300, 500, 0.0)
anchor_verts.InsertNextCell(1, [pt_id])
anchor_colors.InsertNextTuple4(191, 117, 183, 255)

# Row 2, Col 2: Left/Top, orientation=360, pos=(500,500,0)
billboard_2_2 = vtkBillboardTextActor3D()
billboard_2_2.GetTextProperty().SetJustificationToLeft()
billboard_2_2.GetTextProperty().SetVerticalJustificationToTop()
billboard_2_2.GetTextProperty().SetFontSize(20)
billboard_2_2.GetTextProperty().SetOrientation(360.0)
billboard_2_2.GetTextProperty().SetColor(0.75, 0.72, 0.72)
billboard_2_2.GetTextProperty().SetBackgroundColor(0.0, 0.48, 0.48)
billboard_2_2.GetTextProperty().SetBackgroundOpacity(0.85)
billboard_2_2.SetPosition(500, 500, 0.0)
billboard_2_2.SetInput("TProp Angle: 360.0\nHAlign: Left\nVAlign: Top")
pt_id = anchor_points.InsertNextPoint(500, 500, 0.0)
anchor_verts.InsertNextCell(1, [pt_id])
anchor_colors.InsertNextTuple4(191, 183, 183, 255)

# Anchor actor
anchor_mapper = vtkPolyDataMapper()
anchor_mapper.SetInputData(anchors)
anchor_actor = vtkActor()
anchor_actor.SetMapper(anchor_mapper)
anchor_actor.GetProperty().SetPointSize(5)

# Empty text actors (edge cases)
null_input_actor = vtkBillboardTextActor3D()
null_input_actor.SetInput(None)

empty_input_actor = vtkBillboardTextActor3D()
empty_input_actor.SetInput("")

space_actor = vtkBillboardTextActor3D()
space_actor.SetInput(" ")

tab_actor = vtkBillboardTextActor3D()
tab_actor.SetInput("\t")

newline_actor = vtkBillboardTextActor3D()
newline_actor.SetInput("\n")

# Grid polydata
grid = vtkPolyData()
grid_points = vtkPoints()
grid.SetPoints(grid_points)
marks = [0.0, 200.0, 400.0, 600.0]
thickness = 200.0
for x_i in range(4):
    for y_i in range(4):
        grid_points.InsertNextPoint(marks[x_i], marks[y_i], -thickness / 2.0)
        grid_points.InsertNextPoint(marks[x_i], marks[y_i], +thickness / 2.0)

grid_cells = vtkCellArray()
grid.SetPolys(grid_cells)
for c in range(4):
    for r in range(3):
        base = 8 * c + 2 * r
        grid_cells.InsertNextCell(4, [base + 0, base + 1, base + 3, base + 2])

grid_mapper = vtkPolyDataMapper()
grid_mapper.SetInputData(grid)
grid_actor = vtkActor()
grid_actor.GetProperty().SetRepresentationToSurface()
grid_actor.GetProperty().SetColor(0.6, 0.6, 0.6)
grid_actor.SetMapper(grid_mapper)

# Renderer
renderer = vtkRenderer()
renderer.UseDepthPeelingOn()
renderer.SetBackground(0.0, 0.0, 0.0)
renderer.AddActor(billboard_0_0)
renderer.AddActor(billboard_0_1)
renderer.AddActor(billboard_0_2)
renderer.AddActor(billboard_1_0)
renderer.AddActor(billboard_1_1)
renderer.AddActor(billboard_1_2)
renderer.AddActor(billboard_2_0)
renderer.AddActor(billboard_2_1)
renderer.AddActor(billboard_2_2)
renderer.AddActor(anchor_actor)
renderer.AddActor(null_input_actor)
renderer.AddActor(empty_input_actor)
renderer.AddActor(space_actor)
renderer.AddActor(tab_actor)
renderer.AddActor(newline_actor)
renderer.AddActor(grid_actor)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("billboard text actor3d")
render_window.SetMultiSamples(0)
render_window.SetSize(width, height)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.GetActiveCamera().SetPosition(width / 2, height / 2, 1400)
renderer.GetActiveCamera().SetFocalPoint(width / 2, height / 2, 0)
renderer.GetActiveCamera().SetViewUp(0, 1, 0)
renderer.GetActiveCamera().Roll(45.0)
renderer.GetActiveCamera().Elevation(45.0)
renderer.ResetCameraClippingRange()

interactor.Initialize()
interactor.Start()
