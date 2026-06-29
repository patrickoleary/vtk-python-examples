#!/usr/bin/env python

# Demonstrate vtkIconGlyphFilter with various gravity settings by reading
# a PNG icon sheet and rendering 9 rows of icons, each with a different
# gravity anchor point.

import os

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import (
    vtkDoubleArray,
    vtkIntArray,
    vtkPoints,
)
from vtkmodules.vtkCommonDataModel import vtkPolyData
from vtkmodules.vtkFiltersCore import vtkAppendPolyData
from vtkmodules.vtkFiltersGeneral import vtkIconGlyphFilter
from vtkmodules.vtkIOImage import vtkPNGReader
from vtkmodules.vtkRenderingCore import (
    vtkPolyDataMapper2D,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
    vtkTexture,
    vtkTexturedActor2D,
)

# Data directory
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Read icon sheet
image_reader = vtkPNGReader()
image_reader.SetFileName(os.path.join(data_dir, "Tango", "TangoIcons.png"))
image_reader.Update()

image_dims = list(image_reader.GetOutput().GetDimensions())
icon_size = [24, 24]

# Gravity settings: (y_position, icon_offset, gravity_method_name)
gravity_configs = [
    (26.0, 0, "SetGravityToBottomLeft"),
    (52.0, 8, "SetGravityToBottomCenter"),
    (78.0, 16, "SetGravityToBottomRight"),
    (104.0, 24, "SetGravityToCenterLeft"),
    (130.0, 32, "SetGravityToCenterCenter"),
    (156.0, 40, "SetGravityToCenterRight"),
    (182.0, 48, "SetGravityToTopLeft"),
    (208.0, 56, "SetGravityToTopCenter"),
    (234.0, 64, "SetGravityToTopRight"),
]

# Build icon filters for each gravity setting
append = vtkAppendPolyData()

point_data_arr_0 = vtkDoubleArray()
point_data_arr_0.SetNumberOfComponents(3)
pts_0 = vtkPoints()
pts_0.SetData(point_data_arr_0)
point_set_0 = vtkPolyData()
point_set_0.SetPoints(pts_0)
icon_index_0 = vtkIntArray()
icon_index_0.SetNumberOfComponents(1)
point_set_0.GetPointData().SetScalars(icon_index_0)
for i in range(1, 8):
    pts_0.InsertNextPoint(i * 26.0, 26.0, 0.0)
for i in range(pts_0.GetNumberOfPoints()):
    icon_index_0.InsertNextTuple1(i + 0)
icon_filter_0 = vtkIconGlyphFilter()
icon_filter_0.SetInputData(point_set_0)
icon_filter_0.SetIconSize(icon_size[0], icon_size[1])
icon_filter_0.SetUseIconSize(True)
icon_filter_0.SetIconSheetSize(image_dims[0], image_dims[1])
icon_filter_0.SetGravityToBottomLeft()
append.AddInputConnection(icon_filter_0.GetOutputPort())

point_data_arr_1 = vtkDoubleArray()
point_data_arr_1.SetNumberOfComponents(3)
pts_1 = vtkPoints()
pts_1.SetData(point_data_arr_1)
point_set_1 = vtkPolyData()
point_set_1.SetPoints(pts_1)
icon_index_1 = vtkIntArray()
icon_index_1.SetNumberOfComponents(1)
point_set_1.GetPointData().SetScalars(icon_index_1)
for i in range(1, 8):
    pts_1.InsertNextPoint(i * 26.0, 52.0, 0.0)
for i in range(pts_1.GetNumberOfPoints()):
    icon_index_1.InsertNextTuple1(i + 8)
icon_filter_1 = vtkIconGlyphFilter()
icon_filter_1.SetInputData(point_set_1)
icon_filter_1.SetIconSize(icon_size[0], icon_size[1])
icon_filter_1.SetUseIconSize(True)
icon_filter_1.SetIconSheetSize(image_dims[0], image_dims[1])
icon_filter_1.SetGravityToBottomCenter()
append.AddInputConnection(icon_filter_1.GetOutputPort())

point_data_arr_2 = vtkDoubleArray()
point_data_arr_2.SetNumberOfComponents(3)
pts_2 = vtkPoints()
pts_2.SetData(point_data_arr_2)
point_set_2 = vtkPolyData()
point_set_2.SetPoints(pts_2)
icon_index_2 = vtkIntArray()
icon_index_2.SetNumberOfComponents(1)
point_set_2.GetPointData().SetScalars(icon_index_2)
for i in range(1, 8):
    pts_2.InsertNextPoint(i * 26.0, 78.0, 0.0)
for i in range(pts_2.GetNumberOfPoints()):
    icon_index_2.InsertNextTuple1(i + 16)
icon_filter_2 = vtkIconGlyphFilter()
icon_filter_2.SetInputData(point_set_2)
icon_filter_2.SetIconSize(icon_size[0], icon_size[1])
icon_filter_2.SetUseIconSize(True)
icon_filter_2.SetIconSheetSize(image_dims[0], image_dims[1])
icon_filter_2.SetGravityToBottomRight()
append.AddInputConnection(icon_filter_2.GetOutputPort())

point_data_arr_3 = vtkDoubleArray()
point_data_arr_3.SetNumberOfComponents(3)
pts_3 = vtkPoints()
pts_3.SetData(point_data_arr_3)
point_set_3 = vtkPolyData()
point_set_3.SetPoints(pts_3)
icon_index_3 = vtkIntArray()
icon_index_3.SetNumberOfComponents(1)
point_set_3.GetPointData().SetScalars(icon_index_3)
for i in range(1, 8):
    pts_3.InsertNextPoint(i * 26.0, 104.0, 0.0)
for i in range(pts_3.GetNumberOfPoints()):
    icon_index_3.InsertNextTuple1(i + 24)
icon_filter_3 = vtkIconGlyphFilter()
icon_filter_3.SetInputData(point_set_3)
icon_filter_3.SetIconSize(icon_size[0], icon_size[1])
icon_filter_3.SetUseIconSize(True)
icon_filter_3.SetIconSheetSize(image_dims[0], image_dims[1])
icon_filter_3.SetGravityToCenterLeft()
append.AddInputConnection(icon_filter_3.GetOutputPort())

point_data_arr_4 = vtkDoubleArray()
point_data_arr_4.SetNumberOfComponents(3)
pts_4 = vtkPoints()
pts_4.SetData(point_data_arr_4)
point_set_4 = vtkPolyData()
point_set_4.SetPoints(pts_4)
icon_index_4 = vtkIntArray()
icon_index_4.SetNumberOfComponents(1)
point_set_4.GetPointData().SetScalars(icon_index_4)
for i in range(1, 8):
    pts_4.InsertNextPoint(i * 26.0, 130.0, 0.0)
for i in range(pts_4.GetNumberOfPoints()):
    icon_index_4.InsertNextTuple1(i + 32)
icon_filter_4 = vtkIconGlyphFilter()
icon_filter_4.SetInputData(point_set_4)
icon_filter_4.SetIconSize(icon_size[0], icon_size[1])
icon_filter_4.SetUseIconSize(True)
icon_filter_4.SetIconSheetSize(image_dims[0], image_dims[1])
icon_filter_4.SetGravityToCenterCenter()
append.AddInputConnection(icon_filter_4.GetOutputPort())

point_data_arr_5 = vtkDoubleArray()
point_data_arr_5.SetNumberOfComponents(3)
pts_5 = vtkPoints()
pts_5.SetData(point_data_arr_5)
point_set_5 = vtkPolyData()
point_set_5.SetPoints(pts_5)
icon_index_5 = vtkIntArray()
icon_index_5.SetNumberOfComponents(1)
point_set_5.GetPointData().SetScalars(icon_index_5)
for i in range(1, 8):
    pts_5.InsertNextPoint(i * 26.0, 156.0, 0.0)
for i in range(pts_5.GetNumberOfPoints()):
    icon_index_5.InsertNextTuple1(i + 40)
icon_filter_5 = vtkIconGlyphFilter()
icon_filter_5.SetInputData(point_set_5)
icon_filter_5.SetIconSize(icon_size[0], icon_size[1])
icon_filter_5.SetUseIconSize(True)
icon_filter_5.SetIconSheetSize(image_dims[0], image_dims[1])
icon_filter_5.SetGravityToCenterRight()
append.AddInputConnection(icon_filter_5.GetOutputPort())

point_data_arr_6 = vtkDoubleArray()
point_data_arr_6.SetNumberOfComponents(3)
pts_6 = vtkPoints()
pts_6.SetData(point_data_arr_6)
point_set_6 = vtkPolyData()
point_set_6.SetPoints(pts_6)
icon_index_6 = vtkIntArray()
icon_index_6.SetNumberOfComponents(1)
point_set_6.GetPointData().SetScalars(icon_index_6)
for i in range(1, 8):
    pts_6.InsertNextPoint(i * 26.0, 182.0, 0.0)
for i in range(pts_6.GetNumberOfPoints()):
    icon_index_6.InsertNextTuple1(i + 48)
icon_filter_6 = vtkIconGlyphFilter()
icon_filter_6.SetInputData(point_set_6)
icon_filter_6.SetIconSize(icon_size[0], icon_size[1])
icon_filter_6.SetUseIconSize(True)
icon_filter_6.SetIconSheetSize(image_dims[0], image_dims[1])
icon_filter_6.SetGravityToTopLeft()
append.AddInputConnection(icon_filter_6.GetOutputPort())

point_data_arr_7 = vtkDoubleArray()
point_data_arr_7.SetNumberOfComponents(3)
pts_7 = vtkPoints()
pts_7.SetData(point_data_arr_7)
point_set_7 = vtkPolyData()
point_set_7.SetPoints(pts_7)
icon_index_7 = vtkIntArray()
icon_index_7.SetNumberOfComponents(1)
point_set_7.GetPointData().SetScalars(icon_index_7)
for i in range(1, 8):
    pts_7.InsertNextPoint(i * 26.0, 208.0, 0.0)
for i in range(pts_7.GetNumberOfPoints()):
    icon_index_7.InsertNextTuple1(i + 56)
icon_filter_7 = vtkIconGlyphFilter()
icon_filter_7.SetInputData(point_set_7)
icon_filter_7.SetIconSize(icon_size[0], icon_size[1])
icon_filter_7.SetUseIconSize(True)
icon_filter_7.SetIconSheetSize(image_dims[0], image_dims[1])
icon_filter_7.SetGravityToTopCenter()
append.AddInputConnection(icon_filter_7.GetOutputPort())

point_data_arr_8 = vtkDoubleArray()
point_data_arr_8.SetNumberOfComponents(3)
pts_8 = vtkPoints()
pts_8.SetData(point_data_arr_8)
point_set_8 = vtkPolyData()
point_set_8.SetPoints(pts_8)
icon_index_8 = vtkIntArray()
icon_index_8.SetNumberOfComponents(1)
point_set_8.GetPointData().SetScalars(icon_index_8)
for i in range(1, 8):
    pts_8.InsertNextPoint(i * 26.0, 234.0, 0.0)
for i in range(pts_8.GetNumberOfPoints()):
    icon_index_8.InsertNextTuple1(i + 64)
icon_filter_8 = vtkIconGlyphFilter()
icon_filter_8.SetInputData(point_set_8)
icon_filter_8.SetIconSize(icon_size[0], icon_size[1])
icon_filter_8.SetUseIconSize(True)
icon_filter_8.SetIconSheetSize(image_dims[0], image_dims[1])
icon_filter_8.SetGravityToTopRight()
append.AddInputConnection(icon_filter_8.GetOutputPort())

# 2D mapper and textured actor
mapper = vtkPolyDataMapper2D()
mapper.SetInputConnection(append.GetOutputPort())

texture = vtkTexture()
texture.SetInputConnection(image_reader.GetOutputPort())

icon_actor = vtkTexturedActor2D()
icon_actor.SetMapper(mapper)
icon_actor.SetTexture(texture)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(icon_actor)

# Window
render_window = vtkRenderWindow()
render_window.SetSize(208, 260)
render_window.AddRenderer(renderer)
render_window.SetWindowName("icon glyph gravity")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
