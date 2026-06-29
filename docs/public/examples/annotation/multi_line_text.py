#!/usr/bin/env python

# Demonstrate 2D text annotation with single-line and multi-line text
# using various horizontal and vertical justification options.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
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
    vtkTextActor,
    vtkTextProperty,
)

# Colors (normalized RGB)
tomato_rgb = (1.0, 0.388, 0.278)
dark_green_rgb = (0.0, 0.392, 0.0)
peacock_rgb = (0.2, 0.631, 0.788)
dim_gray_rgb = (0.412, 0.412, 0.412)
background_rgb = (0.753, 0.753, 0.753)

font_size = 24

# Text property: shared properties for single-line labels
single_line_prop = vtkTextProperty()
single_line_prop.SetFontSize(font_size)
single_line_prop.SetFontFamilyToArial()
single_line_prop.BoldOff()
single_line_prop.ItalicOff()
single_line_prop.ShadowOff()

# Text property: shared properties for multi-line labels
multi_line_prop = vtkTextProperty()
multi_line_prop.ShallowCopy(single_line_prop)
multi_line_prop.BoldOn()
multi_line_prop.ItalicOn()
multi_line_prop.ShadowOn()
multi_line_prop.SetLineSpacing(0.8)

# Single-line text: bottom-justified
single_bottom_actor = vtkTextActor()
single_bottom_actor.SetInput("Single line (bottom)")
single_bottom_actor.GetPositionCoordinate().SetCoordinateSystemToNormalizedDisplay()
single_bottom_actor.GetPositionCoordinate().SetValue(0.05, 0.85)
tprop = single_bottom_actor.GetTextProperty()
tprop.ShallowCopy(single_line_prop)
tprop.SetVerticalJustificationToBottom()
tprop.SetColor(tomato_rgb)

# Single-line text: center-justified
single_center_actor = vtkTextActor()
single_center_actor.SetInput("Single line (centered)")
single_center_actor.GetPositionCoordinate().SetCoordinateSystemToNormalizedDisplay()
single_center_actor.GetPositionCoordinate().SetValue(0.05, 0.75)
tprop = single_center_actor.GetTextProperty()
tprop.ShallowCopy(single_line_prop)
tprop.SetVerticalJustificationToCentered()
tprop.SetColor(dark_green_rgb)

# Single-line text: top-justified
single_top_actor = vtkTextActor()
single_top_actor.SetInput("Single line (top)")
single_top_actor.GetPositionCoordinate().SetCoordinateSystemToNormalizedDisplay()
single_top_actor.GetPositionCoordinate().SetValue(0.05, 0.65)
tprop = single_top_actor.GetTextProperty()
tprop.ShallowCopy(single_line_prop)
tprop.SetVerticalJustificationToTop()
tprop.SetColor(peacock_rgb)

# Multi-line text: left-justified, top-justified
multi_left_actor = vtkTextActor()
multi_left_actor.SetInput("This is\nmulti-line\ntext output\n(left-top)")
multi_left_actor.GetPositionCoordinate().SetCoordinateSystemToNormalizedDisplay()
multi_left_actor.GetPositionCoordinate().SetValue(0.05, 0.5)
tprop = multi_left_actor.GetTextProperty()
tprop.ShallowCopy(multi_line_prop)
tprop.SetJustificationToLeft()
tprop.SetVerticalJustificationToTop()
tprop.SetColor(tomato_rgb)

# Multi-line text: center-justified
multi_center_actor = vtkTextActor()
multi_center_actor.SetInput("This is\nmulti-line\ntext output\n(centered)")
multi_center_actor.GetPositionCoordinate().SetCoordinateSystemToNormalizedDisplay()
multi_center_actor.GetPositionCoordinate().SetValue(0.5, 0.5)
tprop = multi_center_actor.GetTextProperty()
tprop.ShallowCopy(multi_line_prop)
tprop.SetJustificationToCentered()
tprop.SetVerticalJustificationToCentered()
tprop.SetColor(dark_green_rgb)

# Multi-line text: right-justified, bottom-justified
multi_right_actor = vtkTextActor()
multi_right_actor.SetInput("This is\nmulti-line\ntext output\n(right-bottom)")
multi_right_actor.GetPositionCoordinate().SetCoordinateSystemToNormalizedDisplay()
multi_right_actor.GetPositionCoordinate().SetValue(0.95, 0.5)
tprop = multi_right_actor.GetTextProperty()
tprop.ShallowCopy(multi_line_prop)
tprop.SetJustificationToRight()
tprop.SetVerticalJustificationToBottom()
tprop.SetColor(peacock_rgb)

# Grid: alignment guide lines in normalized viewport coordinates
points = vtkPoints()
points.InsertNextPoint(0.05, 0.0, 0.0)
points.InsertNextPoint(0.05, 1.0, 0.0)
points.InsertNextPoint(0.5, 0.0, 0.0)
points.InsertNextPoint(0.5, 1.0, 0.0)
points.InsertNextPoint(0.95, 0.0, 0.0)
points.InsertNextPoint(0.95, 1.0, 0.0)
points.InsertNextPoint(0.0, 0.5, 0.0)
points.InsertNextPoint(1.0, 0.5, 0.0)
points.InsertNextPoint(0.0, 0.85, 0.0)
points.InsertNextPoint(0.5, 0.85, 0.0)
points.InsertNextPoint(0.0, 0.75, 0.0)
points.InsertNextPoint(0.5, 0.75, 0.0)
points.InsertNextPoint(0.0, 0.65, 0.0)
points.InsertNextPoint(0.5, 0.65, 0.0)

lines = vtkCellArray()
for i in range(0, 14, 2):
    lines.InsertNextCell(2)
    lines.InsertCellPoint(i)
    lines.InsertCellPoint(i + 1)

grid = vtkPolyData()
grid.SetPoints(points)
grid.SetLines(lines)

norm_coords = vtkCoordinate()
norm_coords.SetCoordinateSystemToNormalizedViewport()

grid_mapper = vtkPolyDataMapper2D()
grid_mapper.SetInputData(grid)
grid_mapper.SetTransformCoordinate(norm_coords)

grid_actor = vtkActor2D()
grid_actor.SetMapper(grid_mapper)
grid_actor.GetProperty().SetColor(dim_gray_rgb)

# Renderer: assemble the scene and configure the camera
renderer = vtkRenderer()
renderer.AddViewProp(single_bottom_actor)
renderer.AddViewProp(single_center_actor)
renderer.AddViewProp(single_top_actor)
renderer.AddViewProp(multi_left_actor)
renderer.AddViewProp(multi_center_actor)
renderer.AddViewProp(multi_right_actor)
renderer.AddViewProp(grid_actor)
renderer.SetBackground(background_rgb)

# Render window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("multi line text")
render_window.SetMultiSamples(0)
render_window.SetSize(640, 480)

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Scene: configure the camera
renderer.GetActiveCamera().Zoom(1.5)

# Start: launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
