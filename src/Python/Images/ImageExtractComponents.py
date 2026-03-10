#!/usr/bin/env python

# Extract individual R, G, B channels from a color image and display
# them in a 2x2 grid alongside the original using vtkImageExtractComponents.

import os
from pathlib import Path

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkIOImage import vtkJPEGReader
from vtkmodules.vtkImagingCore import vtkImageExtractComponents
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

# Reader: load a color JPEG image
reader = vtkJPEGReader()
reader.SetFileName(str(data_dir / "Gourds2.jpg"))
reader.Update()

# Extract red channel (component 0)
extract_red = vtkImageExtractComponents()
extract_red.SetInputConnection(reader.GetOutputPort())
extract_red.SetComponents(0)

# Extract green channel (component 1)
extract_green = vtkImageExtractComponents()
extract_green.SetInputConnection(reader.GetOutputPort())
extract_green.SetComponents(1)

# Extract blue channel (component 2)
extract_blue = vtkImageExtractComponents()
extract_blue.SetInputConnection(reader.GetOutputPort())
extract_blue.SetComponents(2)

# Actor 1: original color image (top-left)
actor_original = vtkImageActor()
actor_original.GetMapper().SetInputConnection(reader.GetOutputPort())

# Actor 2: red channel (top-right)
actor_red = vtkImageActor()
actor_red.GetMapper().SetInputConnection(extract_red.GetOutputPort())

# Actor 3: green channel (bottom-left)
actor_green = vtkImageActor()
actor_green.GetMapper().SetInputConnection(extract_green.GetOutputPort())

# Actor 4: blue channel (bottom-right)
actor_blue = vtkImageActor()
actor_blue.GetMapper().SetInputConnection(extract_blue.GetOutputPort())

# Renderer 1: top-left — original
renderer_tl = vtkRenderer()
renderer_tl.SetViewport(0.0, 0.5, 0.5, 1.0)
renderer_tl.AddActor(actor_original)
renderer_tl.SetBackground(black_rgb)
renderer_tl.ResetCamera()
renderer_tl.GetActiveCamera().ParallelProjectionOn()

# Renderer 2: top-right — red channel
renderer_tr = vtkRenderer()
renderer_tr.SetViewport(0.5, 0.5, 1.0, 1.0)
renderer_tr.AddActor(actor_red)
renderer_tr.SetBackground(black_rgb)
renderer_tr.SetActiveCamera(renderer_tl.GetActiveCamera())

# Renderer 3: bottom-left — green channel
renderer_bl = vtkRenderer()
renderer_bl.SetViewport(0.0, 0.0, 0.5, 0.5)
renderer_bl.AddActor(actor_green)
renderer_bl.SetBackground(black_rgb)
renderer_bl.SetActiveCamera(renderer_tl.GetActiveCamera())

# Renderer 4: bottom-right — blue channel
renderer_br = vtkRenderer()
renderer_br.SetViewport(0.5, 0.0, 1.0, 0.5)
renderer_br.AddActor(actor_blue)
renderer_br.SetBackground(black_rgb)
renderer_br.SetActiveCamera(renderer_tl.GetActiveCamera())

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer_tl)
render_window.AddRenderer(renderer_tr)
render_window.AddRenderer(renderer_bl)
render_window.AddRenderer(renderer_br)
render_window.SetSize(800, 600)
render_window.SetWindowName("ImageExtractComponents")

# Interactor: handle mouse and keyboard events with 2D image style
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetInteractorStyle(vtkInteractorStyleImage())
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
