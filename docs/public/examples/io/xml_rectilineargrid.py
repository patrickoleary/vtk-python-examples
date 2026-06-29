#!/usr/bin/env python

# Write and read XML rectilinear grid in ASCII, appended, and binary modes, then render.

import os
import tempfile

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonDataModel import vtkRectilinearGrid
from vtkmodules.vtkFiltersExtraction import vtkExtractRectilinearGrid
from vtkmodules.vtkIOLegacy import vtkRectilinearGridReader
from vtkmodules.vtkIOXML import (
    vtkXMLRectilinearGridReader,
    vtkXMLRectilinearGridWriter,
)
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkDataSetMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Data and temp paths
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))
temp_dir = tempfile.mkdtemp()
file_0 = os.path.join(temp_dir, "rgFile0.vtr")
file_1 = os.path.join(temp_dir, "rgFile1.vtr")
file_2 = os.path.join(temp_dir, "rgFile2.vtr")

# Read rectilinear grid data
grid_reader = vtkRectilinearGridReader()
grid_reader.SetFileName(os.path.join(data_dir, "RectGrid2.vtk"))
grid_reader.Update()

# Extract to reduce extents
extract = vtkExtractRectilinearGrid()
extract.SetInputConnection(grid_reader.GetOutputPort())
extract.SetVOI(0, 23, 0, 32, 0, 10)
extract.Update()

# Write in ASCII mode (extracted piece)
rg_writer = vtkXMLRectilinearGridWriter()
rg_writer.SetFileName(file_0)
rg_writer.SetInputConnection(extract.GetOutputPort())
rg_writer.SetDataModeToAscii()
rg_writer.Write()

# Write in appended mode (whole grid, 2 pieces)
rg_writer.SetFileName(file_1)
rg_writer.SetInputConnection(grid_reader.GetOutputPort())
rg_writer.SetDataModeToAppended()
rg_writer.SetNumberOfPieces(2)
rg_writer.Write()

# Write in binary mode (partial extent, no compressor)
rg_writer.SetFileName(file_2)
rg_writer.SetDataModeToBinary()
rg_writer.SetWriteExtent(3, 46, 6, 32, 1, 5)
rg_writer.SetCompressor(None)
if rg_writer.GetByteOrder():
    rg_writer.SetByteOrder(0)
else:
    rg_writer.SetByteOrder(1)
rg_writer.Write()

# Read the extracted grid
reader = vtkXMLRectilinearGridReader()
reader.SetFileName(file_0)
reader.WholeSlicesOff()
reader.Update()

rg_0 = vtkRectilinearGrid()
rg_0.DeepCopy(reader.GetOutput())
mapper_0 = vtkDataSetMapper()
mapper_0.SetInputData(rg_0)

actor_0 = vtkActor()
actor_0.SetMapper(mapper_0)

# Read the whole grid
reader.SetFileName(file_1)
reader.WholeSlicesOn()
reader.Update()

rg_1 = vtkRectilinearGrid()
rg_1.DeepCopy(reader.GetOutput())
mapper_1 = vtkDataSetMapper()
mapper_1.SetInputData(rg_1)

actor_1 = vtkActor()
actor_1.SetMapper(mapper_1)
actor_1.SetPosition(-1.5, 3, 0)

# Read the partially written grid
reader.SetFileName(file_2)
reader.Update()

mapper_2 = vtkDataSetMapper()
mapper_2.SetInputConnection(reader.GetOutputPort())

actor_2 = vtkActor()
actor_2.SetMapper(mapper_2)
actor_2.SetPosition(1.5, 3, 0)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(actor_0)
renderer.AddActor(actor_1)
renderer.AddActor(actor_2)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("xml rectilineargrid")
render_window.SetMultiSamples(0)
render_window.SetSize(300, 300)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()

# Clean up
for f in [file_0, file_1, file_2]:
    os.remove(f)
os.rmdir(temp_dir)
