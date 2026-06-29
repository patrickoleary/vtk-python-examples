#!/usr/bin/env python

# Test vtkShepardMethod interpolation on random 3D points.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import (
    vtkFloatArray,
    vtkMath,
    vtkPoints,
)
from vtkmodules.vtkCommonDataModel import vtkPolyData
from vtkmodules.vtkImagingHybrid import vtkShepardMethod
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkDataSetMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Create random points with random scalar values
vtk_math = vtkMath()
points = vtkPoints()
for i in range(50):
    points.InsertPoint(i, vtk_math.Random(0, 1), vtk_math.Random(0, 1), vtk_math.Random(0, 1))

scalars = vtkFloatArray()
for i in range(50):
    scalars.InsertValue(i, vtk_math.Random(0, 1))

profile = vtkPolyData()
profile.SetPoints(points)
profile.GetPointData().SetScalars(scalars)

# Shepard interpolation
shepard = vtkShepardMethod()
shepard.SetInputData(profile)
shepard.SetModelBounds(0, 1, 0, 1, 0.1, 0.5)
shepard.SetNullValue(1)
shepard.SetSampleDimensions(20, 20, 20)
shepard.Update()

mapper = vtkDataSetMapper()
mapper.SetInputConnection(shepard.GetOutputPort())

actor = vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetColor(1, 0, 0)

renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(1, 1, 1)

render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(400, 400)
render_window.SetWindowName("shepards")

# Scene
renderer.ResetCamera()
camera = renderer.GetActiveCamera()
camera.Azimuth(160)
camera.Elevation(30)
camera.Zoom(1.5)
renderer.ResetCameraClippingRange()

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
