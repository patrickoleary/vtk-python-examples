#!/usr/bin/env python

# Permute and resample an image with vtkImageReslice using oblique axes.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

import os

from vtkmodules.vtkIOImage import vtkImageReader
from vtkmodules.vtkImagingCore import vtkImageReslice
from vtkmodules.vtkRenderingCore import (
    vtkImageActor,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Image pipeline
reader = vtkImageReader()
reader.ReleaseDataFlagOff()
reader.SetDataByteOrderToLittleEndian()
reader.SetDataExtent(0, 63, 0, 63, 1, 93)
reader.SetDataSpacing(3.2, 3.2, 1.5)
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

reader.SetFilePrefix(os.path.join(data_dir, "headsq", "quarter"))
reader.SetDataMask(0x7fff)

# Reslice with permuted axes and resampling
reslice = vtkImageReslice()
reslice.SetInputConnection(reader.GetOutputPort())
reslice.SetResliceAxesDirectionCosines([0, +1, 0, 0, 0, -1, -1, 0, 0])
reslice.SetOutputSpacing(1.0, 1.0, 1.0)
reslice.Update()

# Display with vtkImageActor at middle Z slice
image_actor = vtkImageActor()
image_actor.GetMapper().SetInputConnection(reslice.GetOutputPort())
ext = reslice.GetOutput().GetExtent()
z_mid = (ext[4] + ext[5]) // 2
image_actor.SetDisplayExtent(ext[0], ext[1], ext[2], ext[3], z_mid, z_mid)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(image_actor)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(200, 140)
render_window.SetWindowName("reslice permute resample")

# Scene
renderer.ResetCamera()

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
