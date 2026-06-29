#!/usr/bin/env python

# Cut a quadratic hexahedron and a linear hexahedron with a plane,
# comparing triangle-generating and polygon-generating cutter modes
# displayed in three viewports.

from math import sqrt

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import (
    vtkFloatArray,
    vtkIdList,
    vtkPoints,
)
from vtkmodules.vtkCommonDataModel import (
    VTK_HEXAHEDRON,
    VTK_QUADRATIC_HEXAHEDRON,
    vtkPlane,
    vtkUnstructuredGrid,
)
from vtkmodules.vtkFiltersCore import vtkCutter
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkDataSetMapper,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Cut plane
plane = vtkPlane()
plane.SetOrigin(5, 5, 9.8)
plane.SetNormal(0, 0, 1)

# Build mesh with a quadratic hex and a linear hex
coords = [
    (0, 0, 0), (10, 0, 0), (10, 10, 0), (0, 10, 0),
    (0, 0, 10), (10, 0, 10), (10, 10, 10), (0, 10, 10),
    (5, 0, 0), (10, 5, 0), (5, 10, 0), (0, 5, 0),
    (5, 0, 9.5), (10, 5, 9.3), (5, 10, 9.5), (0, 5, 9.3),
    (0, 0, 5), (10, 0, 5), (10, 10, 5), (0, 10, 5),
]

data = vtkFloatArray()
points = vtkPoints()
pt_ids = vtkIdList()
mesh = vtkUnstructuredGrid()
mesh.SetPoints(points)
mesh.GetPointData().SetScalars(data)

# Insert quadratic hex points
for pid in range(20):
    x, y, z = coords[pid]
    pt_ids.InsertNextId(pid)
    points.InsertNextPoint(x, y, z)
    data.InsertNextValue(sqrt(x * x + y * y + z * z))
mesh.InsertNextCell(VTK_QUADRATIC_HEXAHEDRON, pt_ids)

# Insert linear hex points (offset by 20,20,0)
pt_ids.Reset()
for pid in range(8):
    x = coords[pid][0] + 20
    y = coords[pid][1] + 20
    z = coords[pid][2]
    pt_ids.InsertNextId(pid + 20)
    points.InsertNextPoint(x, y, z)
    data.InsertNextValue(sqrt(x * x + y * y + z * z))
mesh.InsertNextCell(VTK_HEXAHEDRON, pt_ids)

# Triangle cutter
tri_cutter = vtkCutter()
tri_cutter.SetInputData(mesh)
tri_cutter.SetCutFunction(plane)
tri_cutter.GenerateTrianglesOn()
tri_cutter.Update()

# Polygon cutter
poly_cutter = vtkCutter()
poly_cutter.SetInputData(mesh)
poly_cutter.SetCutFunction(plane)
poly_cutter.GenerateTrianglesOff()
poly_cutter.Update()

# Mesh viewport
mesh_mapper = vtkDataSetMapper()
mesh_mapper.SetInputData(mesh)

mesh_actor = vtkActor()
mesh_actor.SetMapper(mesh_mapper)

renderer_0 = vtkRenderer()
renderer_0.AddActor(mesh_actor)
renderer_0.SetViewport(0.0, 0.0, 0.5, 1.0)

# Triangle cut viewport
tri_cut_mapper = vtkPolyDataMapper()
tri_cut_mapper.SetInputData(tri_cutter.GetOutput())

tri_cut_actor = vtkActor()
tri_cut_actor.SetMapper(tri_cut_mapper)
tri_cut_actor.GetProperty().EdgeVisibilityOn()
tri_cut_actor.GetProperty().SetEdgeColor(1, 1, 1)

renderer_1 = vtkRenderer()
renderer_1.AddActor(tri_cut_actor)
renderer_1.SetViewport(0.5, 0.5, 1.0, 1.0)

# Polygon cut viewport
poly_cut_mapper = vtkPolyDataMapper()
poly_cut_mapper.SetInputData(poly_cutter.GetOutput())

poly_cut_actor = vtkActor()
poly_cut_actor.SetMapper(poly_cut_mapper)

renderer_2 = vtkRenderer()
renderer_2.AddActor(poly_cut_actor)
renderer_2.SetViewport(0.5, 0.0, 1.0, 0.5)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer_0)
render_window.AddRenderer(renderer_1)
render_window.AddRenderer(renderer_2)
render_window.SetSize(800, 400)
render_window.SetWindowName("cut polygons")

# Scene
renderer_0.ResetCamera()
renderer_1.ResetCamera()
renderer_2.ResetCamera()

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
