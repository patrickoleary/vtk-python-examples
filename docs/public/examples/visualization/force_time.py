#!/usr/bin/env python
# Demonstrate vtkForceTime to override pipeline time on a wavelet source.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersGeneral import vtkDataSetTriangleFilter
from vtkmodules.vtkFiltersHybrid import vtkForceTime
from vtkmodules.vtkImagingCore import vtkRTAnalyticSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkDataSetMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Wavelet source (stand-in for temporal source)
wavelet = vtkRTAnalyticSource()

# Tetrahedralize for unstructured grid display
tetrahedralize = vtkDataSetTriangleFilter()
tetrahedralize.SetInputConnection(wavelet.GetOutputPort())

# Force a specific time step
force_time = vtkForceTime()
force_time.SetInputConnection(tetrahedralize.GetOutputPort())
force_time.SetForcedTime(1)
force_time.IgnorePipelineTimeOn()

mapper = vtkDataSetMapper()
mapper.SetInputConnection(force_time.GetOutputPort())
mapper.SetScalarRange(0, 30)

actor = vtkActor()
actor.SetMapper(mapper)

renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(0.3, 0.6, 0.3)

render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("force time")

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
