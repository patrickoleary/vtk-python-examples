#!/usr/bin/env python

# Read a PLY file with face textures using reused texture coordinates and render.

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
ply_reader.SetFileName(os.path.join(data_dir, "FaceTexturedWithReusedTCoords.ply"))
ply_reader.Update()

png_reader = vtkPNGReader()
png_reader.SetFileName(os.path.join(data_dir, "vtk.png"))
png_reader.Update()

face_texture = vtkTexture()
face_texture.SetInputConnection(png_reader.GetOutputPort())

# Mapper
face_mapper = vtkPolyDataMapper()
face_mapper.SetInputConnection(ply_reader.GetOutputPort())
face_mapper.ScalarVisibilityOn()

# Actor
face_actor = vtkActor()
face_actor.SetMapper(face_mapper)
face_actor.SetTexture(face_texture)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(face_actor)
renderer.SetBackground(0, 0, 0)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("ply reader face textured with reused t coord")
render_window.SetMultiSamples(0)
render_window.SetSize(400, 400)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
interactor.Initialize()
interactor.Start()
