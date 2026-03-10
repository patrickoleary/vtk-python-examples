#!/usr/bin/env python

# Compute a 3D Delaunay tetrahedralization from random points using
# vtkDelaunay3D and extract the outer surface with vtkGeometryFilter.

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
from vtkmodules.vtkFiltersCore import vtkDelaunay3D
from vtkmodules.vtkFiltersGeometry import vtkGeometryFilter
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
slate_gray_background_rgb = (0.439, 0.502, 0.565)
alice_blue_rgb = (0.941, 0.973, 1.000)
steel_blue_rgb = (0.275, 0.510, 0.706)

# Generate 100 random 3D points
rng = vtkMinimalStandardRandomSequence()
rng.SetSeed(77665)

points = vtkPoints()
for _ in range(100):
    rng.Next()
    x = rng.GetRangeValue(-1.0, 1.0)
    rng.Next()
    y = rng.GetRangeValue(-1.0, 1.0)
    rng.Next()
    z = rng.GetRangeValue(-1.0, 1.0)
    points.InsertNextPoint(x, y, z)

point_poly = vtkPolyData()
point_poly.SetPoints(points)

# Delaunay3D: tetrahedralize the point cloud
delaunay = vtkDelaunay3D()
delaunay.SetInputData(point_poly)

# GeometryFilter: extract the outer boundary surface
geometry = vtkGeometryFilter()
geometry.SetInputConnection(delaunay.GetOutputPort())

# Mapper: map the boundary surface to graphics primitives
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(geometry.GetOutputPort())
mapper.ScalarVisibilityOff()

# Actor: display the convex hull with visible edges
actor = vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetColor(alice_blue_rgb)
actor.GetProperty().EdgeVisibilityOn()
actor.GetProperty().SetEdgeColor(steel_blue_rgb)
actor.GetProperty().SetOpacity(0.7)

# Renderer: assemble the scene and configure the camera
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(slate_gray_background_rgb)
renderer.ResetCamera()

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(640, 480)
render_window.SetWindowName("Delaunay3D")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
