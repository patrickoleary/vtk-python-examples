#!/usr/bin/env python

# Read ProSTAR cell and vertex files and render.

import os

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkIOGeometry import vtkProStarReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkDataSetMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Source
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Read ProSTAR files
prostar_reader = vtkProStarReader()
prostar_reader.SetFileName(os.path.join(data_dir, "prostar"))
prostar_reader.Update()

# Mapper
dataset_mapper = vtkDataSetMapper()
dataset_mapper.SetInputConnection(prostar_reader.GetOutputPort())

# Actor
prostar_actor = vtkActor()
prostar_actor.SetMapper(dataset_mapper)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(prostar_actor)
renderer.SetBackground(0, 0, 0)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("pro star reader")
render_window.SetMultiSamples(0)
render_window.SetSize(300, 300)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.ResetCamera()

interactor.Initialize()
interactor.Start()
