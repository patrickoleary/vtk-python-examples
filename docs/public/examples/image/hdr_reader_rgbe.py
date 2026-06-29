#!/usr/bin/env python

# Read an HDR file in RGBE format, crop it, and display with vtkImageActor.

import os

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkIOImage import vtkHDRReader
from vtkmodules.vtkImagingCore import vtkImageShiftScale
from vtkmodules.vtkRenderingCore import (
    vtkImageActor,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Source
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Read HDR file
hdr_reader = vtkHDRReader()
hdr_reader.SetFileName(os.path.join(data_dir, "spiaggia_di_mondello_1k.hdr"))
hdr_reader.UpdateInformation()

# Crop the image
data_extent = hdr_reader.GetDataExtent()
extents = [data_extent[0] + data_extent[1] // 5, data_extent[1] - data_extent[1] // 5,
           data_extent[2] + data_extent[3] // 6, data_extent[3] - data_extent[3] // 6, 0, 0]
hdr_reader.UpdateExtent(extents)

# Tone-map HDR float data to displayable range
shift_scale = vtkImageShiftScale()
shift_scale.SetInputData(hdr_reader.GetOutput())
shift_scale.SetShift(0)
shift_scale.SetScale(255)
shift_scale.SetOutputScalarTypeToUnsignedChar()
shift_scale.ClampOverflowOn()

# Display with vtkImageActor
image_actor = vtkImageActor()
image_actor.GetMapper().SetInputConnection(shift_scale.GetOutputPort())

# Renderer
renderer = vtkRenderer()
renderer.AddActor(image_actor)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("hdr reader rgbe")
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
