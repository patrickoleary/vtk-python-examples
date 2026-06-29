#!/usr/bin/env python

# Apply vtkMaskPoints with three different modes (default, uniform
# spatial volume, uniform spatial bounds) and overlay the results.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersCore import vtkMaskPoints
from vtkmodules.vtkImagingCore import vtkRTAnalyticSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkDataSetMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Source: wavelet dataset
wavelet = vtkRTAnalyticSource()
wavelet.SetWholeExtent(-10, 10, -10, 10, -10, 10)
wavelet.SetCenter(0.0, 0.0, 0.0)
wavelet.Update()

# Default mode: contiguous points
mask_default = vtkMaskPoints()
mask_default.SetInputConnection(wavelet.GetOutputPort())
mask_default.SetRandomMode(False)
mask_default.SetMaximumNumberOfPoints(100)
mask_default.GenerateVerticesOn()

# Uniform spatial volume mode
mask_volume = vtkMaskPoints()
mask_volume.SetInputConnection(wavelet.GetOutputPort())
mask_volume.SetRandomMode(True)
mask_volume.SetRandomModeType(2)  # UNIFORM_SPATIAL_VOLUME
mask_volume.SetRandomSeed(12)
mask_volume.SetMaximumNumberOfPoints(100)
mask_volume.GenerateVerticesOn()

# Uniform spatial bounds mode
mask_bounds = vtkMaskPoints()
mask_bounds.SetInputConnection(wavelet.GetOutputPort())
mask_bounds.SetRandomMode(True)
mask_bounds.SetRandomModeType(3)  # UNIFORM_SPATIAL_BOUNDS
mask_bounds.SetRandomSeed(12)
mask_bounds.SetMaximumNumberOfPoints(100)
mask_bounds.GenerateVerticesOn()

# Mapper and actor for default mode (red)
mapper_default = vtkDataSetMapper()
mapper_default.SetInputConnection(mask_default.GetOutputPort())
mapper_default.ScalarVisibilityOff()

actor_default = vtkActor()
actor_default.SetMapper(mapper_default)
actor_default.GetProperty().SetOpacity(0.5)
actor_default.GetProperty().SetPointSize(3)
actor_default.GetProperty().SetColor(1, 0, 0)

# Mapper and actor for volume mode (green)
mapper_volume = vtkDataSetMapper()
mapper_volume.SetInputConnection(mask_volume.GetOutputPort())
mapper_volume.ScalarVisibilityOff()

actor_volume = vtkActor()
actor_volume.SetMapper(mapper_volume)
actor_volume.GetProperty().SetOpacity(0.5)
actor_volume.GetProperty().SetPointSize(5)
actor_volume.GetProperty().SetColor(0, 1, 0)

# Mapper and actor for bounds mode (blue)
mapper_bounds = vtkDataSetMapper()
mapper_bounds.SetInputConnection(mask_bounds.GetOutputPort())
mapper_bounds.ScalarVisibilityOff()

actor_bounds = vtkActor()
actor_bounds.SetMapper(mapper_bounds)
actor_bounds.GetProperty().SetOpacity(0.5)
actor_bounds.GetProperty().SetPointSize(7)
actor_bounds.GetProperty().SetColor(0, 0, 1)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(actor_default)
renderer.AddActor(actor_volume)
renderer.AddActor(actor_bounds)

# Window
render_window = vtkRenderWindow()
render_window.SetSize(300, 300)
render_window.AddRenderer(renderer)
render_window.SetWindowName("mask points modes")

# Scene
renderer.ResetCamera()

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
