#!/usr/bin/env python

# Evaluate the signed distance from a sphere surface on a regular 3-D grid
# using vtkImplicitPolyDataDistance and color the grid points accordingly.

import numpy as np

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkCommonCore import (
    vtkFloatArray,
    vtkPoints,
)
from vtkmodules.vtkCommonDataModel import vtkPolyData
from vtkmodules.vtkFiltersCore import vtkImplicitPolyDataDistance
from vtkmodules.vtkFiltersGeneral import vtkVertexGlyphFilter
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
slate_gray_rgb = (0.439, 0.502, 0.565)

# Source: unit sphere
sphere_source = vtkSphereSource()
sphere_source.SetCenter(0.0, 0.0, 0.0)
sphere_source.SetRadius(1.0)
sphere_source.Update()

# Mapper & Actor: map translucent red sphere to graphics primitives
sphere_mapper = vtkPolyDataMapper()
sphere_mapper.SetInputConnection(sphere_source.GetOutputPort())
sphere_mapper.ScalarVisibilityOff()

sphere_actor = vtkActor()
sphere_actor.SetMapper(sphere_mapper)
sphere_actor.GetProperty().SetOpacity(0.3)
sphere_actor.GetProperty().SetColor(1, 0, 0)

# Implicit function: signed distance from the sphere surface
implicit_distance = vtkImplicitPolyDataDistance()
implicit_distance.SetInput(sphere_source.GetOutput())

# Build a regular 3-D grid of sample points
points = vtkPoints()
step = 0.1
for x in np.arange(-2, 2, step):
    for y in np.arange(-2, 2, step):
        for z in np.arange(-2, 2, step):
            points.InsertNextPoint(x, y, z)

# Evaluate the signed distance at every grid point
signed_distances = vtkFloatArray()
signed_distances.SetNumberOfComponents(1)
signed_distances.SetName("SignedDistances")
for point_id in range(points.GetNumberOfPoints()):
    p = points.GetPoint(point_id)
    signed_distances.InsertNextValue(implicit_distance.EvaluateFunction(p))

grid_polydata = vtkPolyData()
grid_polydata.SetPoints(points)
grid_polydata.GetPointData().SetScalars(signed_distances)

# Filter: create vertex cells so points are renderable
vertex_glyph = vtkVertexGlyphFilter()
vertex_glyph.SetInputData(grid_polydata)

# Mapper & Actor: map distance-coloured point cloud to graphics primitives
distance_mapper = vtkPolyDataMapper()
distance_mapper.SetInputConnection(vertex_glyph.GetOutputPort())
distance_mapper.ScalarVisibilityOn()

distance_actor = vtkActor()
distance_actor.SetMapper(distance_mapper)

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.AddActor(sphere_actor)
renderer.AddActor(distance_actor)
renderer.SetBackground(slate_gray_rgb)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(640, 480)
render_window.SetWindowName("ImplicitPolyDataDistance")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window.Render()
render_window_interactor.Start()
