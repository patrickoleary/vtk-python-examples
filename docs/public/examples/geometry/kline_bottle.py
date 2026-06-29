#!/usr/bin/env python

# Demonstrate vtkLoopSubdivisionFilter on a hand-crafted Klein bottle mesh
# by defining points and triangular faces, subdividing four times, and
# rendering with front/back face coloring.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import vtkPoints
from vtkmodules.vtkCommonDataModel import vtkCellArray, vtkPolyData
from vtkmodules.vtkFiltersModeling import vtkLoopSubdivisionFilter
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkDataSetMapper,
    vtkPolyDataMapper,
    vtkProperty,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)
from vtkmodules.vtkRenderingLOD import vtkLODActor

# Define Klein bottle mesh points
points = vtkPoints()
points.InsertNextPoint(0, -16, 0)
points.InsertNextPoint(0, 0, -14)
points.InsertNextPoint(0, 0, 14)
points.InsertNextPoint(14, 0, 0)
points.InsertNextPoint(10, 20, -10)
points.InsertNextPoint(10, 20, 10)
points.InsertNextPoint(10, -20, -10)
points.InsertNextPoint(10, -20, 10)
points.InsertNextPoint(-10, -20, -10)
points.InsertNextPoint(-10, -20, 10)
points.InsertNextPoint(-10, 20, -10)
points.InsertNextPoint(-10, 20, 10)
points.InsertNextPoint(-2, 27, 0)
points.InsertNextPoint(0, 27, 2)
points.InsertNextPoint(0, 27, -2)
points.InsertNextPoint(2, 27, 0)
points.InsertNextPoint(-14, 4, -1)
points.InsertNextPoint(-14, 3, 0)
points.InsertNextPoint(-14, 5, 0)
points.InsertNextPoint(-14, 4, 1)
points.InsertNextPoint(-1, 38, -2)
points.InsertNextPoint(-1, 38, 2)
points.InsertNextPoint(2, 35, -2)
points.InsertNextPoint(2, 35, 2)
points.InsertNextPoint(17, 42, 0)
points.InsertNextPoint(15, 40, 2)
points.InsertNextPoint(15, 39, -2)
points.InsertNextPoint(13, 37, 0)
points.InsertNextPoint(19, -2, -2)
points.InsertNextPoint(19, -2, 2)
points.InsertNextPoint(15, 2, -2)
points.InsertNextPoint(15, 2, 2)

# Define triangular faces
face_data = [
    (3, 4, 5), (3, 5, 7), (3, 7, 6), (3, 6, 4),
    (0, 6, 7), (0, 7, 9), (0, 9, 8), (0, 8, 6),
    (1, 4, 6), (1, 6, 8), (1, 8, 10), (1, 10, 4),
    (2, 11, 9), (2, 9, 7), (2, 7, 5), (2, 5, 11),
    (4, 15, 5), (4, 14, 15), (5, 13, 11), (5, 15, 13),
    (11, 12, 10), (11, 13, 12), (10, 14, 4), (10, 12, 14),
    (8, 17, 16), (8, 9, 17), (9, 19, 17), (9, 11, 19),
    (11, 18, 19), (11, 10, 18), (10, 16, 18), (10, 8, 16),
    (13, 21, 12), (12, 21, 20), (12, 20, 14), (14, 20, 22),
    (14, 22, 15), (15, 22, 23), (15, 23, 13), (13, 23, 21),
    (21, 25, 24), (21, 24, 20), (20, 24, 26), (20, 26, 22),
    (22, 26, 27), (22, 27, 23), (23, 27, 25), (23, 25, 21),
    (25, 29, 24), (24, 29, 28), (24, 28, 26), (26, 28, 30),
    (26, 30, 27), (27, 30, 31), (27, 31, 25), (25, 31, 29),
    (29, 19, 17), (29, 17, 28), (28, 17, 16), (28, 16, 30),
    (30, 16, 18), (30, 18, 31), (31, 18, 19), (31, 19, 29),
]

faces = vtkCellArray()
for tri in face_data:
    faces.InsertNextCell(3)
    faces.InsertCellPoint(tri[0])
    faces.InsertCellPoint(tri[1])
    faces.InsertCellPoint(tri[2])

model = vtkPolyData()
model.SetPolys(faces)
model.SetPoints(points)

# Loop subdivision
subdivide = vtkLoopSubdivisionFilter()
subdivide.SetInputData(model)
subdivide.SetNumberOfSubdivisions(4)

# Mapper and actor
mapper = vtkDataSetMapper()
mapper.SetInputConnection(subdivide.GetOutputPort())

rose = vtkLODActor()
rose.SetMapper(mapper)

# Backface property
back_prop = vtkProperty()
back_prop.SetDiffuseColor(1, 1, 0.3)
rose.SetBackfaceProperty(back_prop)
rose.GetProperty().SetDiffuseColor(1, 0.4, 0.3)
rose.GetProperty().SetSpecular(0.4)
rose.GetProperty().SetDiffuse(0.8)
rose.GetProperty().SetSpecularPower(40)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(rose)
renderer.SetBackground(0.1, 0.2, 0.4)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(300, 300)
render_window.SetWindowName("kline bottle")

# Scene
renderer.ResetCamera()
renderer.GetActiveCamera().Zoom(4.5)
renderer.GetActiveCamera().Azimuth(-90)
renderer.ResetCameraClippingRange()

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
