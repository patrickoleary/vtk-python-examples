#!/usr/bin/env python

# Create ribbons from a helical polyline using vtkRibbonFilter.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import math

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkCommonCore import vtkPoints
from vtkmodules.vtkCommonDataModel import (
    vtkCellArray,
    vtkPolyData,
)
from vtkmodules.vtkFiltersModeling import vtkRibbonFilter
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
slate_gray_background_rgb = (0.439, 0.502, 0.565)
cornflower_blue_rgb = (0.392, 0.584, 0.929)
tomato_rgb = (1.000, 0.388, 0.278)

# Source: build a helical polyline
n_pts = 200
points = vtkPoints()
lines = vtkCellArray()
lines.InsertNextCell(n_pts)
for i in range(n_pts):
    t = i / (n_pts - 1.0)
    angle = t * 4 * math.pi
    x = math.cos(angle)
    y = math.sin(angle)
    z = t * 6.0
    points.InsertPoint(i, x, y, z)
    lines.InsertCellPoint(i)

helix = vtkPolyData()
helix.SetPoints(points)
helix.SetLines(lines)

# Filter: create ribbon from the helix
ribbon = vtkRibbonFilter()
ribbon.SetInputData(helix)
ribbon.SetWidth(0.2)
ribbon.SetAngle(0)
ribbon.UseDefaultNormalOn()
ribbon.SetDefaultNormal(0, 0, 1)

# Mapper: ribbon surface
ribbon_mapper = vtkPolyDataMapper()
ribbon_mapper.SetInputConnection(ribbon.GetOutputPort())

ribbon_actor = vtkActor()
ribbon_actor.SetMapper(ribbon_mapper)
ribbon_actor.GetProperty().SetColor(cornflower_blue_rgb)

# Mapper: original helix line for reference
line_mapper = vtkPolyDataMapper()
line_mapper.SetInputData(helix)

line_actor = vtkActor()
line_actor.SetMapper(line_mapper)
line_actor.GetProperty().SetColor(tomato_rgb)
line_actor.GetProperty().SetLineWidth(2)

# Renderer: assemble the scene and configure the camera
renderer = vtkRenderer()
renderer.AddActor(ribbon_actor)
renderer.AddActor(line_actor)
renderer.SetBackground(slate_gray_background_rgb)
renderer.ResetCamera()
renderer.GetActiveCamera().Azimuth(30)
renderer.GetActiveCamera().Elevation(30)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(640, 480)
render_window.SetWindowName("RibbonFilter")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
