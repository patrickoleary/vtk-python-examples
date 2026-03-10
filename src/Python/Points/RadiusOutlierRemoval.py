#!/usr/bin/env python

# Remove outlier points from a point cloud using vtkRadiusOutlierRemoval.
# Points that do not have enough neighbors within a specified radius
# are removed. The left viewport shows the original cloud with outliers
# and the right shows the cleaned result.

import math
import random

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
from vtkmodules.vtkFiltersPoints import vtkRadiusOutlierRemoval
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

# Source: create a point cloud on a sphere with scattered outliers
random.seed(42)
points = vtkPoints()
vertices = vtkCellArray()
for i in range(500):
    phi = math.acos(1.0 - 2.0 * (i / 500.0))
    theta = math.pi * (1.0 + 5.0**0.5) * i
    x = math.sin(phi) * math.cos(theta)
    y = math.sin(phi) * math.sin(theta)
    z = math.cos(phi)
    pid = points.InsertNextPoint(x, y, z)
    vertices.InsertNextCell(1, [pid])
for i in range(50):
    x = random.uniform(-2.0, 2.0)
    y = random.uniform(-2.0, 2.0)
    z = random.uniform(-2.0, 2.0)
    pid = points.InsertNextPoint(x, y, z)
    vertices.InsertNextCell(1, [pid])

cloud = vtkPolyData()
cloud.SetPoints(points)
cloud.SetVerts(vertices)

# ---- Left viewport: original cloud with outliers ----
original_mapper = vtkPolyDataMapper()
original_mapper.SetInputData(cloud)

original_actor = vtkActor()
original_actor.SetMapper(original_mapper)
original_actor.GetProperty().SetColor(tomato_rgb)
original_actor.GetProperty().SetPointSize(5)

left_renderer = vtkRenderer()
left_renderer.SetViewport(0.0, 0.0, 0.5, 1.0)
left_renderer.AddActor(original_actor)
left_renderer.SetBackground(slate_gray_background_rgb)
left_renderer.ResetCamera()

# ---- Right viewport: outliers removed ----
remover = vtkRadiusOutlierRemoval()
remover.SetInputData(cloud)
remover.SetRadius(0.3)
remover.SetNumberOfNeighbors(5)

clean_verts = vtkVertexGlyphFilter()
clean_verts.SetInputConnection(remover.GetOutputPort())

clean_mapper = vtkPolyDataMapper()
clean_mapper.SetInputConnection(clean_verts.GetOutputPort())

clean_actor = vtkActor()
clean_actor.SetMapper(clean_mapper)
clean_actor.GetProperty().SetColor(cornflower_blue_rgb)
clean_actor.GetProperty().SetPointSize(5)

right_renderer = vtkRenderer()
right_renderer.SetViewport(0.5, 0.0, 1.0, 1.0)
right_renderer.AddActor(clean_actor)
right_renderer.SetBackground(slate_gray_background_rgb)
right_renderer.SetActiveCamera(left_renderer.GetActiveCamera())

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(left_renderer)
render_window.AddRenderer(right_renderer)
render_window.SetSize(800, 400)
render_window.SetWindowName("RadiusOutlierRemoval")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
