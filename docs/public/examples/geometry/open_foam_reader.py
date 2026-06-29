#!/usr/bin/env python

# Read an OpenFOAM case and render pressure field.

import os

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkIOGeometry import vtkOpenFOAMReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkDataSetMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Source
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Read OpenFOAM case
foam_reader = vtkOpenFOAMReader()
foam_reader.SetFileName(os.path.join(data_dir, "OpenFOAM", "cavity", "cavity.foam"))
foam_reader.Update()
foam_reader.SetTimeValue(0.5)
foam_reader.ReadZonesOn()
foam_reader.Update()

# Get the internal mesh block
block_0 = foam_reader.GetOutput().GetBlock(0)
block_0.GetCellData().SetActiveScalars("p")

# Mapper
dataset_mapper = vtkDataSetMapper()
dataset_mapper.SetInputData(block_0)
dataset_mapper.SetScalarRange(block_0.GetScalarRange())

# Actor
foam_actor = vtkActor()
foam_actor.SetMapper(dataset_mapper)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(foam_actor)
renderer.SetBackground(0.2, 0.4, 0.6)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("open foam reader")
render_window.SetMultiSamples(0)
render_window.SetSize(300, 300)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.ResetCamera()

interactor.Initialize()
interactor.Start()
