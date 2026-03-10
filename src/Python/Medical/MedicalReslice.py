#!/usr/bin/env python

# Display an oblique reslice of a CT head volume using vtkImageReslice.
# The reslice plane is tilted 30 degrees about the X axis through the
# volume center, rendered with the standard vtkImageActor pipeline.

import math
import os
from pathlib import Path

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkCommonCore import vtkLookupTable
from vtkmodules.vtkIOImage import vtkMetaImageReader
from vtkmodules.vtkImagingCore import (
    vtkImageMapToColors,
    vtkImageReslice,
)
from vtkmodules.vtkRenderingCore import (
    vtkImageActor,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Data directory: defaults to the folder containing this script
data_dir = Path(os.environ.get("VPE_DATA_DIR", Path(__file__).parent))

# Reader: load the 3D CT head volume
reader = vtkMetaImageReader()
reader.SetFileName(str(data_dir / "FullHead.mhd"))
reader.Update()

# Compute the center of the volume
extent = reader.GetOutput().GetExtent()
spacing = reader.GetOutput().GetSpacing()
origin = reader.GetOutput().GetOrigin()
center_x = origin[0] + spacing[0] * 0.5 * (extent[0] + extent[1])
center_y = origin[1] + spacing[1] * 0.5 * (extent[2] + extent[3])
center_z = origin[2] + spacing[2] * 0.5 * (extent[4] + extent[5])

# Reslice: extract an oblique slice tilted 30 degrees about X
angle_deg = 30.0
angle_rad = math.radians(angle_deg)
cos_a = math.cos(angle_rad)
sin_a = math.sin(angle_rad)

reslice = vtkImageReslice()
reslice.SetInputConnection(reader.GetOutputPort())
reslice.SetOutputDimensionality(2)
reslice.SetResliceAxesDirectionCosines(
    1, 0, 0,
    0, cos_a, sin_a,
    0, -sin_a, cos_a,
)
reslice.SetResliceAxesOrigin(center_x, center_y, center_z)
reslice.SetInterpolationModeToLinear()
reslice.Update()

# LookupTable: grayscale mapping for CT intensity values
grayscale_lut = vtkLookupTable()
grayscale_lut.SetTableRange(0, 2000)
grayscale_lut.SetSaturationRange(0, 0)
grayscale_lut.SetHueRange(0, 0)
grayscale_lut.SetValueRange(0, 1)
grayscale_lut.Build()

# ColorMap: map resliced scalars to grayscale colors
color_map = vtkImageMapToColors()
color_map.SetInputConnection(reslice.GetOutputPort())
color_map.SetLookupTable(grayscale_lut)
color_map.Update()

# ImageActor: display the resliced image
image_actor = vtkImageActor()
image_actor.GetMapper().SetInputConnection(color_map.GetOutputPort())
image_actor.ForceOpaqueOn()

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.AddActor(image_actor)
renderer.SetBackground(0.0, 0.0, 0.0)
renderer.ResetCamera()

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(640, 480)
render_window.SetWindowName("MedicalReslice")

# Interactor: handle mouse and keyboard events
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window.Render()
interactor.Initialize()
interactor.Start()
