#!/usr/bin/env python

# Perform correlation in frequency domain using FFT multiply and inverse FFT.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkImagingCore import (
    vtkImageConstantPad,
    vtkImageExtractComponents,
)
from vtkmodules.vtkImagingFourier import (
    vtkImageFFT,
    vtkImageRFFT,
)
from vtkmodules.vtkImagingMath import vtkImageMathematics
from vtkmodules.vtkImagingSources import vtkImageCanvasSource2D
from vtkmodules.vtkRenderingCore import (
    vtkImageActor,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Large canvas with triangle
canvas_1 = vtkImageCanvasSource2D()
canvas_1.SetScalarTypeToFloat()
canvas_1.SetExtent(0, 255, 0, 255, 0, 0)
canvas_1.SetDrawColor(0)
canvas_1.FillBox(0, 255, 0, 255)
canvas_1.SetDrawColor(2.0)
canvas_1.FillTriangle(10, 100, 190, 150, 40, 250)

# Small canvas with triangle
canvas_2 = vtkImageCanvasSource2D()
canvas_2.SetScalarTypeToFloat()
canvas_2.SetExtent(0, 31, 0, 31, 0, 0)
canvas_2.SetDrawColor(0.0)
canvas_2.FillBox(0, 31, 0, 31)
canvas_2.SetDrawColor(2.0)
canvas_2.FillTriangle(10, 1, 25, 10, 1, 5)

# FFT of large image
fft1 = vtkImageFFT()
fft1.SetDimensionality(2)
fft1.SetInputConnection(canvas_1.GetOutputPort())
fft1.ReleaseDataFlagOff()
fft1.Update()

# Pad small kernel to same size, then FFT
pad2 = vtkImageConstantPad()
pad2.SetInputConnection(canvas_2.GetOutputPort())
pad2.SetOutputWholeExtent(0, 255, 0, 255, 0, 0)

fft2 = vtkImageFFT()
fft2.SetDimensionality(2)
fft2.SetInputConnection(pad2.GetOutputPort())
fft2.ReleaseDataFlagOff()
fft2.Update()

# Conjugate for correlation (not convolution)
conjugate = vtkImageMathematics()
conjugate.SetOperationToConjugate()
conjugate.SetInput1Data(fft2.GetOutput())
conjugate.Update()

# Complex multiply in frequency space
multiply = vtkImageMathematics()
multiply.SetOperationToComplexMultiply()
multiply.SetInput1Data(fft1.GetOutput())
multiply.SetInput2Data(conjugate.GetOutput())

# Inverse FFT
inverse_fft = vtkImageRFFT()
inverse_fft.SetDimensionality(2)
inverse_fft.SetInputConnection(multiply.GetOutputPort())

# Extract real component
extract_real = vtkImageExtractComponents()
extract_real.SetInputConnection(inverse_fft.GetOutputPort())
extract_real.SetComponents(0)
extract_real.Update()

# Display with vtkImageActor
image_actor = vtkImageActor()
image_actor.GetMapper().SetInputConnection(extract_real.GetOutputPort())

# Renderer
renderer = vtkRenderer()
renderer.AddActor(image_actor)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(256, 256)
render_window.SetWindowName("fft correlation")

# Scene
renderer.ResetCamera()

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
