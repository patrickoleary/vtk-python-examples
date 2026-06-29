#!/usr/bin/env python

# Test vtkCellPicker and vtkHardwarePicker on simple quad polydata.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import vtkPoints
from vtkmodules.vtkCommonDataModel import (
    vtkCellArray,
    vtkPolyData,
)
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkCellPicker,
    vtkHardwarePicker,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Create two quads
points = vtkPoints()
points.SetNumberOfPoints(6)
coords = [(0, 0, 0), (2, 0, 0), (4, 0, 0), (0, 4, 0), (2, 4, 0), (4, 4, 0)]
for i in range(6):
    points.InsertPoint(i, coords[i])

quads = vtkCellArray()
cell_points = [(0, 1, 4, 3), (1, 2, 5, 4)]
for i in range(2):
    quads.InsertNextCell(4)
    for j in range(4):
        quads.InsertCellPoint(cell_points[i][j])

poly_data = vtkPolyData()
poly_data.SetPoints(points)
poly_data.SetPolys(quads)

mapper = vtkPolyDataMapper()
mapper.SetInputData(poly_data)

actor = vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetColor(0.2, 0.6, 0.9)
actor.GetProperty().EdgeVisibilityOn()

renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(0.1, 0.2, 0.4)

render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("pick cell points")
render_window.SetMultiSamples(0)
render_window.SetSize(200, 200)

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.ResetCamera()

render_window.Render()

# Perform picks
pick_positions = [(1, 1), (35, 40), (80, 40), (120, 40), (165, 40),
                  (199, 160), (165, 160), (120, 160), (80, 160), (35, 160)]

cell_picker = vtkCellPicker()
hardware_picker = vtkHardwarePicker()

for i in range(len(pick_positions)):
    cell_picker.Pick(pick_positions[i][0], pick_positions[i][1], 0, renderer)
    hardware_picker.SnapToMeshPointOff()
    hardware_picker.Pick(pick_positions[i][0], pick_positions[i][1], 0, renderer)
    hardware_picker.SnapToMeshPointOn()
    hardware_picker.SetPixelTolerance(20)
    hardware_picker.Pick(pick_positions[i][0], pick_positions[i][1], 0, renderer)

interactor.Initialize()
interactor.Start()
