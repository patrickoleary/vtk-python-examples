#!/usr/bin/env python

# Demonstrate multiline 2D text with various justifications using vtkTextMapper.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import vtkPoints
from vtkmodules.vtkCommonDataModel import (
    vtkCellArray,
    vtkPolyData,
)
from vtkmodules.vtkRenderingCore import (
    vtkActor2D,
    vtkCoordinate,
    vtkPolyDataMapper2D,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
    vtkTextMapper,
    vtkTextProperty,
)

font_size = 14

# Common single-line text property
single_line_text_prop = vtkTextProperty()
single_line_text_prop.SetFontSize(font_size)
single_line_text_prop.SetFontFamilyToArial()
single_line_text_prop.BoldOff()
single_line_text_prop.ItalicOff()
single_line_text_prop.ShadowOff()

# Common multi-line text property
multi_line_text_prop = vtkTextProperty()
multi_line_text_prop.ShallowCopy(single_line_text_prop)
multi_line_text_prop.BoldOn()
multi_line_text_prop.ItalicOn()
multi_line_text_prop.ShadowOn()

# Single line — bottom justified
single_line_text_b = vtkTextMapper()
single_line_text_b.SetInput("Single line (bottom)")
text_property = single_line_text_b.GetTextProperty()
text_property.ShallowCopy(single_line_text_prop)
text_property.SetVerticalJustificationToBottom()
text_property.SetColor(1, 0, 0)

single_line_text_actor_b = vtkActor2D()
single_line_text_actor_b.SetMapper(single_line_text_b)
single_line_text_actor_b.GetPositionCoordinate().SetCoordinateSystemToNormalizedDisplay()
single_line_text_actor_b.GetPositionCoordinate().SetValue(0.05, 0.85)

# Single line — centered
single_line_text_c = vtkTextMapper()
single_line_text_c.SetInput("Single line (centered)")
text_property = single_line_text_c.GetTextProperty()
text_property.ShallowCopy(single_line_text_prop)
text_property.SetVerticalJustificationToCentered()
text_property.SetColor(0, 1, 0)

single_line_text_actor_c = vtkActor2D()
single_line_text_actor_c.SetMapper(single_line_text_c)
single_line_text_actor_c.GetPositionCoordinate().SetCoordinateSystemToNormalizedDisplay()
single_line_text_actor_c.GetPositionCoordinate().SetValue(0.05, 0.75)

# Single line — top justified
single_line_text_t = vtkTextMapper()
single_line_text_t.SetInput("Single line (top)")
text_property = single_line_text_t.GetTextProperty()
text_property.ShallowCopy(single_line_text_prop)
text_property.SetVerticalJustificationToTop()
text_property.SetColor(0, 0, 1)

single_line_text_actor_t = vtkActor2D()
single_line_text_actor_t.SetMapper(single_line_text_t)
single_line_text_actor_t.GetPositionCoordinate().SetCoordinateSystemToNormalizedDisplay()
single_line_text_actor_t.GetPositionCoordinate().SetValue(0.05, 0.65)

# Single line — top below 0.5
single_line_text_tb = vtkTextMapper()
single_line_text_tb.SetInput("Single line below (top)")
text_property = single_line_text_tb.GetTextProperty()
text_property.ShallowCopy(single_line_text_prop)
text_property.SetVerticalJustificationToTop()
text_property.SetColor(0, 0, 1)

single_line_text_actor_tb = vtkActor2D()
single_line_text_actor_tb.SetMapper(single_line_text_tb)
single_line_text_actor_tb.GetPositionCoordinate().SetCoordinateSystemToNormalizedDisplay()
single_line_text_actor_tb.GetPositionCoordinate().SetValue(0.5, 0.25)

# Single line — centered with tight bounding box
single_line_text_cc = vtkTextMapper()
single_line_text_cc.SetInput("HHHHH")
text_property = single_line_text_cc.GetTextProperty()
text_property.ShallowCopy(single_line_text_prop)
text_property.SetJustificationToCentered()
text_property.SetVerticalJustificationToCentered()
text_property.UseTightBoundingBoxOn()
text_property.SetColor(0, 0, 0)

single_line_text_actor_cc = vtkActor2D()
single_line_text_actor_cc.SetMapper(single_line_text_cc)
single_line_text_actor_cc.GetPositionCoordinate().SetCoordinateSystemToNormalizedDisplay()
single_line_text_actor_cc.GetPositionCoordinate().SetValue(0.5, 0.15)

# Single line — bottom-right with tight bounding box
single_line_text_br = vtkTextMapper()
single_line_text_br.SetInput("Line bottom")
text_property = single_line_text_br.GetTextProperty()
text_property.ShallowCopy(single_line_text_prop)
text_property.SetJustificationToRight()
text_property.SetVerticalJustificationToBottom()
text_property.UseTightBoundingBoxOn()
text_property.SetColor(0, 0, 1)

single_line_text_actor_br = vtkActor2D()
single_line_text_actor_br.SetMapper(single_line_text_br)
single_line_text_actor_br.GetPositionCoordinate().SetCoordinateSystemToNormalizedDisplay()
single_line_text_actor_br.GetPositionCoordinate().SetValue(0.95, 0.15)

# Single line — bottom-left with tight bounding box
single_line_text_bl = vtkTextMapper()
single_line_text_bl.SetInput("Tight line (bottom)")
text_property = single_line_text_bl.GetTextProperty()
text_property.ShallowCopy(single_line_text_prop)
text_property.SetJustificationToLeft()
text_property.SetVerticalJustificationToBottom()
text_property.UseTightBoundingBoxOn()
text_property.SetColor(0, 0, 1)

single_line_text_actor_bl = vtkActor2D()
single_line_text_actor_bl.SetMapper(single_line_text_bl)
single_line_text_actor_bl.GetPositionCoordinate().SetCoordinateSystemToNormalizedDisplay()
single_line_text_actor_bl.GetPositionCoordinate().SetValue(0.05, 0.15)

# Single line — left-top with tight bounding box
single_line_text_ltt = vtkTextMapper()
single_line_text_ltt.SetInput("Single line (top)")
text_property = single_line_text_ltt.GetTextProperty()
text_property.ShallowCopy(single_line_text_prop)
text_property.SetVerticalJustificationToTop()
text_property.UseTightBoundingBoxOn()
text_property.SetColor(0, 0, 1)

single_line_text_actor_ltt = vtkActor2D()
single_line_text_actor_ltt.SetMapper(single_line_text_ltt)
single_line_text_actor_ltt.GetPositionCoordinate().SetCoordinateSystemToNormalizedDisplay()
single_line_text_actor_ltt.GetPositionCoordinate().SetValue(0.05, 0.15)

# Single line — right-top with tight bounding box
single_line_text_rtt = vtkTextMapper()
single_line_text_rtt.SetInput("nge ne op")
text_property = single_line_text_rtt.GetTextProperty()
text_property.ShallowCopy(single_line_text_prop)
text_property.SetJustificationToRight()
text_property.SetVerticalJustificationToTop()
text_property.UseTightBoundingBoxOn()
text_property.SetColor(0, 0, 1)

single_line_text_actor_rtt = vtkActor2D()
single_line_text_actor_rtt.SetMapper(single_line_text_rtt)
single_line_text_actor_rtt.GetPositionCoordinate().SetCoordinateSystemToNormalizedDisplay()
single_line_text_actor_rtt.GetPositionCoordinate().SetValue(0.95, 0.15)

# Multi-line — left-top justified
text_mapper_l = vtkTextMapper()
text_mapper_l.SetInput("This is\nmulti-line\ntext output\n(left-top)")
text_property = text_mapper_l.GetTextProperty()
text_property.ShallowCopy(multi_line_text_prop)
text_property.SetJustificationToLeft()
text_property.SetVerticalJustificationToTop()
text_property.SetColor(1, 0, 0)

text_actor_l = vtkActor2D()
text_actor_l.SetMapper(text_mapper_l)
text_actor_l.GetPositionCoordinate().SetCoordinateSystemToNormalizedDisplay()
text_actor_l.GetPositionCoordinate().SetValue(0.05, 0.5)

# Multi-line — left-top above 0.5
text_mapper_la = vtkTextMapper()
text_mapper_la.SetInput("This is\nmulti-line\ntext output\nabove (left-top)")
text_property = text_mapper_la.GetTextProperty()
text_property.ShallowCopy(multi_line_text_prop)
text_property.SetJustificationToLeft()
text_property.SetVerticalJustificationToTop()
text_property.SetColor(1, 0, 0)

text_actor_la = vtkActor2D()
text_actor_la.SetMapper(text_mapper_la)
text_actor_la.GetPositionCoordinate().SetCoordinateSystemToNormalizedDisplay()
text_actor_la.GetPositionCoordinate().SetValue(0.5, 0.85)

# Multi-line — centered
text_mapper_c = vtkTextMapper()
text_mapper_c.SetInput("This is\nmulti-line\ntext output\n(centered)")
text_property = text_mapper_c.GetTextProperty()
text_property.ShallowCopy(multi_line_text_prop)
text_property.SetJustificationToCentered()
text_property.SetVerticalJustificationToCentered()
text_property.SetColor(0, 1, 0)

text_actor_c = vtkActor2D()
text_actor_c.SetMapper(text_mapper_c)
text_actor_c.GetPositionCoordinate().SetCoordinateSystemToNormalizedDisplay()
text_actor_c.GetPositionCoordinate().SetValue(0.5, 0.5)

# Multi-line — right-bottom
text_mapper_r = vtkTextMapper()
text_mapper_r.SetInput("This is\nmulti-line\ntext output\n(right-bottom)")
text_property = text_mapper_r.GetTextProperty()
text_property.ShallowCopy(multi_line_text_prop)
text_property.SetJustificationToRight()
text_property.SetVerticalJustificationToBottom()
text_property.SetColor(0, 0, 1)

text_actor_r = vtkActor2D()
text_actor_r.SetMapper(text_mapper_r)
text_actor_r.GetPositionCoordinate().SetCoordinateSystemToNormalizedDisplay()
text_actor_r.GetPositionCoordinate().SetValue(0.95, 0.5)

# Grid lines for reference
pts = vtkPoints()
pts.InsertNextPoint(0.05, 0.0, 0.0)
pts.InsertNextPoint(0.05, 1.0, 0.0)
pts.InsertNextPoint(0.5, 0.0, 0.0)
pts.InsertNextPoint(0.5, 1.0, 0.0)
pts.InsertNextPoint(0.95, 0.0, 0.0)
pts.InsertNextPoint(0.95, 1.0, 0.0)
pts.InsertNextPoint(0.0, 0.5, 0.0)
pts.InsertNextPoint(1.0, 0.5, 0.0)
pts.InsertNextPoint(0.00, 0.85, 0.0)
pts.InsertNextPoint(1.00, 0.85, 0.0)
pts.InsertNextPoint(0.00, 0.75, 0.0)
pts.InsertNextPoint(0.50, 0.75, 0.0)
pts.InsertNextPoint(0.00, 0.65, 0.0)
pts.InsertNextPoint(0.50, 0.65, 0.0)
pts.InsertNextPoint(0.00, 0.25, 0.0)
pts.InsertNextPoint(1.00, 0.25, 0.0)
pts.InsertNextPoint(0.00, 0.15, 0.0)
pts.InsertNextPoint(1.00, 0.15, 0.0)

lines = vtkCellArray()
lines.InsertNextCell(2)
lines.InsertCellPoint(0)
lines.InsertCellPoint(1)
lines.InsertNextCell(2)
lines.InsertCellPoint(2)
lines.InsertCellPoint(3)
lines.InsertNextCell(2)
lines.InsertCellPoint(4)
lines.InsertCellPoint(5)
lines.InsertNextCell(2)
lines.InsertCellPoint(6)
lines.InsertCellPoint(7)
lines.InsertNextCell(2)
lines.InsertCellPoint(8)
lines.InsertCellPoint(9)
lines.InsertNextCell(2)
lines.InsertCellPoint(10)
lines.InsertCellPoint(11)
lines.InsertNextCell(2)
lines.InsertCellPoint(12)
lines.InsertCellPoint(13)
lines.InsertNextCell(2)
lines.InsertCellPoint(14)
lines.InsertCellPoint(15)
lines.InsertNextCell(2)
lines.InsertCellPoint(16)
lines.InsertCellPoint(17)

grid = vtkPolyData()
grid.SetPoints(pts)
grid.SetLines(lines)

norm_coords = vtkCoordinate()
norm_coords.SetCoordinateSystemToNormalizedDisplay()

grid_mapper = vtkPolyDataMapper2D()
grid_mapper.SetInputData(grid)
grid_mapper.SetTransformCoordinate(norm_coords)

grid_actor = vtkActor2D()
grid_actor.SetMapper(grid_mapper)
grid_actor.GetProperty().SetColor(0.1, 0.1, 0.1)

# Renderer
renderer = vtkRenderer()
renderer.AddViewProp(grid_actor)
renderer.AddViewProp(text_actor_l)
renderer.AddViewProp(single_line_text_actor_t)
renderer.AddViewProp(text_actor_la)
renderer.AddViewProp(text_actor_c)
renderer.AddViewProp(text_actor_r)
renderer.AddViewProp(single_line_text_actor_b)
renderer.AddViewProp(single_line_text_actor_c)
renderer.AddViewProp(single_line_text_actor_ltt)
renderer.AddViewProp(single_line_text_actor_rtt)
renderer.AddViewProp(single_line_text_actor_tb)
renderer.AddViewProp(single_line_text_actor_br)
renderer.AddViewProp(single_line_text_actor_bl)
renderer.AddViewProp(single_line_text_actor_cc)
renderer.SetBackground(1, 1, 1)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("multi line text free type")
render_window.SetMultiSamples(0)
render_window.SetSize(500, 300)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.GetActiveCamera().Zoom(1.5)

interactor.Initialize()
interactor.Start()
