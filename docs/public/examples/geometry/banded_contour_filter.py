#!/usr/bin/env python

# Demonstrate vtkBandedPolyDataContourFilter by manually creating a polydata
# with vertices, lines, polygons, and triangle strips, assigning scalar
# values, generating banded contours, and rendering the result.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import vtkFloatArray, vtkPoints
from vtkmodules.vtkCommonDataModel import vtkCellArray, vtkDataObject, vtkPolyData
from vtkmodules.vtkFiltersModeling import vtkBandedPolyDataContourFilter
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Create points
points = vtkPoints()
points.InsertPoint(0, 0, 0, 0)
points.InsertPoint(1, 0, 1, 0)
points.InsertPoint(2, 0, 2, 0)
points.InsertPoint(3, 1, 0, 0)
points.InsertPoint(4, 1, 1, 0)
points.InsertPoint(5, 1, 2, 0)
points.InsertPoint(6, 2, 0, 0)
points.InsertPoint(7, 2, 2, 0)
points.InsertPoint(8, 3, 0, 0)
points.InsertPoint(9, 3, 1, 0)
points.InsertPoint(10, 3, 2, 0)
points.InsertPoint(11, 4, 0, 0)
points.InsertPoint(12, 6, 0, 0)
points.InsertPoint(13, 5, 2, 0)
points.InsertPoint(14, 7, 0, 0)
points.InsertPoint(15, 9, 0, 0)
points.InsertPoint(16, 7, 2, 0)
points.InsertPoint(17, 9, 2, 0)
points.InsertPoint(18, 10, 0, 0)
points.InsertPoint(19, 12, 0, 0)
points.InsertPoint(20, 10, 1, 0)
points.InsertPoint(21, 12, 1, 0)
points.InsertPoint(22, 10, 2, 0)
points.InsertPoint(23, 12, 2, 0)
points.InsertPoint(24, 10, 3, 0)
points.InsertPoint(25, 12, 3, 0)

# Vertices
verts = vtkCellArray()
verts.InsertNextCell(1)
verts.InsertCellPoint(0)
verts.InsertNextCell(1)
verts.InsertCellPoint(1)
verts.InsertNextCell(1)
verts.InsertCellPoint(2)
verts.InsertNextCell(3)
verts.InsertCellPoint(3)
verts.InsertCellPoint(4)
verts.InsertCellPoint(5)

# Lines
lines = vtkCellArray()
lines.InsertNextCell(2)
lines.InsertCellPoint(6)
lines.InsertCellPoint(7)
lines.InsertNextCell(3)
lines.InsertCellPoint(8)
lines.InsertCellPoint(9)
lines.InsertCellPoint(10)

# Polygons
polys = vtkCellArray()
polys.InsertNextCell(4)
polys.InsertCellPoint(14)
polys.InsertCellPoint(15)
polys.InsertCellPoint(17)
polys.InsertCellPoint(16)
polys.InsertNextCell(3)
polys.InsertCellPoint(11)
polys.InsertCellPoint(12)
polys.InsertCellPoint(13)

# Triangle strips
strips = vtkCellArray()
strips.InsertNextCell(8)
strips.InsertCellPoint(19)
strips.InsertCellPoint(18)
strips.InsertCellPoint(21)
strips.InsertCellPoint(20)
strips.InsertCellPoint(23)
strips.InsertCellPoint(22)
strips.InsertCellPoint(25)
strips.InsertCellPoint(24)

# Scalars
scalars = vtkFloatArray()
scalars.SetName("SomeScalars")
scalars.SetNumberOfTuples(26)
scalar_values = [
    0, 50, 100, 0, 50, 100, 10, 90, 10, 50, 90,
    10, 40, 100, 0, 60, 40, 100, 0, 25, 25, 50, 50, 75, 75, 100,
]
for i, v in enumerate(scalar_values):
    scalars.SetTuple1(i, v)

# Assemble polydata
poly_data = vtkPolyData()
poly_data.SetPoints(points)
poly_data.SetVerts(verts)
poly_data.SetLines(lines)
poly_data.SetPolys(polys)
poly_data.SetStrips(strips)
poly_data.GetPointData().AddArray(scalars)

# Banded contour filter
banded_contour = vtkBandedPolyDataContourFilter()
banded_contour.SetInputArrayToProcess(0, 0, 0, vtkDataObject.FIELD_ASSOCIATION_POINTS, "SomeScalars")
banded_contour.SetInputData(poly_data)
banded_contour.GenerateValues(3, 25, 75)

# Mapper
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(banded_contour.GetOutputPort())
mapper.SetScalarModeToUseCellData()
mapper.SetScalarRange(0, 4)

actor = vtkActor()
actor.SetMapper(mapper)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(0, 0, 0)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(300, 80)
render_window.SetWindowName("banded contour filter")

# Scene
renderer.ResetCamera()
renderer.GetActiveCamera().Zoom(3)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
