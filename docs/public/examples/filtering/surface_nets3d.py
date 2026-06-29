#!/usr/bin/env python

# Demonstrate vtkSurfaceNets3D to extract a smooth isosurface from a
# procedural sinusoidal volume.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkFiltersCore import vtkPolyDataNormals, vtkSurfaceNets3D
from vtkmodules.vtkImagingCore import vtkImageThreshold
from vtkmodules.vtkImagingSources import vtkImageSinusoidSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
cornflower_blue_rgb = (0.392, 0.584, 0.929)
slate_gray_rgb = (0.439, 0.502, 0.565)

# Source: continuous scalar field
sinusoid_source = vtkImageSinusoidSource()
sinusoid_source.SetWholeExtent(0, 63, 0, 63, 0, 63)
sinusoid_source.SetPeriod(30.0)
sinusoid_source.SetAmplitude(100)
sinusoid_source.SetDirection(1, 1, 1)
sinusoid_source.Update()

# Filter: segment into a binary label map (values >= 50 -> label 1, else 0)
segment_threshold = vtkImageThreshold()
segment_threshold.SetInputConnection(sinusoid_source.GetOutputPort())
segment_threshold.ThresholdByUpper(50.0)
segment_threshold.SetInValue(1)
segment_threshold.SetOutValue(0)
segment_threshold.SetOutputScalarTypeToUnsignedChar()

# Filter: extract the label boundary using surface nets
surface_nets = vtkSurfaceNets3D()
surface_nets.SetInputConnection(segment_threshold.GetOutputPort())
surface_nets.SetValue(0, 1)

# Filter: generate normals for proper lighting
normals_filter = vtkPolyDataNormals()
normals_filter.SetInputConnection(surface_nets.GetOutputPort())

# Mapper: map the isosurface to graphics primitives
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(normals_filter.GetOutputPort())
mapper.ScalarVisibilityOff()

# Actor: assign the mapped geometry
actor = vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetColor(cornflower_blue_rgb)

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(slate_gray_rgb)

# Render window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("surface nets3d")
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
