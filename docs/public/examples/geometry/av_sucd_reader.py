#!/usr/bin/env python

# Read AVS UCD data in ASCII and binary form and render side by side.

import os

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkIOGeometry import vtkAVSucdReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkDataSetMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Source
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Read ASCII AVS UCD
ucd_reader_ascii = vtkAVSucdReader()
ucd_reader_ascii.SetFileName(os.path.join(data_dir, "cellsnd.ascii.inp"))

dataset_mapper_0 = vtkDataSetMapper()
dataset_mapper_0.SetInputConnection(ucd_reader_ascii.GetOutputPort())

actor_0 = vtkActor()
actor_0.SetMapper(dataset_mapper_0)

# Read binary AVS UCD
ucd_reader_bin = vtkAVSucdReader()
ucd_reader_bin.SetFileName(os.path.join(data_dir, "cellsnd.bin.inp"))

dataset_mapper_1 = vtkDataSetMapper()
dataset_mapper_1.SetInputConnection(ucd_reader_bin.GetOutputPort())

actor_1 = vtkActor()
actor_1.SetMapper(dataset_mapper_1)
actor_1.AddPosition(5, 0, 0)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(actor_0)
renderer.AddActor(actor_1)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("av sucd reader")
render_window.SetMultiSamples(0)
render_window.SetSize(300, 150)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.ResetCamera()
renderer.GetActiveCamera().Zoom(2)

interactor.Initialize()
interactor.Start()
