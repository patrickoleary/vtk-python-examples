#!/usr/bin/env python

# Read a directory of DICOM files and display the center slice with vtkImageActor.

import os

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkIOImage import vtkDICOMImageReader
from vtkmodules.vtkRenderingCore import (
    vtkImageActor,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Source
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Read DICOM directory
dicom_reader = vtkDICOMImageReader()
dicom_reader.SetDirectoryName(os.path.join(data_dir, "dicom", "collection"))
dicom_reader.Update()

# Print image properties
print("Pixel spacing:", dicom_reader.GetPixelSpacing())
print("Width:", dicom_reader.GetWidth())
print("Height:", dicom_reader.GetHeight())
print("Bits allocated:", dicom_reader.GetBitsAllocated())
print("Number of components:", dicom_reader.GetNumberOfComponents())

# Display center slice
extent = dicom_reader.GetOutput().GetExtent()
center_slice = (extent[5] + extent[4]) // 2

# Display with vtkImageActor
image_actor = vtkImageActor()
image_actor.GetMapper().SetInputConnection(dicom_reader.GetOutputPort())
image_actor.SetDisplayExtent(extent[0], extent[1], extent[2], extent[3], center_slice, center_slice)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(image_actor)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("dicom reader file collection")
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
