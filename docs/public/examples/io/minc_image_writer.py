#!/usr/bin/env python

# Read a MINC image, write it with various attributes, read it back, and display.

import os
import tempfile

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkIOMINC import (
    vtkMINCImageAttributes,
    vtkMINCImageReader,
    vtkMINCImageWriter,
)
from vtkmodules.vtkRenderingCore import (
    vtkImageActor,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Source
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))
temp_dir = tempfile.mkdtemp()

# Read the MINC image
minc_reader = vtkMINCImageReader()
minc_reader.SetFileName(os.path.join(data_dir, "t3_grid_0.mnc"))
minc_reader.RescaleRealValuesOn()

# Write with default attributes
minc_1_file = os.path.join(temp_dir, "minc1.mnc")
minc_writer_1 = vtkMINCImageWriter()
minc_writer_1.SetInputConnection(minc_reader.GetOutputPort())
minc_writer_1.SetFileName(minc_1_file)

# Write with modified attributes
image_attributes = vtkMINCImageAttributes()
image_attributes.ShallowCopy(minc_reader.GetImageAttributes())
image_attributes.SetAttributeValueAsString("patient", "full_name", "DOE^JOHN DAVID")

minc_2_file = os.path.join(temp_dir, "minc2.mnc")
minc_writer_2 = vtkMINCImageWriter()
minc_writer_2.SetImageAttributes(image_attributes)
minc_writer_2.SetInputConnection(minc_reader.GetOutputPort())
minc_writer_2.SetFileName(minc_2_file)

# Write with two input connections (multi-frame)
minc_3_file = os.path.join(temp_dir, "minc3.mnc")
minc_writer_3 = vtkMINCImageWriter()
minc_writer_3.SetImageAttributes(image_attributes)
minc_writer_3.AddInputConnection(minc_reader.GetOutputPort())
minc_writer_3.AddInputConnection(minc_reader.GetOutputPort())
minc_writer_3.SetFileName(minc_3_file)

minc_writer_1.Write()
minc_writer_2.Write()
minc_writer_3.Write()

# Read back the multi-frame file
minc_reader_2 = vtkMINCImageReader()
minc_reader_2.SetFileName(minc_3_file)
minc_reader_2.RescaleRealValuesOn()
minc_reader_2.SetTimeStep(1)
minc_reader_2.Update()

# Display with standard rendering pipeline
image_actor = vtkImageActor()
image_actor.GetMapper().SetInputConnection(minc_reader_2.GetOutputPort())

# Set window/level from actual data range so image is visible
scalar_range = minc_reader_2.GetOutput().GetScalarRange()
image_actor.GetProperty().SetColorWindow(scalar_range[1] - scalar_range[0])
image_actor.GetProperty().SetColorLevel((scalar_range[0] + scalar_range[1]) / 2.0)

renderer = vtkRenderer()
renderer.AddActor(image_actor)
renderer.SetBackground(0.2, 0.3, 0.4)

render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("minc image writer")
render_window.SetMultiSamples(0)
render_window.SetSize(300, 300)

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.GetActiveCamera().ParallelProjectionOn()
renderer.ResetCamera()

interactor.Initialize()
interactor.Start()

# Clean up temp files
for f in [minc_1_file, minc_2_file, minc_3_file]:
    if os.path.exists(f):
        os.remove(f)
os.rmdir(temp_dir)
