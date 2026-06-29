#!/usr/bin/env python

# Read an Analyze 7.5 format file with vtkNIFTIImageReader and display in two viewports.

import os

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkIOImage import vtkNIFTIImageReader
from vtkmodules.vtkRenderingCore import (
    vtkImageSlice,
    vtkImageSliceMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Source
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Read Analyze file
analyze_reader = vtkNIFTIImageReader()
analyze_reader.SetFileName(os.path.join(data_dir, "ANALYZE.HDR"))
analyze_reader.Update()

size = analyze_reader.GetOutput().GetDimensions()
center = analyze_reader.GetOutput().GetCenter()
spacing = analyze_reader.GetOutput().GetSpacing()

center_0 = list(center)
center_1 = list(center)
if size[2] % 2 == 1:
    center_0[2] += 0.5 * spacing[2]
if size[0] % 2 == 1:
    center_1[0] += 0.5 * spacing[0]

vrange = analyze_reader.GetOutput().GetScalarRange()

# Axial view
axial_mapper = vtkImageSliceMapper()
axial_mapper.BorderOn()
axial_mapper.SliceAtFocalPointOn()
axial_mapper.SliceFacesCameraOn()
axial_mapper.SetInputConnection(analyze_reader.GetOutputPort())

axial_slice = vtkImageSlice()
axial_slice.SetMapper(axial_mapper)
axial_slice.GetProperty().SetColorWindow(vrange[1] - vrange[0])
axial_slice.GetProperty().SetColorLevel(0.5 * (vrange[0] + vrange[1]))

# Sagittal view
sagittal_mapper = vtkImageSliceMapper()
sagittal_mapper.BorderOn()
sagittal_mapper.SliceAtFocalPointOn()
sagittal_mapper.SliceFacesCameraOn()
sagittal_mapper.SetInputConnection(analyze_reader.GetOutputPort())

sagittal_slice = vtkImageSlice()
sagittal_slice.SetMapper(sagittal_mapper)
sagittal_slice.GetProperty().SetColorWindow(vrange[1] - vrange[0])
sagittal_slice.GetProperty().SetColorLevel(0.5 * (vrange[0] + vrange[1]))

# Two viewports
ratio = size[0] * 1.0 / (size[0] + size[2])

renderer_0 = vtkRenderer()
renderer_0.SetViewport(0, 0, ratio, 1.0)
renderer_0.AddViewProp(axial_slice)

renderer_1 = vtkRenderer()
renderer_1.SetViewport(ratio, 0.0, 1.0, 1.0)
renderer_1.AddViewProp(sagittal_slice)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer_0)
render_window.AddRenderer(renderer_1)
render_window.SetWindowName("nifti reader analyze")
render_window.SetMultiSamples(0)
render_window.SetSize(size[0] + size[2], size[1])

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
camera_0 = renderer_0.GetActiveCamera()
camera_0.ParallelProjectionOn()
camera_0.SetParallelScale(0.5 * spacing[1] * size[1])
camera_0.SetFocalPoint(center_0[0], center_0[1], center_0[2])
camera_0.SetPosition(center_0[0], center_0[1], center_0[2] - 100.0)

camera_1 = renderer_1.GetActiveCamera()
camera_1.ParallelProjectionOn()
camera_1.SetParallelScale(0.5 * spacing[1] * size[1])
camera_1.SetFocalPoint(center_1[0], center_1[1], center_1[2])
camera_1.SetPosition(center_1[0] + 100.0, center_1[1], center_1[2])

interactor.Initialize()
interactor.Start()
