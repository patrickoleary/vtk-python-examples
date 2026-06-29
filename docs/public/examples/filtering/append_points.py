#!/usr/bin/env python

# Demonstrate vtkAppendPoints by creating two point sets with random
# vertices and appending them together, then visualizing the combined
# result with color-coded point sources.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import (
    vtkMinimalStandardRandomSequence,
    vtkPoints,
    vtkUnsignedCharArray,
)
from vtkmodules.vtkCommonDataModel import (
    vtkCellArray,
    vtkPolyData,
)
from vtkmodules.vtkFiltersGeneral import vtkAppendPoints
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

random_seq = vtkMinimalStandardRandomSequence()
random_seq.SetSeed(1)

# Build two polydata with 4 random vertices each
poly_data_0 = vtkPolyData()
pts_0 = vtkPoints()
pts_0.SetDataType(10)  # VTK_FLOAT
verts_0 = vtkCellArray()
verts_0.InsertNextCell(4)
colors_0 = vtkUnsignedCharArray()
colors_0.SetNumberOfComponents(3)
colors_0.SetName("Colors")
for i in range(4):
    x = random_seq.GetValue(); random_seq.Next()
    y = random_seq.GetValue(); random_seq.Next()
    z = random_seq.GetValue(); random_seq.Next()
    verts_0.InsertCellPoint(pts_0.InsertNextPoint(x, y, z))
    colors_0.InsertNextTuple3(255, 0, 0)
poly_data_0.SetPoints(pts_0)
poly_data_0.SetVerts(verts_0)
poly_data_0.GetPointData().SetScalars(colors_0)

poly_data_1 = vtkPolyData()
pts_1 = vtkPoints()
pts_1.SetDataType(11)  # VTK_DOUBLE
verts_1 = vtkCellArray()
verts_1.InsertNextCell(4)
colors_1 = vtkUnsignedCharArray()
colors_1.SetNumberOfComponents(3)
colors_1.SetName("Colors")
for i in range(4):
    x = random_seq.GetValue(); random_seq.Next()
    y = random_seq.GetValue(); random_seq.Next()
    z = random_seq.GetValue(); random_seq.Next()
    verts_1.InsertCellPoint(pts_1.InsertNextPoint(x, y, z))
    colors_1.InsertNextTuple3(0, 0, 255)
poly_data_1.SetPoints(pts_1)
poly_data_1.SetVerts(verts_1)
poly_data_1.GetPointData().SetScalars(colors_1)

# Append the two point sets
append_points = vtkAppendPoints()
append_points.AddInputData(poly_data_0)
append_points.AddInputData(poly_data_1)
append_points.Update()

# vtkAppendPoints strips vertex cells; re-add them
appended = append_points.GetOutput()
verts_all = vtkCellArray()
for i in range(appended.GetNumberOfPoints()):
    verts_all.InsertNextCell(1)
    verts_all.InsertCellPoint(i)
appended.SetVerts(verts_all)

# Visualize
mapper = vtkPolyDataMapper()
mapper.SetInputData(appended)

actor = vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetPointSize(10.0)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(0.1, 0.2, 0.4)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(400, 400)
render_window.SetWindowName("append points")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.ResetCamera()

interactor.Initialize()
interactor.Start()
