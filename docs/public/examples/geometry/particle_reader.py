#!/usr/bin/env python

# Read particle data and render as colored points.

import os

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkIOGeometry import vtkParticleReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Source
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Read particle data
particle_reader = vtkParticleReader()
particle_reader.SetFileName(os.path.join(data_dir, "Particles.raw"))
particle_reader.SetDataByteOrderToBigEndian()

# Mapper
poly_mapper = vtkPolyDataMapper()
poly_mapper.SetInputConnection(particle_reader.GetOutputPort())
poly_mapper.SetScalarRange(4, 9)
poly_mapper.SetPiece(1)
poly_mapper.SetNumberOfPieces(2)

# Actor
particle_actor = vtkActor()
particle_actor.SetMapper(poly_mapper)
particle_actor.GetProperty().SetPointSize(2.5)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(particle_actor)
renderer.SetBackground(0, 0, 0)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("particle reader")
render_window.SetMultiSamples(0)
render_window.SetSize(200, 200)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.ResetCamera()

interactor.Initialize()
interactor.Start()
