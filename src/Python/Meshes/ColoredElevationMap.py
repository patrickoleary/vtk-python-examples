#!/usr/bin/env python

# Create a colored elevation map from randomly perturbed grid points
# using vtkDelaunay2D for triangulation and vtkElevationFilter for
# height-based coloring.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkCommonCore import (
    vtkMinimalStandardRandomSequence,
    vtkPoints,
)
from vtkmodules.vtkCommonDataModel import vtkPolyData
from vtkmodules.vtkFiltersCore import (
    vtkDelaunay2D,
    vtkElevationFilter,
)
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
slate_gray_background_rgb = (0.439, 0.502, 0.565)

# Generate a 20x20 grid of points with random perturbation in x, y, z
grid_size = 20
rng = vtkMinimalStandardRandomSequence()
rng.SetSeed(8775586)

points = vtkPoints()
for x in range(grid_size):
    for y in range(grid_size):
        rng.Next()
        xx = x + rng.GetRangeValue(-0.2, 0.2)
        rng.Next()
        yy = y + rng.GetRangeValue(-0.2, 0.2)
        rng.Next()
        zz = rng.GetRangeValue(-0.5, 0.5)
        points.InsertNextPoint(xx, yy, zz)

# Wrap points in a polydata object
input_poly_data = vtkPolyData()
input_poly_data.SetPoints(points)

# Delaunay2D: triangulate the scattered points into a surface
delaunay = vtkDelaunay2D()
delaunay.SetInputData(input_poly_data)

# Elevation: color the surface by height (z value)
elevation = vtkElevationFilter()
elevation.SetInputConnection(delaunay.GetOutputPort())
elevation.Update()
bounds = elevation.GetOutput().GetBounds()
elevation.SetLowPoint(0.0, 0.0, bounds[4])
elevation.SetHighPoint(0.0, 0.0, bounds[5])

# Mapper: map the triangulated surface to graphics primitives
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(elevation.GetOutputPort())

# Actor: assign the mapped geometry
actor = vtkActor()
actor.SetMapper(mapper)

# Renderer: assemble the scene and configure the camera
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(slate_gray_background_rgb)
renderer.ResetCamera()

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(640, 480)
render_window.SetWindowName("ColoredElevationMap")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
