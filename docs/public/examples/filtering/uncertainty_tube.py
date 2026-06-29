#!/usr/bin/env python

# Demonstrate vtkUncertaintyTubeFilter by creating two polylines with
# scalar uncertainty and vector data, generating uncertainty tubes,
# triangulating, and rendering the result.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import vtkDoubleArray, vtkMath, vtkPoints
from vtkmodules.vtkCommonDataModel import vtkCellArray, vtkPolyData
from vtkmodules.vtkFiltersCore import vtkTriangleFilter
from vtkmodules.vtkFiltersGeneral import vtkUncertaintyTubeFilter
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Create two polylines with 5 points each
pts = vtkPoints()
pts.SetNumberOfPoints(10)
pts.SetPoint(0, 10, 10, 0)
pts.SetPoint(1, 10, 10, 2)
pts.SetPoint(2, 10, 10, 4)
pts.SetPoint(3, 10, 10, 8)
pts.SetPoint(4, 10, 10, 12)
pts.SetPoint(5, 1, 1, 2)
pts.SetPoint(6, 1, 2, 3)
pts.SetPoint(7, 1, 4, 3)
pts.SetPoint(8, 1, 8, 4)
pts.SetPoint(9, 1, 16, 5)

# Random scalar (uncertainty) and vector data
vtkMath.RandomSeed(1177)
scalars = vtkDoubleArray()
scalars.SetNumberOfComponents(1)
scalars.SetNumberOfTuples(10)
vectors = vtkDoubleArray()
vectors.SetNumberOfComponents(3)
vectors.SetNumberOfTuples(10)
for i in range(10):
    scalars.SetTuple1(i, vtkMath.Random(0, 1))
    x = vtkMath.Random(0.0, 2)
    y = vtkMath.Random(0.0, 2)
    z = vtkMath.Random(0.0, 2)
    vectors.SetTuple3(i, x, y, z)

# Build polylines
lines = vtkCellArray()
lines.InsertNextCell(5)
lines.InsertCellPoint(0)
lines.InsertCellPoint(1)
lines.InsertCellPoint(2)
lines.InsertCellPoint(3)
lines.InsertCellPoint(4)
lines.InsertNextCell(5)
lines.InsertCellPoint(5)
lines.InsertCellPoint(6)
lines.InsertCellPoint(7)
lines.InsertCellPoint(8)
lines.InsertCellPoint(9)

pd = vtkPolyData()
pd.SetPoints(pts)
pd.SetLines(lines)
pd.GetPointData().SetScalars(scalars)
pd.GetPointData().SetVectors(vectors)

# Generate uncertainty tubes
tube_filter = vtkUncertaintyTubeFilter()
tube_filter.SetInputData(pd)
tube_filter.SetNumberOfSides(8)

# Triangulate tubes for smooth rendering
triangle_filter = vtkTriangleFilter()
triangle_filter.SetInputConnection(tube_filter.GetOutputPort())

# Mapper and actor
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(triangle_filter.GetOutputPort())

actor = vtkActor()
actor.SetMapper(mapper)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(0.1, 0.2, 0.4)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(400, 400)
render_window.SetWindowName("uncertainty tube")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.GetActiveCamera().SetPosition(1, 1, 1)
renderer.GetActiveCamera().SetFocalPoint(0, 0, 0)
renderer.ResetCamera()

interactor.Initialize()
interactor.Start()
