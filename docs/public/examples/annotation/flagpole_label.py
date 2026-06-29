#!/usr/bin/env python

# Test vtkFlagpoleLabel with various text alignments and anchor points.

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
from vtkmodules.vtkRenderingCore import vtkFlagpoleLabel

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

# Row 0, Col 0: Right/Bottom
flagpole_0_0 = vtkFlagpoleLabel()
flagpole_0_0.GetTextProperty().SetJustificationToRight()
flagpole_0_0.GetTextProperty().SetVerticalJustificationToBottom()
flagpole_0_0.GetTextProperty().SetColor(0.75, 0.20, 0.20)
flagpole_0_0.GetTextProperty().SetBackgroundColor(0.0, 1.0, 1.0)
flagpole_0_0.GetTextProperty().SetFrameColor(0.0, 1.0, 1.0)
flagpole_0_0.GetTextProperty().SetBackgroundOpacity(0.85)
flagpole_0_0.SetBasePosition(100, 50.0, 0.0)
flagpole_0_0.SetTopPosition(100, 150.0, 0.0)
flagpole_0_0.SetInput("HAlign: Right\nVAlign: Bottom")
pt_id = anchor_points.InsertNextPoint(100, 150.0, 0.0)
anchor_verts.InsertNextCell(1, [pt_id])
anchor_colors.InsertNextTuple4(191, 51, 51, 255)

# Row 0, Col 1: Right/Centered
flagpole_0_1 = vtkFlagpoleLabel()
flagpole_0_1.GetTextProperty().SetJustificationToRight()
flagpole_0_1.GetTextProperty().SetVerticalJustificationToCentered()
flagpole_0_1.GetTextProperty().SetColor(0.75, 0.46, 0.20)
flagpole_0_1.GetTextProperty().SetBackgroundColor(0.0, 0.74, 1.0)
flagpole_0_1.GetTextProperty().SetFrameColor(0.0, 0.74, 1.0)
flagpole_0_1.GetTextProperty().SetBackgroundOpacity(0.85)
flagpole_0_1.SetBasePosition(300, 50.0, 0.0)
flagpole_0_1.SetTopPosition(300, 150.0, 0.0)
flagpole_0_1.SetInput("HAlign: Right\nVAlign: Centered")
pt_id = anchor_points.InsertNextPoint(300, 150.0, 0.0)
anchor_verts.InsertNextCell(1, [pt_id])
anchor_colors.InsertNextTuple4(191, 117, 51, 255)

# Row 0, Col 2: Right/Top
flagpole_0_2 = vtkFlagpoleLabel()
flagpole_0_2.GetTextProperty().SetJustificationToRight()
flagpole_0_2.GetTextProperty().SetVerticalJustificationToTop()
flagpole_0_2.GetTextProperty().SetColor(0.75, 0.72, 0.20)
flagpole_0_2.GetTextProperty().SetBackgroundColor(0.0, 0.48, 1.0)
flagpole_0_2.GetTextProperty().SetFrameColor(0.0, 0.48, 1.0)
flagpole_0_2.GetTextProperty().SetBackgroundOpacity(0.85)
flagpole_0_2.SetBasePosition(500, 50.0, 0.0)
flagpole_0_2.SetTopPosition(500, 150.0, 0.0)
flagpole_0_2.SetInput("HAlign: Right\nVAlign: Top")
pt_id = anchor_points.InsertNextPoint(500, 150.0, 0.0)
anchor_verts.InsertNextCell(1, [pt_id])
anchor_colors.InsertNextTuple4(191, 183, 51, 255)

# Row 1, Col 0: Centered/Bottom
flagpole_1_0 = vtkFlagpoleLabel()
flagpole_1_0.GetTextProperty().SetJustificationToCentered()
flagpole_1_0.GetTextProperty().SetVerticalJustificationToBottom()
flagpole_1_0.GetTextProperty().SetColor(0.75, 0.20, 0.46)
flagpole_1_0.GetTextProperty().SetBackgroundColor(0.0, 1.0, 0.74)
flagpole_1_0.GetTextProperty().SetFrameColor(0.0, 1.0, 0.74)
flagpole_1_0.GetTextProperty().SetBackgroundOpacity(0.85)
flagpole_1_0.SetBasePosition(100, 250.0, 0.0)
flagpole_1_0.SetTopPosition(100, 350.0, 0.0)
flagpole_1_0.SetInput("HAlign: Centered\nVAlign: Bottom")
pt_id = anchor_points.InsertNextPoint(100, 350.0, 0.0)
anchor_verts.InsertNextCell(1, [pt_id])
anchor_colors.InsertNextTuple4(191, 51, 117, 255)

# Row 1, Col 1: Centered/Centered
flagpole_1_1 = vtkFlagpoleLabel()
flagpole_1_1.GetTextProperty().SetJustificationToCentered()
flagpole_1_1.GetTextProperty().SetVerticalJustificationToCentered()
flagpole_1_1.GetTextProperty().SetColor(0.75, 0.46, 0.46)
flagpole_1_1.GetTextProperty().SetBackgroundColor(0.0, 0.74, 0.74)
flagpole_1_1.GetTextProperty().SetFrameColor(0.0, 0.74, 0.74)
flagpole_1_1.GetTextProperty().SetBackgroundOpacity(0.85)
flagpole_1_1.SetBasePosition(300, 250.0, 0.0)
flagpole_1_1.SetTopPosition(300, 350.0, 0.0)
flagpole_1_1.SetInput("HAlign: Centered\nVAlign: Centered")
pt_id = anchor_points.InsertNextPoint(300, 350.0, 0.0)
anchor_verts.InsertNextCell(1, [pt_id])
anchor_colors.InsertNextTuple4(191, 117, 117, 255)

# Row 1, Col 2: Centered/Top
flagpole_1_2 = vtkFlagpoleLabel()
flagpole_1_2.GetTextProperty().SetJustificationToCentered()
flagpole_1_2.GetTextProperty().SetVerticalJustificationToTop()
flagpole_1_2.GetTextProperty().SetColor(0.75, 0.72, 0.46)
flagpole_1_2.GetTextProperty().SetBackgroundColor(0.0, 0.48, 0.74)
flagpole_1_2.GetTextProperty().SetFrameColor(0.0, 0.48, 0.74)
flagpole_1_2.GetTextProperty().SetBackgroundOpacity(0.85)
flagpole_1_2.SetBasePosition(500, 250.0, 0.0)
flagpole_1_2.SetTopPosition(500, 350.0, 0.0)
flagpole_1_2.SetInput("HAlign: Centered\nVAlign: Top")
pt_id = anchor_points.InsertNextPoint(500, 350.0, 0.0)
anchor_verts.InsertNextCell(1, [pt_id])
anchor_colors.InsertNextTuple4(191, 183, 117, 255)

# Row 2, Col 0: Left/Bottom
flagpole_2_0 = vtkFlagpoleLabel()
flagpole_2_0.GetTextProperty().SetJustificationToLeft()
flagpole_2_0.GetTextProperty().SetVerticalJustificationToBottom()
flagpole_2_0.GetTextProperty().SetColor(0.75, 0.20, 0.72)
flagpole_2_0.GetTextProperty().SetBackgroundColor(0.0, 1.0, 0.48)
flagpole_2_0.GetTextProperty().SetFrameColor(0.0, 1.0, 0.48)
flagpole_2_0.GetTextProperty().SetBackgroundOpacity(0.85)
flagpole_2_0.SetBasePosition(100, 450.0, 0.0)
flagpole_2_0.SetTopPosition(100, 550.0, 0.0)
flagpole_2_0.SetInput("HAlign: Left\nVAlign: Bottom")
pt_id = anchor_points.InsertNextPoint(100, 550.0, 0.0)
anchor_verts.InsertNextCell(1, [pt_id])
anchor_colors.InsertNextTuple4(191, 51, 183, 255)

# Row 2, Col 1: Left/Centered
flagpole_2_1 = vtkFlagpoleLabel()
flagpole_2_1.GetTextProperty().SetJustificationToLeft()
flagpole_2_1.GetTextProperty().SetVerticalJustificationToCentered()
flagpole_2_1.GetTextProperty().SetColor(0.75, 0.46, 0.72)
flagpole_2_1.GetTextProperty().SetBackgroundColor(0.0, 0.74, 0.48)
flagpole_2_1.GetTextProperty().SetFrameColor(0.0, 0.74, 0.48)
flagpole_2_1.GetTextProperty().SetBackgroundOpacity(0.85)
flagpole_2_1.SetBasePosition(300, 450.0, 0.0)
flagpole_2_1.SetTopPosition(300, 550.0, 0.0)
flagpole_2_1.SetInput("HAlign: Left\nVAlign: Centered")
pt_id = anchor_points.InsertNextPoint(300, 550.0, 0.0)
anchor_verts.InsertNextCell(1, [pt_id])
anchor_colors.InsertNextTuple4(191, 117, 183, 255)

# Row 2, Col 2: Left/Top
flagpole_2_2 = vtkFlagpoleLabel()
flagpole_2_2.GetTextProperty().SetJustificationToLeft()
flagpole_2_2.GetTextProperty().SetVerticalJustificationToTop()
flagpole_2_2.GetTextProperty().SetColor(0.75, 0.72, 0.72)
flagpole_2_2.GetTextProperty().SetBackgroundColor(0.0, 0.48, 0.48)
flagpole_2_2.GetTextProperty().SetFrameColor(0.0, 0.48, 0.48)
flagpole_2_2.GetTextProperty().SetBackgroundOpacity(0.85)
flagpole_2_2.SetBasePosition(500, 450.0, 0.0)
flagpole_2_2.SetTopPosition(500, 550.0, 0.0)
flagpole_2_2.SetInput("HAlign: Left\nVAlign: Top")
pt_id = anchor_points.InsertNextPoint(500, 550.0, 0.0)
anchor_verts.InsertNextCell(1, [pt_id])
anchor_colors.InsertNextTuple4(191, 183, 183, 255)

# Anchor actor
anchor_mapper = vtkPolyDataMapper()
anchor_mapper.SetInputData(anchors)
anchor_actor = vtkActor()
anchor_actor.SetMapper(anchor_mapper)
anchor_actor.GetProperty().SetPointSize(5)

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
renderer.AddActor(flagpole_0_0)
renderer.AddActor(flagpole_0_1)
renderer.AddActor(flagpole_0_2)
renderer.AddActor(flagpole_1_0)
renderer.AddActor(flagpole_1_1)
renderer.AddActor(flagpole_1_2)
renderer.AddActor(flagpole_2_0)
renderer.AddActor(flagpole_2_1)
renderer.AddActor(flagpole_2_2)
renderer.AddActor(anchor_actor)
renderer.AddActor(grid_actor)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("flagpole label")
render_window.SetMultiSamples(0)
render_window.SetSize(width, height)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.GetActiveCamera().SetPosition(width / 2, height / 2, 1400)
renderer.GetActiveCamera().SetFocalPoint(width / 2, height / 2, 0)
renderer.GetActiveCamera().SetViewUp(0, 1, 0)
renderer.GetActiveCamera().Azimuth(15.0)
renderer.GetActiveCamera().Roll(5.0)
renderer.ResetCameraClippingRange()

interactor.Initialize()
interactor.Start()
