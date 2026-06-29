#!/usr/bin/env python
# Demonstrate vtkDepthSortPolyData with different sort modes and directions.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersHybrid import vtkDepthSortPolyData
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkCamera,
    vtkColorTransferFunction,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Camera for depth sorting
cam = vtkCamera()
cam.SetPosition(1, 2, 0)
cam.SetFocalPoint(1, 1, 0)

# -- Sources (3x3 grid) --
# Row j=0: FIRST_POINT, Row j=1: BOUNDS_CENTER, Row j=2: PARAMETRIC_CENTER
# Col i=0: BACK_TO_FRONT, Col i=1: FRONT_TO_BACK, Col i=2: SPECIFIED_VECTOR

sphere_0_0 = vtkSphereSource()
sphere_0_0.SetThetaResolution(64)
sphere_0_0.SetPhiResolution(64)
sphere_0_0.SetRadius(0.25)
sphere_0_0.SetCenter(0, 0, 0.0)
sphere_0_0.Update()

sphere_0_1 = vtkSphereSource()
sphere_0_1.SetThetaResolution(64)
sphere_0_1.SetPhiResolution(64)
sphere_0_1.SetRadius(0.25)
sphere_0_1.SetCenter(0, 1, 0.0)
sphere_0_1.Update()

sphere_0_2 = vtkSphereSource()
sphere_0_2.SetThetaResolution(64)
sphere_0_2.SetPhiResolution(64)
sphere_0_2.SetRadius(0.25)
sphere_0_2.SetCenter(0, 2, 0.0)
sphere_0_2.Update()

sphere_1_0 = vtkSphereSource()
sphere_1_0.SetThetaResolution(64)
sphere_1_0.SetPhiResolution(64)
sphere_1_0.SetRadius(0.25)
sphere_1_0.SetCenter(1, 0, 0.0)
sphere_1_0.Update()

sphere_1_1 = vtkSphereSource()
sphere_1_1.SetThetaResolution(64)
sphere_1_1.SetPhiResolution(64)
sphere_1_1.SetRadius(0.25)
sphere_1_1.SetCenter(1, 1, 0.0)
sphere_1_1.Update()

sphere_1_2 = vtkSphereSource()
sphere_1_2.SetThetaResolution(64)
sphere_1_2.SetPhiResolution(64)
sphere_1_2.SetRadius(0.25)
sphere_1_2.SetCenter(1, 2, 0.0)
sphere_1_2.Update()

sphere_2_0 = vtkSphereSource()
sphere_2_0.SetThetaResolution(64)
sphere_2_0.SetPhiResolution(64)
sphere_2_0.SetRadius(0.25)
sphere_2_0.SetCenter(2, 0, 0.0)
sphere_2_0.Update()

sphere_2_1 = vtkSphereSource()
sphere_2_1.SetThetaResolution(64)
sphere_2_1.SetPhiResolution(64)
sphere_2_1.SetRadius(0.25)
sphere_2_1.SetCenter(2, 1, 0.0)
sphere_2_1.Update()

sphere_2_2 = vtkSphereSource()
sphere_2_2.SetThetaResolution(64)
sphere_2_2.SetPhiResolution(64)
sphere_2_2.SetRadius(0.25)
sphere_2_2.SetCenter(2, 2, 0.0)
sphere_2_2.Update()

# -- Filters --
# j=0 FIRST_POINT, i=0 BACK_TO_FRONT
depth_sort_0_0 = vtkDepthSortPolyData()
depth_sort_0_0.SetDirection(vtkDepthSortPolyData.VTK_DIRECTION_BACK_TO_FRONT)
depth_sort_0_0.SetDepthSortMode(vtkDepthSortPolyData.VTK_SORT_FIRST_POINT)
depth_sort_0_0.SortScalarsOn()
depth_sort_0_0.SetInputConnection(sphere_0_0.GetOutputPort())
depth_sort_0_0.SetCamera(cam)

# j=0 FIRST_POINT, i=1 FRONT_TO_BACK
depth_sort_0_1 = vtkDepthSortPolyData()
depth_sort_0_1.SetDirection(vtkDepthSortPolyData.VTK_DIRECTION_FRONT_TO_BACK)
depth_sort_0_1.SetDepthSortMode(vtkDepthSortPolyData.VTK_SORT_FIRST_POINT)
depth_sort_0_1.SortScalarsOn()
depth_sort_0_1.SetInputConnection(sphere_0_1.GetOutputPort())
depth_sort_0_1.SetCamera(cam)

# j=0 FIRST_POINT, i=2 SPECIFIED_VECTOR
depth_sort_0_2 = vtkDepthSortPolyData()
depth_sort_0_2.SetDirection(vtkDepthSortPolyData.VTK_DIRECTION_SPECIFIED_VECTOR)
depth_sort_0_2.SetDepthSortMode(vtkDepthSortPolyData.VTK_SORT_FIRST_POINT)
depth_sort_0_2.SortScalarsOn()
depth_sort_0_2.SetInputConnection(sphere_0_2.GetOutputPort())
depth_sort_0_2.SetOrigin(0.0, 0.0, 0.0)
depth_sort_0_2.SetVector(0.5, 0.5, 0.125)

# j=1 BOUNDS_CENTER, i=0 BACK_TO_FRONT
depth_sort_1_0 = vtkDepthSortPolyData()
depth_sort_1_0.SetDirection(vtkDepthSortPolyData.VTK_DIRECTION_BACK_TO_FRONT)
depth_sort_1_0.SetDepthSortMode(vtkDepthSortPolyData.VTK_SORT_BOUNDS_CENTER)
depth_sort_1_0.SortScalarsOn()
depth_sort_1_0.SetInputConnection(sphere_1_0.GetOutputPort())
depth_sort_1_0.SetCamera(cam)

# j=1 BOUNDS_CENTER, i=1 FRONT_TO_BACK
depth_sort_1_1 = vtkDepthSortPolyData()
depth_sort_1_1.SetDirection(vtkDepthSortPolyData.VTK_DIRECTION_FRONT_TO_BACK)
depth_sort_1_1.SetDepthSortMode(vtkDepthSortPolyData.VTK_SORT_BOUNDS_CENTER)
depth_sort_1_1.SortScalarsOn()
depth_sort_1_1.SetInputConnection(sphere_1_1.GetOutputPort())
depth_sort_1_1.SetCamera(cam)

# j=1 BOUNDS_CENTER, i=2 SPECIFIED_VECTOR
depth_sort_1_2 = vtkDepthSortPolyData()
depth_sort_1_2.SetDirection(vtkDepthSortPolyData.VTK_DIRECTION_SPECIFIED_VECTOR)
depth_sort_1_2.SetDepthSortMode(vtkDepthSortPolyData.VTK_SORT_BOUNDS_CENTER)
depth_sort_1_2.SortScalarsOn()
depth_sort_1_2.SetInputConnection(sphere_1_2.GetOutputPort())
depth_sort_1_2.SetOrigin(0.0, 0.0, 0.0)
depth_sort_1_2.SetVector(0.5, 0.5, 0.125)

# j=2 PARAMETRIC_CENTER, i=0 BACK_TO_FRONT
depth_sort_2_0 = vtkDepthSortPolyData()
depth_sort_2_0.SetDirection(vtkDepthSortPolyData.VTK_DIRECTION_BACK_TO_FRONT)
depth_sort_2_0.SetDepthSortMode(vtkDepthSortPolyData.VTK_SORT_PARAMETRIC_CENTER)
depth_sort_2_0.SortScalarsOn()
depth_sort_2_0.SetInputConnection(sphere_2_0.GetOutputPort())
depth_sort_2_0.SetCamera(cam)

# j=2 PARAMETRIC_CENTER, i=1 FRONT_TO_BACK
depth_sort_2_1 = vtkDepthSortPolyData()
depth_sort_2_1.SetDirection(vtkDepthSortPolyData.VTK_DIRECTION_FRONT_TO_BACK)
depth_sort_2_1.SetDepthSortMode(vtkDepthSortPolyData.VTK_SORT_PARAMETRIC_CENTER)
depth_sort_2_1.SortScalarsOn()
depth_sort_2_1.SetInputConnection(sphere_2_1.GetOutputPort())
depth_sort_2_1.SetCamera(cam)

# j=2 PARAMETRIC_CENTER, i=2 SPECIFIED_VECTOR
depth_sort_2_2 = vtkDepthSortPolyData()
depth_sort_2_2.SetDirection(vtkDepthSortPolyData.VTK_DIRECTION_SPECIFIED_VECTOR)
depth_sort_2_2.SetDepthSortMode(vtkDepthSortPolyData.VTK_SORT_PARAMETRIC_CENTER)
depth_sort_2_2.SortScalarsOn()
depth_sort_2_2.SetInputConnection(sphere_2_2.GetOutputPort())
depth_sort_2_2.SetOrigin(0.0, 0.0, 0.0)
depth_sort_2_2.SetVector(0.5, 0.5, 0.125)

nc = sphere_0_0.GetOutput().GetNumberOfCells()

# -- LUTs --
lut_0_0 = vtkColorTransferFunction()
lut_0_0.SetColorSpaceToRGB()
lut_0_0.AddRGBPoint(0.0, 0.0, 0.0, 1.0)
lut_0_0.AddRGBPoint(nc, 1.0, 0.0, 0.0)
lut_0_0.SetColorSpaceToDiverging()
lut_0_0.Build()

lut_0_1 = vtkColorTransferFunction()
lut_0_1.SetColorSpaceToRGB()
lut_0_1.AddRGBPoint(0.0, 0.0, 0.0, 1.0)
lut_0_1.AddRGBPoint(nc, 1.0, 0.0, 0.0)
lut_0_1.SetColorSpaceToDiverging()
lut_0_1.Build()

lut_0_2 = vtkColorTransferFunction()
lut_0_2.SetColorSpaceToRGB()
lut_0_2.AddRGBPoint(0.0, 0.0, 0.0, 1.0)
lut_0_2.AddRGBPoint(nc, 1.0, 0.0, 0.0)
lut_0_2.SetColorSpaceToDiverging()
lut_0_2.Build()

lut_1_0 = vtkColorTransferFunction()
lut_1_0.SetColorSpaceToRGB()
lut_1_0.AddRGBPoint(0.0, 0.0, 0.0, 1.0)
lut_1_0.AddRGBPoint(nc, 1.0, 0.0, 0.0)
lut_1_0.SetColorSpaceToDiverging()
lut_1_0.Build()

lut_1_1 = vtkColorTransferFunction()
lut_1_1.SetColorSpaceToRGB()
lut_1_1.AddRGBPoint(0.0, 0.0, 0.0, 1.0)
lut_1_1.AddRGBPoint(nc, 1.0, 0.0, 0.0)
lut_1_1.SetColorSpaceToDiverging()
lut_1_1.Build()

lut_1_2 = vtkColorTransferFunction()
lut_1_2.SetColorSpaceToRGB()
lut_1_2.AddRGBPoint(0.0, 0.0, 0.0, 1.0)
lut_1_2.AddRGBPoint(nc, 1.0, 0.0, 0.0)
lut_1_2.SetColorSpaceToDiverging()
lut_1_2.Build()

lut_2_0 = vtkColorTransferFunction()
lut_2_0.SetColorSpaceToRGB()
lut_2_0.AddRGBPoint(0.0, 0.0, 0.0, 1.0)
lut_2_0.AddRGBPoint(nc, 1.0, 0.0, 0.0)
lut_2_0.SetColorSpaceToDiverging()
lut_2_0.Build()

lut_2_1 = vtkColorTransferFunction()
lut_2_1.SetColorSpaceToRGB()
lut_2_1.AddRGBPoint(0.0, 0.0, 0.0, 1.0)
lut_2_1.AddRGBPoint(nc, 1.0, 0.0, 0.0)
lut_2_1.SetColorSpaceToDiverging()
lut_2_1.Build()

lut_2_2 = vtkColorTransferFunction()
lut_2_2.SetColorSpaceToRGB()
lut_2_2.AddRGBPoint(0.0, 0.0, 0.0, 1.0)
lut_2_2.AddRGBPoint(nc, 1.0, 0.0, 0.0)
lut_2_2.SetColorSpaceToDiverging()
lut_2_2.Build()

# -- Mappers --
mapper_0_0 = vtkPolyDataMapper()
mapper_0_0.SetInputConnection(depth_sort_0_0.GetOutputPort())
mapper_0_0.SetLookupTable(lut_0_0)
mapper_0_0.SetScalarVisibility(1)
mapper_0_0.SelectColorArray("sortedCellIds")
mapper_0_0.SetUseLookupTableScalarRange(1)
mapper_0_0.SetScalarModeToUseCellFieldData()

mapper_0_1 = vtkPolyDataMapper()
mapper_0_1.SetInputConnection(depth_sort_0_1.GetOutputPort())
mapper_0_1.SetLookupTable(lut_0_1)
mapper_0_1.SetScalarVisibility(1)
mapper_0_1.SelectColorArray("sortedCellIds")
mapper_0_1.SetUseLookupTableScalarRange(1)
mapper_0_1.SetScalarModeToUseCellFieldData()

mapper_0_2 = vtkPolyDataMapper()
mapper_0_2.SetInputConnection(depth_sort_0_2.GetOutputPort())
mapper_0_2.SetLookupTable(lut_0_2)
mapper_0_2.SetScalarVisibility(1)
mapper_0_2.SelectColorArray("sortedCellIds")
mapper_0_2.SetUseLookupTableScalarRange(1)
mapper_0_2.SetScalarModeToUseCellFieldData()

mapper_1_0 = vtkPolyDataMapper()
mapper_1_0.SetInputConnection(depth_sort_1_0.GetOutputPort())
mapper_1_0.SetLookupTable(lut_1_0)
mapper_1_0.SetScalarVisibility(1)
mapper_1_0.SelectColorArray("sortedCellIds")
mapper_1_0.SetUseLookupTableScalarRange(1)
mapper_1_0.SetScalarModeToUseCellFieldData()

mapper_1_1 = vtkPolyDataMapper()
mapper_1_1.SetInputConnection(depth_sort_1_1.GetOutputPort())
mapper_1_1.SetLookupTable(lut_1_1)
mapper_1_1.SetScalarVisibility(1)
mapper_1_1.SelectColorArray("sortedCellIds")
mapper_1_1.SetUseLookupTableScalarRange(1)
mapper_1_1.SetScalarModeToUseCellFieldData()

mapper_1_2 = vtkPolyDataMapper()
mapper_1_2.SetInputConnection(depth_sort_1_2.GetOutputPort())
mapper_1_2.SetLookupTable(lut_1_2)
mapper_1_2.SetScalarVisibility(1)
mapper_1_2.SelectColorArray("sortedCellIds")
mapper_1_2.SetUseLookupTableScalarRange(1)
mapper_1_2.SetScalarModeToUseCellFieldData()

mapper_2_0 = vtkPolyDataMapper()
mapper_2_0.SetInputConnection(depth_sort_2_0.GetOutputPort())
mapper_2_0.SetLookupTable(lut_2_0)
mapper_2_0.SetScalarVisibility(1)
mapper_2_0.SelectColorArray("sortedCellIds")
mapper_2_0.SetUseLookupTableScalarRange(1)
mapper_2_0.SetScalarModeToUseCellFieldData()

mapper_2_1 = vtkPolyDataMapper()
mapper_2_1.SetInputConnection(depth_sort_2_1.GetOutputPort())
mapper_2_1.SetLookupTable(lut_2_1)
mapper_2_1.SetScalarVisibility(1)
mapper_2_1.SelectColorArray("sortedCellIds")
mapper_2_1.SetUseLookupTableScalarRange(1)
mapper_2_1.SetScalarModeToUseCellFieldData()

mapper_2_2 = vtkPolyDataMapper()
mapper_2_2.SetInputConnection(depth_sort_2_2.GetOutputPort())
mapper_2_2.SetLookupTable(lut_2_2)
mapper_2_2.SetScalarVisibility(1)
mapper_2_2.SelectColorArray("sortedCellIds")
mapper_2_2.SetUseLookupTableScalarRange(1)
mapper_2_2.SetScalarModeToUseCellFieldData()

# -- Actors --
actor_0_0 = vtkActor()
actor_0_0.SetMapper(mapper_0_0)

actor_0_1 = vtkActor()
actor_0_1.SetMapper(mapper_0_1)

actor_0_2 = vtkActor()
actor_0_2.SetMapper(mapper_0_2)

actor_1_0 = vtkActor()
actor_1_0.SetMapper(mapper_1_0)

actor_1_1 = vtkActor()
actor_1_1.SetMapper(mapper_1_1)

actor_1_2 = vtkActor()
actor_1_2.SetMapper(mapper_1_2)

actor_2_0 = vtkActor()
actor_2_0.SetMapper(mapper_2_0)

actor_2_1 = vtkActor()
actor_2_1.SetMapper(mapper_2_1)

actor_2_2 = vtkActor()
actor_2_2.SetMapper(mapper_2_2)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(actor_0_0)
renderer.AddActor(actor_0_1)
renderer.AddActor(actor_0_2)
renderer.AddActor(actor_1_0)
renderer.AddActor(actor_1_1)
renderer.AddActor(actor_1_2)
renderer.AddActor(actor_2_0)
renderer.AddActor(actor_2_1)
renderer.AddActor(actor_2_2)
renderer.SetBackground(1.0, 1.0, 1.0)

# Window
render_window = vtkRenderWindow()
render_window.SetSize(400, 400)
render_window.AddRenderer(renderer)
render_window.SetWindowName("depth sort polydata")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
camera = renderer.GetActiveCamera()
camera.SetPosition(1, 1, 10)
renderer.ResetCamera()
camera.Zoom(1.25)

interactor.Initialize()
interactor.Start()
