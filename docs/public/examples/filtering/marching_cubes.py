#!/usr/bin/env python

# Extract an isosurface from CT head data using vtkMarchingCubes with
# a rotated direction matrix.

import os
from math import cos, sin, pi

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersCore import vtkMarchingCubes
from vtkmodules.vtkIOImage import vtkVolume16Reader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Data directory
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Read CT head data with a rotated direction matrix
angle = pi / 2
orientation = [
    -1, 0, 0,
    0, cos(angle), -sin(angle),
    0, -sin(angle), -cos(angle),
]

v16 = vtkVolume16Reader()
v16.SetDataDimensions(64, 64)
v16.SetDataByteOrderToLittleEndian()
v16.SetFilePrefix(os.path.join(data_dir, "headsq", "quarter"))
v16.SetImageRange(1, 93)
v16.SetDataSpacing(3.2, 3.2, 1.5)
v16.SetDataOrigin(0.1, 10, 1000)
v16.GetOutput().SetDirectionMatrix(orientation)
v16.Update()

# Extract isosurface
iso = vtkMarchingCubes()
iso.SetInputData(v16.GetOutput())
iso.ComputeNormalsOn()
iso.SetValue(0, 1150)

iso_mapper = vtkPolyDataMapper()
iso_mapper.SetInputConnection(iso.GetOutputPort())
iso_mapper.ScalarVisibilityOff()

iso_actor = vtkActor()
iso_actor.SetMapper(iso_mapper)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(iso_actor)
renderer.SetBackground(0.2, 0.3, 0.4)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(200, 200)
render_window.SetWindowName("marching cubes")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.ResetCamera()

interactor.Initialize()
interactor.Start()
