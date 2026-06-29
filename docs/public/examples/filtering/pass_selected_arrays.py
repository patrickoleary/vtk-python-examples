#!/usr/bin/env python

# Demonstrate vtkPassSelectedArrays by creating a sphere with multiple
# point and cell data arrays, selectively passing chosen arrays, and
# rendering the result colored by the selected array.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import vtkDoubleArray
from vtkmodules.vtkCommonDataModel import vtkDataObject
from vtkmodules.vtkFiltersGeneral import vtkPassSelectedArrays
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Create a sphere
sphere = vtkSphereSource()
sphere.Update()

pd = sphere.GetOutput()
pd.GetPointData().Initialize()
pd.GetCellData().Initialize()
pd.GetFieldData().Initialize()

# Add point data arrays
temp = vtkDoubleArray()
temp.SetName("Temp")
temp.SetNumberOfTuples(pd.GetNumberOfPoints())
for i in range(pd.GetNumberOfPoints()):
    temp.SetValue(i, float(i))
pd.GetPointData().AddArray(temp)

press = vtkDoubleArray()
press.SetName("Press")
press.SetNumberOfTuples(pd.GetNumberOfPoints())
press.Fill(42.0)
pd.GetPointData().AddArray(press)
pd.GetPointData().SetActiveScalars("Temp")

# Add cell data arrays
cell_var = vtkDoubleArray()
cell_var.SetName("CellVar0")
cell_var.SetNumberOfTuples(pd.GetNumberOfCells())
for i in range(pd.GetNumberOfCells()):
    cell_var.SetValue(i, float(i))
pd.GetCellData().AddArray(cell_var)

# Pass only "Temp" from point data
pass_filter = vtkPassSelectedArrays()
pass_filter.SetInputData(pd)
pass_filter.GetPointDataArraySelection().EnableArray("Temp")
pass_filter.Update()

# Render colored by Temp
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(pass_filter.GetOutputPort())
mapper.SetScalarModeToUsePointFieldData()
mapper.SelectColorArray("Temp")
mapper.SetScalarRange(0, pd.GetNumberOfPoints())

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
render_window.SetWindowName("pass selected arrays")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.ResetCamera()

interactor.Initialize()
interactor.Start()
