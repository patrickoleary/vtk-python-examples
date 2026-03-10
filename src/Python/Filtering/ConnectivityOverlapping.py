#!/usr/bin/env python

# Create two overlapping spheres, tetrahedralize them, combine into one
# dataset, and use vtkConnectivityFilter to show they form a single
# connected region.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkFiltersCore import (
    vtkAppendFilter,
    vtkConnectivityFilter,
    vtkDelaunay3D,
)
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkDataSetMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
background_rgb = (0.3, 0.2, 0.1)

# Source 1: sphere at the origin, tetrahedralized with Delaunay 3D
sphere_source_1 = vtkSphereSource()
sphere_source_1.SetCenter(-0.5, 0.0, 0.0)
delaunay_1 = vtkDelaunay3D()
delaunay_1.SetInputConnection(sphere_source_1.GetOutputPort())

# Source 2: sphere offset slightly so it overlaps sphere 1
sphere_source_2 = vtkSphereSource()
sphere_source_2.SetCenter(0.5, 0.0, 0.0)
delaunay_2 = vtkDelaunay3D()
delaunay_2.SetInputConnection(sphere_source_2.GetOutputPort())

# Filter: combine both tetrahedralized spheres
append_filter = vtkAppendFilter()
append_filter.AddInputConnection(delaunay_1.GetOutputPort())
append_filter.AddInputConnection(delaunay_2.GetOutputPort())

# Filter: identify and color connected regions
connectivity_filter = vtkConnectivityFilter()
connectivity_filter.SetInputConnection(append_filter.GetOutputPort())
connectivity_filter.SetExtractionModeToAllRegions()
connectivity_filter.ColorRegionsOn()

# Mapper: map the connectivity-colored data to graphics primitives
mapper = vtkDataSetMapper()
mapper.SetInputConnection(connectivity_filter.GetOutputPort())

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
render_window.SetWindowName("ConnectivityOverlapping")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
