#!/usr/bin/env python
# Demonstrate vtkTemporalStatistics on temporal fractal data in four viewports.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersGeometry import vtkCompositeDataGeometryFilter
from vtkmodules.vtkFiltersGeneral import vtkTemporalStatistics
from vtkmodules.vtkFiltersHybrid import vtkTemporalFractal
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Temporal fractal source
source = vtkTemporalFractal()
source.SetMaximumLevel(3)
source.DiscreteTimeStepsOn()
source.AdaptiveSubdivisionOff()

# Compute temporal statistics
statistics = vtkTemporalStatistics()
statistics.SetInputConnection(source.GetOutputPort())

# Convert composite data to polydata for rendering
geometry = vtkCompositeDataGeometryFilter()
geometry.SetInputConnection(statistics.GetOutputPort())

# -- Mappers (four viewports: average, minimum, maximum, stddev) --
mapper_0 = vtkPolyDataMapper()
mapper_0.SetInputConnection(geometry.GetOutputPort())
mapper_0.SetScalarModeToUseCellFieldData()
mapper_0.SelectColorArray("Fractal Volume Fraction_average")

mapper_1 = vtkPolyDataMapper()
mapper_1.SetInputConnection(geometry.GetOutputPort())
mapper_1.SetScalarModeToUseCellFieldData()
mapper_1.SelectColorArray("Fractal Volume Fraction_minimum")

mapper_2 = vtkPolyDataMapper()
mapper_2.SetInputConnection(geometry.GetOutputPort())
mapper_2.SetScalarModeToUseCellFieldData()
mapper_2.SelectColorArray("Fractal Volume Fraction_maximum")

mapper_3 = vtkPolyDataMapper()
mapper_3.SetInputConnection(geometry.GetOutputPort())
mapper_3.SetScalarModeToUseCellFieldData()
mapper_3.SelectColorArray("Fractal Volume Fraction_stddev")

# -- Actors --
actor_0 = vtkActor()
actor_0.SetMapper(mapper_0)

actor_1 = vtkActor()
actor_1.SetMapper(mapper_1)

actor_2 = vtkActor()
actor_2.SetMapper(mapper_2)

actor_3 = vtkActor()
actor_3.SetMapper(mapper_3)

# -- Renderers --
renderer_0 = vtkRenderer()
renderer_0.SetViewport(0.0, 0.5, 0.5, 1.0)
renderer_0.SetBackground(0.5, 0.5, 0.5)
renderer_0.AddActor(actor_0)

renderer_1 = vtkRenderer()
renderer_1.SetViewport(0.5, 0.5, 1.0, 1.0)
renderer_1.SetBackground(0.5, 0.5, 0.5)
renderer_1.AddActor(actor_1)

renderer_2 = vtkRenderer()
renderer_2.SetViewport(0.0, 0.0, 0.5, 0.5)
renderer_2.SetBackground(0.5, 0.5, 0.5)
renderer_2.AddActor(actor_2)

renderer_3 = vtkRenderer()
renderer_3.SetViewport(0.5, 0.0, 1.0, 0.5)
renderer_3.SetBackground(0.5, 0.5, 0.5)
renderer_3.AddActor(actor_3)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer_0)
render_window.AddRenderer(renderer_1)
render_window.AddRenderer(renderer_2)
render_window.AddRenderer(renderer_3)
render_window.SetSize(450, 400)
render_window.SetWindowName("hybrid temporal statistics")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer_0.ResetCamera()
renderer_0.GetActiveCamera().Zoom(1.5)
renderer_1.ResetCamera()
renderer_1.GetActiveCamera().Zoom(1.5)
renderer_2.ResetCamera()
renderer_2.GetActiveCamera().Zoom(1.5)
renderer_3.ResetCamera()
renderer_3.GetActiveCamera().Zoom(1.5)

interactor.Initialize()
interactor.Start()
