#!/usr/bin/env python

# Write and read XML structured grid in ASCII, appended, and binary modes, then render contours.

import os
import tempfile

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonDataModel import vtkStructuredGrid
from vtkmodules.vtkFiltersCore import vtkContourFilter
from vtkmodules.vtkFiltersExtraction import vtkExtractGrid
from vtkmodules.vtkIOParallel import vtkMultiBlockPLOT3DReader
from vtkmodules.vtkIOXML import (
    vtkXMLStructuredGridReader,
    vtkXMLStructuredGridWriter,
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
file_0 = os.path.join(temp_dir, "sgFile0.vts")
file_1 = os.path.join(temp_dir, "sgFile1.vts")
file_2 = os.path.join(temp_dir, "sgFile2.vts")

# Read PLOT3D data
comb_reader = vtkMultiBlockPLOT3DReader()
comb_reader.SetXYZFileName(os.path.join(data_dir, "combxyz.bin"))
comb_reader.SetQFileName(os.path.join(data_dir, "combq.bin"))
comb_reader.SetScalarFunctionNumber(100)
comb_reader.Update()
output = comb_reader.GetOutput().GetBlock(0)

# Extract to reduce extents
extract = vtkExtractGrid()
extract.SetInputData(output)
extract.SetVOI(0, 28, 0, 32, 0, 24)
extract.Update()

# Write in ASCII mode (extracted piece)
grid_writer = vtkXMLStructuredGridWriter()
grid_writer.SetFileName(file_0)
grid_writer.SetInputConnection(extract.GetOutputPort())
grid_writer.SetDataModeToAscii()
grid_writer.Write()

# Write in appended mode (whole grid, 2 pieces)
grid_writer.SetInputData(output)
grid_writer.SetFileName(file_1)
grid_writer.SetDataModeToAppended()
grid_writer.SetNumberOfPieces(2)
grid_writer.Write()

# Write in binary mode (partial extent)
grid_writer.SetFileName(file_2)
grid_writer.SetDataModeToBinary()
grid_writer.SetWriteExtent(8, 56, 4, 16, 1, 24)
grid_writer.Write()

# Read the extracted grid
reader = vtkXMLStructuredGridReader()
reader.SetFileName(file_0)
reader.WholeSlicesOff()
reader.Update()

sg_0 = vtkStructuredGrid()
sg_0.DeepCopy(reader.GetOutput())
contour_0 = vtkContourFilter()
contour_0.SetInputData(sg_0)
contour_0.SetValue(0, 0.38)

mapper_0 = vtkPolyDataMapper()
mapper_0.SetInputConnection(contour_0.GetOutputPort())
mapper_0.ScalarVisibilityOff()

actor_0 = vtkActor()
actor_0.SetMapper(mapper_0)

# Read the whole grid
reader.SetFileName(file_1)
reader.WholeSlicesOn()
reader.Update()

sg_1 = vtkStructuredGrid()
sg_1.DeepCopy(reader.GetOutput())
contour_1 = vtkContourFilter()
contour_1.SetInputData(sg_1)
contour_1.SetValue(0, 0.38)

mapper_1 = vtkPolyDataMapper()
mapper_1.SetInputConnection(contour_1.GetOutputPort())
mapper_1.ScalarVisibilityOff()

actor_1 = vtkActor()
actor_1.SetMapper(mapper_1)
actor_1.SetPosition(0, -10, 0)

# Read the partially written grid
reader.SetFileName(file_2)
reader.Update()

contour_2 = vtkContourFilter()
contour_2.SetInputConnection(reader.GetOutputPort())
contour_2.SetValue(0, 0.38)

mapper_2 = vtkPolyDataMapper()
mapper_2.SetInputConnection(contour_2.GetOutputPort())
mapper_2.ScalarVisibilityOff()

actor_2 = vtkActor()
actor_2.SetMapper(mapper_2)
actor_2.SetPosition(0, 10, 0)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(actor_0)
renderer.AddActor(actor_1)
renderer.AddActor(actor_2)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("xml structuredgrid")
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
