#!/usr/bin/env python

# Read a MetaImage (.mha) file and display with vtkImageActor.

import os

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkIOImage import vtkMetaImageReader
from vtkmodules.vtkRenderingCore import (
    vtkImageActor,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Source
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Read MetaImage file
meta_reader = vtkMetaImageReader()
meta_reader.SetFileName(os.path.join(data_dir, "foot.mha"))
meta_reader.Update()

# Display with vtkImageActor at middle Z slice
image_actor = vtkImageActor()
image_actor.GetMapper().SetInputConnection(meta_reader.GetOutputPort())
extent = meta_reader.GetOutput().GetExtent()
z_mid = (extent[4] + extent[5]) // 2
image_actor.SetDisplayExtent(extent[0], extent[1], extent[2], extent[3], z_mid, z_mid)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(image_actor)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("meta image2d")
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
