#!/usr/bin/env python

# Read an Exodus file, write it back out, re-read, and render the first block.

import os
import tempfile

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkIOExodus import vtkExodusIIReader, vtkExodusIIWriter
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkDataSetMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Source
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))
temp_dir = tempfile.mkdtemp()

# Read the Exodus file
exodus_reader = vtkExodusIIReader()
exodus_reader.SetFileName(os.path.join(data_dir, "edgeFaceElem.exii"))
exodus_reader.SetGlobalResultArrayStatus("CALIBER", 1)
exodus_reader.SetGlobalResultArrayStatus("GUNPOWDER", 1)
exodus_reader.Update()

# Write the data back out
output_file = os.path.join(temp_dir, "testExodus.exii")
exodus_writer = vtkExodusIIWriter()
exodus_writer.SetInputConnection(exodus_reader.GetOutputPort())
exodus_writer.SetFileName(output_file)
exodus_writer.WriteOutBlockIdArrayOn()
exodus_writer.WriteOutGlobalNodeIdArrayOn()
exodus_writer.WriteOutGlobalElementIdArrayOn()
exodus_writer.WriteAllTimeStepsOn()
exodus_writer.Update()

# Re-read the written file
exodus_output_reader = vtkExodusIIReader()
exodus_output_reader.SetFileName(output_file)
exodus_output_reader.SetGlobalResultArrayStatus("CALIBER", 1)
exodus_output_reader.SetGlobalResultArrayStatus("GUNPOWDER", 1)
exodus_output_reader.Update()

# Get the first dataset from the output
multi_block = exodus_output_reader.GetOutput()
iterator = multi_block.NewIterator()
iterator.InitTraversal()
dataset = iterator.GetCurrentDataObject()

# Mapper
dataset_mapper = vtkDataSetMapper()
dataset_mapper.SetInputData(dataset)

# Actor
exodus_actor = vtkActor()
exodus_actor.SetMapper(dataset_mapper)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(exodus_actor)
renderer.SetBackground(0.0, 0.0, 0.0)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("multiblock exodus write")
render_window.SetMultiSamples(0)
render_window.SetSize(256, 256)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
camera = renderer.GetActiveCamera()
camera.SetPosition(0.0, 10.0, 14.5)
camera.SetFocalPoint(0, 0, 0)
camera.SetViewUp(0.8, 0.3, -0.5)
camera.SetViewAngle(30)

interactor.Initialize()
interactor.Start()
