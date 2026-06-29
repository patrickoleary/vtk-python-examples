#!/usr/bin/env python
# Demonstrate vtkThinPlateSplineTransform warping a 2D image with grid overlay.

import os

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import vtkLookupTable, vtkPoints
from vtkmodules.vtkCommonTransforms import vtkThinPlateSplineTransform
from vtkmodules.vtkIOImage import vtkBMPReader
from vtkmodules.vtkImagingCore import vtkImageBlend, vtkImageMapToColors, vtkImageReslice
from vtkmodules.vtkImagingSources import vtkImageGridSource
from vtkmodules.vtkRenderingCore import (
    vtkImageActor,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Create grid overlay image.
image_grid = vtkImageGridSource()
image_grid.SetGridSpacing(16, 16, 0)
image_grid.SetGridOrigin(0, 0, 0)
image_grid.SetDataExtent(0, 255, 0, 255, 0, 0)
image_grid.SetDataScalarTypeToUnsignedChar()

table = vtkLookupTable()
table.SetTableRange(0, 1)
table.SetValueRange(1.0, 0.0)
table.SetSaturationRange(0.0, 0.0)
table.SetHueRange(0.0, 0.0)
table.SetAlphaRange(0.0, 1.0)
table.Build()

alpha = vtkImageMapToColors()
alpha.SetInputConnection(image_grid.GetOutputPort())
alpha.SetLookupTable(table)

# Read background image.
reader = vtkBMPReader()
reader.SetFileName(os.path.join(data_dir, "masonry.bmp"))

blend = vtkImageBlend()
blend.AddInputConnection(0, reader.GetOutputPort())
blend.AddInputConnection(0, alpha.GetOutputPort())

# Thin plate spline transform.
source_landmarks = vtkPoints()
source_landmarks.SetNumberOfPoints(8)
source_landmarks.SetPoint(0, 0, 0, 0)
source_landmarks.SetPoint(1, 0, 255, 0)
source_landmarks.SetPoint(2, 255, 0, 0)
source_landmarks.SetPoint(3, 255, 255, 0)
source_landmarks.SetPoint(4, 96, 96, 0)
source_landmarks.SetPoint(5, 96, 159, 0)
source_landmarks.SetPoint(6, 159, 159, 0)
source_landmarks.SetPoint(7, 159, 96, 0)

target_landmarks = vtkPoints()
target_landmarks.SetNumberOfPoints(8)
target_landmarks.SetPoint(0, 0, 0, 0)
target_landmarks.SetPoint(1, 0, 255, 0)
target_landmarks.SetPoint(2, 255, 0, 0)
target_landmarks.SetPoint(3, 255, 255, 0)
target_landmarks.SetPoint(4, 96, 159, 0)
target_landmarks.SetPoint(5, 159, 159, 0)
target_landmarks.SetPoint(6, 159, 96, 0)
target_landmarks.SetPoint(7, 96, 96, 0)

transform = vtkThinPlateSplineTransform()
transform.SetSourceLandmarks(target_landmarks)
transform.SetTargetLandmarks(source_landmarks)
transform.SetBasisToR2LogR()
transform.Inverse()

reslice = vtkImageReslice()
reslice.SetInputConnection(blend.GetOutputPort())
reslice.SetResliceTransform(transform)
reslice.SetInterpolationModeToLinear()

# Display using standard image rendering pipeline.
image_actor = vtkImageActor()
image_actor.GetMapper().SetInputConnection(reslice.GetOutputPort())

renderer = vtkRenderer()
renderer.AddActor(image_actor)

render_window = vtkRenderWindow()
render_window.SetSize(300, 300)
render_window.AddRenderer(renderer)
render_window.SetWindowName("thin plate warp")

renderer.GetActiveCamera().ParallelProjectionOn()
renderer.ResetCamera()

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
