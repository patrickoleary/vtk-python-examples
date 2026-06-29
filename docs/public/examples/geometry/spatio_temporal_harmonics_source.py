#!/usr/bin/env python

# Demonstrate vtkSpatioTemporalHarmonicsSource by creating a 3D image
# data source with multiple harmonics and time steps, rendered with
# a dataset mapper.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersSources import vtkSpatioTemporalHarmonicsSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkDataSetMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Create source with extent and harmonics
max_extent = 10
source = vtkSpatioTemporalHarmonicsSource()
source.SetWholeExtent(-max_extent, max_extent, -max_extent, max_extent, -max_extent, max_extent)

source.ClearHarmonics()
source.AddHarmonic(1.0, 1.0, 1.0, 0.0, 0.0, 0.0)
source.AddHarmonic(2.0, 1.0, 0.0, 1.0, 0.0, 0.0)
source.AddHarmonic(4.0, 1.0, 0.0, 0.0, 1.0, 0.0)

source.ClearTimeStepValues()
source.AddTimeStepValue(0.0)
source.AddTimeStepValue(1.0)
source.AddTimeStepValue(2.0)

source.Update()
source.UpdateTimeStep(1.0)
source.Update()

# Mapper
mapper = vtkDataSetMapper()
mapper.SetInputConnection(source.GetOutputPort())
mapper.SetScalarRange(-6.0, 6.0)

actor = vtkActor()
actor.SetMapper(mapper)

# Renderer
renderer = vtkRenderer()
renderer.SetBackground(0.5, 0.5, 0.5)
renderer.AddActor(actor)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("spatio temporal harmonics source")

# Scene
renderer.ResetCamera()
renderer.GetActiveCamera().SetPosition(50.0, 40.0, 30.0)
renderer.GetActiveCamera().SetFocalPoint(0.0, 0.0, 0.0)
renderer.ResetCameraClippingRange()

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
