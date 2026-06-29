#!/usr/bin/env python

# Test vtkTransformFilter on a wavelet source image data.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonTransforms import vtkTransform
from vtkmodules.vtkFiltersGeneral import vtkTransformFilter
from vtkmodules.vtkImagingCore import vtkRTAnalyticSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkDataSetMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Wavelet source
wavelet = vtkRTAnalyticSource()
wavelet.SetWholeExtent(-100, 100, -100, 100, 0, 0)
wavelet.SetCenter(0, 0, 0)
wavelet.SetMaximum(255)
wavelet.SetStandardDeviation(0.5)
wavelet.SetXFreq(60)
wavelet.SetYFreq(30)
wavelet.SetZFreq(40)
wavelet.SetXMag(10)
wavelet.SetYMag(18)
wavelet.SetZMag(5)
wavelet.SetSubsampleRate(1)

# Linear transform
transform = vtkTransform()
transform.RotateZ(35)

transform_filter = vtkTransformFilter()
transform_filter.SetInputConnection(wavelet.GetOutputPort())
transform_filter.SetTransform(transform)

mapper = vtkDataSetMapper()
mapper.SetInputConnection(transform_filter.GetOutputPort())
mapper.SetScalarRange(75, 290)

actor = vtkActor()
actor.SetMapper(mapper)

renderer = vtkRenderer()
renderer.AddActor(actor)

render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("transform imagedata")
render_window.SetMultiSamples(0)
render_window.SetSize(200, 200)

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.ResetCamera()

interactor.Initialize()
interactor.Start()
