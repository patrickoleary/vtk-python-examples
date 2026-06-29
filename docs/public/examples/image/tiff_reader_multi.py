#!/usr/bin/env python

# Read a TIFF file multiple times to verify no file descriptor leaks, then display.

import os

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkIOImage import vtkTIFFReader
from vtkmodules.vtkRenderingCore import (
    vtkImageActor,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Source
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Read the same file multiple times to check for resource leaks
tiff_reader_0 = vtkTIFFReader()
tiff_reader_0.SetFileName(os.path.join(data_dir, "beach.tif"))
tiff_reader_0.SetOrientationType(4)
tiff_reader_0.Update()

tiff_reader_1 = vtkTIFFReader()
tiff_reader_1.SetFileName(os.path.join(data_dir, "beach.tif"))
tiff_reader_1.SetOrientationType(4)
tiff_reader_1.Update()

tiff_reader_2 = vtkTIFFReader()
tiff_reader_2.SetFileName(os.path.join(data_dir, "beach.tif"))
tiff_reader_2.SetOrientationType(4)
tiff_reader_2.Update()

tiff_reader_3 = vtkTIFFReader()
tiff_reader_3.SetFileName(os.path.join(data_dir, "beach.tif"))
tiff_reader_3.SetOrientationType(4)
tiff_reader_3.Update()

tiff_reader_4 = vtkTIFFReader()
tiff_reader_4.SetFileName(os.path.join(data_dir, "beach.tif"))
tiff_reader_4.SetOrientationType(4)
tiff_reader_4.Update()

tiff_reader_5 = vtkTIFFReader()
tiff_reader_5.SetFileName(os.path.join(data_dir, "beach.tif"))
tiff_reader_5.SetOrientationType(4)
tiff_reader_5.Update()

tiff_reader_6 = vtkTIFFReader()
tiff_reader_6.SetFileName(os.path.join(data_dir, "beach.tif"))
tiff_reader_6.SetOrientationType(4)
tiff_reader_6.Update()

tiff_reader_7 = vtkTIFFReader()
tiff_reader_7.SetFileName(os.path.join(data_dir, "beach.tif"))
tiff_reader_7.SetOrientationType(4)
tiff_reader_7.Update()

tiff_reader_8 = vtkTIFFReader()
tiff_reader_8.SetFileName(os.path.join(data_dir, "beach.tif"))
tiff_reader_8.SetOrientationType(4)
tiff_reader_8.Update()

# Display the last read
image_actor = vtkImageActor()
image_actor.GetMapper().SetInputConnection(tiff_reader_8.GetOutputPort())

# Renderer
renderer = vtkRenderer()
renderer.AddActor(image_actor)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("tiff reader multi")
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
