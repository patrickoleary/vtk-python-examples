#!/usr/bin/env python

# Demonstrate vtkReflectionFilter by reflecting a pyramid across the
# Z-min plane with CopyInput on, and rendering both the original and
# reflected cells with edge visibility.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import vtkPoints
from vtkmodules.vtkCommonCore import vtkIdList
from vtkmodules.vtkCommonDataModel import (
    VTK_PYRAMID,
    vtkUnstructuredGrid,
)
from vtkmodules.vtkFiltersGeneral import vtkReflectionFilter
from vtkmodules.vtkFiltersGeometry import vtkDataSetSurfaceFilter
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Build a pyramid
points = vtkPoints()
points.InsertNextPoint(-1, -1, -1)
points.InsertNextPoint(1, -1, -1)
points.InsertNextPoint(1, 1, -1)
points.InsertNextPoint(-1, 1, -1)
points.InsertNextPoint(0, 0, 1)

pyramid = vtkUnstructuredGrid()
pyramid.SetPoints(points)

verts = vtkIdList()
for i in range(5):
    verts.InsertNextId(i)
pyramid.InsertNextCell(VTK_PYRAMID, verts)

# Reflect across Z-min plane with CopyInput on and FlipAllInputArrays on
reflection = vtkReflectionFilter()
reflection.SetInputData(pyramid)
reflection.CopyInputOn()
reflection.FlipAllInputArraysOn()
reflection.SetPlaneToZMin()
reflection.Update()

# Extract surface
surface = vtkDataSetSurfaceFilter()
surface.SetInputConnection(reflection.GetOutputPort())

# Render
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(surface.GetOutputPort())

actor = vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetEdgeVisibility(True)
actor.GetProperty().SetEdgeColor(0, 0, 0)
actor.GetProperty().SetColor(0.8, 0.4, 0.2)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(0.1, 0.2, 0.4)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(400, 400)
render_window.SetWindowName("reflection")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.ResetCamera()

interactor.Initialize()
interactor.Start()
