#!/usr/bin/env python

# Test vtkBoxClipDataSet on polydata: sphere polygons, triangles on box
# boundaries, co-planar triangles, lines from a cutter, and vertices.
# Four clipping modes per dataset shown in a 5-column x 4-row grid.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import (
    vtkDoubleArray,
    vtkPoints,
)
from vtkmodules.vtkCommonDataModel import (
    vtkCellArray,
    vtkPlane,
    vtkPolyData,
)
from vtkmodules.vtkFiltersCore import vtkCutter
from vtkmodules.vtkFiltersGeneral import vtkBoxClipDataSet
from vtkmodules.vtkFiltersGeometry import vtkDataSetSurfaceFilter
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

minusx = [-1.0, 0.0, 0.0]
minusy = [0.0, -1.0, 0.0]
minusz = [0.0, 0.0, -1.0]
plusx = [1.0, 0.0, 0.0]
plusy = [0.0, 1.0, 0.0]
plusz = [0.0, 0.0, 1.0]

# --- Build the 5 polydata inputs ---

# Dataset 0: sphere polygons
sphere = vtkSphereSource()
sphere.Update()

# Dataset 1 & 2: triangles
num_triangles = 6
triangle_coords = [
    -4.0, -1.0, 0.0, -2.0, -1.0, 0.0, -3.0, -0.5, 0.0,
    -2.0, -1.0, 0.0, -1.0e-17, -1.0, 0.0, -1.0, -0.5, 0.0,
    -3.0, 0.25, 0.0, -4.0, -0.25, 0.0, -2.0, -0.25, 0.0,
    -1.0, 0.25, 0.0, -2.0, -0.25, 0.0, 1.0e-17, -0.25, 0.0,
    -2.0, 0.5, 0.0, -3.0, 1.0, 0.0, -4.0, 0.5, 0.0,
    1.0e-17, 0.5, 0.0, -1.0, 1.0, 0.0, -2.0, 0.5, 0.0,
]

tri_pts_arr = vtkDoubleArray()
tri_pts_arr.SetNumberOfComponents(3)
tri_pts_arr.SetNumberOfTuples(num_triangles * 3)
for i in range(num_triangles * 3):
    tri_pts_arr.SetTuple3(i, triangle_coords[i * 3], triangle_coords[i * 3 + 1], triangle_coords[i * 3 + 2])

tri_points = vtkPoints()
tri_points.SetData(tri_pts_arr)

tri_normals = vtkDoubleArray()
tri_normals.SetName("Normals")
tri_normals.SetNumberOfComponents(3)
tri_normals.SetNumberOfTuples(num_triangles)
for i in range(num_triangles):
    tri_normals.SetTuple3(i, 0.0, 0.0, 1.0)

tri_cells = vtkCellArray()
for i in range(num_triangles):
    tri_cells.InsertNextCell(3, [i * 3, i * 3 + 1, i * 3 + 2])

triangles = vtkPolyData()
triangles.SetPoints(tri_points)
triangles.SetPolys(tri_cells)
triangles.GetCellData().SetNormals(tri_normals)

# Dataset 3: lines from cutting a sphere with a plane
sphere_no_normals = vtkPolyData()
sphere_no_normals.CopyStructure(sphere.GetOutput())

plane = vtkPlane()
plane.SetOrigin(0.0, 0.0, 0.0)
plane.SetNormal(0.0, 0.0, 1.0)

cutter = vtkCutter()
cutter.SetInputData(sphere_no_normals)
cutter.SetCutFunction(plane)
cutter.Update()

# Dataset 4: vertices from sphere points
verts_pd = vtkPolyData()
verts_pd.SetPoints(sphere_no_normals.GetPoints())
vert_cells = vtkCellArray()
for i in range(sphere_no_normals.GetPoints().GetNumberOfPoints()):
    vert_cells.InsertNextCell(1, [i])
verts_pd.SetVerts(vert_cells)

# Bounds for each column
sphere_min = [-1.00002, -0.50002, -0.50002]
sphere_max = [-0.0511337, 0.5, 0.5]
tri_a_min = [-3.0, -1.0, -1.0]
tri_a_max = [-1.0, 1.0, 1.0]
tri_b_min = [-3.0, -1.0, 0.0]
tri_b_max = [0.0, 0.5, 1.0]

# ========== Col 0: sphere polygons ==========

# Row 0: axis-aligned, no clipped output
clip_c0_r0 = vtkBoxClipDataSet()
clip_c0_r0.SetInputData(sphere.GetOutput())
clip_c0_r0.GenerateClippedOutputOff()
clip_c0_r0.SetBoxClip(sphere_min[0], sphere_max[0], sphere_min[1], sphere_max[1], sphere_min[2], sphere_max[2])
surface_c0_r0 = vtkDataSetSurfaceFilter()
surface_c0_r0.SetInputConnection(clip_c0_r0.GetOutputPort(0))
mapper_c0_r0 = vtkPolyDataMapper()
mapper_c0_r0.SetInputConnection(surface_c0_r0.GetOutputPort())
actor_c0_r0 = vtkActor()
actor_c0_r0.SetMapper(mapper_c0_r0)
actor_c0_r0.GetProperty().SetPointSize(3.0)
renderer_c0_r0 = vtkRenderer()
renderer_c0_r0.AddActor(actor_c0_r0)
renderer_c0_r0.SetBackground(0.0, 0.5, 0.5)
renderer_c0_r0.SetViewport(0.0, 0.75, 0.2, 1.0)

# Row 1: axis-aligned, with clipped output
clip_c0_r1 = vtkBoxClipDataSet()
clip_c0_r1.SetInputData(sphere.GetOutput())
clip_c0_r1.GenerateClippedOutputOn()
clip_c0_r1.SetBoxClip(sphere_min[0], sphere_max[0], sphere_min[1], sphere_max[1], sphere_min[2], sphere_max[2])
surface_c0_r1_in = vtkDataSetSurfaceFilter()
surface_c0_r1_in.SetInputConnection(clip_c0_r1.GetOutputPort(0))
mapper_c0_r1_in = vtkPolyDataMapper()
mapper_c0_r1_in.SetInputConnection(surface_c0_r1_in.GetOutputPort())
actor_c0_r1_in = vtkActor()
actor_c0_r1_in.SetMapper(mapper_c0_r1_in)
actor_c0_r1_in.GetProperty().SetPointSize(3.0)
surface_c0_r1_out = vtkDataSetSurfaceFilter()
surface_c0_r1_out.SetInputConnection(clip_c0_r1.GetOutputPort(1))
mapper_c0_r1_out = vtkPolyDataMapper()
mapper_c0_r1_out.SetInputConnection(surface_c0_r1_out.GetOutputPort())
actor_c0_r1_out = vtkActor()
actor_c0_r1_out.SetMapper(mapper_c0_r1_out)
actor_c0_r1_out.GetProperty().SetColor(1.0, 0.5, 0.5)
actor_c0_r1_out.GetProperty().SetPointSize(3.0)
renderer_c0_r1 = vtkRenderer()
renderer_c0_r1.AddActor(actor_c0_r1_in)
renderer_c0_r1.AddActor(actor_c0_r1_out)
renderer_c0_r1.SetBackground(0.0, 0.5, 0.5)
renderer_c0_r1.SetViewport(0.0, 0.5, 0.2, 0.75)

# Row 2: oriented, no clipped output
clip_c0_r2 = vtkBoxClipDataSet()
clip_c0_r2.SetInputData(sphere.GetOutput())
clip_c0_r2.GenerateClippedOutputOff()
clip_c0_r2.SetBoxClip(minusx, sphere_min, minusy, sphere_min, minusz, sphere_min,
                       plusx, sphere_max, plusy, sphere_max, plusz, sphere_max)
surface_c0_r2 = vtkDataSetSurfaceFilter()
surface_c0_r2.SetInputConnection(clip_c0_r2.GetOutputPort(0))
mapper_c0_r2 = vtkPolyDataMapper()
mapper_c0_r2.SetInputConnection(surface_c0_r2.GetOutputPort())
actor_c0_r2 = vtkActor()
actor_c0_r2.SetMapper(mapper_c0_r2)
actor_c0_r2.GetProperty().SetPointSize(3.0)
renderer_c0_r2 = vtkRenderer()
renderer_c0_r2.AddActor(actor_c0_r2)
renderer_c0_r2.SetBackground(0.0, 0.5, 0.5)
renderer_c0_r2.SetViewport(0.0, 0.25, 0.2, 0.5)

# Row 3: oriented, with clipped output
clip_c0_r3 = vtkBoxClipDataSet()
clip_c0_r3.SetInputData(sphere.GetOutput())
clip_c0_r3.GenerateClippedOutputOn()
clip_c0_r3.SetBoxClip(minusx, sphere_min, minusy, sphere_min, minusz, sphere_min,
                       plusx, sphere_max, plusy, sphere_max, plusz, sphere_max)
surface_c0_r3_in = vtkDataSetSurfaceFilter()
surface_c0_r3_in.SetInputConnection(clip_c0_r3.GetOutputPort(0))
mapper_c0_r3_in = vtkPolyDataMapper()
mapper_c0_r3_in.SetInputConnection(surface_c0_r3_in.GetOutputPort())
actor_c0_r3_in = vtkActor()
actor_c0_r3_in.SetMapper(mapper_c0_r3_in)
actor_c0_r3_in.GetProperty().SetPointSize(3.0)
surface_c0_r3_out = vtkDataSetSurfaceFilter()
surface_c0_r3_out.SetInputConnection(clip_c0_r3.GetOutputPort(1))
mapper_c0_r3_out = vtkPolyDataMapper()
mapper_c0_r3_out.SetInputConnection(surface_c0_r3_out.GetOutputPort())
actor_c0_r3_out = vtkActor()
actor_c0_r3_out.SetMapper(mapper_c0_r3_out)
actor_c0_r3_out.GetProperty().SetColor(1.0, 0.5, 0.5)
actor_c0_r3_out.GetProperty().SetPointSize(3.0)
renderer_c0_r3 = vtkRenderer()
renderer_c0_r3.AddActor(actor_c0_r3_in)
renderer_c0_r3.AddActor(actor_c0_r3_out)
renderer_c0_r3.SetBackground(0.0, 0.5, 0.5)
renderer_c0_r3.SetViewport(0.0, 0.0, 0.2, 0.25)

# ========== Col 1: triangles, bounds A ==========

# Row 0: axis-aligned, no clipped output
clip_c1_r0 = vtkBoxClipDataSet()
clip_c1_r0.SetInputData(triangles)
clip_c1_r0.GenerateClippedOutputOff()
clip_c1_r0.SetBoxClip(tri_a_min[0], tri_a_max[0], tri_a_min[1], tri_a_max[1], tri_a_min[2], tri_a_max[2])
surface_c1_r0 = vtkDataSetSurfaceFilter()
surface_c1_r0.SetInputConnection(clip_c1_r0.GetOutputPort(0))
mapper_c1_r0 = vtkPolyDataMapper()
mapper_c1_r0.SetInputConnection(surface_c1_r0.GetOutputPort())
actor_c1_r0 = vtkActor()
actor_c1_r0.SetMapper(mapper_c1_r0)
actor_c1_r0.GetProperty().SetPointSize(3.0)
renderer_c1_r0 = vtkRenderer()
renderer_c1_r0.AddActor(actor_c1_r0)
renderer_c1_r0.SetBackground(0.0, 0.5, 0.5)
renderer_c1_r0.SetViewport(0.2, 0.75, 0.4, 1.0)

# Row 1: axis-aligned, with clipped output
clip_c1_r1 = vtkBoxClipDataSet()
clip_c1_r1.SetInputData(triangles)
clip_c1_r1.GenerateClippedOutputOn()
clip_c1_r1.SetBoxClip(tri_a_min[0], tri_a_max[0], tri_a_min[1], tri_a_max[1], tri_a_min[2], tri_a_max[2])
surface_c1_r1_in = vtkDataSetSurfaceFilter()
surface_c1_r1_in.SetInputConnection(clip_c1_r1.GetOutputPort(0))
mapper_c1_r1_in = vtkPolyDataMapper()
mapper_c1_r1_in.SetInputConnection(surface_c1_r1_in.GetOutputPort())
actor_c1_r1_in = vtkActor()
actor_c1_r1_in.SetMapper(mapper_c1_r1_in)
actor_c1_r1_in.GetProperty().SetPointSize(3.0)
surface_c1_r1_out = vtkDataSetSurfaceFilter()
surface_c1_r1_out.SetInputConnection(clip_c1_r1.GetOutputPort(1))
mapper_c1_r1_out = vtkPolyDataMapper()
mapper_c1_r1_out.SetInputConnection(surface_c1_r1_out.GetOutputPort())
actor_c1_r1_out = vtkActor()
actor_c1_r1_out.SetMapper(mapper_c1_r1_out)
actor_c1_r1_out.GetProperty().SetColor(1.0, 0.5, 0.5)
actor_c1_r1_out.GetProperty().SetPointSize(3.0)
renderer_c1_r1 = vtkRenderer()
renderer_c1_r1.AddActor(actor_c1_r1_in)
renderer_c1_r1.AddActor(actor_c1_r1_out)
renderer_c1_r1.SetBackground(0.0, 0.5, 0.5)
renderer_c1_r1.SetViewport(0.2, 0.5, 0.4, 0.75)

# Row 2: oriented, no clipped output
clip_c1_r2 = vtkBoxClipDataSet()
clip_c1_r2.SetInputData(triangles)
clip_c1_r2.GenerateClippedOutputOff()
clip_c1_r2.SetBoxClip(minusx, tri_a_min, minusy, tri_a_min, minusz, tri_a_min,
                       plusx, tri_a_max, plusy, tri_a_max, plusz, tri_a_max)
surface_c1_r2 = vtkDataSetSurfaceFilter()
surface_c1_r2.SetInputConnection(clip_c1_r2.GetOutputPort(0))
mapper_c1_r2 = vtkPolyDataMapper()
mapper_c1_r2.SetInputConnection(surface_c1_r2.GetOutputPort())
actor_c1_r2 = vtkActor()
actor_c1_r2.SetMapper(mapper_c1_r2)
actor_c1_r2.GetProperty().SetPointSize(3.0)
renderer_c1_r2 = vtkRenderer()
renderer_c1_r2.AddActor(actor_c1_r2)
renderer_c1_r2.SetBackground(0.0, 0.5, 0.5)
renderer_c1_r2.SetViewport(0.2, 0.25, 0.4, 0.5)

# Row 3: oriented, with clipped output
clip_c1_r3 = vtkBoxClipDataSet()
clip_c1_r3.SetInputData(triangles)
clip_c1_r3.GenerateClippedOutputOn()
clip_c1_r3.SetBoxClip(minusx, tri_a_min, minusy, tri_a_min, minusz, tri_a_min,
                       plusx, tri_a_max, plusy, tri_a_max, plusz, tri_a_max)
surface_c1_r3_in = vtkDataSetSurfaceFilter()
surface_c1_r3_in.SetInputConnection(clip_c1_r3.GetOutputPort(0))
mapper_c1_r3_in = vtkPolyDataMapper()
mapper_c1_r3_in.SetInputConnection(surface_c1_r3_in.GetOutputPort())
actor_c1_r3_in = vtkActor()
actor_c1_r3_in.SetMapper(mapper_c1_r3_in)
actor_c1_r3_in.GetProperty().SetPointSize(3.0)
surface_c1_r3_out = vtkDataSetSurfaceFilter()
surface_c1_r3_out.SetInputConnection(clip_c1_r3.GetOutputPort(1))
mapper_c1_r3_out = vtkPolyDataMapper()
mapper_c1_r3_out.SetInputConnection(surface_c1_r3_out.GetOutputPort())
actor_c1_r3_out = vtkActor()
actor_c1_r3_out.SetMapper(mapper_c1_r3_out)
actor_c1_r3_out.GetProperty().SetColor(1.0, 0.5, 0.5)
actor_c1_r3_out.GetProperty().SetPointSize(3.0)
renderer_c1_r3 = vtkRenderer()
renderer_c1_r3.AddActor(actor_c1_r3_in)
renderer_c1_r3.AddActor(actor_c1_r3_out)
renderer_c1_r3.SetBackground(0.0, 0.5, 0.5)
renderer_c1_r3.SetViewport(0.2, 0.0, 0.4, 0.25)

# ========== Col 2: triangles, bounds B ==========

# Row 0: axis-aligned, no clipped output
clip_c2_r0 = vtkBoxClipDataSet()
clip_c2_r0.SetInputData(triangles)
clip_c2_r0.GenerateClippedOutputOff()
clip_c2_r0.SetBoxClip(tri_b_min[0], tri_b_max[0], tri_b_min[1], tri_b_max[1], tri_b_min[2], tri_b_max[2])
surface_c2_r0 = vtkDataSetSurfaceFilter()
surface_c2_r0.SetInputConnection(clip_c2_r0.GetOutputPort(0))
mapper_c2_r0 = vtkPolyDataMapper()
mapper_c2_r0.SetInputConnection(surface_c2_r0.GetOutputPort())
actor_c2_r0 = vtkActor()
actor_c2_r0.SetMapper(mapper_c2_r0)
actor_c2_r0.GetProperty().SetPointSize(3.0)
renderer_c2_r0 = vtkRenderer()
renderer_c2_r0.AddActor(actor_c2_r0)
renderer_c2_r0.SetBackground(0.0, 0.5, 0.5)
renderer_c2_r0.SetViewport(0.4, 0.75, 0.6, 1.0)

# Row 1: axis-aligned, with clipped output
clip_c2_r1 = vtkBoxClipDataSet()
clip_c2_r1.SetInputData(triangles)
clip_c2_r1.GenerateClippedOutputOn()
clip_c2_r1.SetBoxClip(tri_b_min[0], tri_b_max[0], tri_b_min[1], tri_b_max[1], tri_b_min[2], tri_b_max[2])
surface_c2_r1_in = vtkDataSetSurfaceFilter()
surface_c2_r1_in.SetInputConnection(clip_c2_r1.GetOutputPort(0))
mapper_c2_r1_in = vtkPolyDataMapper()
mapper_c2_r1_in.SetInputConnection(surface_c2_r1_in.GetOutputPort())
actor_c2_r1_in = vtkActor()
actor_c2_r1_in.SetMapper(mapper_c2_r1_in)
actor_c2_r1_in.GetProperty().SetPointSize(3.0)
surface_c2_r1_out = vtkDataSetSurfaceFilter()
surface_c2_r1_out.SetInputConnection(clip_c2_r1.GetOutputPort(1))
mapper_c2_r1_out = vtkPolyDataMapper()
mapper_c2_r1_out.SetInputConnection(surface_c2_r1_out.GetOutputPort())
actor_c2_r1_out = vtkActor()
actor_c2_r1_out.SetMapper(mapper_c2_r1_out)
actor_c2_r1_out.GetProperty().SetColor(1.0, 0.5, 0.5)
actor_c2_r1_out.GetProperty().SetPointSize(3.0)
renderer_c2_r1 = vtkRenderer()
renderer_c2_r1.AddActor(actor_c2_r1_in)
renderer_c2_r1.AddActor(actor_c2_r1_out)
renderer_c2_r1.SetBackground(0.0, 0.5, 0.5)
renderer_c2_r1.SetViewport(0.4, 0.5, 0.6, 0.75)

# Row 2: oriented, no clipped output
clip_c2_r2 = vtkBoxClipDataSet()
clip_c2_r2.SetInputData(triangles)
clip_c2_r2.GenerateClippedOutputOff()
clip_c2_r2.SetBoxClip(minusx, tri_b_min, minusy, tri_b_min, minusz, tri_b_min,
                       plusx, tri_b_max, plusy, tri_b_max, plusz, tri_b_max)
surface_c2_r2 = vtkDataSetSurfaceFilter()
surface_c2_r2.SetInputConnection(clip_c2_r2.GetOutputPort(0))
mapper_c2_r2 = vtkPolyDataMapper()
mapper_c2_r2.SetInputConnection(surface_c2_r2.GetOutputPort())
actor_c2_r2 = vtkActor()
actor_c2_r2.SetMapper(mapper_c2_r2)
actor_c2_r2.GetProperty().SetPointSize(3.0)
renderer_c2_r2 = vtkRenderer()
renderer_c2_r2.AddActor(actor_c2_r2)
renderer_c2_r2.SetBackground(0.0, 0.5, 0.5)
renderer_c2_r2.SetViewport(0.4, 0.25, 0.6, 0.5)

# Row 3: oriented, with clipped output
clip_c2_r3 = vtkBoxClipDataSet()
clip_c2_r3.SetInputData(triangles)
clip_c2_r3.GenerateClippedOutputOn()
clip_c2_r3.SetBoxClip(minusx, tri_b_min, minusy, tri_b_min, minusz, tri_b_min,
                       plusx, tri_b_max, plusy, tri_b_max, plusz, tri_b_max)
surface_c2_r3_in = vtkDataSetSurfaceFilter()
surface_c2_r3_in.SetInputConnection(clip_c2_r3.GetOutputPort(0))
mapper_c2_r3_in = vtkPolyDataMapper()
mapper_c2_r3_in.SetInputConnection(surface_c2_r3_in.GetOutputPort())
actor_c2_r3_in = vtkActor()
actor_c2_r3_in.SetMapper(mapper_c2_r3_in)
actor_c2_r3_in.GetProperty().SetPointSize(3.0)
surface_c2_r3_out = vtkDataSetSurfaceFilter()
surface_c2_r3_out.SetInputConnection(clip_c2_r3.GetOutputPort(1))
mapper_c2_r3_out = vtkPolyDataMapper()
mapper_c2_r3_out.SetInputConnection(surface_c2_r3_out.GetOutputPort())
actor_c2_r3_out = vtkActor()
actor_c2_r3_out.SetMapper(mapper_c2_r3_out)
actor_c2_r3_out.GetProperty().SetColor(1.0, 0.5, 0.5)
actor_c2_r3_out.GetProperty().SetPointSize(3.0)
renderer_c2_r3 = vtkRenderer()
renderer_c2_r3.AddActor(actor_c2_r3_in)
renderer_c2_r3.AddActor(actor_c2_r3_out)
renderer_c2_r3.SetBackground(0.0, 0.5, 0.5)
renderer_c2_r3.SetViewport(0.4, 0.0, 0.6, 0.25)

# ========== Col 3: cutter lines ==========

# Row 0: axis-aligned, no clipped output
clip_c3_r0 = vtkBoxClipDataSet()
clip_c3_r0.SetInputData(cutter.GetOutput())
clip_c3_r0.GenerateClippedOutputOff()
clip_c3_r0.SetBoxClip(sphere_min[0], sphere_max[0], sphere_min[1], sphere_max[1], sphere_min[2], sphere_max[2])
surface_c3_r0 = vtkDataSetSurfaceFilter()
surface_c3_r0.SetInputConnection(clip_c3_r0.GetOutputPort(0))
mapper_c3_r0 = vtkPolyDataMapper()
mapper_c3_r0.SetInputConnection(surface_c3_r0.GetOutputPort())
actor_c3_r0 = vtkActor()
actor_c3_r0.SetMapper(mapper_c3_r0)
actor_c3_r0.GetProperty().SetPointSize(3.0)
renderer_c3_r0 = vtkRenderer()
renderer_c3_r0.AddActor(actor_c3_r0)
renderer_c3_r0.SetBackground(0.0, 0.5, 0.5)
renderer_c3_r0.SetViewport(0.6, 0.75, 0.8, 1.0)

# Row 1: axis-aligned, with clipped output
clip_c3_r1 = vtkBoxClipDataSet()
clip_c3_r1.SetInputData(cutter.GetOutput())
clip_c3_r1.GenerateClippedOutputOn()
clip_c3_r1.SetBoxClip(sphere_min[0], sphere_max[0], sphere_min[1], sphere_max[1], sphere_min[2], sphere_max[2])
surface_c3_r1_in = vtkDataSetSurfaceFilter()
surface_c3_r1_in.SetInputConnection(clip_c3_r1.GetOutputPort(0))
mapper_c3_r1_in = vtkPolyDataMapper()
mapper_c3_r1_in.SetInputConnection(surface_c3_r1_in.GetOutputPort())
actor_c3_r1_in = vtkActor()
actor_c3_r1_in.SetMapper(mapper_c3_r1_in)
actor_c3_r1_in.GetProperty().SetPointSize(3.0)
surface_c3_r1_out = vtkDataSetSurfaceFilter()
surface_c3_r1_out.SetInputConnection(clip_c3_r1.GetOutputPort(1))
mapper_c3_r1_out = vtkPolyDataMapper()
mapper_c3_r1_out.SetInputConnection(surface_c3_r1_out.GetOutputPort())
actor_c3_r1_out = vtkActor()
actor_c3_r1_out.SetMapper(mapper_c3_r1_out)
actor_c3_r1_out.GetProperty().SetColor(1.0, 0.5, 0.5)
actor_c3_r1_out.GetProperty().SetPointSize(3.0)
renderer_c3_r1 = vtkRenderer()
renderer_c3_r1.AddActor(actor_c3_r1_in)
renderer_c3_r1.AddActor(actor_c3_r1_out)
renderer_c3_r1.SetBackground(0.0, 0.5, 0.5)
renderer_c3_r1.SetViewport(0.6, 0.5, 0.8, 0.75)

# Row 2: oriented, no clipped output
clip_c3_r2 = vtkBoxClipDataSet()
clip_c3_r2.SetInputData(cutter.GetOutput())
clip_c3_r2.GenerateClippedOutputOff()
clip_c3_r2.SetBoxClip(minusx, sphere_min, minusy, sphere_min, minusz, sphere_min,
                       plusx, sphere_max, plusy, sphere_max, plusz, sphere_max)
surface_c3_r2 = vtkDataSetSurfaceFilter()
surface_c3_r2.SetInputConnection(clip_c3_r2.GetOutputPort(0))
mapper_c3_r2 = vtkPolyDataMapper()
mapper_c3_r2.SetInputConnection(surface_c3_r2.GetOutputPort())
actor_c3_r2 = vtkActor()
actor_c3_r2.SetMapper(mapper_c3_r2)
actor_c3_r2.GetProperty().SetPointSize(3.0)
renderer_c3_r2 = vtkRenderer()
renderer_c3_r2.AddActor(actor_c3_r2)
renderer_c3_r2.SetBackground(0.0, 0.5, 0.5)
renderer_c3_r2.SetViewport(0.6, 0.25, 0.8, 0.5)

# Row 3: oriented, with clipped output
clip_c3_r3 = vtkBoxClipDataSet()
clip_c3_r3.SetInputData(cutter.GetOutput())
clip_c3_r3.GenerateClippedOutputOn()
clip_c3_r3.SetBoxClip(minusx, sphere_min, minusy, sphere_min, minusz, sphere_min,
                       plusx, sphere_max, plusy, sphere_max, plusz, sphere_max)
surface_c3_r3_in = vtkDataSetSurfaceFilter()
surface_c3_r3_in.SetInputConnection(clip_c3_r3.GetOutputPort(0))
mapper_c3_r3_in = vtkPolyDataMapper()
mapper_c3_r3_in.SetInputConnection(surface_c3_r3_in.GetOutputPort())
actor_c3_r3_in = vtkActor()
actor_c3_r3_in.SetMapper(mapper_c3_r3_in)
actor_c3_r3_in.GetProperty().SetPointSize(3.0)
surface_c3_r3_out = vtkDataSetSurfaceFilter()
surface_c3_r3_out.SetInputConnection(clip_c3_r3.GetOutputPort(1))
mapper_c3_r3_out = vtkPolyDataMapper()
mapper_c3_r3_out.SetInputConnection(surface_c3_r3_out.GetOutputPort())
actor_c3_r3_out = vtkActor()
actor_c3_r3_out.SetMapper(mapper_c3_r3_out)
actor_c3_r3_out.GetProperty().SetColor(1.0, 0.5, 0.5)
actor_c3_r3_out.GetProperty().SetPointSize(3.0)
renderer_c3_r3 = vtkRenderer()
renderer_c3_r3.AddActor(actor_c3_r3_in)
renderer_c3_r3.AddActor(actor_c3_r3_out)
renderer_c3_r3.SetBackground(0.0, 0.5, 0.5)
renderer_c3_r3.SetViewport(0.6, 0.0, 0.8, 0.25)

# ========== Col 4: vertices ==========

# Row 0: axis-aligned, no clipped output
clip_c4_r0 = vtkBoxClipDataSet()
clip_c4_r0.SetInputData(verts_pd)
clip_c4_r0.GenerateClippedOutputOff()
clip_c4_r0.SetBoxClip(sphere_min[0], sphere_max[0], sphere_min[1], sphere_max[1], sphere_min[2], sphere_max[2])
surface_c4_r0 = vtkDataSetSurfaceFilter()
surface_c4_r0.SetInputConnection(clip_c4_r0.GetOutputPort(0))
mapper_c4_r0 = vtkPolyDataMapper()
mapper_c4_r0.SetInputConnection(surface_c4_r0.GetOutputPort())
actor_c4_r0 = vtkActor()
actor_c4_r0.SetMapper(mapper_c4_r0)
actor_c4_r0.GetProperty().SetPointSize(3.0)
renderer_c4_r0 = vtkRenderer()
renderer_c4_r0.AddActor(actor_c4_r0)
renderer_c4_r0.SetBackground(0.0, 0.5, 0.5)
renderer_c4_r0.SetViewport(0.8, 0.75, 1.0, 1.0)

# Row 1: axis-aligned, with clipped output
clip_c4_r1 = vtkBoxClipDataSet()
clip_c4_r1.SetInputData(verts_pd)
clip_c4_r1.GenerateClippedOutputOn()
clip_c4_r1.SetBoxClip(sphere_min[0], sphere_max[0], sphere_min[1], sphere_max[1], sphere_min[2], sphere_max[2])
surface_c4_r1_in = vtkDataSetSurfaceFilter()
surface_c4_r1_in.SetInputConnection(clip_c4_r1.GetOutputPort(0))
mapper_c4_r1_in = vtkPolyDataMapper()
mapper_c4_r1_in.SetInputConnection(surface_c4_r1_in.GetOutputPort())
actor_c4_r1_in = vtkActor()
actor_c4_r1_in.SetMapper(mapper_c4_r1_in)
actor_c4_r1_in.GetProperty().SetPointSize(3.0)
surface_c4_r1_out = vtkDataSetSurfaceFilter()
surface_c4_r1_out.SetInputConnection(clip_c4_r1.GetOutputPort(1))
mapper_c4_r1_out = vtkPolyDataMapper()
mapper_c4_r1_out.SetInputConnection(surface_c4_r1_out.GetOutputPort())
actor_c4_r1_out = vtkActor()
actor_c4_r1_out.SetMapper(mapper_c4_r1_out)
actor_c4_r1_out.GetProperty().SetColor(1.0, 0.5, 0.5)
actor_c4_r1_out.GetProperty().SetPointSize(3.0)
renderer_c4_r1 = vtkRenderer()
renderer_c4_r1.AddActor(actor_c4_r1_in)
renderer_c4_r1.AddActor(actor_c4_r1_out)
renderer_c4_r1.SetBackground(0.0, 0.5, 0.5)
renderer_c4_r1.SetViewport(0.8, 0.5, 1.0, 0.75)

# Row 2: oriented, no clipped output
clip_c4_r2 = vtkBoxClipDataSet()
clip_c4_r2.SetInputData(verts_pd)
clip_c4_r2.GenerateClippedOutputOff()
clip_c4_r2.SetBoxClip(minusx, sphere_min, minusy, sphere_min, minusz, sphere_min,
                       plusx, sphere_max, plusy, sphere_max, plusz, sphere_max)
surface_c4_r2 = vtkDataSetSurfaceFilter()
surface_c4_r2.SetInputConnection(clip_c4_r2.GetOutputPort(0))
mapper_c4_r2 = vtkPolyDataMapper()
mapper_c4_r2.SetInputConnection(surface_c4_r2.GetOutputPort())
actor_c4_r2 = vtkActor()
actor_c4_r2.SetMapper(mapper_c4_r2)
actor_c4_r2.GetProperty().SetPointSize(3.0)
renderer_c4_r2 = vtkRenderer()
renderer_c4_r2.AddActor(actor_c4_r2)
renderer_c4_r2.SetBackground(0.0, 0.5, 0.5)
renderer_c4_r2.SetViewport(0.8, 0.25, 1.0, 0.5)

# Row 3: oriented, with clipped output
clip_c4_r3 = vtkBoxClipDataSet()
clip_c4_r3.SetInputData(verts_pd)
clip_c4_r3.GenerateClippedOutputOn()
clip_c4_r3.SetBoxClip(minusx, sphere_min, minusy, sphere_min, minusz, sphere_min,
                       plusx, sphere_max, plusy, sphere_max, plusz, sphere_max)
surface_c4_r3_in = vtkDataSetSurfaceFilter()
surface_c4_r3_in.SetInputConnection(clip_c4_r3.GetOutputPort(0))
mapper_c4_r3_in = vtkPolyDataMapper()
mapper_c4_r3_in.SetInputConnection(surface_c4_r3_in.GetOutputPort())
actor_c4_r3_in = vtkActor()
actor_c4_r3_in.SetMapper(mapper_c4_r3_in)
actor_c4_r3_in.GetProperty().SetPointSize(3.0)
surface_c4_r3_out = vtkDataSetSurfaceFilter()
surface_c4_r3_out.SetInputConnection(clip_c4_r3.GetOutputPort(1))
mapper_c4_r3_out = vtkPolyDataMapper()
mapper_c4_r3_out.SetInputConnection(surface_c4_r3_out.GetOutputPort())
actor_c4_r3_out = vtkActor()
actor_c4_r3_out.SetMapper(mapper_c4_r3_out)
actor_c4_r3_out.GetProperty().SetColor(1.0, 0.5, 0.5)
actor_c4_r3_out.GetProperty().SetPointSize(3.0)
renderer_c4_r3 = vtkRenderer()
renderer_c4_r3.AddActor(actor_c4_r3_in)
renderer_c4_r3.AddActor(actor_c4_r3_out)
renderer_c4_r3.SetBackground(0.0, 0.5, 0.5)
renderer_c4_r3.SetViewport(0.8, 0.0, 1.0, 0.25)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer_c0_r0)
render_window.AddRenderer(renderer_c0_r1)
render_window.AddRenderer(renderer_c0_r2)
render_window.AddRenderer(renderer_c0_r3)
render_window.AddRenderer(renderer_c1_r0)
render_window.AddRenderer(renderer_c1_r1)
render_window.AddRenderer(renderer_c1_r2)
render_window.AddRenderer(renderer_c1_r3)
render_window.AddRenderer(renderer_c2_r0)
render_window.AddRenderer(renderer_c2_r1)
render_window.AddRenderer(renderer_c2_r2)
render_window.AddRenderer(renderer_c2_r3)
render_window.AddRenderer(renderer_c3_r0)
render_window.AddRenderer(renderer_c3_r1)
render_window.AddRenderer(renderer_c3_r2)
render_window.AddRenderer(renderer_c3_r3)
render_window.AddRenderer(renderer_c4_r0)
render_window.AddRenderer(renderer_c4_r1)
render_window.AddRenderer(renderer_c4_r2)
render_window.AddRenderer(renderer_c4_r3)
render_window.SetSize(800, 640)
render_window.SetWindowName("box clip polydata")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
