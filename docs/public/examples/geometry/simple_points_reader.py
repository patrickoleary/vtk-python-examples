#!/usr/bin/env python

# Read simple points text file and render as points.

import os

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkIOLegacy import vtkSimplePointsReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Source
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Read simple points
points_reader = vtkSimplePointsReader()
points_reader.SetFileName(os.path.join(data_dir, "points.txt"))

# Mapper
poly_mapper = vtkPolyDataMapper()
poly_mapper.SetInputConnection(points_reader.GetOutputPort())

# Actor
points_actor = vtkActor()
points_actor.SetMapper(poly_mapper)
points_actor.GetProperty().SetPointSize(5)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(points_actor)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("simple points reader")
render_window.SetMultiSamples(0)
render_window.SetSize(300, 300)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.ResetCamera()

interactor.Initialize()
interactor.Start()
