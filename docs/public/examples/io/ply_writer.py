#!/usr/bin/env python

# Write a PLY file with texture coordinates, read it back and render.

import os
import tempfile

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkIOImage import vtkPNGReader
from vtkmodules.vtkIOPLY import vtkPLYReader, vtkPLYWriter
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
temp_dir = tempfile.mkdtemp()
ply_output_file = os.path.join(temp_dir, "tmp.ply")

ply_reader = vtkPLYReader()
ply_reader.SetFileName(os.path.join(data_dir, "squareTextured.ply"))
ply_reader.Update()

ply_writer = vtkPLYWriter()
ply_writer.SetFileName(ply_output_file)
ply_writer.SetFileTypeToASCII()
ply_writer.SetTextureCoordinatesNameToTextureUV()
ply_writer.SetInputConnection(ply_reader.GetOutputPort())
ply_writer.AddComment("TextureFile vtk.png")
ply_writer.Write()

readback_reader = vtkPLYReader()
readback_reader.SetFileName(ply_output_file)

png_reader = vtkPNGReader()
png_reader.SetFileName(os.path.join(data_dir, "vtk.png"))
png_reader.Update()

png_texture = vtkTexture()
png_texture.SetInputConnection(png_reader.GetOutputPort())

# Mapper
textured_mapper = vtkPolyDataMapper()
textured_mapper.SetInputConnection(readback_reader.GetOutputPort())
textured_mapper.ScalarVisibilityOff()

# Actor
textured_actor = vtkActor()
textured_actor.SetMapper(textured_mapper)
textured_actor.SetTexture(png_texture)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(textured_actor)
renderer.SetBackground(0.2, 0.3, 0.4)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("ply writer")
render_window.SetMultiSamples(0)
render_window.SetSize(300, 300)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
interactor.Initialize()
interactor.Start()
