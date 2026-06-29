#!/usr/bin/env python

# Test vtkPolyDataItem rendering polydata into a context scene with contours.

import os

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
import vtkmodules.vtkRenderingContextOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import VTK_COLOR_MODE_DEFAULT
from vtkmodules.vtkCommonDataModel import vtkRectd
from vtkmodules.vtkFiltersCore import vtkFeatureEdges, vtkPolyDataConnectivityFilter
from vtkmodules.vtkFiltersModeling import vtkBandedPolyDataContourFilter
from vtkmodules.vtkIOXML import vtkXMLPolyDataReader
from vtkmodules.vtkChartsCore import vtkAxis, vtkInteractiveArea
from vtkmodules.vtkRenderingContext2D import (
    vtkContextActor,
    vtkPolyDataItem,
)
from vtkmodules.vtkRenderingCore import (
    VTK_SCALAR_MODE_USE_CELL_DATA,
    VTK_SCALAR_MODE_USE_POINT_DATA,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Read polydata
reader = vtkXMLPolyDataReader()
reader.SetFileName(os.path.join(data_dir, "isofill_0.vtp"))
reader.Update()
poly = reader.GetOutput()

# Create map item from point data
scalar_mode_map = VTK_SCALAR_MODE_USE_POINT_DATA
active_data_map = poly.GetPointData().GetScalars()
range_map = [0.0, 0.0]
active_data_map.GetRange(range_map, 0)

color_lut_map = active_data_map.GetLookupTable()
if not color_lut_map:
    active_data_map.CreateDefaultLookupTable()
    color_lut_map = active_data_map.GetLookupTable()
    color_lut_map.SetAlpha(1.0)
    color_lut_map.SetRange(range_map[0], range_map[1])

mapped_colors_map = color_lut_map.MapScalars(active_data_map, VTK_COLOR_MODE_DEFAULT, 0)

map_item = vtkPolyDataItem()
map_item.SetPolyData(poly)
map_item.SetScalarMode(scalar_mode_map)
map_item.SetMappedColors(mapped_colors_map)

# Create contour item
contour = vtkBandedPolyDataContourFilter()
contour.SetInputConnection(reader.GetOutputPort())
contour.GenerateValues(20, 6, 40)
contour.ClippingOn()
contour.SetClipTolerance(0.0)
contour.Update()

connectivity = vtkPolyDataConnectivityFilter()
connectivity.SetInputConnection(contour.GetOutputPort())
connectivity.SetExtractionModeToAllRegions()
connectivity.ColorRegionsOn()
connectivity.Update()

extract = vtkPolyDataConnectivityFilter()
extract.SetInputConnection(connectivity.GetOutputPort())
extract.ScalarConnectivityOn()
extract.SetScalarRange(6, 58)

edge = vtkFeatureEdges()
edge.SetInputConnection(extract.GetOutputPort())
edge.BoundaryEdgesOn()
edge.FeatureEdgesOff()
edge.ManifoldEdgesOff()
edge.NonManifoldEdgesOff()
edge.Update()

contour_poly = edge.GetOutput()
scalar_mode_contour = VTK_SCALAR_MODE_USE_CELL_DATA
active_data_contour = contour_poly.GetCellData().GetScalars()
range_contour = [0.0, 0.0]
active_data_contour.GetRange(range_contour, 0)

color_lut_contour = active_data_contour.GetLookupTable()
if not color_lut_contour:
    active_data_contour.CreateDefaultLookupTable()
    color_lut_contour = active_data_contour.GetLookupTable()
    color_lut_contour.SetAlpha(1.0)
    color_lut_contour.SetRange(range_contour[0], range_contour[1])

mapped_colors_contour = color_lut_contour.MapScalars(active_data_contour, VTK_COLOR_MODE_DEFAULT, 0)

contour_item = vtkPolyDataItem()
contour_item.SetPolyData(contour_poly)
contour_item.SetScalarMode(scalar_mode_contour)
contour_item.SetMappedColors(mapped_colors_contour)

# Interactive area
area = vtkInteractiveArea()
area.GetDrawAreaItem().AddItem(map_item)
area.GetDrawAreaItem().AddItem(contour_item)

bounds = map_item.GetPolyData().GetBounds()
x_min, x_max, y_min, y_max = bounds[0], bounds[1], bounds[2], bounds[3]
x_len = x_max - x_min
y_len = y_max - y_min
area.SetDrawAreaBounds(vtkRectd(x_min, y_min, x_len, y_len))
area.SetFixedAspect(x_len / y_len)

area.GetAxis(vtkAxis.BOTTOM).SetTitle("X Axis")
area.GetAxis(vtkAxis.LEFT).SetTitle("Y Axis")
area.GetAxis(vtkAxis.TOP).SetVisible(False)
area.GetAxis(vtkAxis.RIGHT).SetVisible(False)

for loc in [vtkAxis.LEFT, vtkAxis.BOTTOM, vtkAxis.RIGHT, vtkAxis.TOP]:
    axis = area.GetAxis(loc)
    axis.GetLabelProperties().SetColor(0.6, 0.6, 0.9)
    axis.GetTitleProperties().SetColor(0.6, 0.6, 0.9)
    axis.GetPen().SetColor(int(0.6 * 255), int(0.6 * 255), int(0.9 * 255), 255)
    axis.GetGridPen().SetColor(int(0.6 * 255), int(0.6 * 255), int(0.9 * 255), 128)

# Renderer
renderer = vtkRenderer()
renderer.SetBackground(0.3, 0.3, 0.3)

# Context actor
context_actor = vtkContextActor()
scene = context_actor.GetScene()
scene.SetRenderer(renderer)
scene.SetUseBufferId(False)
scene.AddItem(area)
renderer.AddActor(context_actor)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("polydata to context")
render_window.SetMultiSamples(0)
render_window.SetSize(600, 400)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
