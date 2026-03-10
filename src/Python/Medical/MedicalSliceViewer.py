#!/usr/bin/env python

# Display a 2D axial slice from a 3D CT head volume using the standard
# rendering pipeline with vtkImageMapToColors and vtkImageActor.

import os
from pathlib import Path

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkCommonCore import vtkLookupTable
from vtkmodules.vtkIOImage import vtkMetaImageReader
from vtkmodules.vtkImagingCore import vtkImageMapToColors
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

# LookupTable: grayscale mapping for CT intensity values
grayscale_lut = vtkLookupTable()
grayscale_lut.SetTableRange(0, 2000)
grayscale_lut.SetSaturationRange(0, 0)
grayscale_lut.SetHueRange(0, 0)
grayscale_lut.SetValueRange(0, 1)
grayscale_lut.Build()

# ColorMap: map scalar values to grayscale colors
color_map = vtkImageMapToColors()
color_map.SetInputConnection(reader.GetOutputPort())
color_map.SetLookupTable(grayscale_lut)
color_map.Update()

# ImageActor: display the middle axial slice
extent = reader.GetOutput().GetExtent()
mid_slice = (extent[4] + extent[5]) // 2

image_actor = vtkImageActor()
image_actor.GetMapper().SetInputConnection(color_map.GetOutputPort())
image_actor.SetDisplayExtent(extent[0], extent[1], extent[2], extent[3], mid_slice, mid_slice)
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
render_window.SetWindowName("MedicalSliceViewer")

# Interactor: handle mouse and keyboard events
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window.Render()
interactor.Initialize()
interactor.Start()
