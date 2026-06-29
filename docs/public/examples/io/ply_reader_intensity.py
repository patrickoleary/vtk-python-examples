#!/usr/bin/env python

# Read a PLY file (Armadillo) with intensity data and render it.

import os

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkIOPLY import vtkPLYReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Source
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

ply_reader = vtkPLYReader()
ply_reader.SetFileName(os.path.join(data_dir, "Armadillo.ply"))

# Mapper
armadillo_mapper = vtkPolyDataMapper()
armadillo_mapper.SetInputConnection(ply_reader.GetOutputPort())
armadillo_mapper.ScalarVisibilityOff()

# Actor
armadillo_actor = vtkActor()
armadillo_actor.SetMapper(armadillo_mapper)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(armadillo_actor)
renderer.SetBackground(0.2, 0.3, 0.5)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("ply reader intensity")
render_window.SetMultiSamples(0)
render_window.SetSize(300, 300)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.ResetCamera()
renderer.GetActiveCamera().Azimuth(210)
renderer.GetActiveCamera().Elevation(30)

interactor.Initialize()
interactor.Start()
