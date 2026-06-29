#!/usr/bin/env python

# Write an image to a parallel raw file, then display the original image.

import os
import tempfile

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkIOImage import vtkTIFFReader
from vtkmodules.vtkIOParallel import vtkPImageWriter
from vtkmodules.vtkRenderingCore import (
    vtkImageActor,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Source
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

tiff_reader = vtkTIFFReader()
tiff_reader.SetFileName(os.path.join(data_dir, "beach.tif"))
tiff_reader.SetOrientationType(4)
tiff_reader.Update()

# Write to a parallel raw file in a temp directory
temp_dir = tempfile.mkdtemp()
raw_file = os.path.join(temp_dir, "piw.raw")

parallel_writer = vtkPImageWriter()
parallel_writer.SetInputConnection(tiff_reader.GetOutputPort())
parallel_writer.SetFileName(raw_file)
parallel_writer.SetMemoryLimit(1)
parallel_writer.Write()

# Clean up temp file
os.remove(raw_file)
os.rmdir(temp_dir)

# Actor
image_actor = vtkImageActor()
image_actor.GetMapper().SetInputConnection(tiff_reader.GetOutputPort())

# Renderer
renderer = vtkRenderer()
renderer.AddActor(image_actor)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("p image writer")
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
