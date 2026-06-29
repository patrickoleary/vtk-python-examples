#!/usr/bin/env python
# Demonstrate vtkTemporalFractal with shift/scale, interpolation, and threshold.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersCore import vtkThreshold
from vtkmodules.vtkFiltersGeometry import vtkCompositeDataGeometryFilter
from vtkmodules.vtkFiltersHybrid import (
    vtkTemporalInterpolator,
    vtkTemporalShiftScale,
)
from vtkmodules.vtkFiltersHybrid import vtkTemporalFractal
from vtkmodules.vtkCommonExecutionModel import vtkStreamingDemandDrivenPipeline
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Temporal fractal source
fractal = vtkTemporalFractal()
fractal.SetMaximumLevel(3)
fractal.DiscreteTimeStepsOn()
fractal.GenerateRectilinearGridsOn()

# Shift and scale the time range to run from -0.5 to 0.5
temp_ss = vtkTemporalShiftScale()
temp_ss.SetScale(0.1)
temp_ss.SetPostShift(-0.5)
temp_ss.SetInputConnection(fractal.GetOutputPort())

# Interpolate between time steps
interp = vtkTemporalInterpolator()
interp.SetInputConnection(temp_ss.GetOutputPort())

# Threshold to filter data
threshold = vtkThreshold()
threshold.SetInputConnection(interp.GetOutputPort())
threshold.SetThresholdFunction(vtkThreshold.THRESHOLD_UPPER)
threshold.SetUpperThreshold(0.5)

# Convert composite data to polydata
geom = vtkCompositeDataGeometryFilter()
geom.SetInputConnection(threshold.GetOutputPort())

mapper = vtkPolyDataMapper()
mapper.SetInputConnection(geom.GetOutputPort())

actor = vtkActor()
actor.SetMapper(mapper)

renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(0.5, 0.5, 0.5)

render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(300, 300)
render_window.SetWindowName("temporal fractal")

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Request specific time steps and render
geom.UpdateInformation()
info = geom.GetOutputInformation(0)

for i in range(10):
    time = i / 25.0 - 0.5
    info.Set(vtkStreamingDemandDrivenPipeline.UPDATE_TIME_STEP(), time)
    mapper.Modified()
    renderer.ResetCameraClippingRange()
    render_window.Render()

interactor.Initialize()
interactor.Start()
