#!/usr/bin/env python

# Demonstrate vtkCountVertices by building an unstructured grid with various
# cell types and visualizing the cells colored by vertex count.

import math

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import vtkPoints
from vtkmodules.vtkCommonDataModel import (
    VTK_HEXAGONAL_PRISM,
    VTK_HEXAHEDRON,
    VTK_LINE,
    VTK_PENTAGONAL_PRISM,
    VTK_PYRAMID,
    VTK_TETRA,
    VTK_TRIANGLE,
    VTK_VERTEX,
    VTK_VOXEL,
    VTK_WEDGE,
    vtkUnstructuredGrid,
)
from vtkmodules.vtkFiltersGeneral import vtkCountVertices
from vtkmodules.vtkFiltersGeometry import vtkDataSetSurfaceFilter
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Build points for all cell types, spread along x axis
points = vtkPoints()

# Vertex (1 point)
points.InsertNextPoint(0, 0, 0)  # 0

# Line (2 points)
points.InsertNextPoint(2, 0, 0)  # 1
points.InsertNextPoint(3, 0, 0)  # 2

# Triangle (3 points)
points.InsertNextPoint(5, 0, 0)  # 3
points.InsertNextPoint(6, 0, 0)  # 4
points.InsertNextPoint(5.5, 1, 0)  # 5

# Tetrahedron (4 points)
points.InsertNextPoint(8, 0, 0)  # 6
points.InsertNextPoint(9, 0, 0)  # 7
points.InsertNextPoint(8.5, 1, 0)  # 8
points.InsertNextPoint(8.5, 0.5, 1)  # 9

# Pyramid (5 points)
points.InsertNextPoint(11, 0, 0)  # 10
points.InsertNextPoint(12, 0, 0)  # 11
points.InsertNextPoint(12, 1, 0)  # 12
points.InsertNextPoint(11, 1, 0)  # 13
points.InsertNextPoint(11.5, 0.5, 1)  # 14

# Wedge (6 points)
points.InsertNextPoint(14, 1, 0)  # 15
points.InsertNextPoint(14, 0, 0)  # 16
points.InsertNextPoint(14, 0.5, 0.5)  # 17
points.InsertNextPoint(15, 1, 0)  # 18
points.InsertNextPoint(15, 0, 0)  # 19
points.InsertNextPoint(15, 0.5, 0.5)  # 20

# Voxel (8 points)
points.InsertNextPoint(17, 0, 0)  # 21
points.InsertNextPoint(18, 0, 0)  # 22
points.InsertNextPoint(17, 1, 0)  # 23
points.InsertNextPoint(18, 1, 0)  # 24
points.InsertNextPoint(17, 0, 1)  # 25
points.InsertNextPoint(18, 0, 1)  # 26
points.InsertNextPoint(17, 1, 1)  # 27
points.InsertNextPoint(18, 1, 1)  # 28

# Hexahedron (8 points)
points.InsertNextPoint(20, 0, 0)  # 29
points.InsertNextPoint(21, 0, 0)  # 30
points.InsertNextPoint(21, 1, 0)  # 31
points.InsertNextPoint(20, 1, 0)  # 32
points.InsertNextPoint(20, 0, 1)  # 33
points.InsertNextPoint(21, 0, 1)  # 34
points.InsertNextPoint(21, 1, 1)  # 35
points.InsertNextPoint(20, 1, 1)  # 36

# Pentagonal prism (10 points)
for i in range(5):
    angle = 2.0 * math.pi * i / 5.0
    points.InsertNextPoint(23 + 0.5 * math.cos(angle), 0.5 + 0.5 * math.sin(angle), 0)  # 37-41
for i in range(5):
    angle = 2.0 * math.pi * i / 5.0
    points.InsertNextPoint(23 + 0.5 * math.cos(angle), 0.5 + 0.5 * math.sin(angle), 1)  # 42-46

# Hexagonal prism (12 points)
for i in range(6):
    angle = 2.0 * math.pi * i / 6.0
    points.InsertNextPoint(26 + 0.5 * math.cos(angle), 0.5 + 0.5 * math.sin(angle), 0)  # 47-52
for i in range(6):
    angle = 2.0 * math.pi * i / 6.0
    points.InsertNextPoint(26 + 0.5 * math.cos(angle), 0.5 + 0.5 * math.sin(angle), 1)  # 53-58

# Build unstructured grid
ugrid = vtkUnstructuredGrid()
ugrid.SetPoints(points)

ugrid.InsertNextCell(VTK_VERTEX, 1, [0])
ugrid.InsertNextCell(VTK_LINE, 2, [1, 2])
ugrid.InsertNextCell(VTK_TRIANGLE, 3, [3, 4, 5])
ugrid.InsertNextCell(VTK_TETRA, 4, [6, 7, 8, 9])
ugrid.InsertNextCell(VTK_PYRAMID, 5, [10, 11, 12, 13, 14])
ugrid.InsertNextCell(VTK_WEDGE, 6, [15, 16, 17, 18, 19, 20])
ugrid.InsertNextCell(VTK_VOXEL, 8, [21, 22, 23, 24, 25, 26, 27, 28])
ugrid.InsertNextCell(VTK_HEXAHEDRON, 8, [29, 30, 31, 32, 33, 34, 35, 36])
ugrid.InsertNextCell(VTK_PENTAGONAL_PRISM, 10, list(range(37, 47)))
ugrid.InsertNextCell(VTK_HEXAGONAL_PRISM, 12, list(range(47, 59)))

# Count vertices
count_vertices = vtkCountVertices()
count_vertices.SetOutputArrayName("Vertices")
count_vertices.SetInputData(ugrid)
count_vertices.Update()

# Extract surface and color by vertex count
surface = vtkDataSetSurfaceFilter()
surface.SetInputConnection(count_vertices.GetOutputPort())

mapper = vtkPolyDataMapper()
mapper.SetInputConnection(surface.GetOutputPort())
mapper.SetScalarModeToUseCellFieldData()
mapper.SelectColorArray("Vertices")
mapper.SetScalarRange(1, 12)

actor = vtkActor()
actor.SetMapper(mapper)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(0.1, 0.2, 0.4)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(600, 300)
render_window.SetWindowName("count vertices")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.ResetCamera()
renderer.GetActiveCamera().Elevation(20)
renderer.GetActiveCamera().Azimuth(20)
renderer.ResetCameraClippingRange()

interactor.Initialize()
interactor.Start()
