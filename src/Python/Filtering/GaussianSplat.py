#!/usr/bin/env python

# Splat sphere surface points into a volume with vtkGaussianSplatter
# and extract an iso-surface with vtkContourFilter.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkCommonDataModel import vtkPolyData
from vtkmodules.vtkFiltersCore import vtkContourFilter
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkImagingHybrid import vtkGaussianSplatter
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
steel_blue_rgb = (0.275, 0.510, 0.706)

# Source: generate sphere surface points
sphere_source = vtkSphereSource()
sphere_source.Update()

polydata = vtkPolyData()
polydata.SetPoints(sphere_source.GetOutput().GetPoints())

# Filter: splat points into a 50x50x50 volume using Gaussian kernels
splatter = vtkGaussianSplatter()
splatter.SetInputData(polydata)
splatter.SetSampleDimensions(50, 50, 50)
splatter.SetRadius(0.5)
splatter.ScalarWarpingOff()

# Filter: extract an iso-surface from the splatted volume
surface = vtkContourFilter()
surface.SetInputConnection(splatter.GetOutputPort())
surface.SetValue(0, 0.01)

# Mapper: map the iso-surface to graphics primitives
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(surface.GetOutputPort())

# Actor: assign the mapped geometry
actor = vtkActor()
actor.SetMapper(mapper)

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(steel_blue_rgb)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(640, 480)
render_window.SetWindowName("GaussianSplat")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
