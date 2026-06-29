#!/usr/bin/env python

# Read a PLY file with per-point texture UV coordinates and render with a PNG texture.

import os

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkIOImage import vtkPNGReader
from vtkmodules.vtkIOPLY import vtkPLYReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
    vtkTexture,
)

# Source
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

ply_reader = vtkPLYReader()
ply_reader.SetFileName(os.path.join(data_dir, "squareTextured.ply"))
ply_reader.Update()

png_reader = vtkPNGReader()
png_reader.SetFileName(os.path.join(data_dir, "vtk.png"))
png_reader.Update()

point_texture = vtkTexture()
point_texture.SetInputConnection(png_reader.GetOutputPort())

# Mapper
textured_mapper = vtkPolyDataMapper()
textured_mapper.SetInputConnection(ply_reader.GetOutputPort())
textured_mapper.ScalarVisibilityOn()

# Actor
textured_actor = vtkActor()
textured_actor.SetMapper(textured_mapper)
textured_actor.SetTexture(point_texture)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(textured_actor)
renderer.SetBackground(0, 0, 0)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("ply reader texture uv points")
render_window.SetMultiSamples(0)
render_window.SetSize(400, 400)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
interactor.Initialize()
interactor.Start()
