#!/usr/bin/env python

# Warp an analytic wavelet image using vtkWarpScalar.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersGeneral import vtkWarpScalar
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

# Warp by scalar values
warp = vtkWarpScalar()
warp.SetInputConnection(wavelet.GetOutputPort())

mapper = vtkDataSetMapper()
mapper.SetInputConnection(warp.GetOutputPort())
mapper.SetScalarRange(75, 290)

actor = vtkActor()
actor.SetMapper(mapper)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(actor)

# Window
render_window = vtkRenderWindow()
render_window.SetMultiSamples(0)
render_window.AddRenderer(renderer)
render_window.SetSize(200, 200)
render_window.SetWindowName("warp scalar image")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.ResetCamera()
renderer.GetActiveCamera().Elevation(-10)

interactor.Initialize()
interactor.Start()
