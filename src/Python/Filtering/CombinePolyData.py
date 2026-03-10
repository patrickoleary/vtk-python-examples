#!/usr/bin/env python

# Combine a sphere and a cone into a single polydata using
# vtkAppendPolyData, then clean duplicate points with vtkCleanPolyData.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkFiltersCore import (
    vtkAppendPolyData,
    vtkCleanPolyData,
)
from vtkmodules.vtkFiltersSources import (
    vtkConeSource,
    vtkSphereSource,
)
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
background_rgb = (0.3, 0.2, 0.1)

# Source 1: generate a sphere offset along X
sphere_source = vtkSphereSource()
sphere_source.SetCenter(5, 0, 0)

# Source 2: generate a cone at the origin
cone_source = vtkConeSource()

# Filter: append the two polydata meshes
append_filter = vtkAppendPolyData()
append_filter.AddInputConnection(sphere_source.GetOutputPort())
append_filter.AddInputConnection(cone_source.GetOutputPort())

# Filter: remove any duplicate points
clean_filter = vtkCleanPolyData()
clean_filter.SetInputConnection(append_filter.GetOutputPort())

# Mapper: map the combined polydata to graphics primitives
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(clean_filter.GetOutputPort())

# Actor: assign the mapped geometry
actor = vtkActor()
actor.SetMapper(mapper)

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(background_rgb)
renderer.GetActiveCamera().Zoom(0.9)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(640, 480)
render_window.SetWindowName("CombinePolyData")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
