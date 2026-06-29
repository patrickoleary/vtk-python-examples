#!/usr/bin/env python

# Demonstrate vtkConnectedPointsFilter with six extraction modes on a
# synthetic point cloud: all regions, point seeded, largest, specified,
# scalar connectivity, and scalar/normal connectivity.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import (
    vtkFloatArray,
    vtkMath,
    vtkPoints,
)
from vtkmodules.vtkCommonDataModel import vtkPolyData
from vtkmodules.vtkCommonSystem import vtkTimerLog
from vtkmodules.vtkFiltersModeling import vtkOutlineFilter
from vtkmodules.vtkFiltersPoints import vtkConnectedPointsFilter
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPointGaussianMapper,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Parameters
n_pts = 5000
math = vtkMath()
math.RandomSeed(31415)

# Create point cloud with four nearly planar regions
points = vtkPoints()
points.SetDataTypeToFloat()
points.SetNumberOfPoints(4 * n_pts + 3)
scalars = vtkFloatArray()
scalars.SetNumberOfTuples(4 * n_pts + 3)
scalars.SetName("scalars")
normals = vtkFloatArray()
normals.SetNumberOfComponents(3)
normals.SetNumberOfTuples(4 * n_pts + 3)
normals.SetName("normals")

# Region 0: lower-left
for i in range(0, n_pts):
    x = math.Random(-8.5, 0)
    y = math.Random(-8.5, -1)
    points.SetPoint(i, x, y, math.Random(-1.45, -1.4))
    if x < -4.25:
        scalars.SetValue(i, 0)
    else:
        scalars.SetValue(i, 1)
    if y < -4.25:
        normals.SetTuple3(i, 0, 0, 1)
    else:
        normals.SetTuple3(i, 0, 0, -1)

# Region 1
for i in range(n_pts, 2 * n_pts):
    points.SetPoint(i, math.Random(-2.5, 1.5), math.Random(2.5, 7.5), math.Random(-0.1, 0.1))
    scalars.SetValue(i, math.Random(1, 2))
    normals.SetTuple3(i, 0, 0, 1)

# Region 2
for i in range(2 * n_pts, 3 * n_pts):
    points.SetPoint(i, math.Random(5, 9.5), math.Random(-2.5, 2.5), math.Random(1.74, 1.75))
    scalars.SetValue(i, math.Random(2, 3))
    normals.SetTuple3(i, 0, 0, 1)

# Region 3 (largest)
for i in range(3 * n_pts, 4 * n_pts + 3):
    points.SetPoint(i, math.Random(-2, 2), math.Random(-2, 2), math.Random(0.74, 0.75))
    scalars.SetValue(i, math.Random(3, 4))
    normals.SetTuple3(i, 0, 0, 1)

polydata = vtkPolyData()
polydata.SetPoints(points)
polydata.GetPointData().SetScalars(scalars)
polydata.GetPointData().SetNormals(normals)

# --- Extract all regions ---
connected_filter_0 = vtkConnectedPointsFilter()
connected_filter_0.SetInputData(polydata)
connected_filter_0.SetExtractionModeToAllRegions()
connected_filter_0.SetRadius(0.25)

timer = vtkTimerLog()
timer.StartTimer()
connected_filter_0.Update()
timer.StopTimer()
print("Number of regions extracted: {0}".format(connected_filter_0.GetNumberOfExtractedRegions()))
print("   Time to extract all regions: {0}".format(timer.GetElapsedTime()))

connected_mapper_0 = vtkPointGaussianMapper()
connected_mapper_0.SetInputConnection(connected_filter_0.GetOutputPort())
connected_mapper_0.EmissiveOff()
connected_mapper_0.SetScaleFactor(0.0)
connected_mapper_0.SetScalarRange(connected_filter_0.GetOutput().GetScalarRange())

connected_actor_0 = vtkActor()
connected_actor_0.SetMapper(connected_mapper_0)

outline_0 = vtkOutlineFilter()
outline_0.SetInputData(polydata)
outline_mapper_0 = vtkPolyDataMapper()
outline_mapper_0.SetInputConnection(outline_0.GetOutputPort())
outline_actor_0 = vtkActor()
outline_actor_0.SetMapper(outline_mapper_0)

# --- Point seeded regions ---
connected_filter_1 = vtkConnectedPointsFilter()
connected_filter_1.SetInputData(polydata)
connected_filter_1.SetRadius(0.25)
connected_filter_1.SetExtractionModeToPointSeededRegions()
connected_filter_1.AddSeed(0)
connected_filter_1.AddSeed(2 * n_pts)

timer.StartTimer()
connected_filter_1.Update()
timer.StopTimer()
print("   Time to extract point seeded regions: {0}".format(timer.GetElapsedTime()))

connected_mapper_1 = vtkPointGaussianMapper()
connected_mapper_1.SetInputConnection(connected_filter_1.GetOutputPort())
connected_mapper_1.EmissiveOff()
connected_mapper_1.SetScaleFactor(0.0)
connected_mapper_1.SetScalarRange(connected_filter_1.GetOutput().GetScalarRange())

connected_actor_1 = vtkActor()
connected_actor_1.SetMapper(connected_mapper_1)

outline_1 = vtkOutlineFilter()
outline_1.SetInputData(polydata)
outline_mapper_1 = vtkPolyDataMapper()
outline_mapper_1.SetInputConnection(outline_1.GetOutputPort())
outline_actor_1 = vtkActor()
outline_actor_1.SetMapper(outline_mapper_1)

# --- Largest region ---
connected_filter_2 = vtkConnectedPointsFilter()
connected_filter_2.SetInputData(polydata)
connected_filter_2.SetRadius(0.25)
connected_filter_2.SetExtractionModeToLargestRegion()

timer.StartTimer()
connected_filter_2.Update()
timer.StopTimer()
print("   Time to extract largest region: {0}".format(timer.GetElapsedTime()))

connected_mapper_2 = vtkPointGaussianMapper()
connected_mapper_2.SetInputConnection(connected_filter_2.GetOutputPort())
connected_mapper_2.EmissiveOff()
connected_mapper_2.SetScaleFactor(0.0)
connected_mapper_2.SetScalarRange(connected_filter_2.GetOutput().GetScalarRange())

connected_actor_2 = vtkActor()
connected_actor_2.SetMapper(connected_mapper_2)

outline_2 = vtkOutlineFilter()
outline_2.SetInputData(polydata)
outline_mapper_2 = vtkPolyDataMapper()
outline_mapper_2.SetInputConnection(outline_2.GetOutputPort())
outline_actor_2 = vtkActor()
outline_actor_2.SetMapper(outline_mapper_2)

# --- Specified regions ---
connected_filter_3 = vtkConnectedPointsFilter()
connected_filter_3.SetInputData(polydata)
connected_filter_3.SetRadius(0.25)
connected_filter_3.SetExtractionModeToSpecifiedRegions()
connected_filter_3.AddSpecifiedRegion(1)
connected_filter_3.AddSpecifiedRegion(3)

timer.StartTimer()
connected_filter_3.Update()
timer.StopTimer()
print("   Time to extract specified regions: {0}".format(timer.GetElapsedTime()))

connected_mapper_3 = vtkPointGaussianMapper()
connected_mapper_3.SetInputConnection(connected_filter_3.GetOutputPort())
connected_mapper_3.EmissiveOff()
connected_mapper_3.SetScaleFactor(0.0)
connected_mapper_3.SetScalarRange(connected_filter_3.GetOutput().GetScalarRange())

connected_actor_3 = vtkActor()
connected_actor_3.SetMapper(connected_mapper_3)

outline_3 = vtkOutlineFilter()
outline_3.SetInputData(polydata)
outline_mapper_3 = vtkPolyDataMapper()
outline_mapper_3.SetInputConnection(outline_3.GetOutputPort())
outline_actor_3 = vtkActor()
outline_actor_3.SetMapper(outline_mapper_3)

# --- Scalar connectivity ---
connected_filter_4 = vtkConnectedPointsFilter()
connected_filter_4.SetInputData(polydata)
connected_filter_4.SetRadius(0.25)
connected_filter_4.SetExtractionModeToLargestRegion()
connected_filter_4.ScalarConnectivityOn()
connected_filter_4.SetScalarRange(0, 0.99)

timer.StartTimer()
connected_filter_4.Update()
timer.StopTimer()
print("Number of regions extracted: {0}".format(connected_filter_4.GetNumberOfExtractedRegions()))
print("   Time to extract scalar connected regions: {0}".format(timer.GetElapsedTime()))

connected_mapper_4 = vtkPointGaussianMapper()
connected_mapper_4.SetInputConnection(connected_filter_4.GetOutputPort())
connected_mapper_4.EmissiveOff()
connected_mapper_4.SetScaleFactor(0.0)
connected_mapper_4.SetScalarRange(connected_filter_4.GetOutput().GetScalarRange())

connected_actor_4 = vtkActor()
connected_actor_4.SetMapper(connected_mapper_4)

outline_4 = vtkOutlineFilter()
outline_4.SetInputData(polydata)
outline_mapper_4 = vtkPolyDataMapper()
outline_mapper_4.SetInputConnection(outline_4.GetOutputPort())
outline_actor_4 = vtkActor()
outline_actor_4.SetMapper(outline_mapper_4)

# --- Scalar + normal connectivity ---
connected_filter_5 = vtkConnectedPointsFilter()
connected_filter_5.SetInputData(polydata)
connected_filter_5.SetRadius(0.25)
connected_filter_5.SetExtractionModeToLargestRegion()
connected_filter_5.ScalarConnectivityOn()
connected_filter_5.SetScalarRange(0, 0.99)
connected_filter_5.AlignedNormalsOn()
connected_filter_5.SetNormalAngle(12.5)

timer.StartTimer()
connected_filter_5.Update()
timer.StopTimer()
print("Number of regions extracted: {0}".format(connected_filter_5.GetNumberOfExtractedRegions()))
print("   Time to extract scalar/normal connected regions: {0}".format(timer.GetElapsedTime()))

connected_mapper_5 = vtkPointGaussianMapper()
connected_mapper_5.SetInputConnection(connected_filter_5.GetOutputPort())
connected_mapper_5.EmissiveOff()
connected_mapper_5.SetScaleFactor(0.0)
connected_mapper_5.SetScalarRange(connected_filter_5.GetOutput().GetScalarRange())

connected_actor_5 = vtkActor()
connected_actor_5.SetMapper(connected_mapper_5)

outline_5 = vtkOutlineFilter()
outline_5.SetInputData(polydata)
outline_mapper_5 = vtkPolyDataMapper()
outline_mapper_5.SetInputConnection(outline_5.GetOutputPort())
outline_actor_5 = vtkActor()
outline_actor_5.SetMapper(outline_mapper_5)

# Six viewports in a 2x3 grid
renderer_0 = vtkRenderer()
renderer_0.SetViewport(0, 0, 0.5, 0.33)
renderer_0.AddActor(connected_actor_0)
renderer_0.AddActor(outline_actor_0)
renderer_0.SetBackground(0.1, 0.2, 0.4)

renderer_1 = vtkRenderer()
renderer_1.SetViewport(0.5, 0, 1, 0.33)
renderer_1.AddActor(connected_actor_1)
renderer_1.AddActor(outline_actor_1)
renderer_1.SetBackground(0.1, 0.2, 0.4)

renderer_2 = vtkRenderer()
renderer_2.SetViewport(0, 0.33, 0.5, 0.67)
renderer_2.AddActor(connected_actor_2)
renderer_2.AddActor(outline_actor_2)
renderer_2.SetBackground(0.1, 0.2, 0.4)

renderer_3 = vtkRenderer()
renderer_3.SetViewport(0.5, 0.33, 1, 0.67)
renderer_3.AddActor(connected_actor_3)
renderer_3.AddActor(outline_actor_3)
renderer_3.SetBackground(0.1, 0.2, 0.4)

renderer_4 = vtkRenderer()
renderer_4.SetViewport(0, 0.67, 0.5, 1)
renderer_4.AddActor(connected_actor_4)
renderer_4.AddActor(outline_actor_4)
renderer_4.SetBackground(0.1, 0.2, 0.4)

renderer_5 = vtkRenderer()
renderer_5.SetViewport(0.5, 0.67, 1, 1)
renderer_5.AddActor(connected_actor_5)
renderer_5.AddActor(outline_actor_5)
renderer_5.SetBackground(0.1, 0.2, 0.4)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer_0)
render_window.AddRenderer(renderer_1)
render_window.AddRenderer(renderer_2)
render_window.AddRenderer(renderer_3)
render_window.AddRenderer(renderer_4)
render_window.AddRenderer(renderer_5)
render_window.SetSize(400, 600)
render_window.SetWindowName("connected cloud")

# Scene
camera = renderer_0.GetActiveCamera()
renderer_1.SetActiveCamera(camera)
renderer_2.SetActiveCamera(camera)
renderer_3.SetActiveCamera(camera)
renderer_4.SetActiveCamera(camera)
renderer_5.SetActiveCamera(camera)
camera.SetFocalPoint(0, 0, 0)
camera.SetPosition(0.5, 0.5, 1)
renderer_0.ResetCamera()

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
