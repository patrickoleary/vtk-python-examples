#!/usr/bin/env python

# Sample a cylinder field onto a sphere isosurface using vtkProbeFilter.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkCommonDataModel import (
    vtkCylinder,
    vtkSphere,
)
from vtkmodules.vtkFiltersCore import (
    vtkFlyingEdges3D,
    vtkProbeFilter,
)
from vtkmodules.vtkImagingHybrid import vtkSampleFunction
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
alice_blue = (0.941, 0.973, 1.000)

# Parameters
sample_resolution = 50
radius = 1.0
x_min = -radius * 2.0
x_max = radius * 2.0

# Source: sample a sphere implicit function on a regular grid
implicit_sphere = vtkSphere()
implicit_sphere.SetRadius(radius)

sampled_sphere = vtkSampleFunction()
sampled_sphere.SetSampleDimensions(sample_resolution, sample_resolution, sample_resolution)
sampled_sphere.SetModelBounds(x_min, x_max, x_min, x_max, x_min, x_max)
sampled_sphere.SetImplicitFunction(implicit_sphere)

# Filter: extract the sphere isosurface
iso_sphere = vtkFlyingEdges3D()
iso_sphere.SetInputConnection(sampled_sphere.GetOutputPort())
iso_sphere.SetValue(0, 1.0)

# Source: sample a cylinder implicit function on a regular grid
implicit_cylinder = vtkCylinder()
implicit_cylinder.SetRadius(radius / 2.0)

sampled_cylinder = vtkSampleFunction()
sampled_cylinder.SetSampleDimensions(sample_resolution, sample_resolution, sample_resolution)
sampled_cylinder.SetModelBounds(x_min, x_max, x_min, x_max, x_min, x_max)
sampled_cylinder.SetImplicitFunction(implicit_cylinder)

# Filter: probe the cylinder field onto the sphere isosurface
probe_cylinder = vtkProbeFilter()
probe_cylinder.SetInputConnection(0, iso_sphere.GetOutputPort())
probe_cylinder.SetInputConnection(1, sampled_cylinder.GetOutputPort())
probe_cylinder.Update()

# Restore the original normals from the isosurface
probe_cylinder.GetOutput().GetPointData().SetNormals(
    iso_sphere.GetOutput().GetPointData().GetNormals())

# Mapper: map probed surface to graphics primitives
map_sphere = vtkPolyDataMapper()
map_sphere.SetInputConnection(probe_cylinder.GetOutputPort())
map_sphere.SetScalarRange(probe_cylinder.GetOutput().GetScalarRange())

# Actor: display the probed sphere
sphere_actor = vtkActor()
sphere_actor.SetMapper(map_sphere)

# Renderer: assemble the scene and configure the camera
renderer = vtkRenderer()
renderer.AddActor(sphere_actor)
renderer.SetBackground(alice_blue)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("IsosurfaceSampling")
render_window.SetSize(640, 480)

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Start()
