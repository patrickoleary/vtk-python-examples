#!/usr/bin/env python

# Write a sphere with normals to PLY, read back, and render to verify normals are preserved.

import os
import tempfile

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkIOPLY import vtkPLYReader, vtkPLYWriter
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Source
temp_dir = tempfile.mkdtemp()

sphere_source = vtkSphereSource()
sphere_source.GenerateNormalsOn()

ply_output_file = os.path.join(temp_dir, "TestPlyWriterNormalsOutput.ply")
ply_writer = vtkPLYWriter()
ply_writer.SetInputConnection(sphere_source.GetOutputPort())
ply_writer.SetFileName(ply_output_file)
ply_writer.Write()

readback_reader = vtkPLYReader()
readback_reader.SetFileName(ply_output_file)

# Mapper
normals_mapper = vtkPolyDataMapper()
normals_mapper.SetInputConnection(readback_reader.GetOutputPort())

# Actor
normals_actor = vtkActor()
normals_actor.SetMapper(normals_mapper)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(normals_actor)
renderer.SetBackground(0.2, 0.3, 0.4)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("ply writer normals")
render_window.SetMultiSamples(0)
render_window.SetSize(300, 300)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
interactor.Initialize()
interactor.Start()
