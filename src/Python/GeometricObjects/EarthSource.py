#!/usr/bin/env python

# Render Earth continent outlines on a sphere using vtkEarthSource.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkFiltersHybrid import vtkEarthSource
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
black_rgb = (0.0, 0.0, 0.0)
peach_puff_rgb = (1.0, 0.855, 0.725)

# Source: generate Earth continent outlines
earth_source = vtkEarthSource()
earth_source.OutlineOn()
earth_source.Update()

# Source: generate a sphere matching the Earth source radius
sphere_source = vtkSphereSource()
sphere_source.SetThetaResolution(100)
sphere_source.SetPhiResolution(100)
sphere_source.SetRadius(earth_source.GetRadius())

# Mapper and actor: Earth outlines
earth_mapper = vtkPolyDataMapper()
earth_mapper.SetInputConnection(earth_source.GetOutputPort())

earth_actor = vtkActor()
earth_actor.SetMapper(earth_mapper)
earth_actor.GetProperty().SetColor(black_rgb)

# Mapper and actor: background sphere
sphere_mapper = vtkPolyDataMapper()
sphere_mapper.SetInputConnection(sphere_source.GetOutputPort())

sphere_actor = vtkActor()
sphere_actor.SetMapper(sphere_mapper)
sphere_actor.GetProperty().SetColor(peach_puff_rgb)

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.AddActor(earth_actor)
renderer.AddActor(sphere_actor)
renderer.SetBackground(black_rgb)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(640, 480)
render_window.SetWindowName("EarthSource")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
