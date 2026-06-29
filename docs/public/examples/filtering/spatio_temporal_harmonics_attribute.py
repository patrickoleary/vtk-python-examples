#!/usr/bin/env python

# Demonstrate vtkSpatioTemporalHarmonicsAttribute by adding multiple
# harmonics to a sphere and rendering the result colored by the
# computed harmonic scalar field.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersGeneral import vtkSpatioTemporalHarmonicsAttribute
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkDataSetMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Create a sphere source
sphere = vtkSphereSource()
sphere.SetRadius(10)
sphere.SetPhiResolution(64)
sphere.SetThetaResolution(64)

# Apply spatio-temporal harmonics
harmonics = vtkSpatioTemporalHarmonicsAttribute()
harmonics.SetInputConnection(sphere.GetOutputPort())

harmonics.AddHarmonic(1.0, 1.0, 1.0, 0.0, 0.0, 0.0)
harmonics.AddHarmonic(2.0, 1.0, 0.0, 1.0, 0.0, 0.0)
harmonics.AddHarmonic(4.0, 1.0, 0.0, 0.0, 1.0, 0.0)

# Mapper and actor
mapper = vtkDataSetMapper()
mapper.SetInputConnection(harmonics.GetOutputPort())
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
render_window.SetSize(400, 400)
render_window.SetWindowName("spatio temporal harmonics attribute")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.ResetCamera()
renderer.GetActiveCamera().SetPosition(40.0, 30.0, 20.0)
renderer.GetActiveCamera().SetFocalPoint(0.0, 0.0, 0.0)
renderer.ResetCameraClippingRange()

interactor.Initialize()
interactor.Start()
