#!/usr/bin/env python

# Demonstrate vtkSurfaceNets3D to extract a smooth isosurface from a
# procedural sinusoidal volume.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkFiltersCore import vtkSurfaceNets3D
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

# Source: procedural sinusoidal volume
source = vtkImageSinusoidSource()
source.SetWholeExtent(0, 63, 0, 63, 0, 63)
source.SetPeriod(30.0)
source.SetAmplitude(100)
source.Update()

# Filter: extract an isosurface using surface nets
surface_nets = vtkSurfaceNets3D()
surface_nets.SetInputConnection(source.GetOutputPort())
surface_nets.SetValue(0, 50.0)

# Mapper: map the isosurface to graphics primitives
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(surface_nets.GetOutputPort())
mapper.ScalarVisibilityOff()

# Actor: assign the mapped geometry
actor = vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetColor(cornflower_blue_rgb)

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(slate_gray_rgb)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(640, 480)
render_window.SetWindowName("SurfaceNets3D")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
