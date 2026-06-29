#!/usr/bin/env python

# Demonstrate camera shift/scale with procedural geometry at large world coordinates.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

import math

from vtkmodules.vtkCommonCore import vtkPoints
from vtkmodules.vtkCommonDataModel import vtkCellArray, vtkPolyData
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Build procedural geometry: ring of triangles at large world offset
xres = 200
yres = 20

points = vtkPoints()
points.SetDataTypeToDouble()
for y in range(yres):
    angle = 2.0 * y / yres
    for x in range(xres):
        step = x // 10
        size = 2.0 ** step
        radius = 0.001 * (1.0 + 10.0 * (size - 1.0) + (x % 10) * size)
        points.InsertNextPoint(40000.0 + radius * math.cos(angle), radius * math.sin(angle), 0.0)

cells = vtkCellArray()
for y in range(yres - 1):
    for x in range(xres - 1):
        cells.InsertNextCell(3)
        cells.InsertCellPoint(y * xres + x)
        cells.InsertCellPoint(y * xres + x + 1)
        cells.InsertCellPoint((y + 1) * xres + x + 1)
        cells.InsertNextCell(3)
        cells.InsertCellPoint(y * xres + x)
        cells.InsertCellPoint((y + 1) * xres + x + 1)
        cells.InsertCellPoint((y + 1) * xres + x)

polydata = vtkPolyData()
polydata.SetPoints(points)
polydata.SetPolys(cells)

mapper = vtkPolyDataMapper()
mapper.SetInputData(polydata)
mapper.SetVBOShiftScaleMethod(3)  # FOCAL_POINT_SHIFT_SCALE

actor = vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetDiffuse(0.0)
actor.GetProperty().SetAmbient(1.0)
actor.GetProperty().SetRepresentationToWireframe()
actor.SetPosition(-40000, 0, 0)

renderer = vtkRenderer()
renderer.SetBackground(0.1, 0.2, 0.4)
renderer.AddActor(actor)

render_window = vtkRenderWindow()
render_window.SetSize(400, 400)
render_window.AddRenderer(renderer)
render_window.SetWindowName("camera shift scale")

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.GetActiveCamera().SetPosition(0.001, 0.0015, 0.01)
renderer.GetActiveCamera().SetFocalPoint(0.001, 0.0015, 0)
renderer.ResetCameraClippingRange()

interactor.Initialize()
interactor.Start()
