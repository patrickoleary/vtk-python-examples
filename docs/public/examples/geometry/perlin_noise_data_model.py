#!/usr/bin/env python
# Demonstrate a three-dimensional Perlin noise pattern.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonDataModel import vtkPerlinNoise
from vtkmodules.vtkFiltersCore import vtkContourFilter
from vtkmodules.vtkImagingHybrid import vtkSampleFunction
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Create Perlin noise implicit function.
perlin = vtkPerlinNoise()
perlin.SetFrequency(2, 1.25, 1.5)
perlin.SetPhase(0, 0, 0)

# Sample the implicit function.
sample = vtkSampleFunction()
sample.SetImplicitFunction(perlin)
sample.SetSampleDimensions(65, 65, 20)
sample.ComputeNormalsOff()

# Extract the zero-level isosurface.
surface = vtkContourFilter()
surface.SetInputConnection(sample.GetOutputPort())
surface.SetValue(0, 0.0)

# Mapper and actor.
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(surface.GetOutputPort())
mapper.ScalarVisibilityOff()

actor = vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetColor(0.2, 0.4, 0.6)

renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(1, 1, 1)

render_window = vtkRenderWindow()
render_window.SetSize(300, 300)
render_window.AddRenderer(renderer)
render_window.SetWindowName("perlin noise data model")

renderer.ResetCamera()
renderer.GetActiveCamera().Dolly(1.35)
renderer.ResetCameraClippingRange()

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
