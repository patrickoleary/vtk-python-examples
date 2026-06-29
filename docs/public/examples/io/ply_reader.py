#!/usr/bin/env python

# Read a PLY file (Stanford bunny) and render it.

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
ply_reader.SetFileName(os.path.join(data_dir, "bunny.ply"))
ply_reader.Update()

# Mapper
bunny_mapper = vtkPolyDataMapper()
bunny_mapper.SetInputConnection(ply_reader.GetOutputPort())
bunny_mapper.ScalarVisibilityOn()

# Actor
bunny_actor = vtkActor()
bunny_actor.SetMapper(bunny_mapper)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(bunny_actor)
renderer.SetBackground(0, 0, 0)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("ply reader")
render_window.SetMultiSamples(0)
render_window.SetSize(300, 300)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
interactor.Initialize()
interactor.Start()
