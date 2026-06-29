#!/usr/bin/env python

# Write a sphere as OBJ, re-read it, and render.

import os
import tempfile

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkIOGeometry import (
    vtkOBJReader,
    vtkOBJWriter,
)
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Create a sphere
sphere_source = vtkSphereSource()
sphere_source.SetThetaResolution(16)
sphere_source.SetPhiResolution(16)
sphere_source.Update()

# Write to OBJ
temp_dir = tempfile.mkdtemp()
obj_file = os.path.join(temp_dir, "sphere.obj")

obj_writer = vtkOBJWriter()
obj_writer.SetFileName(obj_file)
obj_writer.SetInputConnection(sphere_source.GetOutputPort())
obj_writer.Write()

# Re-read OBJ
obj_reader = vtkOBJReader()
obj_reader.SetFileName(obj_file)
obj_reader.Update()

# Mapper
poly_mapper = vtkPolyDataMapper()
poly_mapper.SetInputConnection(obj_reader.GetOutputPort())

# Actor
obj_actor = vtkActor()
obj_actor.SetMapper(poly_mapper)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(obj_actor)
renderer.SetBackground(0.2, 0.3, 0.4)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("obj polydata writer")
render_window.SetMultiSamples(0)
render_window.SetSize(300, 300)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.ResetCamera()

interactor.Initialize()
interactor.Start()

# Clean up
os.remove(obj_file)
os.rmdir(temp_dir)
