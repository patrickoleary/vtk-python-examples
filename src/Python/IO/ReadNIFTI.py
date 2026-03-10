#!/usr/bin/env python

# Read a NIfTI neuroimaging volume (.nii) using vtkNIFTIImageReader and
# display an axial slice with grayscale coloring.  A small synthetic NIfTI
# volume is generated and written to disk if the file does not already exist.

import math
import os
from pathlib import Path

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkCommonCore import vtkLookupTable
from vtkmodules.vtkIOImage import vtkNIFTIImageReader, vtkNIFTIImageWriter
from vtkmodules.vtkImagingCore import vtkImageMapToColors
from vtkmodules.vtkImagingSources import vtkImageSinusoidSource
from vtkmodules.vtkRenderingCore import (
    vtkImageActor,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
black_rgb = (0.0, 0.0, 0.0)

# Data directory: defaults to the folder containing this script
data_dir = Path(os.environ.get("VPE_DATA_DIR", Path(__file__).parent))
nii_path = data_dir / "synthetic.nii"

# Generate a synthetic NIfTI volume if the file does not exist
if not nii_path.exists():
    source = vtkImageSinusoidSource()
    source.SetWholeExtent(0, 63, 0, 63, 0, 31)
    source.SetPeriod(20.0)
    source.SetAmplitude(128)
    source.Update()

    writer = vtkNIFTIImageWriter()
    writer.SetFileName(str(nii_path))
    writer.SetInputConnection(source.GetOutputPort())
    writer.Write()

# Reader: load the NIfTI volume
reader = vtkNIFTIImageReader()
reader.SetFileName(str(nii_path))
reader.Update()

# LookupTable: grayscale mapping
lut = vtkLookupTable()
scalar_range = reader.GetOutput().GetScalarRange()
lut.SetTableRange(scalar_range)
lut.SetSaturationRange(0, 0)
lut.SetHueRange(0, 0)
lut.SetValueRange(0, 1)
lut.Build()

# ColorMap: map scalars to grayscale colors
color_map = vtkImageMapToColors()
color_map.SetInputConnection(reader.GetOutputPort())
color_map.SetLookupTable(lut)
color_map.Update()

# ImageActor: display the middle axial slice
extent = reader.GetOutput().GetExtent()
mid_slice = (extent[4] + extent[5]) // 2

image_actor = vtkImageActor()
image_actor.GetMapper().SetInputConnection(color_map.GetOutputPort())
image_actor.SetDisplayExtent(
    extent[0], extent[1], extent[2], extent[3], mid_slice, mid_slice
)
image_actor.ForceOpaqueOn()

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.AddActor(image_actor)
renderer.SetBackground(black_rgb)
renderer.ResetCamera()

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(640, 480)
render_window.SetWindowName("ReadNIFTI")

# Interactor: handle mouse and keyboard events
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
interactor.Initialize()
interactor.Start()
