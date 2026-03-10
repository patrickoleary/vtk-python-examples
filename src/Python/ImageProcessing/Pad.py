#!/usr/bin/env python

# Compare constant padding and mirror padding for reducing border
# artifacts during frequency-domain processing.  The left viewport
# shows constant-value padding; the right shows mirror padding.

import os
from pathlib import Path

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkIOImage import vtkMetaImageReader
from vtkmodules.vtkImagingColor import vtkImageMapToWindowLevelColors
from vtkmodules.vtkImagingCore import vtkImageConstantPad, vtkImageMirrorPad
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

# Reader: load the 3D medical volume
reader = vtkMetaImageReader()
reader.SetFileName(str(data_dir / "FullHead.mhd"))
reader.Update()

# Constant pad: pad with a constant value of 800
constant_pad = vtkImageConstantPad()
constant_pad.SetInputConnection(reader.GetOutputPort())
constant_pad.SetConstant(800)
constant_pad.SetOutputWholeExtent(-127, 383, -127, 383, 22, 22)

# Mirror pad: pad by reflecting pixels at the borders
mirror_pad = vtkImageMirrorPad()
mirror_pad.SetInputConnection(reader.GetOutputPort())
mirror_pad.SetOutputWholeExtent(constant_pad.GetOutputWholeExtent())

# Actor 1: constant pad (left viewport)
constant_color = vtkImageMapToWindowLevelColors()
constant_color.SetWindow(2000)
constant_color.SetLevel(1000)
constant_color.SetInputConnection(constant_pad.GetOutputPort())

actor_constant = vtkImageActor()
actor_constant.GetMapper().SetInputConnection(constant_color.GetOutputPort())
actor_constant.GetProperty().SetInterpolationTypeToNearest()

# Actor 2: mirror pad (right viewport)
mirror_color = vtkImageMapToWindowLevelColors()
mirror_color.SetWindow(2000)
mirror_color.SetLevel(1000)
mirror_color.SetInputConnection(mirror_pad.GetOutputPort())

actor_mirror = vtkImageActor()
actor_mirror.GetMapper().SetInputConnection(mirror_color.GetOutputPort())
actor_mirror.GetProperty().SetInterpolationTypeToNearest()

# Renderer 1: left viewport — constant padding
renderer_left = vtkRenderer()
renderer_left.SetViewport(0.0, 0.0, 0.5, 1.0)
renderer_left.AddActor(actor_constant)
renderer_left.ResetCamera()
renderer_left.SetBackground(black_rgb)

# Renderer 2: right viewport — mirror padding
renderer_right = vtkRenderer()
renderer_right.SetViewport(0.5, 0.0, 1.0, 1.0)
renderer_right.AddActor(actor_mirror)
renderer_right.SetActiveCamera(renderer_left.GetActiveCamera())
renderer_right.SetBackground(black_rgb)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.SetSize(600, 300)
render_window.SetWindowName("Pad")
render_window.AddRenderer(renderer_left)
render_window.AddRenderer(renderer_right)

# Interactor: handle mouse and keyboard events with 2D image style
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetInteractorStyle(vtkInteractorStyleImage())
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
