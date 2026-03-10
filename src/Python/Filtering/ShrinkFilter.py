#!/usr/bin/env python

# Shrink the cells of a sphere toward their centroids using
# vtkShrinkPolyData, revealing the individual polygonal faces.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkFiltersGeneral import vtkShrinkPolyData
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
peach_puff_rgb = (1.0, 0.855, 0.725)
background_rgb = (0.2, 0.3, 0.4)

# Source: generate a sphere
sphere_source = vtkSphereSource()
sphere_source.SetThetaResolution(30)
sphere_source.SetPhiResolution(30)

# Filter: shrink each cell toward its centroid by 50%
shrink = vtkShrinkPolyData()
shrink.SetInputConnection(sphere_source.GetOutputPort())
shrink.SetShrinkFactor(0.5)

# Mapper: map the shrunk cells to graphics primitives
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(shrink.GetOutputPort())

# Actor: assign the mapped geometry with visible edges
actor = vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetColor(peach_puff_rgb)
actor.GetProperty().EdgeVisibilityOn()

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(background_rgb)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(640, 480)
render_window.SetWindowName("ShrinkFilter")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
