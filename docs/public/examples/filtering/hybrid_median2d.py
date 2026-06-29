#!/usr/bin/env python

# Apply hybrid median filter to remove shot noise from a canvas image.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkImagingCore import vtkImageThreshold
from vtkmodules.vtkImagingGeneral import (
    vtkImageHybridMedian2D,
    vtkImageMedian3D,
)
from vtkmodules.vtkImagingMath import vtkImageMathematics
from vtkmodules.vtkImagingSources import (
    vtkImageCanvasSource2D,
    vtkImageNoiseSource,
)
from vtkmodules.vtkRenderingCore import (
    vtkImageActor,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Draw a pattern on canvas
image_canvas = vtkImageCanvasSource2D()
image_canvas.SetScalarTypeToDouble()
image_canvas.SetExtent(1, 256, 1, 256, 0, 0)
image_canvas.SetDrawColor(0)
image_canvas.FillBox(1, 256, 1, 256)
image_canvas.SetDrawColor(255)
image_canvas.FillBox(30, 225, 30, 225)
image_canvas.SetDrawColor(0)
image_canvas.FillBox(60, 195, 60, 195)
image_canvas.SetDrawColor(255)
image_canvas.FillTube(100, 100, 154, 154, 40.0)
image_canvas.SetDrawColor(0)
image_canvas.DrawSegment(45, 45, 45, 210)
image_canvas.DrawSegment(45, 210, 210, 210)
image_canvas.DrawSegment(210, 210, 210, 45)
image_canvas.DrawSegment(210, 45, 45, 45)
image_canvas.DrawSegment(100, 150, 150, 100)
image_canvas.DrawSegment(110, 160, 160, 110)
image_canvas.DrawSegment(90, 140, 140, 90)
image_canvas.DrawSegment(120, 170, 170, 120)
image_canvas.DrawSegment(80, 130, 130, 80)
image_canvas.Update()

shot_noise_amplitude = 255.0
shot_noise_fraction = 0.1

# Generate noise
shot_noise_source = vtkImageNoiseSource()
shot_noise_source.SetWholeExtent(1, 256, 1, 256, 0, 0)
shot_noise_source.SetMinimum(0.0)
shot_noise_source.SetMaximum(1.0)
shot_noise_source.ReleaseDataFlagOff()

# Positive shot noise
shot_noise_thresh1 = vtkImageThreshold()
shot_noise_thresh1.SetInputConnection(shot_noise_source.GetOutputPort())
shot_noise_thresh1.ThresholdByLower(1.0 - shot_noise_fraction)
shot_noise_thresh1.SetInValue(0)
shot_noise_thresh1.ReplaceInOn()
shot_noise_thresh1.ReplaceOutOn()
shot_noise_thresh1.SetOutValue(shot_noise_amplitude)
shot_noise_thresh1.Update()

# Negative shot noise
shot_noise_thresh2 = vtkImageThreshold()
shot_noise_thresh2.SetInputConnection(shot_noise_source.GetOutputPort())
shot_noise_thresh2.ThresholdByLower(shot_noise_fraction)
shot_noise_thresh2.SetInValue(-shot_noise_amplitude)
shot_noise_thresh2.SetOutValue(0.0)
shot_noise_thresh2.ReplaceInOn()
shot_noise_thresh2.ReplaceOutOn()
shot_noise_thresh2.Update()

# Combine noise
shot_noise = vtkImageMathematics()
shot_noise.SetInput1Data(shot_noise_thresh1.GetOutput())
shot_noise.SetInput2Data(shot_noise_thresh2.GetOutput())
shot_noise.SetOperationToAdd()
shot_noise.Update()

# Add noise to canvas
add = vtkImageMathematics()
add.SetInput1Data(shot_noise.GetOutput())
add.SetInput2Data(image_canvas.GetOutput())
add.SetOperationToAdd()

# Apply hybrid median filter
hybrid1 = vtkImageHybridMedian2D()
hybrid1.SetInputConnection(add.GetOutputPort())
hybrid1.Update()

# Display with vtkImageActor
image_actor = vtkImageActor()
image_actor.GetMapper().SetInputConnection(hybrid1.GetOutputPort())

# Renderer
renderer = vtkRenderer()
renderer.AddActor(image_actor)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(256, 256)
render_window.SetWindowName("hybrid median2d")

# Scene
renderer.ResetCamera()

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
