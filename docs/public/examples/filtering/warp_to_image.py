#!/usr/bin/env python

# Warp an analytic wavelet image toward a point using vtkWarpTo.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersGeneral import vtkWarpTo
from vtkmodules.vtkImagingCore import vtkRTAnalyticSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkDataSetMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Generate wavelet data
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

# Warp toward a point
warp = vtkWarpTo()
warp.SetInputConnection(wavelet.GetOutputPort())
warp.SetScaleFactor(0)
warp.SetPosition(0, 0, 0)

mapper = vtkDataSetMapper()
mapper.SetInputConnection(warp.GetOutputPort())
mapper.SetScalarRange(75, 290)

actor = vtkActor()
actor.SetMapper(mapper)

# Update warp parameters
warp.SetScaleFactor(0.25)
warp.SetPosition(75, 75, 0)
warp.Update()

# Renderer
renderer = vtkRenderer()
renderer.AddActor(actor)

# Window
render_window = vtkRenderWindow()
render_window.SetMultiSamples(0)
render_window.AddRenderer(renderer)
render_window.SetSize(200, 200)
render_window.SetWindowName("warp to image")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.ResetCamera()

interactor.Initialize()
interactor.Start()
