#!/usr/bin/env python
# Demonstrate polyhedron decomposition with contour extraction and surface rendering.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import vtkDoubleArray, vtkIdTypeArray, vtkPoints
from vtkmodules.vtkCommonDataModel import (
    vtkCellArray,
    vtkCellData,
    vtkPointData,
    vtkPolyData,
    vtkPolyhedron,
    vtkPolyhedronUtilities,
    vtkUnstructuredGrid,
)
from vtkmodules.vtkFiltersCore import vtkContourFilter
from vtkmodules.vtkFiltersGeometry import vtkGeometryFilter
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Create polyhedron 1.
polyhedron_1 = vtkPolyhedron()
for i in range(8):
    polyhedron_1.GetPointIds().InsertNextId(i)
polyhedron_1.GetPoints().InsertNextPoint(2.5, -7.5, 2.5)
polyhedron_1.GetPoints().InsertNextPoint(5.31, -5.31, 4.68)
polyhedron_1.GetPoints().InsertNextPoint(2.5, -2.5, 2.5)
polyhedron_1.GetPoints().InsertNextPoint(7.5, -2.5, 2.5)
polyhedron_1.GetPoints().InsertNextPoint(2.5, -7.5, 7.5)
polyhedron_1.GetPoints().InsertNextPoint(6.25, -6.25, 6.25)
polyhedron_1.GetPoints().InsertNextPoint(2.5, -2.5, 7.5)
polyhedron_1.GetPoints().InsertNextPoint(6.25, -3.75, 6.25)

face_offsets_1 = [0, 4, 8, 12, 16, 20, 24]
face_conns_1 = [0, 1, 3, 2, 0, 4, 5, 1, 0, 2, 6, 4, 1, 5, 7, 3, 3, 7, 6, 2, 4, 6, 7, 5]
faces_1 = vtkCellArray()
offsets_arr_1 = vtkIdTypeArray()
offsets_arr_1.SetNumberOfTuples(7)
for i, v in enumerate(face_offsets_1):
    offsets_arr_1.SetValue(i, v)
conns_arr_1 = vtkIdTypeArray()
conns_arr_1.SetNumberOfTuples(24)
for i, v in enumerate(face_conns_1):
    conns_arr_1.SetValue(i, v)
faces_1.SetData(offsets_arr_1, conns_arr_1)
polyhedron_1.SetCellFaces(faces_1)
polyhedron_1.Initialize()

# Create polyhedron 2.
polyhedron_2 = vtkPolyhedron()
for i in range(8, 16):
    polyhedron_2.GetPointIds().InsertNextId(i)
polyhedron_2.GetPoints().InsertNextPoint(2.5, -7.5, 2.5)
polyhedron_2.GetPoints().InsertNextPoint(5.31, -5.31, 4.68)
polyhedron_2.GetPoints().InsertNextPoint(2.5, -12.5, 2.5)
polyhedron_2.GetPoints().InsertNextPoint(7.5, -12.5, 2.5)
polyhedron_2.GetPoints().InsertNextPoint(2.5, -7.5, 7.5)
polyhedron_2.GetPoints().InsertNextPoint(6.25, -6.25, 6.25)
polyhedron_2.GetPoints().InsertNextPoint(2.5, -12.5, 7.5)
polyhedron_2.GetPoints().InsertNextPoint(6.25, -13.75, 6.25)

face_offsets_2 = [0, 4, 8, 12, 16, 20, 24]
face_conns_2 = [10, 11, 9, 8, 9, 13, 12, 8, 12, 14, 10, 8, 11, 15, 13, 9, 10, 14, 15, 11, 13, 15, 14, 12]
faces_2 = vtkCellArray()
offsets_arr_2 = vtkIdTypeArray()
offsets_arr_2.SetNumberOfTuples(7)
for i, v in enumerate(face_offsets_2):
    offsets_arr_2.SetValue(i, v)
conns_arr_2 = vtkIdTypeArray()
conns_arr_2.SetNumberOfTuples(24)
for i, v in enumerate(face_conns_2):
    conns_arr_2.SetValue(i, v)
faces_2.SetData(offsets_arr_2, conns_arr_2)
polyhedron_2.SetCellFaces(faces_2)
polyhedron_2.Initialize()

# Point data for decomposition.
double_values = [2, 5, 2, 2, 2, 3, 2, 3, 2, 5, 2, 2, 2, 3, 2, 3]
point_array_double = vtkDoubleArray()
point_array_double.SetNumberOfValues(16)
point_array_double.SetName("Doubles")
for i, v in enumerate(double_values):
    point_array_double.SetValue(i, v)

point_data = vtkPointData()
point_data.AddArray(point_array_double)

# Cell data.
cell_array_data = vtkDoubleArray()
cell_array_data.SetNumberOfValues(2)
cell_array_data.SetName("Cell array")
cell_array_data.SetValue(0, 1.5)
cell_array_data.SetValue(1, 1.5)
cell_data = vtkCellData()
cell_data.AddArray(cell_array_data)

# Decompose polyhedra.
decomposed_ug_1 = vtkPolyhedronUtilities.Decompose(polyhedron_1, point_data, 0, cell_data)
decomposed_ug_2 = vtkPolyhedronUtilities.Decompose(polyhedron_2, point_data, 1, cell_data)

# Extract contours from decomposed unstructured grids.
contour_filter = vtkContourFilter()
contour_filter.SetInputData(decomposed_ug_1)
contour_filter.SetInputArrayToProcess(0, 0, 0, 0, "Doubles")
contour_filter.SetNumberOfContours(1)
contour_filter.SetValue(0, 3.5)
contour_filter.Update()
contour_1 = vtkPolyData()
contour_1.DeepCopy(contour_filter.GetOutputDataObject(0))

contour_filter.SetInputData(decomposed_ug_2)
contour_filter.Update()
contour_2 = vtkPolyData()
contour_2.DeepCopy(contour_filter.GetOutputDataObject(0))

# Extract surfaces from decomposed unstructured grids.
geo_filter = vtkGeometryFilter()
geo_filter.SetInputDataObject(decomposed_ug_1)
geo_filter.Update()
ug_surface_1 = vtkPolyData()
ug_surface_1.DeepCopy(geo_filter.GetOutputDataObject(0))

geo_filter.SetInputDataObject(decomposed_ug_2)
geo_filter.Update()
ug_surface_2 = vtkPolyData()
ug_surface_2.DeepCopy(geo_filter.GetOutputDataObject(0))

# Mappers.
ug_mapper_1 = vtkPolyDataMapper()
ug_mapper_1.SetInputData(ug_surface_1)
ug_mapper_2 = vtkPolyDataMapper()
ug_mapper_2.SetInputData(ug_surface_2)
contour_mapper_1 = vtkPolyDataMapper()
contour_mapper_1.SetInputData(contour_1)
contour_mapper_2 = vtkPolyDataMapper()
contour_mapper_2.SetInputData(contour_2)

# Actors.
ug_actor_1 = vtkActor()
ug_actor_1.SetMapper(ug_mapper_1)
ug_actor_1.GetProperty().SetOpacity(0.1)
ug_actor_2 = vtkActor()
ug_actor_2.SetMapper(ug_mapper_2)
ug_actor_2.GetProperty().SetOpacity(0.1)
contour_actor_1 = vtkActor()
contour_actor_1.SetMapper(contour_mapper_1)
contour_actor_2 = vtkActor()
contour_actor_2.SetMapper(contour_mapper_2)

# Standard rendering pipeline.
renderer = vtkRenderer()
renderer.AddActor(ug_actor_1)
renderer.AddActor(ug_actor_2)
renderer.AddActor(contour_actor_1)
renderer.AddActor(contour_actor_2)

render_window = vtkRenderWindow()
render_window.SetSize(300, 300)
render_window.AddRenderer(renderer)
render_window.SetWindowName("polyhedron decompose")

renderer.GetActiveCamera().Azimuth(135)
renderer.ResetCamera()

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
