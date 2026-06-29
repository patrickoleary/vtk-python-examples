#!/usr/bin/env python

# Demonstrate vtkParallelVectors finding lines where two vector fields
# are parallel on a hexahedral unstructured grid with a helical field
# profile.

import math

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import (
    vtkDoubleArray,
    vtkPoints,
)
from vtkmodules.vtkCommonDataModel import (
    VTK_HEXAHEDRON,
    vtkCellArray,
    vtkHexahedron,
    vtkUnstructuredGrid,
)
from vtkmodules.vtkFiltersFlowPaths import vtkParallelVectors
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

n_x, n_y, n_z = 5, 5, 5
bounds = [-1.0, 1.0, -1.0, 1.0, -1.0, 1.0]
dx = (bounds[1] - bounds[0]) / n_x
dy = (bounds[3] - bounds[2]) / n_y
dz = (bounds[5] - bounds[4]) / n_z

# Build hexahedral grid
point_array = vtkPoints()
cell_array = vtkCellArray()

# Track unique points via dictionary
point_map = {}
point_count = 0

for xi in range(n_x):
    for yi in range(n_y):
        for zi in range(n_z):
            x0 = bounds[0] + xi * dx
            y0 = bounds[2] + yi * dy
            z0 = bounds[4] + zi * dz
            pts = [
                [x0, y0, z0], [x0 + dx, y0, z0],
                [x0 + dx, y0 + dy, z0], [x0, y0 + dy, z0],
                [x0, y0, z0 + dz], [x0 + dx, y0, z0 + dz],
                [x0 + dx, y0 + dy, z0 + dz], [x0, y0 + dy, z0 + dz],
            ]
            hexahedron = vtkHexahedron()
            for i, p in enumerate(pts):
                key = (round(p[0], 10), round(p[1], 10), round(p[2], 10))
                if key not in point_map:
                    point_map[key] = point_count
                    point_array.InsertNextPoint(p)
                    point_count += 1
                hexahedron.GetPointIds().SetId(i, point_map[key])
            cell_array.InsertNextCell(hexahedron)

grid = vtkUnstructuredGrid()
grid.SetPoints(point_array)
grid.SetCells(VTK_HEXAHEDRON, cell_array)

# Construct helical field profile
z0 = -1.5
amplitude = 0.8
phase = 2.0

v_field = vtkDoubleArray()
v_field.SetName("vField")
v_field.SetNumberOfComponents(3)
v_field.SetNumberOfTuples(point_array.GetNumberOfPoints())

w_field = vtkDoubleArray()
w_field.SetName("wField")
w_field.SetNumberOfComponents(3)
w_field.SetNumberOfTuples(point_array.GetNumberOfPoints())

for i in range(point_array.GetNumberOfPoints()):
    p = point_array.GetPoint(i)
    x, y, z = p[0], p[1], p[2]
    t = z - z0
    ft_x = amplitude * math.cos(2.0 * math.pi * t / phase)
    ft_y = amplitude * math.sin(2.0 * math.pi * t / phase)
    v_field.SetTuple3(i, x - ft_x, y - ft_y, t)
    w_field.SetTuple3(i, ft_x - x, ft_y - y, t)

grid.GetPointData().AddArray(v_field)
grid.GetPointData().AddArray(w_field)

# Find parallel vectors
parallel_vectors = vtkParallelVectors()
parallel_vectors.SetInputData(grid)
parallel_vectors.SetFirstVectorFieldName("vField")
parallel_vectors.SetSecondVectorFieldName("wField")
parallel_vectors.Update()

# Mapper
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(parallel_vectors.GetOutputPort())
mapper.ScalarVisibilityOff()

actor = vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetColor(0, 0, 0)
actor.GetProperty().SetLineWidth(1.0)
actor.SetPosition(0, 0, 1)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(1.0, 1.0, 1.0)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetMultiSamples(0)
render_window.SetSize(300, 300)
render_window.SetWindowName("parallel vectors")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.ResetCamera()

interactor.Initialize()
interactor.Start()
