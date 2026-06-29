#!/usr/bin/env python
# Demonstrate vtkContextArea with fixed aspect ratio using DEM data and contours.

import os

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingContextOpenGL2  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkChartsCore import vtkAxis, vtkContextArea
from vtkmodules.vtkCommonCore import vtkLookupTable
from vtkmodules.vtkCommonDataModel import vtkRectd
from vtkmodules.vtkFiltersCore import vtkContourFilter, vtkStripper
from vtkmodules.vtkFiltersGeometry import vtkImageDataGeometryFilter
from vtkmodules.vtkIOImage import vtkDEMReader
from vtkmodules.vtkRenderingContext2D import vtkContextActor, vtkPropItem
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Read DEM data.
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))
dem_path = os.path.join(data_dir, "data", "SainteHelens.dem")

dem_reader = vtkDEMReader()
dem_reader.SetFileName(dem_path)
dem_reader.Update()

bounds = dem_reader.GetOutput().GetBounds()
scalar_range = dem_reader.GetOutput().GetScalarRange()

# Raw data as geometry.
image_to_pd = vtkImageDataGeometryFilter()
image_to_pd.SetInputConnection(dem_reader.GetOutputPort())

image_mapper = vtkPolyDataMapper()
image_mapper.SetInputConnection(image_to_pd.GetOutputPort())
image_mapper.SetScalarVisibility(1)

image_lut = vtkLookupTable()
image_lut.SetHueRange(0.6, 0)
image_lut.SetSaturationRange(1.0, 0.25)
image_lut.SetValueRange(0.5, 1.0)
image_mapper.SetLookupTable(image_lut)
image_mapper.SetScalarRange(scalar_range)

image_actor = vtkActor()
image_actor.SetMapper(image_mapper)

image_item = vtkPropItem()
image_item.SetPropObject(image_actor)

# Contours.
data_range = dem_reader.GetOutput().GetPointData().GetScalars().GetRange()

contours = vtkContourFilter()
contours.SetInputConnection(dem_reader.GetOutputPort())
contours.GenerateValues(21, data_range[0], data_range[1])

contour_stripper = vtkStripper()
contour_stripper.SetInputConnection(contours.GetOutputPort())

contour_mapper = vtkPolyDataMapper()
contour_mapper.SetInputConnection(contour_stripper.GetOutputPort())

contour_lut = vtkLookupTable()
contour_lut.SetHueRange(0.6, 0)
contour_lut.SetSaturationRange(0.75, 1.0)
contour_lut.SetValueRange(0.25, 0.75)
contour_mapper.SetLookupTable(contour_lut)
contour_mapper.SetScalarRange(scalar_range)

contour_actor = vtkActor()
contour_actor.SetMapper(contour_mapper)

contour_item = vtkPropItem()
contour_item.SetPropObject(contour_actor)

# Set up the context area with fixed aspect ratio.
area = vtkContextArea()
x_min, x_max, y_min, y_max = bounds[0], bounds[1], bounds[2], bounds[3]
x_len = x_max - x_min
y_len = y_max - y_min
area.SetDrawAreaBounds(vtkRectd(x_min, y_min, x_len, y_len))
area.SetFixedAspect(x_len / y_len)

area.GetAxis(vtkAxis.TOP).SetTitle("Top Axis")
area.GetAxis(vtkAxis.BOTTOM).SetTitle("Bottom Axis")
area.GetAxis(vtkAxis.LEFT).SetTitle("Left Axis")
area.GetAxis(vtkAxis.RIGHT).SetTitle("Right Axis")

for loc in (vtkAxis.LEFT, vtkAxis.BOTTOM, vtkAxis.RIGHT, vtkAxis.TOP):
    axis = area.GetAxis(loc)
    axis.GetLabelProperties().SetColor(0.6, 0.6, 0.9)
    axis.GetTitleProperties().SetColor(0.6, 0.6, 0.9)
    axis.GetPen().SetColor(153, 153, 230, 255)
    axis.GetGridPen().SetColor(153, 153, 230, 128)

area.GetDrawAreaItem().AddItem(image_item)
area.GetDrawAreaItem().AddItem(contour_item)

# Context actor and scene wiring.
context_actor = vtkContextActor()
context_actor.GetScene().AddItem(area)

# Renderer
renderer = vtkRenderer()
renderer.SetBackground(0.2, 0.2, 0.7)
context_actor.GetScene().SetRenderer(renderer)
renderer.AddActor(context_actor)

# Window
render_window = vtkRenderWindow()
render_window.SetSize(600, 600)
render_window.StencilCapableOn()
render_window.SetMultiSamples(0)
render_window.AddRenderer(renderer)
render_window.SetWindowName("context area fixed aspect")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
