#!/usr/bin/env python

# Generate a sphere with elevation scalars, then extract cells within
# a scalar range using vtkThreshold to keep only a horizontal band.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkFiltersCore import vtkElevationFilter
from vtkmodules.vtkFiltersCore import vtkThreshold
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkDataSetMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
background_rgb = (0.2, 0.2, 0.3)

# Source: generate a high-resolution sphere
sphere_source = vtkSphereSource()
sphere_source.SetThetaResolution(40)
sphere_source.SetPhiResolution(40)

# Filter: add elevation scalars (height along Y axis)
elevation = vtkElevationFilter()
elevation.SetInputConnection(sphere_source.GetOutputPort())
elevation.SetLowPoint(0, -1, 0)
elevation.SetHighPoint(0, 1, 0)

# Filter: threshold to keep cells in the middle elevation band
threshold = vtkThreshold()
threshold.SetInputConnection(elevation.GetOutputPort())
threshold.SetThresholdFunction(threshold.THRESHOLD_BETWEEN)
threshold.SetLowerThreshold(0.3)
threshold.SetUpperThreshold(0.7)

# Mapper: map the thresholded cells to graphics primitives
mapper = vtkDataSetMapper()
mapper.SetInputConnection(threshold.GetOutputPort())
mapper.SetScalarRange(0.3, 0.7)

# Actor: assign the mapped geometry
actor = vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().EdgeVisibilityOn()

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(background_rgb)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(640, 480)
render_window.SetWindowName("ThresholdFilter")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
