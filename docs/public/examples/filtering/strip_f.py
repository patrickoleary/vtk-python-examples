#!/usr/bin/env python

# Demonstrate vtkStripper and vtkMaskPolyData on fran's face data.

import os

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersCore import (
    vtkMaskPolyData,
    vtkPolyDataNormals,
    vtkStripper,
)
from vtkmodules.vtkIOLegacy import vtkPolyDataReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkCamera,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Data directory
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Read the Cyberware scan
cyber = vtkPolyDataReader()
cyber.SetFileName(os.path.join(data_dir, "fran_cut.vtk"))

normals = vtkPolyDataNormals()
normals.SetInputConnection(cyber.GetOutputPort())
normals.FlipNormalsOn()

stripper = vtkStripper()
stripper.SetInputConnection(cyber.GetOutputPort())

mask = vtkMaskPolyData()
mask.SetInputConnection(stripper.GetOutputPort())
mask.SetOnRatio(2)

mapper = vtkPolyDataMapper()
mapper.SetInputConnection(mask.GetOutputPort())

actor = vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetColor(1.0, 0.49, 0.25)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(1, 1, 1)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(300, 300)
render_window.SetWindowName("strip f")

# Scene
camera = vtkCamera()
camera.SetFocalPoint(0.0520703, -0.128547, -0.0581083)
camera.SetPosition(0.419653, -0.120916, -0.321626)
camera.SetViewAngle(21.4286)
camera.SetViewUp(-0.0136986, 0.999858, 0.00984497)
renderer.SetActiveCamera(camera)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
