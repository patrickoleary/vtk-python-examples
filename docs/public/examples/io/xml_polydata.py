#!/usr/bin/env python

# Write and read XML polydata in ASCII, appended, and binary modes, then render.

import os
import tempfile

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonDataModel import vtkPolyData
from vtkmodules.vtkFiltersParallel import vtkExtractPolyDataPiece
from vtkmodules.vtkIOLegacy import vtkPolyDataReader
from vtkmodules.vtkIOXML import (
    vtkXMLPolyDataReader,
    vtkXMLPolyDataWriter,
)
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Data and temp paths
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))
temp_dir = tempfile.mkdtemp()
file_0 = os.path.join(temp_dir, "idFile0.vtp")
file_1 = os.path.join(temp_dir, "idFile1.vtp")
file_2 = os.path.join(temp_dir, "idFile2.vtp")

# Read poly data
pd_reader = vtkPolyDataReader()
pd_reader.SetFileName(os.path.join(data_dir, "fran_cut.vtk"))
pd_reader.Update()

extract = vtkExtractPolyDataPiece()
extract.SetInputConnection(pd_reader.GetOutputPort())

# Write in ASCII mode
pd_writer = vtkXMLPolyDataWriter()
pd_writer.SetFileName(file_0)
pd_writer.SetDataModeToAscii()
pd_writer.SetInputConnection(pd_reader.GetOutputPort())
pd_writer.Write()

# Write in appended mode (2 pieces)
pd_writer.SetFileName(file_1)
pd_writer.SetInputConnection(extract.GetOutputPort())
pd_writer.SetDataModeToAppended()
pd_writer.SetNumberOfPieces(2)
pd_writer.Write()

# Write in binary mode (with ghost level)
pd_writer.SetFileName(file_2)
pd_writer.SetDataModeToBinary()
pd_writer.SetGhostLevel(3)
pd_writer.Write()

# Read the ASCII version
reader = vtkXMLPolyDataReader()
reader.SetFileName(file_0)
reader.Update()

pd_0 = vtkPolyData()
pd_0.DeepCopy(reader.GetOutput())
mapper_0 = vtkPolyDataMapper()
mapper_0.SetInputData(pd_0)

actor_0 = vtkActor()
actor_0.SetMapper(mapper_0)
actor_0.SetPosition(0, 0.15, 0)

# Read appended piece 0
reader.SetFileName(file_1)

mapper_1 = vtkPolyDataMapper()
mapper_1.SetInputConnection(reader.GetOutputPort())
mapper_1.SetPiece(0)
mapper_1.SetNumberOfPieces(2)

actor_1 = vtkActor()
actor_1.SetMapper(mapper_1)

# Read binary piece 0 (with ghost level)
reader_2 = vtkXMLPolyDataReader()
reader_2.SetFileName(file_2)

mapper_2 = vtkPolyDataMapper()
mapper_2.SetInputConnection(reader_2.GetOutputPort())
mapper_2.SetPiece(0)
mapper_2.SetNumberOfPieces(2)

actor_2 = vtkActor()
actor_2.SetMapper(mapper_2)
actor_2.SetPosition(0, 0, 0.1)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(actor_0)
renderer.AddActor(actor_1)
renderer.AddActor(actor_2)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("xml polydata")
render_window.SetMultiSamples(0)
render_window.SetSize(300, 300)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.GetActiveCamera().SetPosition(0.514096, -0.14323, -0.441177)
renderer.GetActiveCamera().SetFocalPoint(0.0528, -0.0780001, -0.0379661)

interactor.Initialize()
interactor.Start()

# Clean up
for f in [file_0, file_1, file_2]:
    os.remove(f)
os.rmdir(temp_dir)
