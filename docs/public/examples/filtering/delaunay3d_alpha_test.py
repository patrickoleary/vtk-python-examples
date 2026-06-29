#!/usr/bin/env python

# Demonstrate vtkDelaunay3D with alpha shapes on a set of manually
# defined 3D points.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import vtkPoints
from vtkmodules.vtkCommonDataModel import vtkPolyData
from vtkmodules.vtkFiltersCore import vtkDelaunay3D
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkDataSetMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Data from Sandia
points = vtkPoints()
points.InsertNextPoint(0, 0, 0)
points.InsertNextPoint(1, 0, 0)
points.InsertNextPoint(1, 1, 0)
points.InsertNextPoint(0, 1, 0)
points.InsertNextPoint(0, 0, 5)
points.InsertNextPoint(1, 0, 4)
points.InsertNextPoint(1, 1, 4)
points.InsertNextPoint(0, 1, 5)
points.InsertNextPoint(5, 0, 7)
points.InsertNextPoint(5, 0, 6)
points.InsertNextPoint(5, 1, 6)
points.InsertNextPoint(5, 1, 7)
points.InsertNextPoint(11, 1, 5)
points.InsertNextPoint(10, 1, 4)
points.InsertNextPoint(10, 0, 4)
points.InsertNextPoint(11, 0, 5)
points.InsertNextPoint(10, 0, 0)
points.InsertNextPoint(11, 0, 0)
points.InsertNextPoint(11, 1, 0)
points.InsertNextPoint(10, 1, 0)

profile = vtkPolyData()
profile.SetPoints(points)

# Triangulate with alpha shape
delaunay = vtkDelaunay3D()
delaunay.SetInputData(profile)
delaunay.SetTolerance(0.01)
delaunay.SetAlpha(2.8)
delaunay.AlphaTetsOn()
delaunay.AlphaTrisOn()
delaunay.AlphaLinesOff()
delaunay.AlphaVertsOn()

mapper = vtkDataSetMapper()
mapper.SetInputConnection(delaunay.GetOutputPort())

actor = vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetColor(1, 0, 0)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(1, 1, 1)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(250, 250)
render_window.SetWindowName("delaunay3d alpha test")

# Scene
camera = renderer.GetActiveCamera()
camera.SetFocalPoint(0, 0, 0)
camera.SetPosition(1, 1, 1)
renderer.ResetCamera()

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
