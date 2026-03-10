#!/usr/bin/env python

# Compute point occupancy on a regular grid using vtkPointOccupancyFilter.
# A procedural point cloud is binned into voxels and the occupancy count
# is rendered as an image slice.

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
from vtkmodules.vtkFiltersPoints import vtkPointOccupancyFilter
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkImageActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
slate_gray_background_rgb = (0.439, 0.502, 0.565)

# Source: create a 2D point cloud with a spiral pattern
points = vtkPoints()
vertices = vtkCellArray()
for i in range(3000):
    t = i / 3000.0 * 6.0 * math.pi
    r = 0.5 + t / (2.0 * math.pi)
    x = r * math.cos(t) + 0.05 * math.sin(50.0 * t)
    y = r * math.sin(t) + 0.05 * math.cos(50.0 * t)
    pid = points.InsertNextPoint(x, y, 0.0)
    vertices.InsertNextCell(1, [pid])

cloud = vtkPolyData()
cloud.SetPoints(points)
cloud.SetVerts(vertices)

# Filter: compute point occupancy on a regular grid
occupancy = vtkPointOccupancyFilter()
occupancy.SetInputData(cloud)
occupancy.SetSampleDimensions(128, 128, 1)
occupancy.SetModelBounds(-4.0, 4.0, -4.0, 4.0, -0.5, 0.5)
occupancy.SetOccupiedValue(255)
occupancy.SetEmptyValue(0)
occupancy.Update()

# ImageActor: display the occupancy grid
occupancy_actor = vtkImageActor()
occupancy_actor.GetMapper().SetInputData(occupancy.GetOutput())

# Cloud overlay
cloud_mapper = vtkPolyDataMapper()
cloud_mapper.SetInputData(cloud)

cloud_actor = vtkActor()
cloud_actor.SetMapper(cloud_mapper)
cloud_actor.GetProperty().SetPointSize(2)
cloud_actor.GetProperty().SetColor(1.0, 0.4, 0.3)
cloud_actor.GetProperty().SetOpacity(0.4)

# Renderer: assemble the scene and configure the camera
renderer = vtkRenderer()
renderer.AddActor(occupancy_actor)
renderer.AddActor(cloud_actor)
renderer.SetBackground(slate_gray_background_rgb)
renderer.ResetCamera()

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(640, 480)
render_window.SetWindowName("PointOccupancy")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
