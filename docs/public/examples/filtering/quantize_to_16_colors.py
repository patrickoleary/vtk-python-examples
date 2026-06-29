#!/usr/bin/env python

# Quantize an earth image to 16 colors using vtkImageQuantizeRGBToIndex.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

import os

from vtkmodules.vtkIOImage import vtkPNMReader
from vtkmodules.vtkImagingColor import (
    vtkImageMapToRGBA,
    vtkImageQuantizeRGBToIndex,
)
from vtkmodules.vtkImagingCore import vtkImageMirrorPad
from vtkmodules.vtkRenderingCore import (
    vtkImageActor,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Read earth image
reader = vtkPNMReader()
reader.ReleaseDataFlagOff()
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

reader.SetFileName(os.path.join(data_dir, "earth.ppm"))

# Mirror pad to make image larger
pad = vtkImageMirrorPad()
pad.SetInputConnection(reader.GetOutputPort())
pad.SetOutputWholeExtent(-120, 320, -120, 320, 0, 0)

# Quantize to 16 colors
quantize = vtkImageQuantizeRGBToIndex()
quantize.SetInputConnection(pad.GetOutputPort())
quantize.SetNumberOfColors(16)
quantize.Update()

# Map indexed image back to RGBA
color_map = vtkImageMapToRGBA()
color_map.SetInputConnection(quantize.GetOutputPort())
color_map.SetLookupTable(quantize.GetLookupTable())
color_map.Update()

# Display with vtkImageActor
image_actor = vtkImageActor()
image_actor.GetMapper().SetInputConnection(color_map.GetOutputPort())

# Renderer
renderer = vtkRenderer()
renderer.AddActor(image_actor)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(440, 440)
render_window.SetWindowName("quantize to 16 colors")

# Scene
renderer.ResetCamera()

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
