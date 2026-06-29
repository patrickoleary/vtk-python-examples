#!/usr/bin/env python

# Read an 8-bit BMP file with Allow8BitBMP off (renders as RGB directly).

import os

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkIOImage import vtkBMPReader
from vtkmodules.vtkRenderingCore import (
    vtkImageActor,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Source
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Read BMP with Allow8BitBMP off
bmp_reader = vtkBMPReader()
bmp_reader.SetFileName(os.path.join(data_dir, "masonry.bmp"))
bmp_reader.SetAllow8BitBMP(0)
bmp_reader.Update()

# Print image properties
print("Depth:", bmp_reader.GetDepth())
print("File extensions:", bmp_reader.GetFileExtensions())
print("Allow8BitBMP:", bmp_reader.GetAllow8BitBMP())

# Display with vtkImageActor
image_actor = vtkImageActor()
image_actor.GetMapper().SetInputConnection(bmp_reader.GetOutputPort())

# Renderer
renderer = vtkRenderer()
renderer.AddActor(image_actor)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("bmp reader do not allow 8 bit bmp")
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
