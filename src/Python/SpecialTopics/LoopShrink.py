#!/usr/bin/env python

# Shrink the cells of a sphere and color by elevation.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkFiltersCore import vtkElevationFilter
from vtkmodules.vtkFiltersGeneral import vtkShrinkFilter
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkDataSetMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
lavender_blush_rgb = (1.0, 0.941, 0.961)

# Source: generate sphere polygon data
sphere = vtkSphereSource()
sphere.SetThetaResolution(12)
sphere.SetPhiResolution(12)

# ShrinkFilter: pull each cell inward by a factor of 0.9
shrink = vtkShrinkFilter()
shrink.SetInputConnection(sphere.GetOutputPort())
shrink.SetShrinkFactor(0.9)

# ElevationFilter: color cells by height (z-axis)
color_it = vtkElevationFilter()
color_it.SetInputConnection(shrink.GetOutputPort())
color_it.SetLowPoint(0, 0, -0.5)
color_it.SetHighPoint(0, 0, 0.5)

# Mapper: map data set to graphics primitives
mapper = vtkDataSetMapper()
mapper.SetInputConnection(color_it.GetOutputPort())

# Actor: assign the mapped geometry
actor = vtkActor()
actor.SetMapper(mapper)

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.GetCullers().RemoveAllItems()
renderer.AddActor(actor)
renderer.SetBackground(lavender_blush_rgb)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.SetSize(600, 600)
render_window.SetWindowName("LoopShrink")
render_window.AddRenderer(renderer)

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

render_window.Render()
renderer.GetActiveCamera().Zoom(1.5)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
