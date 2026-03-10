#!/usr/bin/env python

# Demonstrate various binary morphological filters that can alter the
# shape of segmented regions.  Six viewports (2×3 grid): original,
# connectivity, erosion, dilation, opening, closing.

import os
from pathlib import Path

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkIOImage import vtkPNMReader
from vtkmodules.vtkImagingMorphological import (
    vtkImageDilateErode3D,
    vtkImageSeedConnectivity,
)
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

# Reader: load the binary PGM image
reader = vtkPNMReader()
reader.SetFileName(str(data_dir / "binary.pgm"))
reader.Update()

# Dilate: grow dark (0) regions into light (255)
dilate = vtkImageDilateErode3D()
dilate.SetInputConnection(reader.GetOutputPort())
dilate.SetDilateValue(0)
dilate.SetErodeValue(255)
dilate.SetKernelSize(31, 31, 1)

# Erode: grow light (255) regions into dark (0)
erode = vtkImageDilateErode3D()
erode.SetInputConnection(reader.GetOutputPort())
erode.SetDilateValue(255)
erode.SetErodeValue(0)
erode.SetKernelSize(31, 31, 1)

# Opening: dilate then erode — removes small islands
open_dilate = vtkImageDilateErode3D()
open_dilate.SetInputConnection(reader.GetOutputPort())
open_dilate.SetDilateValue(0)
open_dilate.SetErodeValue(255)
open_dilate.SetKernelSize(31, 31, 1)

open_erode = vtkImageDilateErode3D()
open_erode.SetInputConnection(open_dilate.GetOutputPort())
open_erode.SetDilateValue(255)
open_erode.SetErodeValue(0)
open_erode.SetKernelSize(31, 31, 1)

# Closing: erode then dilate — fills small holes
close_erode = vtkImageDilateErode3D()
close_erode.SetInputConnection(reader.GetOutputPort())
close_erode.SetDilateValue(255)
close_erode.SetErodeValue(0)
close_erode.SetKernelSize(31, 31, 1)

close_dilate = vtkImageDilateErode3D()
close_dilate.SetInputConnection(close_erode.GetOutputPort())
close_dilate.SetDilateValue(0)
close_dilate.SetErodeValue(255)
close_dilate.SetKernelSize(31, 31, 1)

# Connectivity: extract the connected region touching a seed point
connectivity = vtkImageSeedConnectivity()
connectivity.SetInputConnection(reader.GetOutputPort())
connectivity.AddSeed(300, 200)
connectivity.SetInputConnectValue(0)
connectivity.SetOutputConnectedValue(0)
connectivity.SetOutputUnconnectedValue(255)

# Actor 1: original
actor_original = vtkImageActor()
actor_original.GetMapper().SetInputConnection(reader.GetOutputPort())
actor_original.GetProperty().SetInterpolationTypeToNearest()

# Actor 2: connectivity
actor_connected = vtkImageActor()
actor_connected.GetMapper().SetInputConnection(connectivity.GetOutputPort())
actor_connected.GetProperty().SetInterpolationTypeToNearest()

# Actor 3: erosion
actor_erode = vtkImageActor()
actor_erode.GetMapper().SetInputConnection(erode.GetOutputPort())
actor_erode.GetProperty().SetInterpolationTypeToNearest()

# Actor 4: dilation
actor_dilate = vtkImageActor()
actor_dilate.GetMapper().SetInputConnection(dilate.GetOutputPort())
actor_dilate.GetProperty().SetInterpolationTypeToNearest()

# Actor 5: opening
actor_opening = vtkImageActor()
actor_opening.GetMapper().SetInputConnection(close_dilate.GetOutputPort())
actor_opening.GetProperty().SetInterpolationTypeToNearest()

# Actor 6: closing
actor_closing = vtkImageActor()
actor_closing.GetMapper().SetInputConnection(open_erode.GetOutputPort())
actor_closing.GetProperty().SetInterpolationTypeToNearest()

# Renderer 1: top-left — original
renderer_0 = vtkRenderer()
renderer_0.AddActor(actor_original)
renderer_0.SetViewport(0.0, 0.667, 0.5, 1.0)
renderer_0.SetBackground(black_rgb)
renderer_0.ResetCamera()

# Renderer 2: top-right — connectivity
renderer_1 = vtkRenderer()
renderer_1.AddActor(actor_connected)
renderer_1.SetViewport(0.5, 0.667, 1.0, 1.0)
renderer_1.SetBackground(black_rgb)
renderer_1.SetActiveCamera(renderer_0.GetActiveCamera())

# Renderer 3: middle-left — erosion
renderer_2 = vtkRenderer()
renderer_2.AddActor(actor_erode)
renderer_2.SetViewport(0.0, 0.333, 0.5, 0.667)
renderer_2.SetBackground(black_rgb)
renderer_2.SetActiveCamera(renderer_0.GetActiveCamera())

# Renderer 4: middle-right — dilation
renderer_3 = vtkRenderer()
renderer_3.AddActor(actor_dilate)
renderer_3.SetViewport(0.5, 0.333, 1.0, 0.667)
renderer_3.SetBackground(black_rgb)
renderer_3.SetActiveCamera(renderer_0.GetActiveCamera())

# Renderer 5: bottom-left — opening
renderer_4 = vtkRenderer()
renderer_4.AddActor(actor_opening)
renderer_4.SetViewport(0.0, 0.0, 0.5, 0.333)
renderer_4.SetBackground(black_rgb)
renderer_4.SetActiveCamera(renderer_0.GetActiveCamera())

# Renderer 6: bottom-right — closing
renderer_5 = vtkRenderer()
renderer_5.AddActor(actor_closing)
renderer_5.SetViewport(0.5, 0.0, 1.0, 0.333)
renderer_5.SetBackground(black_rgb)
renderer_5.SetActiveCamera(renderer_0.GetActiveCamera())

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.SetSize(600, 900)
render_window.AddRenderer(renderer_0)
render_window.AddRenderer(renderer_1)
render_window.AddRenderer(renderer_2)
render_window.AddRenderer(renderer_3)
render_window.AddRenderer(renderer_4)
render_window.AddRenderer(renderer_5)
render_window.SetWindowName("MorphologyComparison")

# Interactor: handle mouse and keyboard events with 2D image style
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetInteractorStyle(vtkInteractorStyleImage())
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
