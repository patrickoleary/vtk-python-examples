#!/usr/bin/env python

# Create a capped sphere by rotationally extruding a semicircular arc.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import math

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkCommonCore import vtkPoints
from vtkmodules.vtkCommonDataModel import (
    vtkCellArray,
    vtkLine,
    vtkPolyData,
)
from vtkmodules.vtkFiltersModeling import vtkRotationalExtrusionFilter
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
light_slate_gray_background_rgb = (0.467, 0.533, 0.600)
khaki_rgb = (0.941, 0.902, 0.549)

# Source: build the semicircular arc as a polyline
angle = math.radians(90)
step = math.radians(1)
radius = 1.0
start = math.radians(90)

pts = []
theta = 0.0
while theta <= angle:
    x = radius * math.cos(start - theta)
    z = radius * math.sin(theta - start)
    if x < 0:
        pts.append((0.0, 0.0, z))
        break
    pts.append((max(x, 0.0), 0.0, z))
    theta += step

# Cap: drop a perpendicular from the last point to the axis
if pts[-1][0] > 0:
    last_x, _, last_z = pts[-1]
    num_pts = 10
    for i in range(1, num_pts + 1):
        x = last_x - i * last_x / num_pts
        if x < 0:
            x = 0.0
        pts.append((x, 0.0, last_z))
        if x == 0.0:
            break

points = vtkPoints()
lines = vtkCellArray()
for pt in pts:
    pt_id = points.InsertNextPoint(pt)
    if pt_id < len(pts) - 1:
        line = vtkLine()
        line.GetPointIds().SetId(0, pt_id)
        line.GetPointIds().SetId(1, pt_id + 1)
        lines.InsertNextCell(line)

polydata = vtkPolyData()
polydata.SetPoints(points)
polydata.SetLines(lines)

# Filter: rotationally extrude the arc to form the sphere surface
extrude = vtkRotationalExtrusionFilter()
extrude.SetInputData(polydata)
extrude.SetResolution(60)

# Mapper: map the extruded sphere surface
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(extrude.GetOutputPort())

# Actor: the capped sphere
actor = vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetColor(khaki_rgb)

# Renderer: assemble the scene and configure the camera
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(light_slate_gray_background_rgb)
renderer.ResetCamera()
renderer.GetActiveCamera().Azimuth(0)
renderer.GetActiveCamera().Elevation(60)
renderer.ResetCameraClippingRange()

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(640, 480)
render_window.SetWindowName("CappedSphere")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
