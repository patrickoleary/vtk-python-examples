#!/usr/bin/env python

# Demonstrate vtkStaticCleanPolyData merging points with texture
# coordinates, verifying that points are only merged when both
# geometry and TCoords match.

import os

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
    vtkPolyData,
)
from vtkmodules.vtkFiltersCore import (
    vtkAppendPolyData,
    vtkStaticCleanPolyData,
)
from vtkmodules.vtkIOImage import vtkTIFFReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
    vtkTexture,
)

data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Texture map
cheers = vtkTIFFReader()
cheers.SetFileName(os.path.join(data_dir, "beach.tif"))

image_texture = vtkTexture()
image_texture.InterpolateOn()
image_texture.SetInputConnection(cheers.GetOutputPort())

# First plane patch (upper-left region)
polydata_0 = vtkPolyData()
points_0 = vtkPoints()
polys_0 = vtkCellArray()
polydata_0.SetPoints(points_0)
polydata_0.SetPolys(polys_0)

points_0.SetNumberOfPoints(9)
points_0.SetPoint(0, 0, 4, 0)
points_0.SetPoint(1, 1, 4, 0)
points_0.SetPoint(2, 2, 4, 0)
points_0.SetPoint(3, 0, 5, 0)
points_0.SetPoint(4, 1, 5, 0)
points_0.SetPoint(5, 2, 5, 0)
points_0.SetPoint(6, 0, 6, 0)
points_0.SetPoint(7, 1, 6, 0)
points_0.SetPoint(8, 2, 6, 0)

t_0 = vtkDoubleArray()
t_0.SetName("TCoords")
t_0.SetNumberOfComponents(2)
t_0.SetNumberOfTuples(9)
t_0.SetTuple2(0, 0, 0)
t_0.SetTuple2(1, 0, 0.5)
t_0.SetTuple2(2, 0, 1.0)
t_0.SetTuple2(3, 0.5, 0)
t_0.SetTuple2(4, 0.5, 0.5)
t_0.SetTuple2(5, 0.5, 1.0)
t_0.SetTuple2(6, 1.0, 0)
t_0.SetTuple2(7, 1.0, 0.5)
t_0.SetTuple2(8, 1.0, 1.0)
polydata_0.GetPointData().SetTCoords(t_0)

for cell in [[0, 1, 4, 3], [1, 2, 5, 4], [3, 4, 7, 6], [4, 5, 8, 7]]:
    polys_0.InsertNextCell(4, cell)

# Second plane patch (upper-right region)
polydata_1 = vtkPolyData()
points_1 = vtkPoints()
polys_1 = vtkCellArray()
polydata_1.SetPoints(points_1)
polydata_1.SetPolys(polys_1)

points_1.SetNumberOfPoints(9)
points_1.SetPoint(0, 2, 4, 0)
points_1.SetPoint(1, 3, 4, 0)
points_1.SetPoint(2, 4, 4, 0)
points_1.SetPoint(3, 2, 5, 0)
points_1.SetPoint(4, 3, 5, 0)
points_1.SetPoint(5, 4, 5, 0)
points_1.SetPoint(6, 2, 6, 0)
points_1.SetPoint(7, 3, 6, 0)
points_1.SetPoint(8, 4, 6, 0)

t_1 = vtkDoubleArray()
t_1.SetName("TCoords")
t_1.SetNumberOfComponents(2)
t_1.SetNumberOfTuples(9)
t_1.SetTuple2(0, 0, 0)
t_1.SetTuple2(1, 0, 0.5)
t_1.SetTuple2(2, 0, 1.0)
t_1.SetTuple2(3, 0.5, 0)
t_1.SetTuple2(4, 0.5, 0.5)
t_1.SetTuple2(5, 0.5, 1.0)
t_1.SetTuple2(6, 1.0, 0)
t_1.SetTuple2(7, 1.0, 0.5)
t_1.SetTuple2(8, 1.0, 1.0)
polydata_1.GetPointData().SetTCoords(t_1)

for cell in [[0, 1, 4, 3], [1, 2, 5, 4], [3, 4, 7, 6], [4, 5, 8, 7]]:
    polys_1.InsertNextCell(4, cell)

# Third plane patch (lower-left region, taller)
polydata_2 = vtkPolyData()
points_2 = vtkPoints()
polys_2 = vtkCellArray()
polydata_2.SetPoints(points_2)
polydata_2.SetPolys(polys_2)

points_2.SetNumberOfPoints(15)
points_2.SetPoint(0, 0, 0, 0)
points_2.SetPoint(1, 1, 0, 0)
points_2.SetPoint(2, 2, 0, 0)
points_2.SetPoint(3, 0, 1, 0)
points_2.SetPoint(4, 1, 1, 0)
points_2.SetPoint(5, 2, 1, 0)
points_2.SetPoint(6, 0, 2, 0)
points_2.SetPoint(7, 1, 2, 0)
points_2.SetPoint(8, 2, 2, 0)
points_2.SetPoint(9, 0, 3, 0)
points_2.SetPoint(10, 1, 3, 0)
points_2.SetPoint(11, 2, 3, 0)
points_2.SetPoint(12, 0, 4, 0)
points_2.SetPoint(13, 1, 4, 0)
points_2.SetPoint(14, 2, 4, 0)

t_2 = vtkDoubleArray()
t_2.SetName("TCoords")
t_2.SetNumberOfComponents(2)
t_2.SetNumberOfTuples(15)
t_2.SetTuple2(0, 0.00, 0.0)
t_2.SetTuple2(1, 0.25, 0.0)
t_2.SetTuple2(2, 0.50, 0.0)
t_2.SetTuple2(3, 0.00, 0.25)
t_2.SetTuple2(4, 0.25, 0.25)
t_2.SetTuple2(5, 0.50, 0.25)
t_2.SetTuple2(6, 0.00, 0.5)
t_2.SetTuple2(7, 0.25, 0.5)
t_2.SetTuple2(8, 0.50, 0.5)
t_2.SetTuple2(9, 0.00, 0.75)
t_2.SetTuple2(10, 0.25, 0.75)
t_2.SetTuple2(11, 0.50, 0.75)
t_2.SetTuple2(12, 0.00, 1.0)
t_2.SetTuple2(13, 0.25, 1.0)
t_2.SetTuple2(14, 0.50, 1.0)
polydata_2.GetPointData().SetTCoords(t_2)

for cell in [[0, 1, 4, 3], [1, 2, 5, 4], [3, 4, 7, 6], [4, 5, 8, 7],
             [6, 7, 10, 9], [7, 8, 11, 10], [9, 10, 13, 12], [10, 11, 14, 13]]:
    polys_2.InsertNextCell(4, cell)

# Fourth plane patch (lower-right region, taller)
polydata_3 = vtkPolyData()
points_3 = vtkPoints()
polys_3 = vtkCellArray()
polydata_3.SetPoints(points_3)
polydata_3.SetPolys(polys_3)

points_3.SetNumberOfPoints(15)
points_3.SetPoint(0, 2, 0, 0)
points_3.SetPoint(1, 3, 0, 0)
points_3.SetPoint(2, 4, 0, 0)
points_3.SetPoint(3, 2, 1, 0)
points_3.SetPoint(4, 3, 1, 0)
points_3.SetPoint(5, 4, 1, 0)
points_3.SetPoint(6, 2, 2, 0)
points_3.SetPoint(7, 3, 2, 0)
points_3.SetPoint(8, 4, 2, 0)
points_3.SetPoint(9, 2, 3, 0)
points_3.SetPoint(10, 3, 3, 0)
points_3.SetPoint(11, 4, 3, 0)
points_3.SetPoint(12, 2, 4, 0)
points_3.SetPoint(13, 3, 4, 0)
points_3.SetPoint(14, 4, 4, 0)

t_3 = vtkDoubleArray()
t_3.SetName("TCoords")
t_3.SetNumberOfComponents(2)
t_3.SetNumberOfTuples(15)
t_3.SetTuple2(0, 0.50, 0.0)
t_3.SetTuple2(1, 0.75, 0.0)
t_3.SetTuple2(2, 1.0, 0.0)
t_3.SetTuple2(3, 0.50, 0.25)
t_3.SetTuple2(4, 0.75, 0.25)
t_3.SetTuple2(5, 1.0, 0.25)
t_3.SetTuple2(6, 0.50, 0.5)
t_3.SetTuple2(7, 0.75, 0.5)
t_3.SetTuple2(8, 1.0, 0.5)
t_3.SetTuple2(9, 0.50, 0.75)
t_3.SetTuple2(10, 0.75, 0.75)
t_3.SetTuple2(11, 1.0, 0.75)
t_3.SetTuple2(12, 0.50, 1.0)
t_3.SetTuple2(13, 0.75, 1.0)
t_3.SetTuple2(14, 1.0, 1.0)
polydata_3.GetPointData().SetTCoords(t_3)

for cell in [[0, 1, 4, 3], [1, 2, 5, 4], [3, 4, 7, 6], [4, 5, 8, 7],
             [6, 7, 10, 9], [7, 8, 11, 10], [9, 10, 13, 12], [10, 11, 14, 13]]:
    polys_3.InsertNextCell(4, cell)

# Append all patches
append = vtkAppendPolyData()
append.AddInputData(polydata_0)
append.AddInputData(polydata_1)
append.AddInputData(polydata_2)
append.AddInputData(polydata_3)
append.Update()

num_append_pts = append.GetOutput().GetNumberOfPoints()
print("Number of points before merging: ", num_append_pts)
assert num_append_pts == 48

# Merge with TCoords awareness
merge = vtkStaticCleanPolyData()
merge.SetInputConnection(append.GetOutputPort())
merge.SetMergingArray("TCoords")
merge.Update()

num_merged_pts = merge.GetOutput().GetNumberOfPoints()
print("Number of points after merging: ", num_merged_pts)
assert num_merged_pts == 43

# Mapper and actor
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(merge.GetOutputPort())

actor = vtkActor()
actor.SetMapper(mapper)
actor.SetTexture(image_texture)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(0, 0, 0)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(256, 256)
render_window.SetWindowName("merge points with tcoords")

# Scene
renderer.GetActiveCamera().SetPosition(0, 0, 1)
renderer.GetActiveCamera().SetFocalPoint(0, 0, 0)
renderer.ResetCamera()

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
