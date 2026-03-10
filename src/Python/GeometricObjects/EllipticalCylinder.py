#!/usr/bin/env python

# Create an elliptical cylinder by extruding an elliptical cross-section.

import math

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkCommonCore import (
    vtkMath,
    vtkPoints,
)
from vtkmodules.vtkCommonDataModel import (
    vtkCellArray,
    vtkPolyData,
    vtkPolyLine,
)
from vtkmodules.vtkFiltersModeling import vtkLinearExtrusionFilter
from vtkmodules.vtkInteractionStyle import vtkInteractorStyleTrackballCamera
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkCamera,
    vtkPolyDataMapper,
    vtkProperty,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
peacock_rgb = (0.2, 0.631, 0.788)
banana_rgb = (0.890, 0.812, 0.341)
tomato_rgb = (1.0, 0.388, 0.278)
slate_gray_background_rgb = (0.439, 0.502, 0.565)

# Data: generate elliptical cross-section points
r1 = 50
r2 = 30
center_x = 10.0
center_y = 5.0

points = vtkPoints()
angle = 0.0
idx = 0
while angle <= 2.0 * vtkMath.Pi() + (vtkMath.Pi() / 60.0):
    points.InsertNextPoint(
        r1 * math.cos(angle) + center_x,
        r2 * math.sin(angle) + center_y,
        0.0,
    )
    angle = angle + (vtkMath.Pi() / 60.0)
    idx += 1

# Polyline: connect the ellipse points into a closed loop
poly_line = vtkPolyLine()
poly_line.GetPointIds().SetNumberOfIds(idx)
for i in range(0, idx):
    poly_line.GetPointIds().SetId(i, i)

lines = vtkCellArray()
lines.InsertNextCell(poly_line)

poly_data = vtkPolyData()
poly_data.SetPoints(points)
poly_data.SetLines(lines)

# Filter: extrude the elliptical cross-section along z
extrude = vtkLinearExtrusionFilter()
extrude.SetInputData(poly_data)
extrude.SetExtrusionTypeToNormalExtrusion()
extrude.SetVector(0, 0, 100.0)
extrude.Update()

# Mapper and actor: elliptical outline
line_mapper = vtkPolyDataMapper()
line_mapper.SetInputData(poly_data)

line_actor = vtkActor()
line_actor.SetMapper(line_mapper)
line_actor.GetProperty().SetColor(peacock_rgb)

# Mapper and actor: extruded cylinder with backface coloring
cylinder_mapper = vtkPolyDataMapper()
cylinder_mapper.SetInputConnection(extrude.GetOutputPort())

back_property = vtkProperty()
back_property.SetColor(tomato_rgb)

cylinder_actor = vtkActor()
cylinder_actor.SetMapper(cylinder_mapper)
cylinder_actor.GetProperty().SetColor(banana_rgb)
cylinder_actor.SetBackfaceProperty(back_property)

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.SetBackground(slate_gray_background_rgb)
renderer.AddActor(cylinder_actor)
renderer.AddActor(line_actor)

# Camera: position for a 3D view
camera = vtkCamera()
camera.SetPosition(0, 1, 0)
camera.SetFocalPoint(0, 0, 0)
camera.SetViewUp(0, 0, 1)
camera.Azimuth(30)
camera.Elevation(30)

renderer.SetActiveCamera(camera)
renderer.ResetCamera()
renderer.ResetCameraClippingRange()

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(600, 600)
render_window.SetWindowName("EllipticalCylinder")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

style = vtkInteractorStyleTrackballCamera()
render_window_interactor.SetInteractorStyle(style)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
