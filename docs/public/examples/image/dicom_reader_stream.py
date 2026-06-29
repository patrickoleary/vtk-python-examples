#!/usr/bin/env python

# Read a DICOM file via vtkFileResourceStream and display with vtkImageActor.

import os

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkIOCore import vtkFileResourceStream
from vtkmodules.vtkIOImage import vtkDICOMImageReader
from vtkmodules.vtkRenderingCore import (
    vtkImageActor,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Source
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Open file via stream
file_stream = vtkFileResourceStream()
file_stream.Open(os.path.join(data_dir, "dicom", "prostate.IMG"))

# Read DICOM from stream
dicom_reader = vtkDICOMImageReader()
dicom_reader.SetStream(file_stream)
dicom_reader.Update()

# Print DICOM metadata
print(f"File Extensions: {dicom_reader.GetFileExtensions()}")
print(f"Descriptive Name: {dicom_reader.GetDescriptiveName()}")
print(f"Width: {dicom_reader.GetWidth()}")
print(f"Height: {dicom_reader.GetHeight()}")
print(f"Bits Allocated: {dicom_reader.GetBitsAllocated()}")
print(f"Number of Components: {dicom_reader.GetNumberOfComponents()}")

# Display center slice with image actor
extent = dicom_reader.GetOutput().GetExtent()
slice_number = (extent[5] + extent[4]) // 2

image_actor = vtkImageActor()
image_actor.GetMapper().SetInputConnection(dicom_reader.GetOutputPort())
image_actor.SetDisplayExtent(extent[0], extent[1], extent[2], extent[3], slice_number, slice_number)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(image_actor)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("dicom reader stream")
render_window.SetMultiSamples(0)
render_window.SetSize(300, 300)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.GetActiveCamera().ParallelProjectionOn()
renderer.ResetCamera()

interactor.Initialize()
interactor.Start()
