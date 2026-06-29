#!/usr/bin/env python

# Test vtkImageThresholdConnectivity with 12 configurations on CT slices.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

import os

from vtkmodules.vtkCommonCore import vtkPoints
from vtkmodules.vtkIOImage import vtkImageReader2
from vtkmodules.vtkImagingMorphological import vtkImageThresholdConnectivity
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

# Seed points
seeds = vtkPoints()
seeds.InsertNextPoint(1, 1, 5.25)
seeds.InsertNextPoint(100.8, 100.8, 5.25)

# --- Pipeline 0: i=0, j=0, k=0 — Lower(800), ReplaceIn=True, ReplaceOut=True ---
connectivity_0 = vtkImageThresholdConnectivity()
connectivity_0.SetInputConnection(reader.GetOutputPort())
connectivity_0.SetSeedPoints(seeds)
connectivity_0.SetInValue(2000)
connectivity_0.SetOutValue(0)
connectivity_0.SetReplaceIn(True)
connectivity_0.SetReplaceOut(True)
connectivity_0.ThresholdByLower(800)
connectivity_0.UpdateExtent([0, 63, 0, 63, 3, 3])

mapper_0 = vtkImageSliceMapper()
mapper_0.SetInputConnection(connectivity_0.GetOutputPort())
mapper_0.BorderOn()
mapper_0.SliceFacesCameraOn()
mapper_0.SliceAtFocalPointOn()

actor_0 = vtkImageSlice()
actor_0.SetMapper(mapper_0)
actor_0.GetProperty().SetColorWindow(2000)
actor_0.GetProperty().SetColorLevel(1000)

# --- Pipeline 1: i=1, j=1, k=0 — Lower(800), ReplaceIn=True, ReplaceOut=False ---
connectivity_1 = vtkImageThresholdConnectivity()
connectivity_1.SetInputConnection(reader.GetOutputPort())
connectivity_1.SetSeedPoints(seeds)
connectivity_1.SetInValue(2000)
connectivity_1.SetOutValue(0)
connectivity_1.SetReplaceIn(True)
connectivity_1.SetReplaceOut(False)
connectivity_1.ThresholdByLower(800)
connectivity_1.UpdateExtent([0, 63, 0, 63, 3, 3])

mapper_1 = vtkImageSliceMapper()
mapper_1.SetInputConnection(connectivity_1.GetOutputPort())
mapper_1.BorderOn()
mapper_1.SliceFacesCameraOn()
mapper_1.SliceAtFocalPointOn()

actor_1 = vtkImageSlice()
actor_1.SetMapper(mapper_1)
actor_1.GetProperty().SetColorWindow(2000)
actor_1.GetProperty().SetColorLevel(1000)

# --- Pipeline 2: i=2, j=2, k=0 — Lower(800), ReplaceIn=False, ReplaceOut=True ---
connectivity_2 = vtkImageThresholdConnectivity()
connectivity_2.SetInputConnection(reader.GetOutputPort())
connectivity_2.SetSeedPoints(seeds)
connectivity_2.SetInValue(2000)
connectivity_2.SetOutValue(0)
connectivity_2.SetReplaceIn(False)
connectivity_2.SetReplaceOut(True)
connectivity_2.ThresholdByLower(800)
connectivity_2.UpdateExtent([0, 63, 0, 63, 3, 3])

mapper_2 = vtkImageSliceMapper()
mapper_2.SetInputConnection(connectivity_2.GetOutputPort())
mapper_2.BorderOn()
mapper_2.SliceFacesCameraOn()
mapper_2.SliceAtFocalPointOn()

actor_2 = vtkImageSlice()
actor_2.SetMapper(mapper_2)
actor_2.GetProperty().SetColorWindow(2000)
actor_2.GetProperty().SetColorLevel(1000)

# --- Pipeline 3: i=3, j=3, k=0 — Lower(800), ReplaceIn=False, ReplaceOut=False ---
connectivity_3 = vtkImageThresholdConnectivity()
connectivity_3.SetInputConnection(reader.GetOutputPort())
connectivity_3.SetSeedPoints(seeds)
connectivity_3.SetInValue(2000)
connectivity_3.SetOutValue(0)
connectivity_3.SetReplaceIn(False)
connectivity_3.SetReplaceOut(False)
connectivity_3.ThresholdByLower(800)
connectivity_3.UpdateExtent([0, 63, 0, 63, 3, 3])

mapper_3 = vtkImageSliceMapper()
mapper_3.SetInputConnection(connectivity_3.GetOutputPort())
mapper_3.BorderOn()
mapper_3.SliceFacesCameraOn()
mapper_3.SliceAtFocalPointOn()

actor_3 = vtkImageSlice()
actor_3.SetMapper(mapper_3)
actor_3.GetProperty().SetColorWindow(2000)
actor_3.GetProperty().SetColorLevel(1000)

# --- Pipeline 4: i=4, j=0, k=1 — Upper(1200), ReplaceIn=True, ReplaceOut=True ---
connectivity_4 = vtkImageThresholdConnectivity()
connectivity_4.SetInputConnection(reader.GetOutputPort())
connectivity_4.SetSeedPoints(seeds)
connectivity_4.SetInValue(2000)
connectivity_4.SetOutValue(0)
connectivity_4.SetReplaceIn(True)
connectivity_4.SetReplaceOut(True)
connectivity_4.ThresholdByUpper(1200)
connectivity_4.UpdateExtent([0, 63, 0, 63, 3, 3])

mapper_4 = vtkImageSliceMapper()
mapper_4.SetInputConnection(connectivity_4.GetOutputPort())
mapper_4.BorderOn()
mapper_4.SliceFacesCameraOn()
mapper_4.SliceAtFocalPointOn()

actor_4 = vtkImageSlice()
actor_4.SetMapper(mapper_4)
actor_4.GetProperty().SetColorWindow(2000)
actor_4.GetProperty().SetColorLevel(1000)

# --- Pipeline 5: i=5, j=1, k=1 — Upper(1200), ReplaceIn=True, ReplaceOut=False ---
connectivity_5 = vtkImageThresholdConnectivity()
connectivity_5.SetInputConnection(reader.GetOutputPort())
connectivity_5.SetSeedPoints(seeds)
connectivity_5.SetInValue(2000)
connectivity_5.SetOutValue(0)
connectivity_5.SetReplaceIn(True)
connectivity_5.SetReplaceOut(False)
connectivity_5.ThresholdByUpper(1200)
connectivity_5.UpdateExtent([0, 63, 0, 63, 3, 3])

mapper_5 = vtkImageSliceMapper()
mapper_5.SetInputConnection(connectivity_5.GetOutputPort())
mapper_5.BorderOn()
mapper_5.SliceFacesCameraOn()
mapper_5.SliceAtFocalPointOn()

actor_5 = vtkImageSlice()
actor_5.SetMapper(mapper_5)
actor_5.GetProperty().SetColorWindow(2000)
actor_5.GetProperty().SetColorLevel(1000)

# --- Pipeline 6: i=6, j=2, k=1 — Upper(1200), ReplaceIn=False, ReplaceOut=True ---
connectivity_6 = vtkImageThresholdConnectivity()
connectivity_6.SetInputConnection(reader.GetOutputPort())
connectivity_6.SetSeedPoints(seeds)
connectivity_6.SetInValue(2000)
connectivity_6.SetOutValue(0)
connectivity_6.SetReplaceIn(False)
connectivity_6.SetReplaceOut(True)
connectivity_6.ThresholdByUpper(1200)
connectivity_6.UpdateExtent([0, 63, 0, 63, 3, 3])

mapper_6 = vtkImageSliceMapper()
mapper_6.SetInputConnection(connectivity_6.GetOutputPort())
mapper_6.BorderOn()
mapper_6.SliceFacesCameraOn()
mapper_6.SliceAtFocalPointOn()

actor_6 = vtkImageSlice()
actor_6.SetMapper(mapper_6)
actor_6.GetProperty().SetColorWindow(2000)
actor_6.GetProperty().SetColorLevel(1000)

# --- Pipeline 7: i=7, j=3, k=1 — Upper(1200), ReplaceIn=False, ReplaceOut=False ---
connectivity_7 = vtkImageThresholdConnectivity()
connectivity_7.SetInputConnection(reader.GetOutputPort())
connectivity_7.SetSeedPoints(seeds)
connectivity_7.SetInValue(2000)
connectivity_7.SetOutValue(0)
connectivity_7.SetReplaceIn(False)
connectivity_7.SetReplaceOut(False)
connectivity_7.ThresholdByUpper(1200)
connectivity_7.UpdateExtent([0, 63, 0, 63, 3, 3])

mapper_7 = vtkImageSliceMapper()
mapper_7.SetInputConnection(connectivity_7.GetOutputPort())
mapper_7.BorderOn()
mapper_7.SliceFacesCameraOn()
mapper_7.SliceAtFocalPointOn()

actor_7 = vtkImageSlice()
actor_7.SetMapper(mapper_7)
actor_7.GetProperty().SetColorWindow(2000)
actor_7.GetProperty().SetColorLevel(1000)

# --- Pipeline 8: i=8, j=0, k=2 — Between(800,1200), ReplaceIn=True, ReplaceOut=True ---
connectivity_8 = vtkImageThresholdConnectivity()
connectivity_8.SetInputConnection(reader.GetOutputPort())
connectivity_8.SetSeedPoints(seeds)
connectivity_8.SetInValue(2000)
connectivity_8.SetOutValue(0)
connectivity_8.SetReplaceIn(True)
connectivity_8.SetReplaceOut(True)
connectivity_8.ThresholdBetween(800, 1200)
connectivity_8.UpdateExtent([0, 63, 0, 63, 3, 3])

mapper_8 = vtkImageSliceMapper()
mapper_8.SetInputConnection(connectivity_8.GetOutputPort())
mapper_8.BorderOn()
mapper_8.SliceFacesCameraOn()
mapper_8.SliceAtFocalPointOn()

actor_8 = vtkImageSlice()
actor_8.SetMapper(mapper_8)
actor_8.GetProperty().SetColorWindow(2000)
actor_8.GetProperty().SetColorLevel(1000)

# --- Pipeline 9: i=9, j=1, k=2 — Between(800,1200), ReplaceIn=True, ReplaceOut=False ---
connectivity_9 = vtkImageThresholdConnectivity()
connectivity_9.SetInputConnection(reader.GetOutputPort())
connectivity_9.SetSeedPoints(seeds)
connectivity_9.SetInValue(2000)
connectivity_9.SetOutValue(0)
connectivity_9.SetReplaceIn(True)
connectivity_9.SetReplaceOut(False)
connectivity_9.ThresholdBetween(800, 1200)
connectivity_9.UpdateExtent([0, 63, 0, 63, 3, 3])

mapper_9 = vtkImageSliceMapper()
mapper_9.SetInputConnection(connectivity_9.GetOutputPort())
mapper_9.BorderOn()
mapper_9.SliceFacesCameraOn()
mapper_9.SliceAtFocalPointOn()

actor_9 = vtkImageSlice()
actor_9.SetMapper(mapper_9)
actor_9.GetProperty().SetColorWindow(2000)
actor_9.GetProperty().SetColorLevel(1000)

# --- Pipeline 10: i=10, j=2, k=2 — Between(800,1200), ReplaceIn=False, ReplaceOut=True ---
connectivity_10 = vtkImageThresholdConnectivity()
connectivity_10.SetInputConnection(reader.GetOutputPort())
connectivity_10.SetSeedPoints(seeds)
connectivity_10.SetInValue(2000)
connectivity_10.SetOutValue(0)
connectivity_10.SetReplaceIn(False)
connectivity_10.SetReplaceOut(True)
connectivity_10.ThresholdBetween(800, 1200)
connectivity_10.UpdateExtent([0, 63, 0, 63, 3, 3])

mapper_10 = vtkImageSliceMapper()
mapper_10.SetInputConnection(connectivity_10.GetOutputPort())
mapper_10.BorderOn()
mapper_10.SliceFacesCameraOn()
mapper_10.SliceAtFocalPointOn()

actor_10 = vtkImageSlice()
actor_10.SetMapper(mapper_10)
actor_10.GetProperty().SetColorWindow(2000)
actor_10.GetProperty().SetColorLevel(1000)

# --- Pipeline 11: i=11, j=3, k=2 — Between(800,1200), ReplaceIn=False, ReplaceOut=False ---
connectivity_11 = vtkImageThresholdConnectivity()
connectivity_11.SetInputConnection(reader.GetOutputPort())
connectivity_11.SetSeedPoints(seeds)
connectivity_11.SetInValue(2000)
connectivity_11.SetOutValue(0)
connectivity_11.SetReplaceIn(False)
connectivity_11.SetReplaceOut(False)
connectivity_11.ThresholdBetween(800, 1200)
connectivity_11.UpdateExtent([0, 63, 0, 63, 3, 3])

mapper_11 = vtkImageSliceMapper()
mapper_11.SetInputConnection(connectivity_11.GetOutputPort())
mapper_11.BorderOn()
mapper_11.SliceFacesCameraOn()
mapper_11.SliceAtFocalPointOn()

actor_11 = vtkImageSlice()
actor_11.SetMapper(mapper_11)
actor_11.GetProperty().SetColorWindow(2000)
actor_11.GetProperty().SetColorLevel(1000)

# Renderers (3x4 grid: k=col, j=row)
renderer_0 = vtkRenderer()
renderer_0.SetBackground(0.0, 0.0, 0.0)
renderer_0.SetViewport(0.0, 0.0, 1.0 / 3.0, 1.0 / 4.0)
renderer_0.AddViewProp(actor_0)

renderer_1 = vtkRenderer()
renderer_1.SetBackground(0.0, 0.0, 0.0)
renderer_1.SetViewport(0.0, 1.0 / 4.0, 1.0 / 3.0, 2.0 / 4.0)
renderer_1.AddViewProp(actor_1)

renderer_2 = vtkRenderer()
renderer_2.SetBackground(0.0, 0.0, 0.0)
renderer_2.SetViewport(0.0, 2.0 / 4.0, 1.0 / 3.0, 3.0 / 4.0)
renderer_2.AddViewProp(actor_2)

renderer_3 = vtkRenderer()
renderer_3.SetBackground(0.0, 0.0, 0.0)
renderer_3.SetViewport(0.0, 3.0 / 4.0, 1.0 / 3.0, 1.0)
renderer_3.AddViewProp(actor_3)

renderer_4 = vtkRenderer()
renderer_4.SetBackground(0.0, 0.0, 0.0)
renderer_4.SetViewport(1.0 / 3.0, 0.0, 2.0 / 3.0, 1.0 / 4.0)
renderer_4.AddViewProp(actor_4)

renderer_5 = vtkRenderer()
renderer_5.SetBackground(0.0, 0.0, 0.0)
renderer_5.SetViewport(1.0 / 3.0, 1.0 / 4.0, 2.0 / 3.0, 2.0 / 4.0)
renderer_5.AddViewProp(actor_5)

renderer_6 = vtkRenderer()
renderer_6.SetBackground(0.0, 0.0, 0.0)
renderer_6.SetViewport(1.0 / 3.0, 2.0 / 4.0, 2.0 / 3.0, 3.0 / 4.0)
renderer_6.AddViewProp(actor_6)

renderer_7 = vtkRenderer()
renderer_7.SetBackground(0.0, 0.0, 0.0)
renderer_7.SetViewport(1.0 / 3.0, 3.0 / 4.0, 2.0 / 3.0, 1.0)
renderer_7.AddViewProp(actor_7)

renderer_8 = vtkRenderer()
renderer_8.SetBackground(0.0, 0.0, 0.0)
renderer_8.SetViewport(2.0 / 3.0, 0.0, 1.0, 1.0 / 4.0)
renderer_8.AddViewProp(actor_8)

renderer_9 = vtkRenderer()
renderer_9.SetBackground(0.0, 0.0, 0.0)
renderer_9.SetViewport(2.0 / 3.0, 1.0 / 4.0, 1.0, 2.0 / 4.0)
renderer_9.AddViewProp(actor_9)

renderer_10 = vtkRenderer()
renderer_10.SetBackground(0.0, 0.0, 0.0)
renderer_10.SetViewport(2.0 / 3.0, 2.0 / 4.0, 1.0, 3.0 / 4.0)
renderer_10.AddViewProp(actor_10)

renderer_11 = vtkRenderer()
renderer_11.SetBackground(0.0, 0.0, 0.0)
renderer_11.SetViewport(2.0 / 3.0, 3.0 / 4.0, 1.0, 1.0)
renderer_11.AddViewProp(actor_11)

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
render_window.AddRenderer(renderer_9)
render_window.AddRenderer(renderer_10)
render_window.AddRenderer(renderer_11)
render_window.SetSize(192, 256)
render_window.SetWindowName("threshold connectivity")

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

camera_9 = renderer_9.GetActiveCamera()
camera_9.SetFocalPoint(focal_point)
camera_9.SetPosition(focal_point[0], focal_point[1], focal_point[2] + 500.0)
camera_9.SetViewUp(0.0, 1.0, 0.0)
camera_9.ParallelProjectionOn()
camera_9.SetParallelScale(3.2 * 32)

camera_10 = renderer_10.GetActiveCamera()
camera_10.SetFocalPoint(focal_point)
camera_10.SetPosition(focal_point[0], focal_point[1], focal_point[2] + 500.0)
camera_10.SetViewUp(0.0, 1.0, 0.0)
camera_10.ParallelProjectionOn()
camera_10.SetParallelScale(3.2 * 32)

camera_11 = renderer_11.GetActiveCamera()
camera_11.SetFocalPoint(focal_point)
camera_11.SetPosition(focal_point[0], focal_point[1], focal_point[2] + 500.0)
camera_11.SetViewUp(0.0, 1.0, 0.0)
camera_11.ParallelProjectionOn()
camera_11.SetParallelScale(3.2 * 32)

style = vtkInteractorStyleImage()
style.SetInteractionModeToImageSlicing()

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)
interactor.SetInteractorStyle(style)

interactor.Initialize()
interactor.Start()
