#!/usr/bin/env python

# Create a helix from a set of points and wrap tubes around the line
# using vtkTubeFilter with varying radius based on scalar values.

import math

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkCommonCore import (
    vtkFloatArray,
    vtkPoints,
)
from vtkmodules.vtkCommonDataModel import (
    vtkCellArray,
    vtkPolyData,
)
from vtkmodules.vtkFiltersCore import vtkTubeFilter
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
background_rgb = (0.1, 0.1, 0.2)

# Source: create a helix polyline
n_points = 100
points = vtkPoints()
radius_scalars = vtkFloatArray()
radius_scalars.SetName("TubeRadius")
for i in range(n_points):
    t = i / (n_points - 1.0)
    angle = t * 4 * math.pi
    x = math.cos(angle)
    y = math.sin(angle)
    z = t * 3.0 - 1.5
    points.InsertNextPoint(x, y, z)
    radius_scalars.InsertNextValue(0.02 + 0.08 * abs(math.sin(angle)))

lines = vtkCellArray()
lines.InsertNextCell(n_points)
for i in range(n_points):
    lines.InsertCellPoint(i)

helix = vtkPolyData()
helix.SetPoints(points)
helix.SetLines(lines)
helix.GetPointData().AddArray(radius_scalars)
helix.GetPointData().SetActiveScalars("TubeRadius")

# Filter: generate tubes around the helix with radius varying by scalars
tube_filter = vtkTubeFilter()
tube_filter.SetInputData(helix)
tube_filter.SetNumberOfSides(16)
tube_filter.SetVaryRadiusToVaryRadiusByAbsoluteScalar()

# Mapper: map the tubes to graphics primitives
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(tube_filter.GetOutputPort())

# Actor: assign the mapped geometry
actor = vtkActor()
actor.SetMapper(mapper)

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(background_rgb)

# Render window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("tube")
render_window.SetMultiSamples(0)
render_window.SetSize(640, 480)

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Scene: configure the camera
renderer.ResetCamera()

# Start: launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
