#!/usr/bin/env python
# Demonstrate vtkThinPlateSplineTransform warping a 3D volume dataset.

import os

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import vtkPoints
from vtkmodules.vtkCommonTransforms import vtkThinPlateSplineTransform
from vtkmodules.vtkIOImage import vtkImageReader
from vtkmodules.vtkImagingCore import vtkImageReslice
from vtkmodules.vtkRenderingCore import (
    vtkImageActor,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Read volume data.
reader = vtkImageReader()
reader.ReleaseDataFlagOff()
reader.SetDataByteOrderToLittleEndian()
reader.SetDataExtent(0, 63, 0, 63, 1, 93)
reader.SetDataSpacing(3.2, 3.2, 1.5)
reader.SetDataOrigin(-100.8, -100.8, -69)
reader.SetFilePrefix(os.path.join(data_dir, "headsq", "quarter"))
reader.SetDataMask(0x7FFF)
reader.Update()

# Source and target landmarks.
source_landmarks = vtkPoints()
target_landmarks = vtkPoints()
source_landmarks.InsertNextPoint(0, 0, 0)
target_landmarks.InsertNextPoint(-60, 10, 20)
source_landmarks.InsertNextPoint(-100, -100, -50)
target_landmarks.InsertNextPoint(-100, -100, -50)
source_landmarks.InsertNextPoint(-100, -100, 50)
target_landmarks.InsertNextPoint(-100, -100, 50)
source_landmarks.InsertNextPoint(-100, 100, -50)
target_landmarks.InsertNextPoint(-100, 100, -50)
source_landmarks.InsertNextPoint(-100, 100, 50)
target_landmarks.InsertNextPoint(-100, 100, 50)
source_landmarks.InsertNextPoint(100, -100, -50)
target_landmarks.InsertNextPoint(100, -100, -50)
source_landmarks.InsertNextPoint(100, -100, 50)
target_landmarks.InsertNextPoint(100, -100, 50)
source_landmarks.InsertNextPoint(100, 100, -50)
target_landmarks.InsertNextPoint(100, 100, -50)
source_landmarks.InsertNextPoint(100, 100, 50)
target_landmarks.InsertNextPoint(100, 100, 50)

# Thin plate spline transform.
transform = vtkThinPlateSplineTransform()
transform.SetSourceLandmarks(source_landmarks)
transform.SetTargetLandmarks(target_landmarks)
transform.SetBasisToR()

# Reslice the volume with the transform.
reslice = vtkImageReslice()
reslice.SetInputConnection(reader.GetOutputPort())
reslice.SetResliceTransform(transform)
reslice.SetInterpolationModeToLinear()
reslice.SetOutputSpacing(1, 1, 1)

# Display a single slice using standard image rendering pipeline.
image_actor = vtkImageActor()
image_actor.GetMapper().SetInputConnection(reslice.GetOutputPort())
image_actor.SetDisplayExtent(0, 63, 0, 63, 90, 90)

renderer = vtkRenderer()
renderer.AddActor(image_actor)

render_window = vtkRenderWindow()
render_window.SetSize(200, 200)
render_window.AddRenderer(renderer)
render_window.SetWindowName("thin plate warp3d")

renderer.GetActiveCamera().ParallelProjectionOn()
renderer.ResetCamera()

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
