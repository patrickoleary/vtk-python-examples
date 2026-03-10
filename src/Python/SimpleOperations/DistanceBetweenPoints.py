#!/usr/bin/env python

# Visualize the distance between two 3D points.

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
)
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkActor2D,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)
from vtkmodules.vtkRenderingFreeType import vtkVectorText
from vtkmodules.vtkRenderingLabel import vtkLabeledDataMapper

# Colors (normalized RGB)
tomato_rgb = (1.0, 0.388, 0.278)
steel_blue_rgb = (0.275, 0.510, 0.706)
white_rgb = (1.0, 1.0, 1.0)
yellow_rgb = (1.0, 1.0, 0.0)
dark_slate_gray_rgb = (0.184, 0.310, 0.310)

p0 = (0.0, 0.0, 0.0)
p1 = (3.0, 4.0, 0.0)

# Distance: compute squared distance and Euclidean distance using vtkMath
dist_squared = vtkMath.Distance2BetweenPoints(p0, p1)
dist = math.sqrt(dist_squared)

# Source: sphere at p0
sphere0 = vtkSphereSource()
sphere0.SetCenter(p0)
sphere0.SetRadius(0.15)
sphere0.SetPhiResolution(16)
sphere0.SetThetaResolution(16)

mapper0 = vtkPolyDataMapper()
mapper0.SetInputConnection(sphere0.GetOutputPort())

actor0 = vtkActor()
actor0.SetMapper(mapper0)
actor0.GetProperty().SetColor(tomato_rgb)

# Source: sphere at p1
sphere1 = vtkSphereSource()
sphere1.SetCenter(p1)
sphere1.SetRadius(0.15)
sphere1.SetPhiResolution(16)
sphere1.SetThetaResolution(16)

mapper1 = vtkPolyDataMapper()
mapper1.SetInputConnection(sphere1.GetOutputPort())

actor1 = vtkActor()
actor1.SetMapper(mapper1)
actor1.GetProperty().SetColor(steel_blue_rgb)

# Line: connect the two points with a dashed line
line_points = vtkPoints()
line_points.InsertNextPoint(p0)
line_points.InsertNextPoint(p1)

line_cells = vtkCellArray()
line_cells.InsertNextCell(2)
line_cells.InsertCellPoint(0)
line_cells.InsertCellPoint(1)

line_poly = vtkPolyData()
line_poly.SetPoints(line_points)
line_poly.SetLines(line_cells)

line_mapper = vtkPolyDataMapper()
line_mapper.SetInputData(line_poly)

line_actor = vtkActor()
line_actor.SetMapper(line_mapper)
line_actor.GetProperty().SetColor(white_rgb)
line_actor.GetProperty().SetLineWidth(2.0)

# Label: display the distance at the midpoint
mid = ((p0[0] + p1[0]) / 2.0, (p0[1] + p1[1]) / 2.0, (p0[2] + p1[2]) / 2.0)

label_text = vtkVectorText()
label_text.SetText(f"d = {dist:.2f}")

label_mapper = vtkPolyDataMapper()
label_mapper.SetInputConnection(label_text.GetOutputPort())

label_actor = vtkActor()
label_actor.SetMapper(label_mapper)
label_actor.SetScale(0.3, 0.3, 0.3)
label_actor.SetPosition(mid[0] + 0.2, mid[1] + 0.2, mid[2])
label_actor.GetProperty().SetColor(yellow_rgb)

# Label: point coordinates
p0_label = vtkVectorText()
p0_label.SetText(f"({p0[0]:.0f}, {p0[1]:.0f}, {p0[2]:.0f})")

p0_label_mapper = vtkPolyDataMapper()
p0_label_mapper.SetInputConnection(p0_label.GetOutputPort())

p0_label_actor = vtkActor()
p0_label_actor.SetMapper(p0_label_mapper)
p0_label_actor.SetScale(0.2, 0.2, 0.2)
p0_label_actor.SetPosition(p0[0] - 0.8, p0[1] - 0.4, p0[2])
p0_label_actor.GetProperty().SetColor(tomato_rgb)

p1_label = vtkVectorText()
p1_label.SetText(f"({p1[0]:.0f}, {p1[1]:.0f}, {p1[2]:.0f})")

p1_label_mapper = vtkPolyDataMapper()
p1_label_mapper.SetInputConnection(p1_label.GetOutputPort())

p1_label_actor = vtkActor()
p1_label_actor.SetMapper(p1_label_mapper)
p1_label_actor.SetScale(0.2, 0.2, 0.2)
p1_label_actor.SetPosition(p1[0] + 0.2, p1[1] + 0.2, p1[2])
p1_label_actor.GetProperty().SetColor(steel_blue_rgb)

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.AddActor(actor0)
renderer.AddActor(actor1)
renderer.AddActor(line_actor)
renderer.AddActor(label_actor)
renderer.AddActor(p0_label_actor)
renderer.AddActor(p1_label_actor)
renderer.SetBackground(dark_slate_gray_rgb)
renderer.ResetCamera()
renderer.GetActiveCamera().Dolly(1.2)
renderer.ResetCameraClippingRange()

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(640, 480)
render_window.SetWindowName("DistanceBetweenPoints")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
