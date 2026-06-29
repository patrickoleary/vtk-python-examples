#!/usr/bin/env python

# Compute volumes and areas of multiple polygonal objects using
# vtkMultiObjectMassProperties, including valid and invalid meshes.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import vtkPoints
from vtkmodules.vtkCommonDataModel import (
    vtkCellArray,
    vtkPolyData,
)
from vtkmodules.vtkFiltersCore import vtkMultiObjectMassProperties
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Build polydata with five "blocks": four unit cubes and one invalid X-mesh
poly_data = vtkPolyData()
grid_points = vtkPoints()
polys = vtkCellArray()
poly_data.SetPoints(grid_points)
poly_data.SetPolys(polys)

grid_points.SetNumberOfPoints(42)

# First block (unit cube at lower-left)
grid_points.SetPoint(0, -2, -2, -0.5)
grid_points.SetPoint(1, -1, -2, -0.5)
grid_points.SetPoint(2, -2, -1, -0.5)
grid_points.SetPoint(3, -1, -1, -0.5)
grid_points.SetPoint(4, -2, -2, 0.5)
grid_points.SetPoint(5, -1, -2, 0.5)
grid_points.SetPoint(6, -2, -1, 0.5)
grid_points.SetPoint(7, -1, -1, 0.5)

# Second block (unit cube at lower-right)
grid_points.SetPoint(8, 1, -2, -0.5)
grid_points.SetPoint(9, 2, -2, -0.5)
grid_points.SetPoint(10, 1, -1, -0.5)
grid_points.SetPoint(11, 2, -1, -0.5)
grid_points.SetPoint(12, 1, -2, 0.5)
grid_points.SetPoint(13, 2, -2, 0.5)
grid_points.SetPoint(14, 1, -1, 0.5)
grid_points.SetPoint(15, 2, -1, 0.5)

# Third block (unit cube at upper-left)
grid_points.SetPoint(16, -2, 1, -0.5)
grid_points.SetPoint(17, -1, 1, -0.5)
grid_points.SetPoint(18, -2, 2, -0.5)
grid_points.SetPoint(19, -1, 2, -0.5)
grid_points.SetPoint(20, -2, 1, 0.5)
grid_points.SetPoint(21, -1, 1, 0.5)
grid_points.SetPoint(22, -2, 2, 0.5)
grid_points.SetPoint(23, -1, 2, 0.5)

# Fourth block (unit cube at upper-right)
grid_points.SetPoint(24, 1, 1, -0.5)
grid_points.SetPoint(25, 2, 1, -0.5)
grid_points.SetPoint(26, 1, 2, -0.5)
grid_points.SetPoint(27, 2, 2, -0.5)
grid_points.SetPoint(28, 1, 1, 0.5)
grid_points.SetPoint(29, 2, 1, 0.5)
grid_points.SetPoint(30, 1, 2, 0.5)
grid_points.SetPoint(31, 2, 2, 0.5)

# Invalid poly mesh (an X shape)
grid_points.SetPoint(32, 0, -0.5, -0.5)
grid_points.SetPoint(33, 0, 0.5, -0.5)
grid_points.SetPoint(34, -0.5, -0.5, 0)
grid_points.SetPoint(35, 0, -0.5, 0)
grid_points.SetPoint(36, 0.5, -0.5, 0)
grid_points.SetPoint(37, -0.5, 0.5, 0)
grid_points.SetPoint(38, 0, 0.5, 0)
grid_points.SetPoint(39, 0.5, 0.5, 0)
grid_points.SetPoint(40, 0, -0.5, 0.5)
grid_points.SetPoint(41, 0, 0.5, 0.5)

# First block - all quads, consistent order
for face in [[0,1,3,2], [4,6,7,5], [0,4,5,1], [3,7,6,2], [1,5,7,3], [2,6,4,0]]:
    polys.InsertNextCell(4)
    for p in face:
        polys.InsertCellPoint(p)

# Second block - quads with a reversed polygon
for face in [[8,9,11,10], [12,13,15,14], [8,12,13,9], [11,15,14,10], [9,13,15,11], [10,14,12,8]]:
    polys.InsertNextCell(4)
    for p in face:
        polys.InsertCellPoint(p)

# Third block - triangles + quads
for face in [[16,17,19], [19,18,16]]:
    polys.InsertNextCell(3)
    for p in face:
        polys.InsertCellPoint(p)
for face in [[20,22,23,21], [16,20,21,17], [19,23,22,18], [17,21,23,19], [18,22,20,16]]:
    polys.InsertNextCell(4)
    for p in face:
        polys.InsertCellPoint(p)

# Fourth block - triangles + quads + reversals
for face in [[24,25,27], [26,27,24]]:
    polys.InsertNextCell(3)
    for p in face:
        polys.InsertCellPoint(p)
for face in [[28,30,31,29], [24,28,29,25], [27,31,30,26], [25,29,31,27], [26,30,28,24]]:
    polys.InsertNextCell(4)
    for p in face:
        polys.InsertCellPoint(p)

# Non-manifold X mesh - four quads
for face in [[32,33,38,35], [34,35,38,37], [35,36,39,38], [35,38,41,40]]:
    polys.InsertNextCell(4)
    for p in face:
        polys.InsertCellPoint(p)

# Compute mass properties
mass_props = vtkMultiObjectMassProperties()
mass_props.SetInputData(poly_data)
mass_props.Update()

num_objects = mass_props.GetNumberOfObjects()
print(f"Number of objects: {num_objects}")
print(f"All valid: {mass_props.GetAllValid()}")
print(f"Total area: {mass_props.GetTotalArea()}")
print(f"Total volume: {mass_props.GetTotalVolume()}")

validity = mass_props.GetOutput().GetFieldData().GetArray("ObjectValidity")
areas = mass_props.GetOutput().GetFieldData().GetArray("ObjectAreas")
volumes = mass_props.GetOutput().GetFieldData().GetArray("ObjectVolumes")
centroids = mass_props.GetOutput().GetFieldData().GetArray("ObjectCentroids")
print("Object ID, Valid, Area, Volume, Centroid")
for i in range(num_objects):
    print(i, validity.GetTuple1(i), areas.GetTuple1(i),
          volumes.GetTuple1(i), centroids.GetTuple3(i))

# Mapper
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(mass_props.GetOutputPort())
mapper.ScalarVisibilityOff()

# Actor
actor = vtkActor()
actor.SetMapper(mapper)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(actor)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("multi object mass properties")

# Scene
renderer.GetActiveCamera().SetPosition(0.5, 0.5, 1)
renderer.GetActiveCamera().SetFocalPoint(0, 0, 0)
renderer.ResetCamera()

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
