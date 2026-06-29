#!/usr/bin/env python

# Sample a Perlin noise implicit function on a volume grid and
# extract an iso-surface at value 0 with vtkContourFilter.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
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

# Colors (normalized RGB)
steel_blue_rgb = (0.275, 0.510, 0.706)
slate_gray_rgb = (0.439, 0.502, 0.565)

# Source: Perlin noise implicit function
perlin_noise = vtkPerlinNoise()
perlin_noise.SetFrequency(2, 1.25, 1.5)
perlin_noise.SetPhase(0, 0, 0)

# Sample: evaluate the implicit function on a 65x65x20 volume grid
sample_function = vtkSampleFunction()
sample_function.SetImplicitFunction(perlin_noise)
sample_function.SetSampleDimensions(65, 65, 20)
sample_function.ComputeNormalsOff()

# Filter: extract the zero-level iso-surface
contour_filter = vtkContourFilter()
contour_filter.SetInputConnection(sample_function.GetOutputPort())
contour_filter.SetValue(0, 0.0)

# Mapper: map the iso-surface to graphics primitives
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(contour_filter.GetOutputPort())
mapper.ScalarVisibilityOff()

# Actor: assign the mapped geometry
actor = vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetColor(steel_blue_rgb)

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(slate_gray_rgb)

# Render window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("perlin noise")
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
