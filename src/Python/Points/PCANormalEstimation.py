#!/usr/bin/env python

# Estimate normals for a point cloud using vtkPCANormalEstimation and
# display the normals as hedgehog glyphs on a sphere point cloud.

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
from vtkmodules.vtkFiltersCore import vtkHedgeHog
from vtkmodules.vtkFiltersPoints import vtkPCANormalEstimation
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
tomato_rgb = (1.000, 0.388, 0.278)
white_rgb = (1.000, 1.000, 1.000)
slate_gray_background_rgb = (0.439, 0.502, 0.565)

# Source: create a point cloud on a sphere
points = vtkPoints()
vertices = vtkCellArray()
for i in range(400):
    phi = math.acos(1.0 - 2.0 * (i / 400.0))
    theta = math.pi * (1.0 + 5.0**0.5) * i
    x = math.sin(phi) * math.cos(theta)
    y = math.sin(phi) * math.sin(theta)
    z = math.cos(phi)
    pid = points.InsertNextPoint(x, y, z)
    vertices.InsertNextCell(1, [pid])

cloud = vtkPolyData()
cloud.SetPoints(points)
cloud.SetVerts(vertices)

# Filter: estimate normals using PCA
normals = vtkPCANormalEstimation()
normals.SetInputData(cloud)
normals.SetSampleSize(20)
normals.SetNormalOrientationToGraphTraversal()
normals.FlipNormalsOn()

# Hedgehog: display normals as short lines from each point
hedgehog = vtkHedgeHog()
hedgehog.SetInputConnection(normals.GetOutputPort())
hedgehog.SetVectorModeToUseNormal()
hedgehog.SetScaleFactor(0.1)

hedgehog_mapper = vtkPolyDataMapper()
hedgehog_mapper.SetInputConnection(hedgehog.GetOutputPort())

hedgehog_actor = vtkActor()
hedgehog_actor.SetMapper(hedgehog_mapper)
hedgehog_actor.GetProperty().SetColor(white_rgb)

# Points: render the original cloud
cloud_mapper = vtkPolyDataMapper()
cloud_mapper.SetInputData(cloud)

cloud_actor = vtkActor()
cloud_actor.SetMapper(cloud_mapper)
cloud_actor.GetProperty().SetColor(tomato_rgb)
cloud_actor.GetProperty().SetPointSize(5)

# Renderer: assemble the scene and configure the camera
renderer = vtkRenderer()
renderer.AddActor(cloud_actor)
renderer.AddActor(hedgehog_actor)
renderer.SetBackground(slate_gray_background_rgb)
renderer.ResetCamera()

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(640, 480)
render_window.SetWindowName("PCANormalEstimation")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
