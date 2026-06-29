#!/usr/bin/env python

# Demonstrate vtkDataSetRegionSurfaceFilter on a tetrahedral cube
# with material IDs assigned per octant.

import math

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import (
    vtkIntArray,
    vtkPoints,
)
from vtkmodules.vtkCommonDataModel import (
    VTK_TETRA,
    vtkCellArray,
    vtkTetra,
    vtkUnstructuredGrid,
)
from vtkmodules.vtkFiltersGeometry import vtkDataSetRegionSurfaceFilter
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkCamera,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

n_x = 2
n_y = 2
n_z = 2

bounds = [-1.0, 1.0, -1.0, 1.0, -1.0, 1.0]
dx = (bounds[1] - bounds[0]) / n_x
dy = (bounds[3] - bounds[2]) / n_y
dz = (bounds[5] - bounds[4]) / n_z

# Build hexahedral grid decomposed into 5 tetrahedra per hex
point_array = vtkPoints()
cell_array = vtkCellArray()
point_map = {}
point_count = 0


# Region array
region = vtkIntArray()
region.SetName("Regions")
region.SetNumberOfTuples(5 * n_x * n_y * n_z)
counter = 0

# Build the initial hex corner template
p = [[bounds[2 * j] for j in range(3)] for _ in range(8)]
p[1][0] += dx
p[2][0] += dx
p[2][1] += dy
p[3][1] += dy
p[5][0] += dx
p[5][2] += dz
p[6][0] += dx
p[6][1] += dy
p[6][2] += dz
p[7][1] += dy
p[7][2] += dz

for x_inc in range(n_x):
    for i in range(8):
        if i in (0, 1, 4, 5):
            p[i][1] = bounds[2]
        else:
            p[i][1] = bounds[2] + dy

    for y_inc in range(n_y):
        for i in range(8):
            if i < 4:
                p[i][2] = bounds[4]
            else:
                p[i][2] = bounds[4] + dz

        for z_inc in range(n_z):
            # Decompose hex into 5 tetrahedra
            tet_corners = [
                (p[0], p[1], p[2], p[5]),
                (p[0], p[2], p[3], p[7]),
                (p[0], p[5], p[7], p[4]),
                (p[2], p[5], p[6], p[7]),
                (p[0], p[2], p[5], p[7]),
            ]
            for corners in tet_corners:
                t = vtkTetra()
                for idx, pt in enumerate(corners):
                    key = (round(pt[0], 10), round(pt[1], 10), round(pt[2], 10))
                    if key not in point_map:
                        point_map[key] = point_count
                        point_array.InsertNextPoint(pt)
                        point_count += 1
                    t.GetPointIds().SetId(idx, point_map[key])
                cell_array.InsertNextCell(t)

            r = 4 * (2 * x_inc // n_x) + 2 * (2 * y_inc // n_y) + (2 * z_inc // n_z)
            for _ in range(5):
                region.SetTuple1(counter, r)
                counter += 1

            for i in range(8):
                p[i][2] += dz

        for i in range(8):
            p[i][1] += dy

    for i in range(8):
        p[i][0] += dx

grid = vtkUnstructuredGrid()
grid.SetPoints(point_array)
grid.SetCells(VTK_TETRA, cell_array)
grid.GetCellData().AddArray(region)
grid.GetCellData().SetScalars(region)

# Compute max distance from origin for camera positioning
n_points = point_array.GetNumberOfPoints()
max_dist = 0
for i in range(n_points):
    xyz = point_array.GetPoint(i)
    dist = math.sqrt(xyz[0] ** 2 + xyz[1] ** 2 + xyz[2] ** 2)
    if dist > max_dist:
        max_dist = dist

# Surface filter
surface_filter = vtkDataSetRegionSurfaceFilter()
surface_filter.SetRegionArrayName("Regions")
surface_filter.SetInputData(grid)

# Mapper
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(surface_filter.GetOutputPort())
mapper.SetScalarRange(0, 7)

actor = vtkActor()
actor.SetMapper(mapper)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(actor)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(300, 300)
render_window.SetWindowName("dataset region surface filter")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
camera = vtkCamera()
camera.SetPosition(3.0 * max_dist, 3.0 * max_dist, -3.0 * max_dist)
camera.SetFocalPoint(0.0, 0.0, 0.0)
renderer.SetActiveCamera(camera)

interactor.Initialize()
interactor.Start()
