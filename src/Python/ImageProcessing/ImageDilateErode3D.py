#!/usr/bin/env python

# Apply morphological dilation and erosion to a binary image using
# vtkImageDilateErode3D and display original, dilated, and eroded
# images in a 3-viewport layout.

import os
from pathlib import Path

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkIOImage import vtkPNMReader
from vtkmodules.vtkImagingMorphological import vtkImageDilateErode3D
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

# Reader: load a binary PGM image
reader = vtkPNMReader()
reader.SetFileName(str(data_dir / "binary.pgm"))

# Dilate: expand bright regions (dilate=255, erode=0)
dilate = vtkImageDilateErode3D()
dilate.SetInputConnection(reader.GetOutputPort())
dilate.SetKernelSize(9, 9, 1)
dilate.SetDilateValue(255)
dilate.SetErodeValue(0)

# Erode: shrink bright regions (dilate=0, erode=255)
erode = vtkImageDilateErode3D()
erode.SetInputConnection(reader.GetOutputPort())
erode.SetKernelSize(9, 9, 1)
erode.SetDilateValue(0)
erode.SetErodeValue(255)

# Actor 1: original image (left viewport)
actor_original = vtkImageActor()
actor_original.GetMapper().SetInputConnection(reader.GetOutputPort())

# Actor 2: dilated image (center viewport)
actor_dilated = vtkImageActor()
actor_dilated.GetMapper().SetInputConnection(dilate.GetOutputPort())

# Actor 3: eroded image (right viewport)
actor_eroded = vtkImageActor()
actor_eroded.GetMapper().SetInputConnection(erode.GetOutputPort())

# Renderer 1: left viewport — original
renderer_left = vtkRenderer()
renderer_left.SetViewport(0.0, 0.0, 0.333, 1.0)
renderer_left.AddActor(actor_original)
renderer_left.SetBackground(black_rgb)
renderer_left.ResetCamera()
renderer_left.GetActiveCamera().ParallelProjectionOn()

# Renderer 2: center viewport — dilated
renderer_center = vtkRenderer()
renderer_center.SetViewport(0.333, 0.0, 0.667, 1.0)
renderer_center.AddActor(actor_dilated)
renderer_center.SetBackground(black_rgb)
renderer_center.SetActiveCamera(renderer_left.GetActiveCamera())

# Renderer 3: right viewport — eroded
renderer_right = vtkRenderer()
renderer_right.SetViewport(0.667, 0.0, 1.0, 1.0)
renderer_right.AddActor(actor_eroded)
renderer_right.SetBackground(black_rgb)
renderer_right.SetActiveCamera(renderer_left.GetActiveCamera())

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer_left)
render_window.AddRenderer(renderer_center)
render_window.AddRenderer(renderer_right)
render_window.SetSize(900, 300)
render_window.SetWindowName("ImageDilateErode3D")

# Interactor: handle mouse and keyboard events with 2D image style
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetInteractorStyle(vtkInteractorStyleImage())
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
