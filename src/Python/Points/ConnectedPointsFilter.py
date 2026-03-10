#!/usr/bin/env python

# Extract connected point regions from a point cloud using
# vtkConnectedPointsFilter. Points within a specified radius
# of each other are grouped into connected regions.

import math

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkCommonCore import vtkPoints
from vtkmodules.vtkCommonDataModel import vtkPolyData
from vtkmodules.vtkFiltersGeneral import vtkVertexGlyphFilter
from vtkmodules.vtkFiltersPoints import vtkConnectedPointsFilter
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
slate_gray_background_rgb = (0.439, 0.502, 0.565)

# Source: create two separated clusters of points
points = vtkPoints()
for i in range(200):
    angle = 2.0 * math.pi * i / 200.0
    r = 1.0 + 0.2 * math.sin(7.0 * angle)
    points.InsertNextPoint(r * math.cos(angle), r * math.sin(angle), 0.0)
for i in range(150):
    angle = 2.0 * math.pi * i / 150.0
    r = 0.5 + 0.1 * math.sin(5.0 * angle)
    points.InsertNextPoint(4.0 + r * math.cos(angle), r * math.sin(angle), 0.0)
for i in range(100):
    angle = 2.0 * math.pi * i / 100.0
    r = 0.3
    points.InsertNextPoint(-3.0 + r * math.cos(angle), 2.0 + r * math.sin(angle), 0.0)

point_cloud = vtkPolyData()
point_cloud.SetPoints(points)

# Filter: extract connected regions based on proximity
connected = vtkConnectedPointsFilter()
connected.SetInputData(point_cloud)
connected.SetRadius(0.5)
connected.SetExtractionModeToAllRegions()

glyphs = vtkVertexGlyphFilter()
glyphs.SetInputConnection(connected.GetOutputPort())

# Mapper: map the connected regions
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(glyphs.GetOutputPort())
mapper.SetScalarRange(0, 2)

# Actor: assign the mapped geometry
actor = vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetPointSize(5)

# Renderer: assemble the scene and configure the camera
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(slate_gray_background_rgb)
renderer.ResetCamera()

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(640, 480)
render_window.SetWindowName("ConnectedPointsFilter")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
