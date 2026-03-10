#!/usr/bin/env python

# Densify a sparse point cloud using vtkDensifyPointCloudFilter.
# The left viewport shows the original sparse cloud and the right
# shows the densified result with additional interpolated points.

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
from vtkmodules.vtkFiltersGeneral import vtkVertexGlyphFilter
from vtkmodules.vtkFiltersPoints import vtkDensifyPointCloudFilter
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
tomato_rgb = (1.000, 0.388, 0.278)
cornflower_blue_rgb = (0.392, 0.584, 0.929)
slate_gray_background_rgb = (0.439, 0.502, 0.565)

# Source: create a sparse point cloud on a hemisphere
points = vtkPoints()
vertices = vtkCellArray()
for i in range(100):
    phi = math.acos(1.0 - (i / 100.0))
    theta = math.pi * (1.0 + 5.0**0.5) * i
    x = math.sin(phi) * math.cos(theta)
    y = math.sin(phi) * math.sin(theta)
    z = math.cos(phi)
    pid = points.InsertNextPoint(x, y, z)
    vertices.InsertNextCell(1, [pid])

sparse_cloud = vtkPolyData()
sparse_cloud.SetPoints(points)
sparse_cloud.SetVerts(vertices)

# ---- Left viewport: original sparse cloud ----
sparse_mapper = vtkPolyDataMapper()
sparse_mapper.SetInputData(sparse_cloud)

sparse_actor = vtkActor()
sparse_actor.SetMapper(sparse_mapper)
sparse_actor.GetProperty().SetColor(tomato_rgb)
sparse_actor.GetProperty().SetPointSize(6)

left_renderer = vtkRenderer()
left_renderer.SetViewport(0.0, 0.0, 0.5, 1.0)
left_renderer.AddActor(sparse_actor)
left_renderer.SetBackground(slate_gray_background_rgb)
left_renderer.ResetCamera()

# ---- Right viewport: densified cloud ----
densify = vtkDensifyPointCloudFilter()
densify.SetInputData(sparse_cloud)
densify.SetTargetDistance(0.1)
densify.SetMaximumNumberOfIterations(3)

dense_verts = vtkVertexGlyphFilter()
dense_verts.SetInputConnection(densify.GetOutputPort())

dense_mapper = vtkPolyDataMapper()
dense_mapper.SetInputConnection(dense_verts.GetOutputPort())

dense_actor = vtkActor()
dense_actor.SetMapper(dense_mapper)
dense_actor.GetProperty().SetColor(cornflower_blue_rgb)
dense_actor.GetProperty().SetPointSize(3)

right_renderer = vtkRenderer()
right_renderer.SetViewport(0.5, 0.0, 1.0, 1.0)
right_renderer.AddActor(dense_actor)
right_renderer.SetBackground(slate_gray_background_rgb)
right_renderer.SetActiveCamera(left_renderer.GetActiveCamera())

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(left_renderer)
render_window.AddRenderer(right_renderer)
render_window.SetSize(800, 400)
render_window.SetWindowName("DensifyPointCloud")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
