#!/usr/bin/env python

# Test image writers by reading TIFF, writing in multiple formats, and displaying luminance.

import os
import tempfile

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkIOImage import (
    vtkBMPWriter,
    vtkJPEGWriter,
    vtkPNGWriter,
    vtkPNMWriter,
    vtkPostScriptWriter,
    vtkTIFFReader,
    vtkTIFFWriter,
)
from vtkmodules.vtkImagingColor import vtkImageLuminance
from vtkmodules.vtkRenderingCore import (
    vtkImageActor,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Source
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))
temp_dir = tempfile.mkdtemp()

# Read TIFF image
image_reader = vtkTIFFReader()
image_reader.SetFileName(os.path.join(data_dir, "beach.tif"))
image_reader.SetOrientationType(4)
image_reader.Update()

# Compute luminance
luminance = vtkImageLuminance()
luminance.SetInputConnection(image_reader.GetOutputPort())

# Test various writers with both color and luminance
tiff_writer_1 = vtkTIFFWriter()
tiff_writer_1.SetInputConnection(image_reader.GetOutputPort())
tiff_writer_1.SetFileName(os.path.join(temp_dir, "tiff1.tif"))
tiff_writer_1.Write()
os.remove(os.path.join(temp_dir, "tiff1.tif"))

tiff_writer_2 = vtkTIFFWriter()
tiff_writer_2.SetInputConnection(luminance.GetOutputPort())
tiff_writer_2.SetFileName(os.path.join(temp_dir, "tiff2.tif"))
tiff_writer_2.Write()
os.remove(os.path.join(temp_dir, "tiff2.tif"))

bmp_writer_1 = vtkBMPWriter()
bmp_writer_1.SetInputConnection(image_reader.GetOutputPort())
bmp_writer_1.SetFileName(os.path.join(temp_dir, "bmp1.bmp"))
bmp_writer_1.Write()
os.remove(os.path.join(temp_dir, "bmp1.bmp"))

bmp_writer_2 = vtkBMPWriter()
bmp_writer_2.SetInputConnection(luminance.GetOutputPort())
bmp_writer_2.SetFileName(os.path.join(temp_dir, "bmp2.bmp"))
bmp_writer_2.Write()
os.remove(os.path.join(temp_dir, "bmp2.bmp"))

pnm_writer_1 = vtkPNMWriter()
pnm_writer_1.SetInputConnection(image_reader.GetOutputPort())
pnm_writer_1.SetFileName(os.path.join(temp_dir, "pnm1.pnm"))
pnm_writer_1.Write()
os.remove(os.path.join(temp_dir, "pnm1.pnm"))

pnm_writer_2 = vtkPNMWriter()
pnm_writer_2.SetInputConnection(luminance.GetOutputPort())
pnm_writer_2.SetFileName(os.path.join(temp_dir, "pnm2.pnm"))
pnm_writer_2.Write()
os.remove(os.path.join(temp_dir, "pnm2.pnm"))

ps_writer_1 = vtkPostScriptWriter()
ps_writer_1.SetInputConnection(image_reader.GetOutputPort())
ps_writer_1.SetFileName(os.path.join(temp_dir, "psw1.ps"))
ps_writer_1.Write()
os.remove(os.path.join(temp_dir, "psw1.ps"))

ps_writer_2 = vtkPostScriptWriter()
ps_writer_2.SetInputConnection(luminance.GetOutputPort())
ps_writer_2.SetFileName(os.path.join(temp_dir, "psw2.ps"))
ps_writer_2.Write()
os.remove(os.path.join(temp_dir, "psw2.ps"))

png_writer_1 = vtkPNGWriter()
png_writer_1.SetInputConnection(image_reader.GetOutputPort())
png_writer_1.SetFileName(os.path.join(temp_dir, "pngw1.png"))
png_writer_1.Write()
os.remove(os.path.join(temp_dir, "pngw1.png"))

png_writer_2 = vtkPNGWriter()
png_writer_2.SetInputConnection(luminance.GetOutputPort())
png_writer_2.SetFileName(os.path.join(temp_dir, "pngw2.png"))
png_writer_2.Write()
os.remove(os.path.join(temp_dir, "pngw2.png"))

jpeg_writer_1 = vtkJPEGWriter()
jpeg_writer_1.SetInputConnection(image_reader.GetOutputPort())
jpeg_writer_1.SetFileName(os.path.join(temp_dir, "jpgw1.jpg"))
jpeg_writer_1.Write()
os.remove(os.path.join(temp_dir, "jpgw1.jpg"))

jpeg_writer_2 = vtkJPEGWriter()
jpeg_writer_2.SetInputConnection(luminance.GetOutputPort())
jpeg_writer_2.SetFileName(os.path.join(temp_dir, "jpgw2.jpg"))
jpeg_writer_2.Write()
os.remove(os.path.join(temp_dir, "jpgw2.jpg"))

os.rmdir(temp_dir)

# Display luminance with vtkImageActor
image_actor = vtkImageActor()
image_actor.GetMapper().SetInputConnection(luminance.GetOutputPort())

# Renderer
renderer = vtkRenderer()
renderer.AddActor(image_actor)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("writers")
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
