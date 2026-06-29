#!/usr/bin/env python

# Read a binary AVS UCD file with temperature scalars and render with edge visibility.

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

# Read binary AVS UCD
ucd_reader = vtkAVSucdReader()
ucd_reader.SetFileName(os.path.join(data_dir, "cellsnd.bin.inp"))
ucd_reader.Update()

# Set active scalars
ucd_reader.GetOutput().GetPointData().SetActiveScalars("temperature")

# Mapper
dataset_mapper = vtkDataSetMapper()
dataset_mapper.SetInputData(ucd_reader.GetOutput())
dataset_mapper.ScalarVisibilityOn()
dataset_mapper.SetScalarRange(ucd_reader.GetOutput().GetPointData().GetScalars().GetRange())

# Actor
ucd_actor = vtkActor()
ucd_actor.SetMapper(dataset_mapper)
ucd_actor.GetProperty().EdgeVisibilityOn()

# Renderer
renderer = vtkRenderer()
renderer.AddActor(ucd_actor)
renderer.SetBackground(0, 0, 0)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("av sucd reader binary")
render_window.SetMultiSamples(0)
render_window.SetSize(300, 300)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.ResetCamera()

interactor.Initialize()
interactor.Start()
