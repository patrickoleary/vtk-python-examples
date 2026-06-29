#!/usr/bin/env python
# Demonstrate mean value coordinates interpolation on polygon cells with vtkProbeFilter.

import math

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import vtkDoubleArray, vtkPoints
from vtkmodules.vtkCommonDataModel import vtkCellArray, vtkPolyData
from vtkmodules.vtkFiltersCore import vtkProbeFilter
from vtkmodules.vtkFiltersSources import vtkPlaneSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkProperty,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Case 0: convex pentagon.
pentagon = []
for i in range(5):
    x = math.sin(math.radians(72.0 * i))
    y = math.cos(math.radians(72.0 * i))
    pentagon.append([x, y, 0.0])

pentagon_cell = vtkCellArray()
pentagon_cell.InsertNextCell(5)
for i in range(5):
    pentagon_cell.InsertCellPoint(i)

pentagon_points = vtkPoints()
for pt in pentagon:
    pentagon_points.InsertNextPoint(pt)

point_data_array = vtkDoubleArray()
for pt in pentagon:
    point_data_array.InsertNextValue((pt[0] + 1.0) / 2.0)

polydata = vtkPolyData()
polydata.SetPoints(pentagon_points)
polydata.SetPolys(pentagon_cell)
polydata.GetPointData().SetScalars(point_data_array)

# Sample on a plane.
p_source = vtkPlaneSource()
p_source.SetOrigin(-1.0, -1.0, 0)
p_source.SetPoint1(1.0, -1.0, 0)
p_source.SetPoint2(-1.0, 1.0, 0)
p_source.SetXResolution(100)
p_source.SetYResolution(100)

interp = vtkProbeFilter()
interp.SetInputConnection(p_source.GetOutputPort())
interp.SetSourceData(polydata)

interp_mapper = vtkPolyDataMapper()
interp_mapper.SetInputConnection(interp.GetOutputPort())
interp_actor = vtkActor()
interp_actor.SetMapper(interp_mapper)

# Case 1: non-convex polygon (move vertex 0 to origin).
pentagon_1 = list(pentagon)
pentagon_1[0] = [0.0, 0.0, 0.0]

pentagon_points_1 = vtkPoints()
for pt in pentagon_1:
    pentagon_points_1.InsertNextPoint(pt)

pentagon_cell_1 = vtkCellArray()
pentagon_cell_1.InsertNextCell(5)
for i in range(5):
    pentagon_cell_1.InsertCellPoint(i)

point_data_array_1 = vtkDoubleArray()
for pt in pentagon_1:
    point_data_array_1.InsertNextValue((pt[0] + 1.0) / 2.0)

polydata_1 = vtkPolyData()
polydata_1.SetPoints(pentagon_points_1)
polydata_1.SetPolys(pentagon_cell_1)
polydata_1.GetPointData().SetScalars(point_data_array_1)

p_source_1 = vtkPlaneSource()
p_source_1.SetOrigin(-1.0, -1.0, 0)
p_source_1.SetPoint1(1.0, -1.0, 0)
p_source_1.SetPoint2(-1.0, 1.0, 0)
p_source_1.SetXResolution(100)
p_source_1.SetYResolution(100)

interp_1 = vtkProbeFilter()
interp_1.SetInputConnection(p_source_1.GetOutputPort())
interp_1.SetSourceData(polydata_1)

interp_mapper_1 = vtkPolyDataMapper()
interp_mapper_1.SetInputConnection(interp_1.GetOutputPort())
interp_actor_1 = vtkActor()
interp_actor_1.SetMapper(interp_mapper_1)

# Turn off lighting.
light_property = vtkProperty()
light_property.LightingOff()
interp_actor.SetProperty(light_property)
interp_actor_1.SetProperty(light_property)

# Renderers.
renderer_0 = vtkRenderer()
renderer_0.SetViewport(0, 0, 0.5, 1)
renderer_0.AddActor(interp_actor)

renderer_1 = vtkRenderer()
renderer_1.SetViewport(0.5, 0, 1, 1)
renderer_1.AddActor(interp_actor_1)

render_window = vtkRenderWindow()
render_window.SetMultiSamples(0)
render_window.SetSize(600, 300)
render_window.AddRenderer(renderer_0)
render_window.AddRenderer(renderer_1)
render_window.SetWindowName("mean value coords polygon")

# Scene.
renderer_0.ResetCamera()
renderer_0.SetBackground(1, 1, 1)
renderer_1.ResetCamera()
renderer_1.SetBackground(1, 1, 1)

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
