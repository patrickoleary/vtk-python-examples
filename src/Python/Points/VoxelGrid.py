#!/usr/bin/env python

# Downsample a point cloud using vtkVoxelGrid. The left viewport shows
# the original dense cloud and the right shows the voxelized result
# with one representative point per voxel.

import math

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkCommonCore import vtkFloatArray, vtkPoints
from vtkmodules.vtkCommonDataModel import (
    vtkCellArray,
    vtkPolyData,
)
from vtkmodules.vtkFiltersGeneral import vtkVertexGlyphFilter
from vtkmodules.vtkFiltersPoints import vtkVoxelGrid
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
slate_gray_background_rgb = (0.439, 0.502, 0.565)

# Source: create a dense spherical point cloud with elevation scalars
points = vtkPoints()
vertices = vtkCellArray()
scalars = vtkFloatArray()
scalars.SetName("Elevation")
for i in range(5000):
    phi = math.acos(1.0 - 2.0 * (i / 5000.0))
    theta = math.pi * (1.0 + 5.0**0.5) * i
    x = math.sin(phi) * math.cos(theta)
    y = math.sin(phi) * math.sin(theta)
    z = math.cos(phi)
    pid = points.InsertNextPoint(x, y, z)
    vertices.InsertNextCell(1, [pid])
    scalars.InsertNextValue(z)

cloud = vtkPolyData()
cloud.SetPoints(points)
cloud.SetVerts(vertices)
cloud.GetPointData().SetScalars(scalars)

# ---- Left viewport: original dense cloud ----
dense_mapper = vtkPolyDataMapper()
dense_mapper.SetInputData(cloud)
dense_mapper.SetScalarRange(-1.0, 1.0)

dense_actor = vtkActor()
dense_actor.SetMapper(dense_mapper)
dense_actor.GetProperty().SetPointSize(3)

left_renderer = vtkRenderer()
left_renderer.SetViewport(0.0, 0.0, 0.5, 1.0)
left_renderer.AddActor(dense_actor)
left_renderer.SetBackground(slate_gray_background_rgb)
left_renderer.ResetCamera()

# ---- Right viewport: voxelized (downsampled) cloud ----
voxel = vtkVoxelGrid()
voxel.SetInputData(cloud)
voxel.SetConfigurationStyleToLeafSize()
voxel.SetLeafSize(0.15, 0.15, 0.15)

voxel_verts = vtkVertexGlyphFilter()
voxel_verts.SetInputConnection(voxel.GetOutputPort())

voxel_mapper = vtkPolyDataMapper()
voxel_mapper.SetInputConnection(voxel_verts.GetOutputPort())
voxel_mapper.SetScalarRange(-1.0, 1.0)

voxel_actor = vtkActor()
voxel_actor.SetMapper(voxel_mapper)
voxel_actor.GetProperty().SetPointSize(5)

right_renderer = vtkRenderer()
right_renderer.SetViewport(0.5, 0.0, 1.0, 1.0)
right_renderer.AddActor(voxel_actor)
right_renderer.SetBackground(slate_gray_background_rgb)
right_renderer.SetActiveCamera(left_renderer.GetActiveCamera())

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(left_renderer)
render_window.AddRenderer(right_renderer)
render_window.SetSize(800, 400)
render_window.SetWindowName("VoxelGrid")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
