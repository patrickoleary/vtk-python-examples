#!/usr/bin/env python

# Demonstrate vtkTubeFilter with different GenerateTCoords modes on
# simple polylines, textured with a JPEG image.

import math
import os

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import (
    vtkIntArray,
    vtkPoints,
)
from vtkmodules.vtkCommonDataModel import (
    vtkCellArray,
    vtkPolyData,
    vtkPolyLine,
)
from vtkmodules.vtkFiltersCore import vtkTubeFilter
from vtkmodules.vtkIOImage import vtkJPEGReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
    vtkTexture,
)

# Data directory
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Read texture image
jpeg_reader = vtkJPEGReader()
jpeg_reader.SetFileName(os.path.join(data_dir, "beach.jpg"))

texture = vtkTexture()
texture.SetInputConnection(jpeg_reader.GetOutputPort())
texture.InterpolateOn()
texture.RepeatOff()
texture.EdgeClampOn()

# --- Tube 1: VTK_TCOORDS_FROM_NORMALIZED_LENGTH ---
points_1 = vtkPoints()
points_1.InsertNextPoint(0.0, 3.0, 0.0)
points_1.InsertNextPoint(1.0, 2.0, 0.0)
points_1.InsertNextPoint(5.0, 2.0, 0.0)

poly_line_1 = vtkPolyLine()
poly_line_1.GetPointIds().SetNumberOfIds(3)
poly_line_1.GetPointIds().SetId(0, 0)
poly_line_1.GetPointIds().SetId(1, 1)
poly_line_1.GetPointIds().SetId(2, 2)

cells_1 = vtkCellArray()
cells_1.InsertNextCell(poly_line_1)

input_polydata_1 = vtkPolyData()
input_polydata_1.SetPoints(points_1)
input_polydata_1.SetLines(cells_1)

tube_filter_1 = vtkTubeFilter()
tube_filter_1.SetInputData(input_polydata_1)
tube_filter_1.SetNumberOfSides(50)
tube_filter_1.SetGenerateTCoords(1)
tube_filter_1.Update()

tube_mapper_1 = vtkPolyDataMapper()
tube_mapper_1.SetInputData(tube_filter_1.GetOutput())

tube_actor_1 = vtkActor()
tube_actor_1.SetMapper(tube_mapper_1)
tube_actor_1.SetTexture(texture)

# --- Tube 2: VTK_TCOORDS_FROM_LENGTH ---
points_2 = vtkPoints()
points_2.InsertNextPoint(0.0, 5.0, 0.0)
points_2.InsertNextPoint(1.0, 4.0, 0.0)
points_2.InsertNextPoint(5.0, 4.0, 0.0)

poly_line_2 = vtkPolyLine()
poly_line_2.GetPointIds().SetNumberOfIds(3)
poly_line_2.GetPointIds().SetId(0, 0)
poly_line_2.GetPointIds().SetId(1, 1)
poly_line_2.GetPointIds().SetId(2, 2)

cells_2 = vtkCellArray()
cells_2.InsertNextCell(poly_line_2)

input_polydata_2 = vtkPolyData()
input_polydata_2.SetPoints(points_2)
input_polydata_2.SetLines(cells_2)

tube_filter_2 = vtkTubeFilter()
tube_filter_2.SetInputData(input_polydata_2)
tube_filter_2.SetNumberOfSides(50)
tube_filter_2.SetGenerateTCoords(2)

input_length_2 = 0.0
for i in range(input_polydata_2.GetNumberOfPoints() - 1):
    current_pt = input_polydata_2.GetPoint(i)
    next_pt = input_polydata_2.GetPoint(i + 1)
    dx = next_pt[0] - current_pt[0]
    dy = next_pt[1] - current_pt[1]
    dz = next_pt[2] - current_pt[2]
    input_length_2 += math.sqrt(dx * dx + dy * dy + dz * dz)
tube_filter_2.SetTextureLength(input_length_2)
tube_filter_2.Update()

tube_mapper_2 = vtkPolyDataMapper()
tube_mapper_2.SetInputData(tube_filter_2.GetOutput())

tube_actor_2 = vtkActor()
tube_actor_2.SetMapper(tube_mapper_2)
tube_actor_2.SetTexture(texture)

# --- Tube 3: VTK_TCOORDS_FROM_SCALARS ---
points_3 = vtkPoints()
points_3.InsertNextPoint(0.0, 7.0, 0.0)
points_3.InsertNextPoint(1.0, 6.0, 0.0)
points_3.InsertNextPoint(5.0, 6.0, 0.0)

poly_line_3 = vtkPolyLine()
poly_line_3.GetPointIds().SetNumberOfIds(3)
poly_line_3.GetPointIds().SetId(0, 0)
poly_line_3.GetPointIds().SetId(1, 1)
poly_line_3.GetPointIds().SetId(2, 2)

cells_3 = vtkCellArray()
cells_3.InsertNextCell(poly_line_3)

input_polydata_3 = vtkPolyData()
input_polydata_3.SetPoints(points_3)
input_polydata_3.SetLines(cells_3)

active_scalars = vtkIntArray()
active_scalars.SetName("ActiveScalars")
active_scalars.SetNumberOfComponents(1)
active_scalars.SetNumberOfTuples(3)
active_scalars.SetTuple1(0, 0)
active_scalars.SetTuple1(1, 1)
active_scalars.SetTuple1(2, 2)
input_polydata_3.GetPointData().AddArray(active_scalars)
input_polydata_3.GetPointData().SetActiveScalars("ActiveScalars")
scalar_range = active_scalars.GetRange()

tube_filter_3 = vtkTubeFilter()
tube_filter_3.SetInputData(input_polydata_3)
tube_filter_3.SetNumberOfSides(50)
tube_filter_3.SetGenerateTCoords(3)
tube_filter_3.SetTextureLength(scalar_range[1] - scalar_range[0])
tube_filter_3.Update()

tube_mapper_3 = vtkPolyDataMapper()
tube_mapper_3.SetInputData(tube_filter_3.GetOutput())

tube_actor_3 = vtkActor()
tube_actor_3.SetMapper(tube_mapper_3)
tube_actor_3.SetTexture(texture)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(tube_actor_1)
renderer.AddActor(tube_actor_2)
renderer.AddActor(tube_actor_3)
renderer.SetBackground(0.5, 0.5, 0.5)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(300, 300)
render_window.SetWindowName("tube basic")

# Scene
renderer.ResetCamera()

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
