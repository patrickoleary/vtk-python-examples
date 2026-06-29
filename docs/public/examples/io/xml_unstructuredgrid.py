#!/usr/bin/env python

# Write and read XML unstructured grid in ASCII, appended, and binary modes, then render.

import os
import tempfile

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonDataModel import vtkUnstructuredGrid
from vtkmodules.vtkFiltersGeometry import vtkDataSetSurfaceFilter
from vtkmodules.vtkFiltersParallel import vtkExtractUnstructuredGridPiece
from vtkmodules.vtkIOLegacy import vtkUnstructuredGridReader
from vtkmodules.vtkIOXML import (
    vtkXMLUnstructuredGridReader,
    vtkXMLUnstructuredGridWriter,
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
file_0 = os.path.join(temp_dir, "ugFile0.vtu")
file_1 = os.path.join(temp_dir, "ugFile1.vtu")
file_2 = os.path.join(temp_dir, "ugFile2.vtu")

# Read unstructured grid data
ug_reader = vtkUnstructuredGridReader()
ug_reader.SetFileName(os.path.join(data_dir, "blow.vtk"))
ug_reader.SetScalarsName("thickness9")
ug_reader.SetVectorsName("displacement9")

extract = vtkExtractUnstructuredGridPiece()
extract.SetInputConnection(ug_reader.GetOutputPort())

# Write in ASCII mode
ug_writer = vtkXMLUnstructuredGridWriter()
ug_writer.SetFileName(file_0)
ug_writer.SetDataModeToAscii()
ug_writer.SetInputConnection(ug_reader.GetOutputPort())
ug_writer.Write()

# Write in appended mode (2 pieces)
ug_writer.SetFileName(file_1)
ug_writer.SetInputConnection(extract.GetOutputPort())
ug_writer.SetDataModeToAppended()
ug_writer.SetNumberOfPieces(2)
ug_writer.Write()

# Write in binary mode (with ghost level)
ug_writer.SetFileName(file_2)
ug_writer.SetDataModeToBinary()
ug_writer.SetGhostLevel(2)
ug_writer.Write()

# Read the ASCII version
reader = vtkXMLUnstructuredGridReader()
reader.SetFileName(file_0)
reader.Update()

ug_0 = vtkUnstructuredGrid()
ug_0.DeepCopy(reader.GetOutput())
surface_0 = vtkDataSetSurfaceFilter()
surface_0.SetInputData(ug_0)

mapper_0 = vtkPolyDataMapper()
mapper_0.SetInputConnection(surface_0.GetOutputPort())

actor_0 = vtkActor()
actor_0.SetMapper(mapper_0)
actor_0.SetPosition(0, 40, 20)

# Read appended piece 1
reader.SetFileName(file_1)

surface_1 = vtkDataSetSurfaceFilter()
surface_1.SetInputConnection(reader.GetOutputPort())

mapper_1 = vtkPolyDataMapper()
mapper_1.SetInputConnection(surface_1.GetOutputPort())
mapper_1.SetPiece(1)
mapper_1.SetNumberOfPieces(2)

actor_1 = vtkActor()
actor_1.SetMapper(mapper_1)

# Read binary piece 1 (with ghost level)
reader_2 = vtkXMLUnstructuredGridReader()
reader_2.SetFileName(file_2)

surface_2 = vtkDataSetSurfaceFilter()
surface_2.SetInputConnection(reader_2.GetOutputPort())

mapper_2 = vtkPolyDataMapper()
mapper_2.SetInputConnection(surface_2.GetOutputPort())
mapper_2.SetPiece(1)
mapper_2.SetNumberOfPieces(2)
mapper_2.SetGhostLevel(2)

actor_2 = vtkActor()
actor_2.SetMapper(mapper_2)
actor_2.SetPosition(0, 0, 30)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(actor_0)
renderer.AddActor(actor_1)
renderer.AddActor(actor_2)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("xml unstructuredgrid")
render_window.SetMultiSamples(0)
render_window.SetSize(300, 300)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.ResetCamera()
renderer.GetActiveCamera().SetPosition(180, 55, 65)
renderer.GetActiveCamera().SetFocalPoint(3.5, 32, 15)

interactor.Initialize()
interactor.Start()

# Clean up
for f in [file_0, file_1, file_2]:
    os.remove(f)
os.rmdir(temp_dir)
