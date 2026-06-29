#!/usr/bin/env python

# Demonstrate spherical texture mapping on a soccer ball geometry
# using vtkTextureMapToSphere with cell and vertex coloring.

import os

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import (
    vtkFloatArray,
    vtkLookupTable,
    vtkPoints,
)
from vtkmodules.vtkCommonDataModel import (
    vtkCellArray,
    vtkPolyData,
)
from vtkmodules.vtkFiltersTexture import vtkTextureMapToSphere
from vtkmodules.vtkIOImage import vtkPNMReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkDataSetMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
    vtkTexture,
)

data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Soccer ball vertices (first point repeated because polygons were 1-offset)
points = vtkPoints()
points.InsertNextPoint(0.348012, 0, 0.93749)
points.InsertNextPoint(0.348012, 0, 0.93749)
points.InsertNextPoint(0.107542, 0.330979, 0.93749)
points.InsertNextPoint(-0.281548, 0.204556, 0.93749)
points.InsertNextPoint(-0.281548, -0.204556, 0.93749)
points.InsertNextPoint(0.107542, -0.330979, 0.93749)
points.InsertNextPoint(0.694318, 0, 0.719669)
points.InsertNextPoint(0.799191, -0.327801, 0.502204)
points.InsertNextPoint(0.965027, -0.20654, 0.154057)
points.InsertNextPoint(0.965027, 0.20654, 0.154057)
points.InsertNextPoint(0.799191, 0.327801, 0.502204)
points.InsertNextPoint(0.214556, 0.660335, 0.719669)
points.InsertNextPoint(0.558721, 0.65878, 0.502204)
points.InsertNextPoint(0.494641, 0.853971, 0.154057)
points.InsertNextPoint(0.101778, 0.981619, 0.154057)
points.InsertNextPoint(-0.0647933, 0.861372, 0.502204)
points.InsertNextPoint(-0.561715, 0.40811, 0.719669)
points.InsertNextPoint(-0.453883, 0.734949, 0.502204)
points.InsertNextPoint(-0.659322, 0.734323, 0.154057)
points.InsertNextPoint(-0.902124, 0.400134, 0.154057)
points.InsertNextPoint(-0.839236, 0.204556, 0.502204)
points.InsertNextPoint(-0.561715, -0.40811, 0.719669)
points.InsertNextPoint(-0.839236, -0.204556, 0.502204)
points.InsertNextPoint(-0.902124, -0.400134, 0.154057)
points.InsertNextPoint(-0.659322, -0.734323, 0.154057)
points.InsertNextPoint(-0.453883, -0.734949, 0.502204)
points.InsertNextPoint(0.214556, -0.660335, 0.719669)
points.InsertNextPoint(-0.0647933, -0.861372, 0.502204)
points.InsertNextPoint(0.101778, -0.981619, 0.154057)
points.InsertNextPoint(0.494641, -0.853971, 0.154057)
points.InsertNextPoint(0.558721, -0.65878, 0.502204)
points.InsertNextPoint(0.902124, 0.400134, -0.154057)
points.InsertNextPoint(0.839236, 0.204556, -0.502204)
points.InsertNextPoint(0.561715, 0.40811, -0.719669)
points.InsertNextPoint(0.453883, 0.734949, -0.502204)
points.InsertNextPoint(0.659322, 0.734323, -0.154057)
points.InsertNextPoint(-0.101778, 0.981619, -0.154057)
points.InsertNextPoint(0.0647933, 0.861372, -0.502204)
points.InsertNextPoint(-0.214556, 0.660335, -0.719669)
points.InsertNextPoint(-0.558721, 0.65878, -0.502204)
points.InsertNextPoint(-0.494641, 0.853971, -0.154057)
points.InsertNextPoint(-0.965027, 0.20654, -0.154057)
points.InsertNextPoint(-0.799191, 0.327801, -0.502204)
points.InsertNextPoint(-0.694318, 0, -0.719669)
points.InsertNextPoint(-0.799191, -0.327801, -0.502204)
points.InsertNextPoint(-0.965027, -0.20654, -0.154057)
points.InsertNextPoint(-0.494641, -0.853971, -0.154057)
points.InsertNextPoint(-0.558721, -0.65878, -0.502204)
points.InsertNextPoint(-0.214556, -0.660335, -0.719669)
points.InsertNextPoint(0.0647933, -0.861372, -0.502204)
points.InsertNextPoint(-0.101778, -0.981619, -0.154057)
points.InsertNextPoint(0.659322, -0.734323, -0.154057)
points.InsertNextPoint(0.453883, -0.734949, -0.502204)
points.InsertNextPoint(0.561715, -0.40811, -0.719669)
points.InsertNextPoint(0.839236, -0.204556, -0.502204)
points.InsertNextPoint(0.902124, -0.400134, -0.154057)
points.InsertNextPoint(0.281548, -0.204556, -0.93749)
points.InsertNextPoint(-0.107542, -0.330979, -0.93749)
points.InsertNextPoint(-0.348012, 0, -0.93749)
points.InsertNextPoint(-0.107542, 0.330979, -0.93749)
points.InsertNextPoint(0.281548, 0.204556, -0.93749)

# Pentagonal faces (12 pentagons)
faces = vtkCellArray()
pent_faces = [
    [5, 4, 3, 2, 1],
    [10, 9, 8, 7, 6],
    [15, 14, 13, 12, 11],
    [20, 19, 18, 17, 16],
    [25, 24, 23, 22, 21],
    [30, 29, 28, 27, 26],
    [35, 34, 33, 32, 31],
    [40, 39, 38, 37, 36],
    [45, 44, 43, 42, 41],
    [50, 49, 48, 47, 46],
    [55, 54, 53, 52, 51],
    [60, 59, 58, 57, 56],
]
for f in pent_faces:
    faces.InsertNextCell(5)
    for p in f:
        faces.InsertCellPoint(p)

# Hexagonal faces (20 hexagons)
hex_faces = [
    [2, 11, 12, 10, 6, 1],
    [3, 16, 17, 15, 11, 2],
    [4, 21, 22, 20, 16, 3],
    [5, 26, 27, 25, 21, 4],
    [1, 6, 7, 30, 26, 5],
    [12, 13, 35, 31, 9, 10],
    [17, 18, 40, 36, 14, 15],
    [22, 23, 45, 41, 19, 20],
    [27, 28, 50, 46, 24, 25],
    [7, 8, 55, 51, 29, 30],
    [9, 31, 32, 54, 55, 8],
    [14, 36, 37, 34, 35, 13],
    [19, 41, 42, 39, 40, 18],
    [24, 46, 47, 44, 45, 23],
    [29, 51, 52, 49, 50, 28],
    [32, 33, 60, 56, 53, 54],
    [37, 38, 59, 60, 33, 34],
    [42, 43, 58, 59, 38, 39],
    [47, 48, 57, 58, 43, 44],
    [52, 53, 56, 57, 48, 49],
]
for f in hex_faces:
    faces.InsertNextCell(6)
    for p in f:
        faces.InsertCellPoint(p)

# Cell colors: 12 pentagons = 1, 20 hexagons = 2
face_colors = vtkFloatArray()
for _ in range(12):
    face_colors.InsertNextValue(1)
for _ in range(20):
    face_colors.InsertNextValue(2)

# Vertex colors: all = 2
vertex_colors = vtkFloatArray()
for _ in range(61):
    vertex_colors.InsertNextValue(2)

# Assemble polydata
model = vtkPolyData()
model.SetPolys(faces)
model.SetPoints(points)
model.GetCellData().SetScalars(face_colors)
model.GetPointData().SetScalars(vertex_colors)

# Spherical texture mapping
ball_tc = vtkTextureMapToSphere()
ball_tc.SetInputData(model)

# Lookup table for black / red / light-grey
lookup_table = vtkLookupTable()
lookup_table.SetNumberOfColors(3)
lookup_table.Build()
lookup_table.SetTableValue(0, 0, 0, 0, 1)
lookup_table.SetTableValue(1, 1, 0.3, 0.3, 1)
lookup_table.SetTableValue(2, 0.8, 0.8, 0.9, 1)

# Mapper
mapper = vtkDataSetMapper()
mapper.SetInputConnection(ball_tc.GetOutputPort())
mapper.SetScalarModeToUseCellData()
mapper.SetLookupTable(lookup_table)
mapper.SetScalarRange(0, 2)

# Read earth texture
earth = vtkPNMReader()
earth.SetFileName(os.path.join(data_dir, "earth.ppm"))

texture = vtkTexture()
texture.SetInputConnection(earth.GetOutputPort())

# Actor
soccer_ball = vtkActor()
soccer_ball.SetMapper(mapper)
soccer_ball.SetTexture(texture)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(soccer_ball)
renderer.SetBackground(0.1, 0.2, 0.4)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(300, 300)
render_window.SetWindowName("socbal")

# Scene
renderer.GetActiveCamera().SetPosition(4.19682, 4.65178, 6.23545)
renderer.GetActiveCamera().SetFocalPoint(0, 0, 0)
renderer.GetActiveCamera().SetViewAngle(21.4286)
renderer.GetActiveCamera().SetViewUp(0.451577, -0.833646, 0.317981)
renderer.GetActiveCamera().Zoom(1.4)
renderer.ResetCameraClippingRange()

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
