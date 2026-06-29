#!/usr/bin/env python

# Normalize a 3D gradient field from a sinusoidal source.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkImagingCore import vtkImageShiftScale
from vtkmodules.vtkImagingGeneral import (
    vtkImageGradient,
    vtkImageNormalize,
)
from vtkmodules.vtkImagingSources import vtkImageSinusoidSource
from vtkmodules.vtkRenderingCore import (
    vtkImageActor,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Sinusoidal source
sinusoid_source = vtkImageSinusoidSource()
sinusoid_source.SetWholeExtent(0, 225, 0, 225, 0, 20)
sinusoid_source.SetAmplitude(250)
sinusoid_source.SetDirection(1, 1, 1)
sinusoid_source.SetPeriod(20)
sinusoid_source.ReleaseDataFlagOff()

# Gradient
gradient = vtkImageGradient()
gradient.SetInputConnection(sinusoid_source.GetOutputPort())
gradient.SetDimensionality(3)

# Normalize
normalize = vtkImageNormalize()
normalize.SetInputConnection(gradient.GetOutputPort())
normalize.Update()

# Map normalized [-1,1] to [0,255] for display
shift_scale = vtkImageShiftScale()
shift_scale.SetInputConnection(normalize.GetOutputPort())
shift_scale.SetShift(1.0)
shift_scale.SetScale(127.5)
shift_scale.SetOutputScalarTypeToUnsignedChar()
shift_scale.ClampOverflowOn()
shift_scale.Update()

# Display with vtkImageActor at middle Z slice
image_actor = vtkImageActor()
image_actor.GetMapper().SetInputConnection(shift_scale.GetOutputPort())
ext = shift_scale.GetOutput().GetExtent()
z_mid = (ext[4] + ext[5]) // 2
image_actor.SetDisplayExtent(ext[0], ext[1], ext[2], ext[3], z_mid, z_mid)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(image_actor)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(256, 256)
render_window.SetWindowName("normalize")

# Scene
renderer.ResetCamera()

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
