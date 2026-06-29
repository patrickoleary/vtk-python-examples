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
elevation_filter = vtkElevationFilter()
elevation_filter.SetInputConnection(sphere_source.GetOutputPort())
elevation_filter.SetLowPoint(0, -1, 0)
elevation_filter.SetHighPoint(0, 1, 0)

# Filter: threshold to keep cells in the middle elevation band
threshold_filter = vtkThreshold()
threshold_filter.SetInputConnection(elevation_filter.GetOutputPort())
threshold_filter.SetThresholdFunction(threshold_filter.THRESHOLD_BETWEEN)
threshold_filter.SetLowerThreshold(0.3)
threshold_filter.SetUpperThreshold(0.7)

# Mapper: map the thresholded cells to graphics primitives
mapper = vtkDataSetMapper()
mapper.SetInputConnection(threshold_filter.GetOutputPort())
mapper.SetScalarRange(0.3, 0.7)

# Actor: assign the mapped geometry
actor = vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().EdgeVisibilityOn()

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(background_rgb)

# Render window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("threshold3D")
render_window.SetMultiSamples(0)
render_window.SetSize(640, 480)

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Scene: configure the camera
renderer.ResetCamera()

# Start: launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
