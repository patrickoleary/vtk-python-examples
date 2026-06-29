#!/usr/bin/env python

# Test vtkDistanceToCamera with polydata and unstructured grid pipelines.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import (
    vtkFloatArray,
    vtkPoints,
)
from vtkmodules.vtkCommonDataModel import (
    VTK_HEXAHEDRON,
    vtkCellArray,
    vtkPolyData,
    vtkUnstructuredGrid,
)
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkDataSetMapper,
    vtkDistanceToCamera,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Create hexahedron points and scalar values
points = vtkPoints()
values = vtkFloatArray()
values.SetName("values")
for z in [0, 1]:
    for y in [0, 1]:
        for x in [0, 1]:
            points.InsertNextPoint(x * 2, y * 3, z * 4)

point_data = [-1, -2, -2, -1, 1, 2, 2, 1]
for v in point_data:
    values.InsertNextValue(v)

quad_cells = [[0, 1, 3, 2], [4, 5, 7, 6], [0, 1, 5, 4], [1, 3, 7, 5], [3, 2, 6, 7], [0, 2, 6, 4]]
hexa_cells = [[0, 1, 3, 2, 4, 5, 7, 6]]

# Polydata pipeline (left viewport)
poly_data = vtkPolyData()
poly_data.SetPoints(points)
poly_data.GetPointData().SetScalars(values)
quads = vtkCellArray()
for cell in quad_cells:
    quads.InsertNextCell(len(cell))
    for p in cell:
        quads.InsertCellPoint(p)
poly_data.SetPolys(quads)

poly_distance = vtkDistanceToCamera()
poly_distance.SetInputData(poly_data)

poly_mapper = vtkPolyDataMapper()
poly_mapper.SetInputConnection(poly_distance.GetOutputPort())
poly_mapper.SetScalarModeToUsePointFieldData()
poly_mapper.SelectColorArray("DistanceToCamera")

poly_actor = vtkActor()
poly_actor.SetMapper(poly_mapper)

renderer_0 = vtkRenderer()
renderer_0.AddViewProp(poly_actor)
renderer_0.SetBackground(0.2, 0.2, 0.2)
renderer_0.SetViewport(0.0, 0.0, 0.5, 1.0)
poly_distance.SetRenderer(renderer_0)
renderer_0.GetActiveCamera().SetFocalPoint(1, 1.5, 2)
renderer_0.GetActiveCamera().SetPosition(-2, -4, 6)
renderer_0.ResetCamera()

# Unstructured grid pipeline (right viewport)
unstructured_grid = vtkUnstructuredGrid()
unstructured_grid.SetPoints(points)
for cell in hexa_cells:
    unstructured_grid.InsertNextCell(VTK_HEXAHEDRON, len(cell), cell)
unstructured_grid.GetPointData().SetScalars(values)

ug_distance = vtkDistanceToCamera()
ug_distance.SetInputData(unstructured_grid)
ug_distance.SetDistanceArrayName("d2c")
ug_distance.ScalingOn()
ug_distance.SetInputArrayToProcess(0, 0, 0, 0, "values")

ug_mapper = vtkDataSetMapper()
ug_mapper.SetInputConnection(ug_distance.GetOutputPort())
ug_mapper.SetScalarModeToUsePointFieldData()
ug_mapper.SelectColorArray("d2c")

ug_actor = vtkActor()
ug_actor.SetMapper(ug_mapper)

renderer_1 = vtkRenderer()
renderer_1.AddViewProp(ug_actor)
renderer_1.SetBackground(0.4, 0.4, 0.4)
renderer_1.SetViewport(0.5, 0.0, 1.0, 1.0)
ug_distance.SetRenderer(renderer_1)
renderer_1.GetActiveCamera().SetFocalPoint(1, 1.5, 2)
renderer_1.GetActiveCamera().SetPosition(-2, -4, 6)
renderer_1.ResetCamera()

# Render
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer_0)
render_window.AddRenderer(renderer_1)
render_window.SetWindowName("distance to camera")
render_window.SetMultiSamples(0)
render_window.SetSize(600, 300)

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Test zoomed out
renderer_1.GetActiveCamera().Zoom(0.3)
renderer_0.GetActiveCamera().Zoom(0.3)

interactor.Initialize()
interactor.Start()
