#!/usr/bin/env python

# Compute point density on a 2D image using vtkPointDensityFilter.
# A procedural point cloud is projected onto a density image and
# rendered with a color map.

import math

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkCommonCore import vtkPoints
from vtkmodules.vtkCommonDataModel import (
    vtkCellArray,
    vtkPolyData,
)
from vtkmodules.vtkFiltersPoints import vtkPointDensityFilter
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkImageActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
    vtkWindowLevelLookupTable,
)

# Colors (normalized RGB)
slate_gray_background_rgb = (0.439, 0.502, 0.565)

# Source: create a 2D point cloud with two dense clusters
points = vtkPoints()
vertices = vtkCellArray()
for i in range(2000):
    angle = 2.0 * math.pi * i / 2000.0
    r = 2.0 + 0.5 * math.sin(5.0 * angle)
    x = r * math.cos(angle) + 0.1 * math.sin(37.0 * angle)
    y = r * math.sin(angle) + 0.1 * math.cos(41.0 * angle)
    pid = points.InsertNextPoint(x, y, 0.0)
    vertices.InsertNextCell(1, [pid])
for i in range(1000):
    angle = 2.0 * math.pi * i / 1000.0
    r = 0.8 + 0.2 * math.sin(3.0 * angle)
    x = r * math.cos(angle)
    y = r * math.sin(angle)
    pid = points.InsertNextPoint(x, y, 0.0)
    vertices.InsertNextCell(1, [pid])

cloud = vtkPolyData()
cloud.SetPoints(points)
cloud.SetVerts(vertices)

# Filter: compute point density on a regular grid
density = vtkPointDensityFilter()
density.SetInputData(cloud)
density.SetSampleDimensions(128, 128, 1)
density.SetModelBounds(-4.0, 4.0, -4.0, 4.0, -0.5, 0.5)
density.SetDensityEstimateToFixedRadius()
density.SetRadius(0.3)
density.SetScalarWeighting(False)

# Mapper: map the density volume as a surface
mapper = vtkPolyDataMapper()
mapper.SetInputData(cloud)

cloud_actor = vtkActor()
cloud_actor.SetMapper(mapper)
cloud_actor.GetProperty().SetPointSize(2)
cloud_actor.GetProperty().SetColor(1.0, 1.0, 1.0)
cloud_actor.GetProperty().SetOpacity(0.3)

density_actor = vtkImageActor()
density.Update()
density_actor.GetMapper().SetInputData(density.GetOutput())

# Renderer: assemble the scene and configure the camera
renderer = vtkRenderer()
renderer.AddActor(density_actor)
renderer.AddActor(cloud_actor)
renderer.SetBackground(slate_gray_background_rgb)
renderer.ResetCamera()

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(640, 480)
render_window.SetWindowName("PointDensity")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
