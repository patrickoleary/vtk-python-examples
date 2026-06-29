#!/usr/bin/env python

# Write and read XML image data in ASCII, appended, and binary modes, then render contours.

import os
import tempfile

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonDataModel import vtkImageData
from vtkmodules.vtkFiltersCore import vtkContourFilter
from vtkmodules.vtkIOImage import vtkImageReader
from vtkmodules.vtkIOXML import (
    vtkXMLImageDataReader,
    vtkXMLImageDataWriter,
)
from vtkmodules.vtkImagingCore import vtkExtractVOI
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
file_0 = os.path.join(temp_dir, "idFile0.vti")
file_1 = os.path.join(temp_dir, "idFile1.vti")
file_2 = os.path.join(temp_dir, "idFile2.vti")

# Read image data
image_reader = vtkImageReader()
image_reader.SetDataByteOrderToLittleEndian()
image_reader.SetDataExtent(0, 63, 0, 63, 1, 93)
image_reader.SetDataSpacing(3.2, 3.2, 1.5)
image_reader.SetFilePrefix(os.path.join(data_dir, "headsq", "quarter"))
image_reader.Update()

# Add direction matrix
direction = [1, 0, 0, 0, -1, 0, 0, 0, -1]
image = image_reader.GetOutput()
image.SetDirectionMatrix(direction)

# Extract a sub-volume
extract = vtkExtractVOI()
extract.SetInputData(image)
extract.SetVOI(0, 63, 0, 63, 0, 45)
extract.Update()

# Write in ASCII mode (extracted piece)
id_writer = vtkXMLImageDataWriter()
id_writer.SetFileName(file_0)
id_writer.SetDataModeToAscii()
id_writer.SetInputData(extract.GetOutput())
id_writer.Write()

# Write in appended mode (whole image, 2 pieces)
id_writer.SetFileName(file_1)
id_writer.SetDataModeToAppended()
id_writer.SetInputData(image)
id_writer.SetNumberOfPieces(2)
id_writer.Write()

# Write in binary mode (partial extent)
id_writer.SetFileName(file_2)
id_writer.SetDataModeToBinary()
id_writer.SetWriteExtent(1, 31, 4, 63, 12, 92)
id_writer.Write()

# Read the extracted grid
reader = vtkXMLImageDataReader()
reader.SetFileName(file_0)
reader.WholeSlicesOff()
reader.Update()

id_0 = vtkImageData()
id_0.DeepCopy(reader.GetOutput())
contour_0 = vtkContourFilter()
contour_0.SetInputData(id_0)
contour_0.SetValue(0, 500)

mapper_0 = vtkPolyDataMapper()
mapper_0.SetInputConnection(contour_0.GetOutputPort())
mapper_0.ScalarVisibilityOff()

actor_0 = vtkActor()
actor_0.SetMapper(mapper_0)
actor_0.SetPosition(180, -60, 0)

# Read the whole image (verify direction matrix)
reader.SetFileName(file_1)
reader.WholeSlicesOn()
reader.Update()

read_direction = reader.GetOutput().GetDirectionMatrix()
for i in range(3):
    for j in range(3):
        assert read_direction.GetElement(i, j) == direction[i * 3 + j]

id_1 = vtkImageData()
id_1.DeepCopy(reader.GetOutput())
contour_1 = vtkContourFilter()
contour_1.SetInputData(id_1)
contour_1.SetValue(0, 500)

mapper_1 = vtkPolyDataMapper()
mapper_1.SetInputConnection(contour_1.GetOutputPort())
mapper_1.ScalarVisibilityOff()

actor_1 = vtkActor()
actor_1.SetMapper(mapper_1)
actor_1.SetOrientation(90, 0, 0)

# Read the partially written image
reader.SetFileName(file_2)
reader.Update()

contour_2 = vtkContourFilter()
contour_2.SetInputConnection(reader.GetOutputPort())
contour_2.SetValue(0, 500)

mapper_2 = vtkPolyDataMapper()
mapper_2.SetInputConnection(contour_2.GetOutputPort())
mapper_2.ScalarVisibilityOff()

actor_2 = vtkActor()
actor_2.SetMapper(mapper_2)
actor_2.SetOrientation(0, -90, 0)
actor_2.SetPosition(180, -30, 0)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(actor_0)
renderer.AddActor(actor_1)
renderer.AddActor(actor_2)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("xml imagedata")
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
