#!/usr/bin/env python

# Read a GAMBIT neutral file and render.

import os

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkIOGeometry import vtkGAMBITReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkDataSetMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Source
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Read GAMBIT file
gambit_reader = vtkGAMBITReader()
gambit_reader.SetFileName(os.path.join(data_dir, "prism.neu"))

# Mapper
dataset_mapper = vtkDataSetMapper()
dataset_mapper.SetInputConnection(gambit_reader.GetOutputPort())

# Actor
gambit_actor = vtkActor()
gambit_actor.SetMapper(dataset_mapper)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(gambit_actor)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("gambit reader")
render_window.SetMultiSamples(0)
render_window.SetSize(300, 300)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.ResetCamera()

interactor.Initialize()
interactor.Start()
