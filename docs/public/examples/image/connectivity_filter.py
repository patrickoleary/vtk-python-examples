#!/usr/bin/env python

# Test vtkImageConnectivityFilter with nine different configurations on CT slices.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

import os

from vtkmodules.vtkCommonCore import vtkPoints, vtkUnsignedCharArray
from vtkmodules.vtkCommonDataModel import vtkPolyData
from vtkmodules.vtkIOImage import vtkImageReader2
from vtkmodules.vtkImagingMorphological import vtkImageConnectivityFilter
from vtkmodules.vtkInteractionStyle import vtkInteractorStyleImage
from vtkmodules.vtkRenderingCore import (
    vtkImageSlice,
    vtkImageSliceMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Read 3D CT volume (3 slices)
reader = vtkImageReader2()
reader.SetDataByteOrderToLittleEndian()
reader.SetDataExtent(0, 63, 0, 63, 2, 4)
reader.SetDataSpacing(3.2, 3.2, 1.5)
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

reader.SetFilePrefix(os.path.join(data_dir, "headsq", "quarter"))

# Create two seed points with scalar labels
seed_points = vtkPoints()
seed_points.InsertNextPoint(25.6, 100.8, 2.25)
seed_points.InsertNextPoint(100.8, 100.8, 2.25)

seed_scalars = vtkUnsignedCharArray()
seed_scalars.InsertNextValue(2)
seed_scalars.InsertNextValue(5)

seed_data = vtkPolyData()
seed_data.SetPoints(seed_points)
seed_data.GetPointData().SetScalars(seed_scalars)

# --- Pipeline 0: All regions, constant labels, generate extents ---
connectivity_0 = vtkImageConnectivityFilter()
connectivity_0.SetInputConnection(reader.GetOutputPort())
connectivity_0.GenerateRegionExtentsOn()
connectivity_0.SetScalarRange(800, 1200)
connectivity_0.UpdateExtent([0, 63, 0, 63, 3, 3])

mapper_0 = vtkImageSliceMapper()
mapper_0.SetInputConnection(connectivity_0.GetOutputPort())
mapper_0.BorderOn()
mapper_0.SliceFacesCameraOn()
mapper_0.SliceAtFocalPointOn()

actor_0 = vtkImageSlice()
actor_0.SetMapper(mapper_0)
actor_0.GetProperty().SetColorWindow(6)
actor_0.GetProperty().SetColorLevel(3)

# --- Pipeline 1: Largest region ---
connectivity_1 = vtkImageConnectivityFilter()
connectivity_1.SetInputConnection(reader.GetOutputPort())
connectivity_1.SetScalarRange(800, 1200)
connectivity_1.SetExtractionModeToLargestRegion()
connectivity_1.Update()

mapper_1 = vtkImageSliceMapper()
mapper_1.SetInputConnection(connectivity_1.GetOutputPort())
mapper_1.BorderOn()
mapper_1.SliceFacesCameraOn()
mapper_1.SliceAtFocalPointOn()

actor_1 = vtkImageSlice()
actor_1.SetMapper(mapper_1)
actor_1.GetProperty().SetColorWindow(6)
actor_1.GetProperty().SetColorLevel(3)

# --- Pipeline 2: Size range filter ---
connectivity_2 = vtkImageConnectivityFilter()
connectivity_2.SetInputConnection(reader.GetOutputPort())
connectivity_2.SetScalarRange(800, 1200)
connectivity_2.SetSizeRange(10, 99)
connectivity_2.Update()

mapper_2 = vtkImageSliceMapper()
mapper_2.SetInputConnection(connectivity_2.GetOutputPort())
mapper_2.BorderOn()
mapper_2.SliceFacesCameraOn()
mapper_2.SliceAtFocalPointOn()

actor_2 = vtkImageSlice()
actor_2.SetMapper(mapper_2)
actor_2.GetProperty().SetColorWindow(6)
actor_2.GetProperty().SetColorLevel(3)

# --- Pipeline 3: Seeded with scalar labels ---
connectivity_3 = vtkImageConnectivityFilter()
connectivity_3.SetInputConnection(reader.GetOutputPort())
connectivity_3.SetScalarRange(800, 1200)
connectivity_3.SetSeedData(seed_data)
connectivity_3.Update()

mapper_3 = vtkImageSliceMapper()
mapper_3.SetInputConnection(connectivity_3.GetOutputPort())
mapper_3.BorderOn()
mapper_3.SliceFacesCameraOn()
mapper_3.SliceAtFocalPointOn()

actor_3 = vtkImageSlice()
actor_3.SetMapper(mapper_3)
actor_3.GetProperty().SetColorWindow(6)
actor_3.GetProperty().SetColorLevel(3)

# --- Pipeline 4: All regions, size rank labels ---
connectivity_4 = vtkImageConnectivityFilter()
connectivity_4.SetInputConnection(reader.GetOutputPort())
connectivity_4.SetScalarRange(800, 1200)
connectivity_4.SetSeedData(seed_data)
connectivity_4.SetExtractionModeToAllRegions()
connectivity_4.SetLabelModeToSizeRank()
connectivity_4.Update()

mapper_4 = vtkImageSliceMapper()
mapper_4.SetInputConnection(connectivity_4.GetOutputPort())
mapper_4.BorderOn()
mapper_4.SliceFacesCameraOn()
mapper_4.SliceAtFocalPointOn()

actor_4 = vtkImageSlice()
actor_4.SetMapper(mapper_4)
actor_4.GetProperty().SetColorWindow(6)
actor_4.GetProperty().SetColorLevel(3)

# --- Pipeline 5: Seeds without scalars ---
seed_data.GetPointData().SetScalars(None)
connectivity_5 = vtkImageConnectivityFilter()
connectivity_5.SetInputConnection(reader.GetOutputPort())
connectivity_5.SetScalarRange(800, 1200)
connectivity_5.SetSeedData(seed_data)
connectivity_5.Update()

mapper_5 = vtkImageSliceMapper()
mapper_5.SetInputConnection(connectivity_5.GetOutputPort())
mapper_5.BorderOn()
mapper_5.SliceFacesCameraOn()
mapper_5.SliceAtFocalPointOn()

actor_5 = vtkImageSlice()
actor_5.SetMapper(mapper_5)
actor_5.GetProperty().SetColorWindow(6)
actor_5.GetProperty().SetColorLevel(3)

# --- Pipeline 6: Scalar range 1200-4095 ---
connectivity_6 = vtkImageConnectivityFilter()
connectivity_6.SetInputConnection(reader.GetOutputPort())
connectivity_6.SetScalarRange(1200, 4095)
connectivity_6.Update()

mapper_6 = vtkImageSliceMapper()
mapper_6.SetInputConnection(connectivity_6.GetOutputPort())
mapper_6.BorderOn()
mapper_6.SliceFacesCameraOn()
mapper_6.SliceAtFocalPointOn()

actor_6 = vtkImageSlice()
actor_6.SetMapper(mapper_6)
actor_6.GetProperty().SetColorWindow(6)
actor_6.GetProperty().SetColorLevel(3)

# --- Pipeline 7: Scalar range 0-800 ---
connectivity_7 = vtkImageConnectivityFilter()
connectivity_7.SetInputConnection(reader.GetOutputPort())
connectivity_7.SetScalarRange(0, 800)
connectivity_7.Update()

mapper_7 = vtkImageSliceMapper()
mapper_7.SetInputConnection(connectivity_7.GetOutputPort())
mapper_7.BorderOn()
mapper_7.SliceFacesCameraOn()
mapper_7.SliceAtFocalPointOn()

actor_7 = vtkImageSlice()
actor_7.SetMapper(mapper_7)
actor_7.GetProperty().SetColorWindow(6)
actor_7.GetProperty().SetColorLevel(3)

# --- Pipeline 8: Default scalar range ---
connectivity_8 = vtkImageConnectivityFilter()
connectivity_8.SetInputConnection(reader.GetOutputPort())
connectivity_8.Update()

mapper_8 = vtkImageSliceMapper()
mapper_8.SetInputConnection(connectivity_8.GetOutputPort())
mapper_8.BorderOn()
mapper_8.SliceFacesCameraOn()
mapper_8.SliceAtFocalPointOn()

actor_8 = vtkImageSlice()
actor_8.SetMapper(mapper_8)
actor_8.GetProperty().SetColorWindow(6)
actor_8.GetProperty().SetColorLevel(3)

# Renderers (3x3 grid: i=0 top-left, i=8 bottom-right)
renderer_0 = vtkRenderer()
renderer_0.SetBackground(0.0, 0.0, 0.0)
renderer_0.SetViewport(0.0, 2.0 / 3.0, 1.0 / 3.0, 1.0)
renderer_0.AddViewProp(actor_0)

renderer_1 = vtkRenderer()
renderer_1.SetBackground(0.0, 0.0, 0.0)
renderer_1.SetViewport(1.0 / 3.0, 2.0 / 3.0, 2.0 / 3.0, 1.0)
renderer_1.AddViewProp(actor_1)

renderer_2 = vtkRenderer()
renderer_2.SetBackground(0.0, 0.0, 0.0)
renderer_2.SetViewport(2.0 / 3.0, 2.0 / 3.0, 1.0, 1.0)
renderer_2.AddViewProp(actor_2)

renderer_3 = vtkRenderer()
renderer_3.SetBackground(0.0, 0.0, 0.0)
renderer_3.SetViewport(0.0, 1.0 / 3.0, 1.0 / 3.0, 2.0 / 3.0)
renderer_3.AddViewProp(actor_3)

renderer_4 = vtkRenderer()
renderer_4.SetBackground(0.0, 0.0, 0.0)
renderer_4.SetViewport(1.0 / 3.0, 1.0 / 3.0, 2.0 / 3.0, 2.0 / 3.0)
renderer_4.AddViewProp(actor_4)

renderer_5 = vtkRenderer()
renderer_5.SetBackground(0.0, 0.0, 0.0)
renderer_5.SetViewport(2.0 / 3.0, 1.0 / 3.0, 1.0, 2.0 / 3.0)
renderer_5.AddViewProp(actor_5)

renderer_6 = vtkRenderer()
renderer_6.SetBackground(0.0, 0.0, 0.0)
renderer_6.SetViewport(0.0, 0.0, 1.0 / 3.0, 1.0 / 3.0)
renderer_6.AddViewProp(actor_6)

renderer_7 = vtkRenderer()
renderer_7.SetBackground(0.0, 0.0, 0.0)
renderer_7.SetViewport(1.0 / 3.0, 0.0, 2.0 / 3.0, 1.0 / 3.0)
renderer_7.AddViewProp(actor_7)

renderer_8 = vtkRenderer()
renderer_8.SetBackground(0.0, 0.0, 0.0)
renderer_8.SetViewport(2.0 / 3.0, 0.0, 1.0, 1.0 / 3.0)
renderer_8.AddViewProp(actor_8)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer_0)
render_window.AddRenderer(renderer_1)
render_window.AddRenderer(renderer_2)
render_window.AddRenderer(renderer_3)
render_window.AddRenderer(renderer_4)
render_window.AddRenderer(renderer_5)
render_window.AddRenderer(renderer_6)
render_window.AddRenderer(renderer_7)
render_window.AddRenderer(renderer_8)
render_window.SetSize(192, 256)
render_window.SetWindowName("connectivity filter")

# Scene
focal_point = [100.8, 100.8, 5.25]

camera_0 = renderer_0.GetActiveCamera()
camera_0.SetFocalPoint(focal_point)
camera_0.SetPosition(focal_point[0], focal_point[1], focal_point[2] + 500.0)
camera_0.SetViewUp(0.0, 1.0, 0.0)
camera_0.ParallelProjectionOn()
camera_0.SetParallelScale(3.2 * 32)

camera_1 = renderer_1.GetActiveCamera()
camera_1.SetFocalPoint(focal_point)
camera_1.SetPosition(focal_point[0], focal_point[1], focal_point[2] + 500.0)
camera_1.SetViewUp(0.0, 1.0, 0.0)
camera_1.ParallelProjectionOn()
camera_1.SetParallelScale(3.2 * 32)

camera_2 = renderer_2.GetActiveCamera()
camera_2.SetFocalPoint(focal_point)
camera_2.SetPosition(focal_point[0], focal_point[1], focal_point[2] + 500.0)
camera_2.SetViewUp(0.0, 1.0, 0.0)
camera_2.ParallelProjectionOn()
camera_2.SetParallelScale(3.2 * 32)

camera_3 = renderer_3.GetActiveCamera()
camera_3.SetFocalPoint(focal_point)
camera_3.SetPosition(focal_point[0], focal_point[1], focal_point[2] + 500.0)
camera_3.SetViewUp(0.0, 1.0, 0.0)
camera_3.ParallelProjectionOn()
camera_3.SetParallelScale(3.2 * 32)

camera_4 = renderer_4.GetActiveCamera()
camera_4.SetFocalPoint(focal_point)
camera_4.SetPosition(focal_point[0], focal_point[1], focal_point[2] + 500.0)
camera_4.SetViewUp(0.0, 1.0, 0.0)
camera_4.ParallelProjectionOn()
camera_4.SetParallelScale(3.2 * 32)

camera_5 = renderer_5.GetActiveCamera()
camera_5.SetFocalPoint(focal_point)
camera_5.SetPosition(focal_point[0], focal_point[1], focal_point[2] + 500.0)
camera_5.SetViewUp(0.0, 1.0, 0.0)
camera_5.ParallelProjectionOn()
camera_5.SetParallelScale(3.2 * 32)

camera_6 = renderer_6.GetActiveCamera()
camera_6.SetFocalPoint(focal_point)
camera_6.SetPosition(focal_point[0], focal_point[1], focal_point[2] + 500.0)
camera_6.SetViewUp(0.0, 1.0, 0.0)
camera_6.ParallelProjectionOn()
camera_6.SetParallelScale(3.2 * 32)

camera_7 = renderer_7.GetActiveCamera()
camera_7.SetFocalPoint(focal_point)
camera_7.SetPosition(focal_point[0], focal_point[1], focal_point[2] + 500.0)
camera_7.SetViewUp(0.0, 1.0, 0.0)
camera_7.ParallelProjectionOn()
camera_7.SetParallelScale(3.2 * 32)

camera_8 = renderer_8.GetActiveCamera()
camera_8.SetFocalPoint(focal_point)
camera_8.SetPosition(focal_point[0], focal_point[1], focal_point[2] + 500.0)
camera_8.SetViewUp(0.0, 1.0, 0.0)
camera_8.ParallelProjectionOn()
camera_8.SetParallelScale(3.2 * 32)

style = vtkInteractorStyleImage()
style.SetInteractionModeToImageSlicing()

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)
interactor.SetInteractorStyle(style)

interactor.Initialize()
interactor.Start()
