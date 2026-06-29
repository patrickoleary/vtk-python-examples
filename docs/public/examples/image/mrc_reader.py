#!/usr/bin/env python

# Read an MRC file and display a slice with vtkImageSliceMapper.

import os

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkIOImage import vtkMRCReader
from vtkmodules.vtkRenderingCore import (
    vtkImageSlice,
    vtkImageSliceMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Source
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Read MRC file
mrc_reader = vtkMRCReader()
mrc_reader.SetFileName(os.path.join(data_dir, "mrc", "emd_1056.mrc"))
mrc_reader.Update()

size = mrc_reader.GetOutput().GetDimensions()
center = list(mrc_reader.GetOutput().GetCenter())
spacing = mrc_reader.GetOutput().GetSpacing()

if size[2] % 2 == 1:
    center[2] += 0.5 * spacing[2]

vrange = mrc_reader.GetOutput().GetScalarRange()

# Slice mapper
slice_mapper = vtkImageSliceMapper()
slice_mapper.BorderOn()
slice_mapper.SliceAtFocalPointOn()
slice_mapper.SliceFacesCameraOn()
slice_mapper.SetInputConnection(mrc_reader.GetOutputPort())

# Image slice
image_slice = vtkImageSlice()
image_slice.SetMapper(slice_mapper)
image_slice.GetProperty().SetColorWindow(vrange[1] - vrange[0])
image_slice.GetProperty().SetColorLevel(0.5 * (vrange[0] + vrange[1]))

# Renderer
renderer = vtkRenderer()
renderer.AddViewProp(image_slice)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("mrc reader")
render_window.SetMultiSamples(0)
render_window.SetSize(size[0], size[1])

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
camera = renderer.GetActiveCamera()
camera.ParallelProjectionOn()
camera.SetParallelScale(0.5 * spacing[1] * size[1])
camera.SetFocalPoint(center[0], center[1], center[2])
camera.SetPosition(center[0], center[1], center[2] - 100.0)

interactor.Initialize()
interactor.Start()
