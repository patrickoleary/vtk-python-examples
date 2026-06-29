#!/usr/bin/env python

# Demonstrate vtkPassArrays by creating a polydata with point, cell, and
# field data arrays, selectively passing one array, and rendering the
# result to verify the filter behavior.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import (
    vtkIntArray,
    vtkPoints,
)
from vtkmodules.vtkCommonDataModel import (
    vtkCellArray,
    vtkPolyData,
)
from vtkmodules.vtkFiltersGeneral import vtkPassArrays
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Build a simple polydata with two arrays in point, cell, and field data
poly = vtkPolyData()
pts = vtkPoints()
cells = vtkCellArray()

col1 = vtkIntArray()
col1.SetName("column1")

col2 = vtkIntArray()
col2.SetName("column2")

for i in range(10):
    col1.InsertNextValue(i)
    col2.InsertNextValue(-i)
    pts.InsertNextPoint(i * 0.1, 0, 0)
    cells.InsertNextCell(1, [i])

poly.SetPoints(pts)
poly.SetVerts(cells)
poly.GetCellData().AddArray(col1)
poly.GetCellData().AddArray(col2)
poly.GetPointData().AddArray(col1)
poly.GetPointData().AddArray(col2)
poly.GetFieldData().AddArray(col1)
poly.GetFieldData().AddArray(col2)

# Pass only "column1" from point data (type 0)
pass_filter = vtkPassArrays()
pass_filter.SetInputData(poly)
pass_filter.AddArray(0, "column1")
pass_filter.SetRemoveArrays(False)
pass_filter.Update()

# Render
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(pass_filter.GetOutputPort())
mapper.SetScalarModeToUsePointFieldData()
mapper.SelectColorArray("column1")
mapper.SetScalarRange(0, 9)

actor = vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetPointSize(8.0)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(0.1, 0.2, 0.4)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(400, 400)
render_window.SetWindowName("pass arrays")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.ResetCamera()

interactor.Initialize()
interactor.Start()
