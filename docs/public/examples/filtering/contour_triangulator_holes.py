#!/usr/bin/env python

# Demonstrate vtkContourTriangulator with difficult holes by creating
# closed contours representing a square with rectangular cutouts and
# triangulating them.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import vtkPoints
from vtkmodules.vtkCommonDataModel import (
    vtkCellArray,
    vtkPolyData,
)
from vtkmodules.vtkFiltersGeneral import vtkContourTriangulator
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkDataSetMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Define 6 closed contours: outer square + 5 inner holes
polys = [
    [(-100.0, -100.0, 0.0), (100.0, -100.0, 0.0),
     (100.0, 100.0, 0.0), (-100.0, 100.0, 0.0)],
    [(-30.0, 30.0, 0.0), (30.0, 30.0, 0.0),
     (30.0, -30.0, 0.0), (-30.0, -30.0, 0.0)],
    [(-40.0, 80.0, 0.0), (40.0, 80.0, 0.0),
     (40.0, 50.0, 0.0), (-40.0, 50.0, 0.0)],
    [(-40.0, -50.0, 0.0), (40.0, -50.0, 0.0),
     (40.0, -80.0, 0.0), (-40.0, -80.0, 0.0)],
    [(-90.0, 90.0, 0.0), (-50.0, 90.0, 0.0),
     (-50.0, -90.0, 0.0), (-90.0, -90.0, 0.0)],
    [(50.0, 90.0, 0.0), (90.0, 90.0, 0.0),
     (90.0, -90.0, 0.0), (50.0, -90.0, 0.0)],
]

# Build polydata with closed line contours
points = vtkPoints()
lines = vtkCellArray()

for contour in polys:
    ids = []
    for pt in contour:
        ids.append(points.InsertNextPoint(pt[0], pt[1], pt[2]))
    # Close the contour by appending the first point id
    ids.append(ids[0])
    lines.InsertNextCell(len(ids), ids)

data = vtkPolyData()
data.SetPoints(points)
data.SetLines(lines)
data.BuildLinks()

# Triangulate the contours
triangulator = vtkContourTriangulator()
triangulator.SetInputData(data)

# Mapper and actor
mapper = vtkDataSetMapper()
mapper.SetInputConnection(triangulator.GetOutputPort())
mapper.ScalarVisibilityOff()

actor = vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetColor(1.0, 1.0, 1.0)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(0.5, 0.5, 0.5)

# Window
render_window = vtkRenderWindow()
render_window.SetMultiSamples(0)
render_window.AddRenderer(renderer)
render_window.SetSize(300, 300)
render_window.SetWindowName("contour triangulator holes")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.ResetCamera()
renderer.GetActiveCamera().Zoom(1.4)

interactor.Initialize()
interactor.Start()
