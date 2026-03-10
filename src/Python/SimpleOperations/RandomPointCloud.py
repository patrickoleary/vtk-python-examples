#!/usr/bin/env python

# Generate and visualize a random 3D point cloud using vtkMath.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkCommonCore import (
    vtkMath,
    vtkPoints,
    vtkUnsignedCharArray,
)
from vtkmodules.vtkCommonDataModel import (
    vtkCellArray,
    vtkPolyData,
)
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
black_rgb = (0.0, 0.0, 0.0)

# Parameters
num_points = 500
seed = 42

# RandomPointCloud: generate random points using vtkMath.
# vtkMath.Random() returns a uniform random number in [min, max].
# vtkMath.Gaussian() returns a Gaussian-distributed random number.
vtkMath.RandomSeed(seed)

points = vtkPoints()
point_colors = vtkUnsignedCharArray()
point_colors.SetNumberOfComponents(3)
point_colors.SetName("Colors")

vertices = vtkCellArray()

for i in range(num_points):
    x = vtkMath.Gaussian(0.0, 1.0)
    y = vtkMath.Gaussian(0.0, 1.0)
    z = vtkMath.Gaussian(0.0, 1.0)
    pid = points.InsertNextPoint(x, y, z)
    vertices.InsertNextCell(1)
    vertices.InsertCellPoint(pid)

    r = int(255 * abs(x) / 3.0)
    g = int(255 * abs(y) / 3.0)
    b = int(255 * abs(z) / 3.0)
    r = min(r, 255)
    g = min(g, 255)
    b = min(b, 255)
    point_colors.InsertNextTuple3(r, g, b)

point_cloud = vtkPolyData()
point_cloud.SetPoints(points)
point_cloud.SetVerts(vertices)
point_cloud.GetPointData().SetScalars(point_colors)

# Mapper: map point cloud to graphics primitives
mapper = vtkPolyDataMapper()
mapper.SetInputData(point_cloud)

# Actor: display the point cloud
actor = vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetPointSize(4)

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(black_rgb)
renderer.ResetCamera()

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(640, 480)
render_window.SetWindowName("RandomPointCloud")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
