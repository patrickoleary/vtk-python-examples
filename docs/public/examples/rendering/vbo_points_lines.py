#!/usr/bin/env python

# Demonstrate VBO rendering with points, lines, and triangles in a single polydata.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import vtkPoints
from vtkmodules.vtkCommonDataModel import vtkCellArray, vtkPolyData
from vtkmodules.vtkCommonExecutionModel import vtkTrivialProducer
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Build polydata with points, lines, and triangles
points = vtkPoints()
points.SetNumberOfPoints(7)
points.SetPoint(0, 0, 0, 0)
points.SetPoint(1, 1, 0, 0)
points.SetPoint(2, 0, 1, 0)
points.SetPoint(3, 1, 1, -1)
points.SetPoint(4, 1, 2, 1)
points.SetPoint(5, 4, 1, -9)
points.SetPoint(6, 3, -2, 1)

# Vertices
verts = vtkCellArray()
verts.InsertNextCell(1)
verts.InsertCellPoint(0)
verts.InsertNextCell(1)
verts.InsertCellPoint(1)
verts.InsertNextCell(1)
verts.InsertCellPoint(5)
verts.InsertNextCell(1)
verts.InsertCellPoint(6)

# Lines
lines = vtkCellArray()
lines.InsertNextCell(2)
lines.InsertCellPoint(2)
lines.InsertCellPoint(3)
lines.InsertNextCell(2)
lines.InsertCellPoint(0)
lines.InsertCellPoint(4)
# Polyline
lines.InsertNextCell(4)
lines.InsertCellPoint(0)
lines.InsertCellPoint(2)
lines.InsertCellPoint(3)
lines.InsertCellPoint(4)

# Triangles
tris = vtkCellArray()
tris.InsertNextCell(3)
tris.InsertCellPoint(0)
tris.InsertCellPoint(2)
tris.InsertCellPoint(3)

polydata = vtkPolyData()
polydata.SetPoints(points)
polydata.SetVerts(verts)
polydata.SetLines(lines)
polydata.SetPolys(tris)

prod = vtkTrivialProducer()
prod.SetOutput(polydata)

mapper = vtkPolyDataMapper()
mapper.SetInputConnection(prod.GetOutputPort())

actor = vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetPointSize(5)
actor.GetProperty().SetLineWidth(2)
actor.GetProperty().SetAmbientColor(0.2, 0.2, 1.0)
actor.GetProperty().SetDiffuseColor(1.0, 0.65, 0.7)
actor.GetProperty().SetSpecularColor(1.0, 1.0, 1.0)
actor.GetProperty().SetSpecular(0.5)
actor.GetProperty().SetDiffuse(0.7)
actor.GetProperty().SetAmbient(0.5)
actor.GetProperty().SetSpecularPower(20.0)
actor.GetProperty().SetOpacity(1.0)

renderer = vtkRenderer()
renderer.SetBackground(0.0, 0.0, 0.0)
renderer.AddActor(actor)

render_window = vtkRenderWindow()
render_window.SetMultiSamples(0)
render_window.SetSize(300, 300)
render_window.AddRenderer(renderer)
render_window.SetWindowName("vbo points lines")

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Pipeline exception: render, change property, re-render
render_window.Render()
actor.GetProperty().SetPointSize(2.0)
render_window.Render()

interactor.Initialize()
interactor.Start()
