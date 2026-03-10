#!/usr/bin/env python

# Triangulate a set of randomly scattered 2D points using vtkDelaunay2D
# and display the resulting triangulation with visible edges.

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
from vtkmodules.vtkFiltersCore import vtkDelaunay2D
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

# Generate 50 random 2D points (z = 0)
rng = vtkMinimalStandardRandomSequence()
rng.SetSeed(99887)

points = vtkPoints()
for _ in range(50):
    rng.Next()
    x = rng.GetRangeValue(-5.0, 5.0)
    rng.Next()
    y = rng.GetRangeValue(-5.0, 5.0)
    points.InsertNextPoint(x, y, 0.0)

point_poly = vtkPolyData()
point_poly.SetPoints(points)

# Delaunay2D: triangulate the scattered points
delaunay = vtkDelaunay2D()
delaunay.SetInputData(point_poly)

# Mapper: map the triangulation to graphics primitives
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(delaunay.GetOutputPort())
mapper.ScalarVisibilityOff()

# Actor: display the triangulation with visible edges
actor = vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetColor(alice_blue_rgb)
actor.GetProperty().EdgeVisibilityOn()
actor.GetProperty().SetEdgeColor(steel_blue_rgb)

# Renderer: assemble the scene and configure the camera
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(slate_gray_background_rgb)
renderer.ResetCamera()

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(640, 480)
render_window.SetWindowName("Triangulation")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
