#!/usr/bin/env python

# Test JSON image writer by writing a slice of analytic source, verifying contents, and rendering the source volume.

import json
import os
import tempfile

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
import vtkmodules.vtkRenderingVolumeOpenGL2  # noqa: F401

from vtkmodules.vtkIOImage import vtkJSONImageWriter
from vtkmodules.vtkImagingCore import vtkRTAnalyticSource
from vtkmodules.vtkRenderingCore import (
    vtkColorTransferFunction,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
    vtkVolume,
    vtkVolumeProperty,
)
from vtkmodules.vtkRenderingVolume import vtkGPUVolumeRayCastMapper
from vtkmodules.vtkCommonDataModel import vtkPiecewiseFunction

# Generate analytic image data
analytic_source = vtkRTAnalyticSource()
analytic_source.Update()
output = analytic_source.GetOutput()
dim_ref = list(output.GetDimensions())
origin_ref = list(output.GetOrigin())
spacing_ref = list(output.GetSpacing())

# Write a slice as JSON
temp_dir = tempfile.mkdtemp()
tmp_file = os.path.join(temp_dir, "wavelet_slice_3.json")

json_writer = vtkJSONImageWriter()
json_writer.SetInputData(analytic_source.GetOutput())
json_writer.SetFileName(tmp_file)
json_writer.SetArrayName("RTData")
json_writer.SetSlice(3)
json_writer.Write()

# Verify JSON contents
with open(tmp_file, "r") as f:
    json_obj = json.load(f)

assert json_obj["dimensions"] == dim_ref, "Dimension mismatch"
assert json_obj["origin"] == origin_ref, "Origin mismatch"
assert json_obj["spacing"] == spacing_ref, "Spacing mismatch"

slice_data = json_obj["RTData"]
assert len(slice_data) == 441, f"Slice size error: got {len(slice_data)}"

expected_first_values = [
    75.9335, 102.695, 91.2387, 115.507, 105.995, 125.724, 118.773,
    132.24, 128.255, 134.254, 133.446, 131.431, 133.843, 123.998, 129.505,
]
for i, expected in enumerate(expected_first_values):
    assert slice_data[i] == expected, f"Value mismatch at index {i}"

# Clean up
os.remove(tmp_file)
os.rmdir(temp_dir)

# Render the analytic source as a volume
scalar_range = output.GetScalarRange()

color_transfer = vtkColorTransferFunction()
color_transfer.AddRGBPoint(scalar_range[0], 0.0, 0.0, 1.0)
color_transfer.AddRGBPoint(scalar_range[1], 1.0, 0.0, 0.0)

opacity_function = vtkPiecewiseFunction()
opacity_function.AddPoint(scalar_range[0], 0.0)
opacity_function.AddPoint(scalar_range[1], 0.3)

volume_property = vtkVolumeProperty()
volume_property.SetColor(color_transfer)
volume_property.SetScalarOpacity(opacity_function)

volume_mapper = vtkGPUVolumeRayCastMapper()
volume_mapper.SetInputConnection(analytic_source.GetOutputPort())

volume = vtkVolume()
volume.SetMapper(volume_mapper)
volume.SetProperty(volume_property)

# Renderer
renderer = vtkRenderer()
renderer.AddVolume(volume)
renderer.SetBackground(0.2, 0.2, 0.3)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("json writer")
render_window.SetMultiSamples(0)
render_window.SetSize(400, 400)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.ResetCamera()

interactor.Initialize()
interactor.Start()
