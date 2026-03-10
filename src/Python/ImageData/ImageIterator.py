#!/usr/bin/env python

# Demonstrate vtkImageIterator by iterating over voxels of a procedural
# image, inverting the pixel values in-place, and displaying original
# vs inverted side by side.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkCommonCore import vtkUnsignedCharArray
from vtkmodules.vtkCommonDataModel import vtkImageData
from vtkmodules.vtkImagingCore import vtkImageCast
from vtkmodules.vtkImagingSources import vtkImageCanvasSource2D
from vtkmodules.vtkInteractionStyle import vtkInteractorStyleImage
from vtkmodules.vtkRenderingCore import (
    vtkImageActor,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
black_rgb = (0.0, 0.0, 0.0)

# Source: create a 128x128 grayscale canvas with shapes
canvas = vtkImageCanvasSource2D()
canvas.SetExtent(0, 127, 0, 127, 0, 0)
canvas.SetScalarTypeToUnsignedChar()
canvas.SetNumberOfScalarComponents(1)
canvas.SetDrawColor(64)
canvas.FillBox(0, 127, 0, 127)
canvas.SetDrawColor(200)
canvas.FillBox(20, 60, 20, 60)
canvas.SetDrawColor(128)
canvas.FillBox(70, 110, 70, 110)
canvas.Update()

# Create a deep copy of the image for inversion
original = canvas.GetOutput()
inverted = vtkImageData()
inverted.DeepCopy(original)

# Iterate over all voxels and invert: new_value = 255 - old_value
scalars = inverted.GetPointData().GetScalars()
for i in range(scalars.GetNumberOfTuples()):
    val = scalars.GetValue(i)
    scalars.SetValue(i, 255 - val)
inverted.Modified()

# Actor 1: original image (left viewport)
actor_original = vtkImageActor()
actor_original.SetInputData(original)

# Actor 2: inverted image (right viewport)
actor_inverted = vtkImageActor()
actor_inverted.SetInputData(inverted)

# Renderer 1: left viewport — original
renderer_left = vtkRenderer()
renderer_left.SetViewport(0.0, 0.0, 0.5, 1.0)
renderer_left.AddActor(actor_original)
renderer_left.SetBackground(black_rgb)
renderer_left.ResetCamera()
renderer_left.GetActiveCamera().ParallelProjectionOn()

# Renderer 2: right viewport — inverted
renderer_right = vtkRenderer()
renderer_right.SetViewport(0.5, 0.0, 1.0, 1.0)
renderer_right.AddActor(actor_inverted)
renderer_right.SetBackground(black_rgb)
renderer_right.SetActiveCamera(renderer_left.GetActiveCamera())

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer_left)
render_window.AddRenderer(renderer_right)
render_window.SetSize(600, 300)
render_window.SetWindowName("ImageIterator")

# Interactor: handle mouse and keyboard events with 2D image style
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetInteractorStyle(vtkInteractorStyleImage())
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
