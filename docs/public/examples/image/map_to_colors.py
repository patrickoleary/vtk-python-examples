#!/usr/bin/env python

# Convert an RGB image to grayscale luminance, then apply a rainbow
# lookup table via vtkImageMapToColors.  The left viewport shows the
# original image; the right shows the false-color result.

import os
from pathlib import Path

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkCommonCore import vtkLookupTable
from vtkmodules.vtkIOImage import vtkJPEGReader
from vtkmodules.vtkImagingCore import vtkImageMapToColors
from vtkmodules.vtkImagingMath import vtkImageMagnitude
from vtkmodules.vtkInteractionStyle import vtkInteractorStyleImage
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

# Reader: load an RGB JPEG image
reader = vtkJPEGReader()
reader.SetFileName(str(data_dir / "Gourds2.jpg"))
reader.Update()

# Luminance: compute grayscale magnitude from the RGB components
luminance = vtkImageMagnitude()
luminance.SetInputConnection(reader.GetOutputPort())
luminance.Update()

# LookupTable: build a rainbow ramp (blue → cyan → green → yellow → red)
lut = vtkLookupTable()
lut.SetNumberOfTableValues(256)
lut.SetRange(luminance.GetOutput().GetScalarRange())
lut.SetHueRange(0.667, 0.0)
lut.SetSaturationRange(1.0, 1.0)
lut.SetValueRange(1.0, 1.0)
lut.Build()

# MapToColors: apply the rainbow LUT to the single-component luminance
color_map = vtkImageMapToColors()
color_map.SetLookupTable(lut)
color_map.SetInputConnection(luminance.GetOutputPort())

# Actor 1: original RGB image (left viewport)
actor_original = vtkImageActor()
actor_original.GetMapper().SetInputConnection(reader.GetOutputPort())

# Actor 2: false-color image (right viewport)
actor_colored = vtkImageActor()
actor_colored.GetMapper().SetInputConnection(color_map.GetOutputPort())

# Renderer 1: left viewport — original
renderer_left = vtkRenderer()
renderer_left.SetViewport(0.0, 0.0, 0.5, 1.0)
renderer_left.AddActor(actor_original)
renderer_left.SetBackground(black_rgb)

# Renderer 2: right viewport — false-color
renderer_right = vtkRenderer()
renderer_right.SetViewport(0.5, 0.0, 1.0, 1.0)
renderer_right.AddActor(actor_colored)
renderer_right.SetBackground(black_rgb)
renderer_right.SetActiveCamera(renderer_left.GetActiveCamera())

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer_left)
render_window.AddRenderer(renderer_right)
render_window.SetWindowName("map to colors")
render_window.SetMultiSamples(0)
render_window.SetSize(800, 400)

# Interactor: handle mouse and keyboard events with 2D image style
render_window_interactor = vtkRenderWindowInteractor()
interactor_style_image = vtkInteractorStyleImage()
render_window_interactor.SetInteractorStyle(interactor_style_image)
render_window_interactor.SetRenderWindow(render_window)

# Scene: configure parallel projection for 2D image viewing
renderer_left.ResetCamera()
renderer_left.GetActiveCamera().ParallelProjectionOn()

render_window_interactor.Initialize()
render_window_interactor.Start()
