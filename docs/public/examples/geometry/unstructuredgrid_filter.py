#!/usr/bin/env python

# Demonstrate vtkUnstructuredGridGeometryFilter on an unstructured grid
# containing all VTK linear and quadratic cell types, with shared faces
# between adjacent cells of the same type, colored by blue-to-red LUT.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import (
    vtkFloatArray,
    vtkIdList,
    vtkIntArray,
    vtkPoints,
)
from vtkmodules.vtkCommonDataModel import (
    VTK_HEXAGONAL_PRISM,
    VTK_HEXAHEDRON,
    VTK_LINE,
    VTK_PENTAGONAL_PRISM,
    VTK_PIXEL,
    VTK_POLY_LINE,
    VTK_POLY_VERTEX,
    VTK_POLYGON,
    VTK_PYRAMID,
    VTK_QUAD,
    VTK_QUADRATIC_HEXAHEDRON,
    VTK_QUADRATIC_PYRAMID,
    VTK_QUADRATIC_QUAD,
    VTK_QUADRATIC_TETRA,
    VTK_QUADRATIC_TRIANGLE,
    VTK_QUADRATIC_WEDGE,
    VTK_TETRA,
    VTK_TRIANGLE,
    VTK_TRIANGLE_STRIP,
    VTK_VERTEX,
    VTK_VOXEL,
    VTK_WEDGE,
    vtkUnstructuredGrid,
)
from vtkmodules.vtkFiltersGeometry import (
    vtkGeometryFilter,
    vtkUnstructuredGridGeometryFilter,
)
from vtkmodules.vtkCommonCore import vtkLookupTable
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

points = vtkPoints()
scalars = vtkFloatArray()
scalars.SetName("Scalars")
cell_ids = vtkIntArray()
cell_ids.SetName("CellIds")

grid = vtkUnstructuredGrid()

scalar = 0.0
scalar_step = 0.01
point_id = 0
cell_id = 0
x_offset = 0.0
y_offset = 0.0

# ========== 0D cells ==========

# Vertex: 3 vertices
pid = point_id
for px, py, pz in [(0.0, 0.0, 0.0), (0.5, 0.0, 0.0), (1.0, 0.0, 0.0)]:
    points.InsertNextPoint(x_offset + px, y_offset + py, pz)
    scalars.InsertNextValue(scalar)
    scalar += scalar_step
    point_id += 1
id_list_v0 = vtkIdList()
id_list_v0.InsertNextId(pid)
cell_ids.InsertNextValue(cell_id)
cell_id += 1
grid.InsertNextCell(VTK_VERTEX, id_list_v0)
id_list_v1 = vtkIdList()
id_list_v1.InsertNextId(pid + 1)
cell_ids.InsertNextValue(cell_id)
cell_id += 1
grid.InsertNextCell(VTK_VERTEX, id_list_v1)
id_list_v2 = vtkIdList()
id_list_v2.InsertNextId(pid + 2)
cell_ids.InsertNextValue(cell_id)
cell_id += 1
grid.InsertNextCell(VTK_VERTEX, id_list_v2)

# Poly-vertex
x_offset += 2.0
pid = point_id
for px, py, pz in [(0.0, 0.0, 0.0), (0.5, 0.0, 0.0), (1.0, 0.0, 0.0)]:
    points.InsertNextPoint(x_offset + px, y_offset + py, pz)
    scalars.InsertNextValue(scalar)
    scalar += scalar_step
    point_id += 1
id_list = vtkIdList()
for i in [pid, pid + 1, pid + 2]:
    id_list.InsertNextId(i)
cell_ids.InsertNextValue(cell_id)
cell_id += 1
grid.InsertNextCell(VTK_POLY_VERTEX, id_list)

# ========== 1D cells ==========

# Line: 3 lines, sharing endpoints
x_offset += 2.0
pid = point_id
for px, py, pz in [(0.0, 0.0, 0.0), (1.0, 0.0, 0.0), (2.0, 0.0, 0.0), (0.5, 1.0, 0.0)]:
    points.InsertNextPoint(x_offset + px, y_offset + py, pz)
    scalars.InsertNextValue(scalar)
    scalar += scalar_step
    point_id += 1
id_list_l0 = vtkIdList()
id_list_l0.InsertNextId(pid)
id_list_l0.InsertNextId(pid + 1)
cell_ids.InsertNextValue(cell_id)
cell_id += 1
grid.InsertNextCell(VTK_LINE, id_list_l0)
id_list_l1 = vtkIdList()
id_list_l1.InsertNextId(pid + 1)
id_list_l1.InsertNextId(pid + 2)
cell_ids.InsertNextValue(cell_id)
cell_id += 1
grid.InsertNextCell(VTK_LINE, id_list_l1)
id_list_l2 = vtkIdList()
id_list_l2.InsertNextId(pid + 1)
id_list_l2.InsertNextId(pid + 3)
cell_ids.InsertNextValue(cell_id)
cell_id += 1
grid.InsertNextCell(VTK_LINE, id_list_l2)

# Poly-line: 2 polylines sharing a point
x_offset += 3.0
pid = point_id
for px, py, pz in [(0.0, 0.0, 0.0), (1.0, 0.0, 0.0), (2.0, 0.0, 0.0), (1.0, 1.0, 0.0)]:
    points.InsertNextPoint(x_offset + px, y_offset + py, pz)
    scalars.InsertNextValue(scalar)
    scalar += scalar_step
    point_id += 1
id_list_pl0 = vtkIdList()
id_list_pl0.InsertNextId(pid)
id_list_pl0.InsertNextId(pid + 1)
id_list_pl0.InsertNextId(pid + 2)
cell_ids.InsertNextValue(cell_id)
cell_id += 1
grid.InsertNextCell(VTK_POLY_LINE, id_list_pl0)
id_list_pl1 = vtkIdList()
id_list_pl1.InsertNextId(pid + 1)
id_list_pl1.InsertNextId(pid + 3)
cell_ids.InsertNextValue(cell_id)
cell_id += 1
grid.InsertNextCell(VTK_POLY_LINE, id_list_pl1)

# ========== 2D cells ==========

# Triangle: 3 triangles sharing edges
y_offset += 3.0
x_offset = 0.0
pid = point_id
points.InsertNextPoint(x_offset + 0.0, y_offset + 0.0, 0.0)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
points.InsertNextPoint(x_offset + 1.0, y_offset + 0.0, 0.0)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
points.InsertNextPoint(x_offset + 0.5, y_offset + 1.0, 0.0)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
points.InsertNextPoint(x_offset + 1.5, y_offset + 1.0, 0.0)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
id_list = vtkIdList()
for i in [pid, pid + 1, pid + 2]:
    id_list.InsertNextId(i)
cell_ids.InsertNextValue(cell_id)
cell_id += 1
grid.InsertNextCell(VTK_TRIANGLE, id_list)
id_list = vtkIdList()
for i in [pid + 1, pid + 3, pid + 2]:
    id_list.InsertNextId(i)
cell_ids.InsertNextValue(cell_id)
cell_id += 1
grid.InsertNextCell(VTK_TRIANGLE, id_list)
id_list = vtkIdList()
for i in [pid + 1, pid + 3, pid]:
    id_list.InsertNextId(i)
cell_ids.InsertNextValue(cell_id)
cell_id += 1
grid.InsertNextCell(VTK_TRIANGLE, id_list)

# Triangle strip
x_offset += 3.0
pid = point_id
points.InsertNextPoint(x_offset + 0.0, y_offset + 0.0, 0.0)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
points.InsertNextPoint(x_offset + 1.0, y_offset + 0.0, 0.0)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
points.InsertNextPoint(x_offset + 0.5, y_offset + 1.0, 0.0)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
points.InsertNextPoint(x_offset + 1.5, y_offset + 1.0, 0.0)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
points.InsertNextPoint(x_offset + 1.0, y_offset + 2.0, 0.0)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
id_list = vtkIdList()
for i in [pid, pid + 1, pid + 2, pid + 3, pid + 4]:
    id_list.InsertNextId(i)
cell_ids.InsertNextValue(cell_id)
cell_id += 1
grid.InsertNextCell(VTK_TRIANGLE_STRIP, id_list)

# Quad: 2 quads sharing an edge
x_offset += 3.0
pid = point_id
points.InsertNextPoint(x_offset + 0.0, y_offset + 0.0, 0.0)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
points.InsertNextPoint(x_offset + 1.0, y_offset + 0.0, 0.0)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
points.InsertNextPoint(x_offset + 1.0, y_offset + 1.0, 0.0)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
points.InsertNextPoint(x_offset + 0.0, y_offset + 1.0, 0.0)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
points.InsertNextPoint(x_offset + 2.0, y_offset + 0.0, 0.0)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
points.InsertNextPoint(x_offset + 2.0, y_offset + 1.0, 0.0)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
id_list = vtkIdList()
for i in [pid, pid + 1, pid + 2, pid + 3]:
    id_list.InsertNextId(i)
cell_ids.InsertNextValue(cell_id)
cell_id += 1
grid.InsertNextCell(VTK_QUAD, id_list)
id_list = vtkIdList()
for i in [pid + 1, pid + 4, pid + 5, pid + 2]:
    id_list.InsertNextId(i)
cell_ids.InsertNextValue(cell_id)
cell_id += 1
grid.InsertNextCell(VTK_QUAD, id_list)

# Pixel: 2 pixels sharing an edge
x_offset += 4.0
pid = point_id
points.InsertNextPoint(x_offset + 0.0, y_offset + 0.0, 0.0)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
points.InsertNextPoint(x_offset + 1.0, y_offset + 0.0, 0.0)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
points.InsertNextPoint(x_offset + 0.0, y_offset + 1.0, 0.0)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
points.InsertNextPoint(x_offset + 1.0, y_offset + 1.0, 0.0)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
points.InsertNextPoint(x_offset + 2.0, y_offset + 0.0, 0.0)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
points.InsertNextPoint(x_offset + 2.0, y_offset + 1.0, 0.0)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
id_list = vtkIdList()
for i in [pid, pid + 1, pid + 2, pid + 3]:
    id_list.InsertNextId(i)
cell_ids.InsertNextValue(cell_id)
cell_id += 1
grid.InsertNextCell(VTK_PIXEL, id_list)
id_list = vtkIdList()
for i in [pid + 1, pid + 4, pid + 3, pid + 5]:
    id_list.InsertNextId(i)
cell_ids.InsertNextValue(cell_id)
cell_id += 1
grid.InsertNextCell(VTK_PIXEL, id_list)

# Polygon: 2 pentagons sharing an edge
x_offset += 4.0
pid = point_id
points.InsertNextPoint(x_offset + 0.0, y_offset + 0.0, 0.0)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
points.InsertNextPoint(x_offset + 1.0, y_offset + 0.0, 0.0)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
points.InsertNextPoint(x_offset + 1.5, y_offset + 0.5, 0.0)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
points.InsertNextPoint(x_offset + 0.5, y_offset + 1.0, 0.0)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
points.InsertNextPoint(x_offset - 0.5, y_offset + 0.5, 0.0)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
points.InsertNextPoint(x_offset + 2.0, y_offset + 0.0, 0.0)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
points.InsertNextPoint(x_offset + 2.5, y_offset + 0.5, 0.0)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
points.InsertNextPoint(x_offset + 2.0, y_offset + 1.0, 0.0)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
id_list = vtkIdList()
for i in [pid, pid + 1, pid + 2, pid + 3, pid + 4]:
    id_list.InsertNextId(i)
cell_ids.InsertNextValue(cell_id)
cell_id += 1
grid.InsertNextCell(VTK_POLYGON, id_list)
id_list = vtkIdList()
for i in [pid + 1, pid + 5, pid + 6, pid + 7, pid + 2]:
    id_list.InsertNextId(i)
cell_ids.InsertNextValue(cell_id)
cell_id += 1
grid.InsertNextCell(VTK_POLYGON, id_list)

# Quadratic triangle: 2 sharing an edge
x_offset += 4.0
pid = point_id
# Corner points
points.InsertNextPoint(x_offset + 0.0, y_offset + 0.0, 0.0)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
points.InsertNextPoint(x_offset + 1.0, y_offset + 0.0, 0.0)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
points.InsertNextPoint(x_offset + 0.5, y_offset + 1.0, 0.0)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
points.InsertNextPoint(x_offset + 1.5, y_offset + 1.0, 0.0)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
# Mid-edge points for first triangle
points.InsertNextPoint(x_offset + 0.5, y_offset + 0.0, 0.0)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
points.InsertNextPoint(x_offset + 0.75, y_offset + 0.5, 0.0)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
points.InsertNextPoint(x_offset + 0.25, y_offset + 0.5, 0.0)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
# Mid-edge points for second triangle
points.InsertNextPoint(x_offset + 1.25, y_offset + 0.5, 0.0)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
points.InsertNextPoint(x_offset + 1.0, y_offset + 1.0, 0.0)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
id_list = vtkIdList()
for i in [pid, pid + 1, pid + 2, pid + 4, pid + 5, pid + 6]:
    id_list.InsertNextId(i)
cell_ids.InsertNextValue(cell_id)
cell_id += 1
grid.InsertNextCell(VTK_QUADRATIC_TRIANGLE, id_list)
id_list = vtkIdList()
for i in [pid + 1, pid + 3, pid + 2, pid + 7, pid + 8, pid + 5]:
    id_list.InsertNextId(i)
cell_ids.InsertNextValue(cell_id)
cell_id += 1
grid.InsertNextCell(VTK_QUADRATIC_TRIANGLE, id_list)

# Quadratic quad: 2 sharing an edge
x_offset += 3.0
pid = point_id
# Corners
points.InsertNextPoint(x_offset + 0.0, y_offset + 0.0, 0.0)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
points.InsertNextPoint(x_offset + 1.0, y_offset + 0.0, 0.0)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
points.InsertNextPoint(x_offset + 1.0, y_offset + 1.0, 0.0)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
points.InsertNextPoint(x_offset + 0.0, y_offset + 1.0, 0.0)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
points.InsertNextPoint(x_offset + 2.0, y_offset + 0.0, 0.0)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
points.InsertNextPoint(x_offset + 2.0, y_offset + 1.0, 0.0)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
# Mid-edge points first quad
points.InsertNextPoint(x_offset + 0.5, y_offset + 0.0, 0.0)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
points.InsertNextPoint(x_offset + 1.0, y_offset + 0.5, 0.0)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
points.InsertNextPoint(x_offset + 0.5, y_offset + 1.0, 0.0)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
points.InsertNextPoint(x_offset + 0.0, y_offset + 0.5, 0.0)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
# Mid-edge points second quad
points.InsertNextPoint(x_offset + 1.5, y_offset + 0.0, 0.0)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
points.InsertNextPoint(x_offset + 2.0, y_offset + 0.5, 0.0)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
points.InsertNextPoint(x_offset + 1.5, y_offset + 1.0, 0.0)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
id_list = vtkIdList()
for i in [pid, pid + 1, pid + 2, pid + 3, pid + 6, pid + 7, pid + 8, pid + 9]:
    id_list.InsertNextId(i)
cell_ids.InsertNextValue(cell_id)
cell_id += 1
grid.InsertNextCell(VTK_QUADRATIC_QUAD, id_list)
id_list = vtkIdList()
for i in [pid + 1, pid + 4, pid + 5, pid + 2, pid + 10, pid + 11, pid + 12, pid + 7]:
    id_list.InsertNextId(i)
cell_ids.InsertNextValue(cell_id)
cell_id += 1
grid.InsertNextCell(VTK_QUADRATIC_QUAD, id_list)

# ========== 3D cells ==========

# Tetra: 2 tetra sharing a face
y_offset += 3.0
x_offset = 0.0
pid = point_id
points.InsertNextPoint(x_offset + 0.0, y_offset + 0.0, 0.0)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
points.InsertNextPoint(x_offset + 0.5, y_offset + 1.0, 0.0)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
points.InsertNextPoint(x_offset + 0.0, y_offset + 2.0, 0.0)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
points.InsertNextPoint(x_offset + 0.0, y_offset + 0.5, 1.0)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
points.InsertNextPoint(x_offset + 0.25, y_offset + 0.3, -2.0)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
id_list = vtkIdList()
for i in [pid, pid + 1, pid + 2, pid + 3]:
    id_list.InsertNextId(i)
cell_ids.InsertNextValue(cell_id)
cell_id += 1
grid.InsertNextCell(VTK_TETRA, id_list)
id_list = vtkIdList()
for i in [pid, pid + 2, pid + 1, pid + 4]:
    id_list.InsertNextId(i)
cell_ids.InsertNextValue(cell_id)
cell_id += 1
grid.InsertNextCell(VTK_TETRA, id_list)

# Hexahedron: 2 hexahedra sharing a face
x_offset += 2.0
pid = point_id
# Back face
points.InsertNextPoint(x_offset + 0.0, y_offset + 0.0, 0.0)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
points.InsertNextPoint(x_offset + 1.0, y_offset + 0.0, 0.0)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
points.InsertNextPoint(x_offset + 1.0, y_offset + 2.0, 0.0)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
points.InsertNextPoint(x_offset + 0.0, y_offset + 2.0, 0.0)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
# Common face
points.InsertNextPoint(x_offset + 0.1, y_offset + 0.1, 3.0)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
points.InsertNextPoint(x_offset + 0.9, y_offset + 0.1, 3.0)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
points.InsertNextPoint(x_offset + 0.9, y_offset + 1.9, 3.0)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
points.InsertNextPoint(x_offset + 0.1, y_offset + 1.9, 3.0)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
# Front face
points.InsertNextPoint(x_offset + 0.0, y_offset + 0.0, 4.0)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
points.InsertNextPoint(x_offset + 1.0, y_offset + 0.0, 4.0)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
points.InsertNextPoint(x_offset + 1.0, y_offset + 2.0, 5.0)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
points.InsertNextPoint(x_offset + 0.0, y_offset + 2.0, 5.0)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
id_list = vtkIdList()
for i in [pid, pid + 1, pid + 2, pid + 3, pid + 4, pid + 5, pid + 6, pid + 7]:
    id_list.InsertNextId(i)
cell_ids.InsertNextValue(cell_id)
cell_id += 1
grid.InsertNextCell(VTK_HEXAHEDRON, id_list)
id_list = vtkIdList()
for i in [pid + 4, pid + 5, pid + 6, pid + 7, pid + 8, pid + 9, pid + 10, pid + 11]:
    id_list.InsertNextId(i)
cell_ids.InsertNextValue(cell_id)
cell_id += 1
grid.InsertNextCell(VTK_HEXAHEDRON, id_list)

# Voxel: 2 voxels sharing a face
x_offset += 2.0
pid = point_id
points.InsertNextPoint(x_offset + 0.0, y_offset + 0.0, 0.0)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
points.InsertNextPoint(x_offset + 1.0, y_offset + 0.0, 0.0)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
points.InsertNextPoint(x_offset + 0.0, y_offset + 1.0, 0.0)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
points.InsertNextPoint(x_offset + 1.0, y_offset + 1.0, 0.0)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
points.InsertNextPoint(x_offset + 0.0, y_offset + 0.0, 1.0)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
points.InsertNextPoint(x_offset + 1.0, y_offset + 0.0, 1.0)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
points.InsertNextPoint(x_offset + 0.0, y_offset + 1.0, 1.0)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
points.InsertNextPoint(x_offset + 1.0, y_offset + 1.0, 1.0)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
points.InsertNextPoint(x_offset + 0.0, y_offset + 0.0, 2.0)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
points.InsertNextPoint(x_offset + 1.0, y_offset + 0.0, 2.0)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
points.InsertNextPoint(x_offset + 0.0, y_offset + 1.0, 2.0)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
points.InsertNextPoint(x_offset + 1.0, y_offset + 1.0, 2.0)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
id_list = vtkIdList()
for i in [pid, pid + 1, pid + 2, pid + 3, pid + 4, pid + 5, pid + 6, pid + 7]:
    id_list.InsertNextId(i)
cell_ids.InsertNextValue(cell_id)
cell_id += 1
grid.InsertNextCell(VTK_VOXEL, id_list)
id_list = vtkIdList()
for i in [pid + 4, pid + 5, pid + 6, pid + 7, pid + 8, pid + 9, pid + 10, pid + 11]:
    id_list.InsertNextId(i)
cell_ids.InsertNextValue(cell_id)
cell_id += 1
grid.InsertNextCell(VTK_VOXEL, id_list)

# Wedge: 3 wedges, sharing triangle and quad faces
x_offset += 2.0
pid = point_id
points.InsertNextPoint(x_offset + 0.0, y_offset + 0.0, 1.0)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
points.InsertNextPoint(x_offset + 1.0, y_offset + 0.0, 1.0)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
points.InsertNextPoint(x_offset + 0.5, y_offset + 1.0, 1.0)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
points.InsertNextPoint(x_offset + 0.0, y_offset + 0.0, 0.0)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
points.InsertNextPoint(x_offset + 1.0, y_offset + 0.0, 0.0)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
points.InsertNextPoint(x_offset + 0.5, y_offset + 1.0, 0.0)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
points.InsertNextPoint(x_offset + 0.1, y_offset + 0.1, -1.0)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
points.InsertNextPoint(x_offset + 0.9, y_offset + 0.1, -1.0)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
points.InsertNextPoint(x_offset + 0.5, y_offset + 0.9, -1.0)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
points.InsertNextPoint(x_offset + 1.0, y_offset + 1.0, 1.0)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
points.InsertNextPoint(x_offset + 1.0, y_offset + 1.0, 0.0)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
id_list = vtkIdList()
for i in [pid, pid + 1, pid + 2, pid + 3, pid + 4, pid + 5]:
    id_list.InsertNextId(i)
cell_ids.InsertNextValue(cell_id)
cell_id += 1
grid.InsertNextCell(VTK_WEDGE, id_list)
id_list = vtkIdList()
for i in [pid + 3, pid + 4, pid + 5, pid + 6, pid + 7, pid + 8]:
    id_list.InsertNextId(i)
cell_ids.InsertNextValue(cell_id)
cell_id += 1
grid.InsertNextCell(VTK_WEDGE, id_list)
id_list = vtkIdList()
for i in [pid + 2, pid + 1, pid + 9, pid + 5, pid + 4, pid + 10]:
    id_list.InsertNextId(i)
cell_ids.InsertNextValue(cell_id)
cell_id += 1
grid.InsertNextCell(VTK_WEDGE, id_list)

# Pyramid: 3 pyramids, sharing base and triangle faces
x_offset += 2.0
pid = point_id
points.InsertNextPoint(x_offset + 0.0, y_offset + 0.0, 0.2)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
points.InsertNextPoint(x_offset + 1.0, y_offset + 0.0, 0.0)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
points.InsertNextPoint(x_offset + 1.0, y_offset + 0.0, -1.0)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
points.InsertNextPoint(x_offset + 0.0, y_offset + 0.0, -1.2)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
points.InsertNextPoint(x_offset + 0.5, y_offset + 1.0, -0.5)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
points.InsertNextPoint(x_offset + 0.5, y_offset - 1.0, -0.5)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
points.InsertNextPoint(x_offset + 2.0, y_offset + 0.0, -0.1)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
points.InsertNextPoint(x_offset + 2.0, y_offset + 0.0, -0.9)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
id_list = vtkIdList()
for i in [pid, pid + 1, pid + 2, pid + 3, pid + 4]:
    id_list.InsertNextId(i)
cell_ids.InsertNextValue(cell_id)
cell_id += 1
grid.InsertNextCell(VTK_PYRAMID, id_list)
id_list = vtkIdList()
for i in [pid + 3, pid + 2, pid + 1, pid, pid + 5]:
    id_list.InsertNextId(i)
cell_ids.InsertNextValue(cell_id)
cell_id += 1
grid.InsertNextCell(VTK_PYRAMID, id_list)
id_list = vtkIdList()
for i in [pid + 1, pid + 6, pid + 7, pid + 2, pid + 4]:
    id_list.InsertNextId(i)
cell_ids.InsertNextValue(cell_id)
cell_id += 1
grid.InsertNextCell(VTK_PYRAMID, id_list)

# Pentagonal prism: 3 prisms sharing faces
x_offset += 4.0
pid = point_id
# Top pentagon
points.InsertNextPoint(x_offset + 0.0, y_offset + 0.0, 1.0)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
points.InsertNextPoint(x_offset + 1.0, y_offset + 0.0, 1.0)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
points.InsertNextPoint(x_offset + 1.5, y_offset + 0.5, 1.0)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
points.InsertNextPoint(x_offset + 0.5, y_offset + 1.0, 1.0)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
points.InsertNextPoint(x_offset - 0.5, y_offset + 0.5, 1.0)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
# Middle pentagon
points.InsertNextPoint(x_offset + 0.0, y_offset + 0.0, 0.0)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
points.InsertNextPoint(x_offset + 1.0, y_offset + 0.0, 0.0)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
points.InsertNextPoint(x_offset + 1.5, y_offset + 0.5, 0.0)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
points.InsertNextPoint(x_offset + 0.5, y_offset + 1.0, 0.0)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
points.InsertNextPoint(x_offset - 0.5, y_offset + 0.5, 0.0)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
# Bottom pentagon
points.InsertNextPoint(x_offset + 0.0, y_offset + 0.0, -1.0)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
points.InsertNextPoint(x_offset + 1.0, y_offset + 0.0, -1.0)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
points.InsertNextPoint(x_offset + 1.5, y_offset + 0.5, -1.0)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
points.InsertNextPoint(x_offset + 0.5, y_offset + 1.0, -1.0)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
points.InsertNextPoint(x_offset - 0.5, y_offset + 0.5, -1.0)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
id_list = vtkIdList()
for i in [pid, pid + 4, pid + 3, pid + 2, pid + 1, pid + 5, pid + 9, pid + 8, pid + 7, pid + 6]:
    id_list.InsertNextId(i)
cell_ids.InsertNextValue(cell_id)
cell_id += 1
grid.InsertNextCell(VTK_PENTAGONAL_PRISM, id_list)
id_list = vtkIdList()
for i in [pid + 5, pid + 9, pid + 8, pid + 7, pid + 6, pid + 10, pid + 14, pid + 13, pid + 12, pid + 11]:
    id_list.InsertNextId(i)
cell_ids.InsertNextValue(cell_id)
cell_id += 1
grid.InsertNextCell(VTK_PENTAGONAL_PRISM, id_list)

# Hexagonal prism: 2 prisms sharing a face
x_offset += 4.0
pid = point_id
# Top hexagon
points.InsertNextPoint(x_offset + 0.0, y_offset + 0.0, 1.0)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
points.InsertNextPoint(x_offset + 1.0, y_offset + 0.0, 1.0)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
points.InsertNextPoint(x_offset + 1.5, y_offset + 0.5, 1.0)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
points.InsertNextPoint(x_offset + 1.0, y_offset + 1.0, 1.0)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
points.InsertNextPoint(x_offset + 0.0, y_offset + 1.0, 1.0)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
points.InsertNextPoint(x_offset - 0.5, y_offset + 0.5, 1.0)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
# Middle hexagon
points.InsertNextPoint(x_offset + 0.0, y_offset + 0.0, 0.0)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
points.InsertNextPoint(x_offset + 1.0, y_offset + 0.0, 0.0)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
points.InsertNextPoint(x_offset + 1.5, y_offset + 0.5, 0.0)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
points.InsertNextPoint(x_offset + 1.0, y_offset + 1.0, 0.0)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
points.InsertNextPoint(x_offset + 0.0, y_offset + 1.0, 0.0)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
points.InsertNextPoint(x_offset - 0.5, y_offset + 0.5, 0.0)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
# Bottom hexagon
points.InsertNextPoint(x_offset + 0.0, y_offset + 0.0, -1.0)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
points.InsertNextPoint(x_offset + 1.0, y_offset + 0.0, -1.0)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
points.InsertNextPoint(x_offset + 1.5, y_offset + 0.5, -1.0)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
points.InsertNextPoint(x_offset + 1.0, y_offset + 1.0, -1.0)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
points.InsertNextPoint(x_offset + 0.0, y_offset + 1.0, -1.0)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
points.InsertNextPoint(x_offset - 0.5, y_offset + 0.5, -1.0)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
id_list = vtkIdList()
for i in [pid, pid + 5, pid + 4, pid + 3, pid + 2, pid + 1, pid + 6, pid + 11, pid + 10, pid + 9, pid + 8, pid + 7]:
    id_list.InsertNextId(i)
cell_ids.InsertNextValue(cell_id)
cell_id += 1
grid.InsertNextCell(VTK_HEXAGONAL_PRISM, id_list)
id_list = vtkIdList()
for i in [pid + 6, pid + 11, pid + 10, pid + 9, pid + 8, pid + 7, pid + 12, pid + 17, pid + 16, pid + 15, pid + 14, pid + 13]:
    id_list.InsertNextId(i)
cell_ids.InsertNextValue(cell_id)
cell_id += 1
grid.InsertNextCell(VTK_HEXAGONAL_PRISM, id_list)

# ========== Quadratic 3D cells ==========

# Quadratic tetra: 2 sharing a face
y_offset += 3.0
x_offset = 0.0
pid = point_id
# Corner points
points.InsertNextPoint(x_offset + 0.0, y_offset + 0.0, 0.0)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
points.InsertNextPoint(x_offset + 0.5, y_offset + 1.0, 0.0)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
points.InsertNextPoint(x_offset + 0.0, y_offset + 2.0, 0.0)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
points.InsertNextPoint(x_offset + 0.0, y_offset + 0.5, 1.0)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
points.InsertNextPoint(x_offset + 0.25, y_offset + 0.3, -2.0)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
# Mid-edge on common face
points.InsertNextPoint(x_offset + 0.25, y_offset + 0.6, 0.0)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
points.InsertNextPoint(x_offset + 0.3, y_offset + 1.5, 0.0)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
points.InsertNextPoint(x_offset - 0.2, y_offset + 1.0, 0.0)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
# Mid-edge first tetra
points.InsertNextPoint(x_offset + 0.0, y_offset + 0.3, 0.5)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
points.InsertNextPoint(x_offset + 0.4, y_offset + 0.75, 0.5)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
points.InsertNextPoint(x_offset + 0.0, y_offset + 1.25, 1.0)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
# Mid-edge second tetra
points.InsertNextPoint(x_offset + 0.125, y_offset + 0.15, -1.0)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
points.InsertNextPoint(x_offset + 0.125, y_offset + 1.15, -1.0)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
points.InsertNextPoint(x_offset + 0.375, y_offset + 0.65, -1.0)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
id_list = vtkIdList()
for i in [pid, pid + 1, pid + 2, pid + 3, pid + 5, pid + 6, pid + 7, pid + 8, pid + 9, pid + 10]:
    id_list.InsertNextId(i)
cell_ids.InsertNextValue(cell_id)
cell_id += 1
grid.InsertNextCell(VTK_QUADRATIC_TETRA, id_list)
id_list = vtkIdList()
for i in [pid, pid + 2, pid + 1, pid + 4, pid + 7, pid + 6, pid + 5, pid + 11, pid + 12, pid + 13]:
    id_list.InsertNextId(i)
cell_ids.InsertNextValue(cell_id)
cell_id += 1
grid.InsertNextCell(VTK_QUADRATIC_TETRA, id_list)

# Quadratic hexahedron: 2 sharing a face
x_offset += 2.0
pid = point_id
# Back face 0-3
points.InsertNextPoint(x_offset + 0.0, y_offset + 0.0, 0.0)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
points.InsertNextPoint(x_offset + 1.0, y_offset + 0.0, 0.0)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
points.InsertNextPoint(x_offset + 1.0, y_offset + 2.0, 0.0)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
points.InsertNextPoint(x_offset + 0.0, y_offset + 2.0, 0.0)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
# Common face 4-7
points.InsertNextPoint(x_offset + 0.1, y_offset + 0.1, 3.0)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
points.InsertNextPoint(x_offset + 0.9, y_offset + 0.1, 3.0)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
points.InsertNextPoint(x_offset + 0.9, y_offset + 1.9, 3.0)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
points.InsertNextPoint(x_offset + 0.1, y_offset + 1.9, 3.0)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
# Front face 8-11
points.InsertNextPoint(x_offset + 0.0, y_offset + 0.0, 4.0)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
points.InsertNextPoint(x_offset + 1.0, y_offset + 0.0, 4.0)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
points.InsertNextPoint(x_offset + 1.0, y_offset + 2.0, 5.0)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
points.InsertNextPoint(x_offset + 0.0, y_offset + 2.0, 5.0)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
# Mid-edge back face 12-15
points.InsertNextPoint(x_offset + 0.5, y_offset + 0.0, 0.0)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
points.InsertNextPoint(x_offset + 1.0, y_offset + 1.0, 0.0)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
points.InsertNextPoint(x_offset + 0.5, y_offset + 2.0, 0.0)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
points.InsertNextPoint(x_offset + 0.0, y_offset + 1.0, 0.0)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
# Mid-edge common face 16-19
points.InsertNextPoint(x_offset + 0.5, y_offset + 0.1, 3.0)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
points.InsertNextPoint(x_offset + 0.9, y_offset + 1.0, 3.0)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
points.InsertNextPoint(x_offset + 0.5, y_offset + 1.9, 3.0)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
points.InsertNextPoint(x_offset + 0.1, y_offset + 1.0, 3.0)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
# Mid-edge between back and common 20-23
points.InsertNextPoint(x_offset + 0.05, y_offset + 0.05, 1.5)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
points.InsertNextPoint(x_offset + 0.95, y_offset + 0.05, 1.5)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
points.InsertNextPoint(x_offset + 0.95, y_offset + 1.95, 1.5)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
points.InsertNextPoint(x_offset + 0.05, y_offset + 1.95, 1.5)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
# Mid-edge front face 24-27
points.InsertNextPoint(x_offset + 0.5, y_offset + 0.0, 4.0)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
points.InsertNextPoint(x_offset + 1.0, y_offset + 1.0, 4.5)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
points.InsertNextPoint(x_offset + 0.5, y_offset + 2.0, 5.0)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
points.InsertNextPoint(x_offset + 0.0, y_offset + 1.0, 4.5)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
# Mid-edge between common and front 28-31
points.InsertNextPoint(x_offset + 0.05, y_offset + 0.05, 3.5)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
points.InsertNextPoint(x_offset + 0.95, y_offset + 0.05, 3.5)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
points.InsertNextPoint(x_offset + 0.95, y_offset + 1.95, 4.0)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
points.InsertNextPoint(x_offset + 0.05, y_offset + 1.95, 4.0)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
id_list = vtkIdList()
for i in [pid, pid + 1, pid + 2, pid + 3,pid + 4, pid + 5, pid + 6, pid + 7,pid + 12, pid + 13, pid + 14, pid + 15,pid + 16, pid + 17, pid + 18, pid + 19,pid + 20, pid + 21, pid + 22, pid + 23]:
    id_list.InsertNextId(i)
cell_ids.InsertNextValue(cell_id)
cell_id += 1
grid.InsertNextCell(VTK_QUADRATIC_HEXAHEDRON, id_list)
id_list = vtkIdList()
for i in [pid + 4, pid + 5, pid + 6, pid + 7,pid + 8, pid + 9, pid + 10, pid + 11,pid + 16, pid + 17, pid + 18, pid + 19,pid + 24, pid + 25, pid + 26, pid + 27,pid + 28, pid + 29, pid + 30, pid + 31]:
    id_list.InsertNextId(i)
cell_ids.InsertNextValue(cell_id)
cell_id += 1
grid.InsertNextCell(VTK_QUADRATIC_HEXAHEDRON, id_list)

# Quadratic wedge: 2 sharing a triangle face
x_offset += 2.0
pid = point_id
# First wedge triangle face
points.InsertNextPoint(x_offset + 0.0, y_offset + 0.0, 1.0)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
points.InsertNextPoint(x_offset + 1.0, y_offset + 0.0, 1.0)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
points.InsertNextPoint(x_offset + 0.5, y_offset + 1.0, 1.0)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
# Common triangle face
points.InsertNextPoint(x_offset + 0.0, y_offset + 0.0, 0.0)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
points.InsertNextPoint(x_offset + 1.0, y_offset + 0.0, 0.0)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
points.InsertNextPoint(x_offset + 0.5, y_offset + 1.0, 0.0)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
# Second wedge triangle face
points.InsertNextPoint(x_offset + 0.1, y_offset + 0.1, -1.0)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
points.InsertNextPoint(x_offset + 0.9, y_offset + 0.1, -1.0)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
points.InsertNextPoint(x_offset + 0.5, y_offset + 0.9, -1.0)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
# Mid-edge first triangle face
points.InsertNextPoint(x_offset + 0.5, y_offset + 0.0, 1.0)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
points.InsertNextPoint(x_offset + 0.75, y_offset + 0.5, 1.0)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
points.InsertNextPoint(x_offset + 0.25, y_offset + 0.5, 1.0)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
# Mid-edge common triangle face
points.InsertNextPoint(x_offset + 0.5, y_offset + 0.0, 0.0)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
points.InsertNextPoint(x_offset + 0.75, y_offset + 0.5, 0.0)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
points.InsertNextPoint(x_offset + 0.25, y_offset + 0.5, 0.0)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
# Mid-edge first wedge lateral
points.InsertNextPoint(x_offset + 0.0, y_offset + 0.0, 0.5)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
points.InsertNextPoint(x_offset + 1.0, y_offset + 0.0, 0.5)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
points.InsertNextPoint(x_offset + 0.5, y_offset + 1.0, 0.5)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
# Mid-edge second wedge triangle face
points.InsertNextPoint(x_offset + 0.5, y_offset + 0.1, -1.0)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
points.InsertNextPoint(x_offset + 0.7, y_offset + 0.5, -1.0)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
points.InsertNextPoint(x_offset + 0.3, y_offset + 0.5, -1.0)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
# Mid-edge second wedge lateral
points.InsertNextPoint(x_offset + 0.05, y_offset + 0.05, -0.5)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
points.InsertNextPoint(x_offset + 0.95, y_offset + 0.05, -0.5)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
points.InsertNextPoint(x_offset + 0.5, y_offset + 0.95, -0.5)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
id_list = vtkIdList()
for i in [pid, pid + 1, pid + 2, pid + 3, pid + 4, pid + 5,pid + 9, pid + 10, pid + 11, pid + 12, pid + 13, pid + 14,pid + 15, pid + 16, pid + 17]:
    id_list.InsertNextId(i)
cell_ids.InsertNextValue(cell_id)
cell_id += 1
grid.InsertNextCell(VTK_QUADRATIC_WEDGE, id_list)
id_list = vtkIdList()
for i in [pid + 3, pid + 4, pid + 5, pid + 6, pid + 7, pid + 8,pid + 12, pid + 13, pid + 14, pid + 18, pid + 19, pid + 20,pid + 21, pid + 22, pid + 23]:
    id_list.InsertNextId(i)
cell_ids.InsertNextValue(cell_id)
cell_id += 1
grid.InsertNextCell(VTK_QUADRATIC_WEDGE, id_list)

# Quadratic pyramid: 2 sharing the base quad face
x_offset += 2.0
pid = point_id
# Quad face
points.InsertNextPoint(x_offset + 0.0, y_offset + 0.0, 0.2)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
points.InsertNextPoint(x_offset + 1.0, y_offset + 0.0, 0.0)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
points.InsertNextPoint(x_offset + 1.0, y_offset + 0.0, -1.0)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
points.InsertNextPoint(x_offset + 0.0, y_offset + 0.0, -1.2)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
# Top vertex
points.InsertNextPoint(x_offset + 0.5, y_offset + 1.0, -0.5)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
# Bottom vertex
points.InsertNextPoint(x_offset + 0.5, y_offset - 1.0, -0.5)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
# Mid-edge base
points.InsertNextPoint(x_offset + 0.5, y_offset + 0.0, 0.1)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
points.InsertNextPoint(x_offset + 1.0, y_offset + 0.0, -0.5)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
points.InsertNextPoint(x_offset + 0.5, y_offset + 0.0, -1.1)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
points.InsertNextPoint(x_offset + 0.0, y_offset + 0.0, -0.5)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
# Mid-edge to top
points.InsertNextPoint(x_offset + 0.25, y_offset + 0.5, -0.15)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
points.InsertNextPoint(x_offset + 0.75, y_offset + 0.5, -0.25)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
points.InsertNextPoint(x_offset + 0.75, y_offset + 0.5, -0.75)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
points.InsertNextPoint(x_offset + 0.25, y_offset + 0.5, -0.85)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
# Mid-edge to bottom
points.InsertNextPoint(x_offset + 0.25, y_offset - 0.5, -0.85)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
points.InsertNextPoint(x_offset + 0.75, y_offset - 0.5, -0.75)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
points.InsertNextPoint(x_offset + 0.75, y_offset - 0.5, -0.25)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
points.InsertNextPoint(x_offset + 0.25, y_offset - 0.5, -0.15)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
id_list = vtkIdList()
for i in [pid, pid + 1, pid + 2, pid + 3, pid + 4,pid + 6, pid + 7, pid + 8, pid + 9,pid + 10, pid + 11, pid + 12, pid + 13]:
    id_list.InsertNextId(i)
cell_ids.InsertNextValue(cell_id)
cell_id += 1
grid.InsertNextCell(VTK_QUADRATIC_PYRAMID, id_list)
id_list = vtkIdList()
for i in [pid + 3, pid + 2, pid + 1, pid, pid + 5,pid + 8, pid + 7, pid + 6, pid + 9,pid + 14, pid + 15, pid + 16, pid + 17]:
    id_list.InsertNextId(i)
cell_ids.InsertNextValue(cell_id)
cell_id += 1
grid.InsertNextCell(VTK_QUADRATIC_PYRAMID, id_list)

# ========== Polyhedron: 2 hexahedra sharing a face ==========
x_offset += 4.0
pid = point_id
points.InsertNextPoint(x_offset + 0.0, y_offset + 0.0, 0.0)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
points.InsertNextPoint(x_offset + 2.0, y_offset + 0.0, 0.0)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
points.InsertNextPoint(x_offset + 2.0, y_offset + 2.0, 0.0)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
points.InsertNextPoint(x_offset + 0.0, y_offset + 2.0, 0.0)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
points.InsertNextPoint(x_offset + 0.1, y_offset + 0.1, 3.0)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
points.InsertNextPoint(x_offset + 0.9, y_offset + 0.1, 3.0)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
points.InsertNextPoint(x_offset + 0.9, y_offset + 1.9, 3.0)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
points.InsertNextPoint(x_offset + 0.1, y_offset + 1.9, 3.0)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
points.InsertNextPoint(x_offset + 0.0, y_offset + 0.0, 4.0)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
points.InsertNextPoint(x_offset + 2.0, y_offset + 0.0, 4.0)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
points.InsertNextPoint(x_offset + 2.0, y_offset + 2.0, 5.0)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1
points.InsertNextPoint(x_offset + 0.0, y_offset + 2.0, 5.0)
scalars.InsertNextValue(scalar)
scalar += scalar_step
point_id += 1

# Polyhedron faces for first hex
face_stream_1 = [6,
                 4, pid, pid + 4, pid + 7, pid + 3,
                 4, pid + 1, pid + 2, pid + 6, pid + 5,
                 4, pid, pid + 1, pid + 5, pid + 4,
                 4, pid + 3, pid + 7, pid + 6, pid + 2,
                 4, pid, pid + 3, pid + 2, pid + 1,
                 4, pid + 4, pid + 5, pid + 6, pid + 7]
id_list_1 = vtkIdList()
for v in face_stream_1:
    id_list_1.InsertNextId(v)
cell_ids.InsertNextValue(cell_id)
cell_id += 1
grid.InsertNextCell(42, id_list_1)  # VTK_POLYHEDRON = 42

# Polyhedron faces for second hex
face_stream_2 = [6,
                 4, pid + 4, pid + 8, pid + 11, pid + 7,
                 4, pid + 5, pid + 6, pid + 10, pid + 9,
                 4, pid + 4, pid + 5, pid + 9, pid + 8,
                 4, pid + 7, pid + 11, pid + 10, pid + 6,
                 4, pid + 4, pid + 7, pid + 6, pid + 5,
                 4, pid + 8, pid + 9, pid + 10, pid + 11]
id_list_2 = vtkIdList()
for v in face_stream_2:
    id_list_2.InsertNextId(v)
cell_ids.InsertNextValue(cell_id)
cell_id += 1
grid.InsertNextCell(42, id_list_2)  # VTK_POLYHEDRON = 42

# ========== Assemble grid ==========
grid.SetPoints(points)
grid.GetPointData().SetScalars(scalars)
grid.GetCellData().SetScalars(cell_ids)

# Unstructured grid geometry filter
geom = vtkUnstructuredGridGeometryFilter()
geom.SetInputData(grid)
geom.Update()

# Geometry filter for final surface
linear_geom = vtkGeometryFilter()
linear_geom.SetInputConnection(geom.GetOutputPort())
linear_geom.Update()

# Blue-to-red lookup table
lut = vtkLookupTable()
lut.SetHueRange(0.667, 0.0)

# Mapper
mapper = vtkPolyDataMapper()
mapper.SetLookupTable(lut)
mapper.SetInputConnection(linear_geom.GetOutputPort())
if linear_geom.GetOutput().GetPointData().GetScalars():
    mapper.SetScalarRange(linear_geom.GetOutput().GetPointData().GetScalars().GetRange())

actor = vtkActor()
actor.SetMapper(mapper)

# Renderer
renderer = vtkRenderer()
renderer.SetBackground(0.5, 0.5, 0.5)
renderer.AddActor(actor)

# Window
render_window = vtkRenderWindow()
render_window.SetSize(300, 300)
render_window.AddRenderer(renderer)
render_window.SetWindowName("unstructuredgrid filter")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

render_window.Render()
interactor.Start()
