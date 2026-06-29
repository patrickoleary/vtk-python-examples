#!/usr/bin/env python

# Test rendering a single point vertex.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import vtkPoints
from vtkmodules.vtkCommonDataModel import (
    vtkCellArray,
    vtkPolyData,
)
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Single point
points = vtkPoints()
points.InsertPoint(0, 0.0, 0.0, 0.0)

verts = vtkCellArray()
verts.InsertNextCell(1)
verts.InsertCellPoint(0)

poly_data = vtkPolyData()
poly_data.SetPoints(points)
poly_data.SetVerts(verts)

point_mapper = vtkPolyDataMapper()
point_mapper.SetInputData(poly_data)

point_actor = vtkActor()
point_actor.SetMapper(point_mapper)
point_actor.GetProperty().SetPointSize(8)

renderer = vtkRenderer()
renderer.AddViewProp(point_actor)

render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("one point")
render_window.SetMultiSamples(0)
render_window.SetSize(300, 300)

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
