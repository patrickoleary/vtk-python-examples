#!/usr/bin/env python

# Permute image axes using vtkImagePermute on volumetric medical data.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

import os

from vtkmodules.vtkIOImage import vtkImageReader
from vtkmodules.vtkImagingCore import vtkImagePermute
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
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

reader.SetFilePrefix(os.path.join(data_dir, "headsq", "quarter"))
reader.SetDataMask(0x7fff)

# Permute axes
permute = vtkImagePermute()
permute.SetInputConnection(reader.GetOutputPort())
permute.SetFilteredAxes(1, 2, 0)
permute.Update()

# Display with vtkImageActor at middle Z slice
image_actor = vtkImageActor()
image_actor.GetMapper().SetInputConnection(permute.GetOutputPort())
ext = permute.GetOutput().GetExtent()
z_mid = (ext[4] + ext[5]) // 2
image_actor.SetDisplayExtent(ext[0], ext[1], ext[2], ext[3], z_mid, z_mid)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(image_actor)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(256, 256)
render_window.SetWindowName("permute")

# Scene
renderer.ResetCamera()

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
