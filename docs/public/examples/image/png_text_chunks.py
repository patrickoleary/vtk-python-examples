#!/usr/bin/env python

# Test PNG text chunk writing and reading, then render the source image.

import os
import tempfile

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import vtkCommand
from vtkmodules.vtkIOImage import (
    vtkPNGReader,
    vtkPNGWriter,
    vtkTIFFReader,
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
filename = os.path.join(temp_dir, "pngw1.png")

# Read a TIFF source image
image_reader = vtkTIFFReader()
image_reader.SetFileName(os.path.join(data_dir, "beach.tif"))
image_reader.SetOrientationType(4)
image_reader.Update()

test_key = "test key"
test_value = "test value"
long_key = "0123456789012345678901234567890123456789" \
           "0123456789012345678901234567890123456789"
long_key_value = "this also prints a warning"

got_warning = False

def warning_callback(obj, evt):
    global got_warning
    got_warning = True

# Write PNG with text chunks
png_writer = vtkPNGWriter()
png_writer.SetInputConnection(image_reader.GetOutputPort())
png_writer.SetFileName(filename)
png_writer.AddText(test_key, test_value)
png_writer.AddText(test_key, test_value)

# Test clearing
png_writer.ClearText()
png_writer.AddText(test_key, test_value)
png_writer.AddText(test_key, test_value)

observer_id = png_writer.AddObserver(vtkCommand.WarningEvent, warning_callback)

# Empty key should warn
png_writer.AddText("", "this prints a warning")
assert got_warning, "Expected warning for empty key"

got_warning = False

# Long key should warn
png_writer.AddText(long_key, long_key_value)
assert got_warning, "Expected warning for key longer than 79 characters"

png_writer.RemoveObserver(observer_id)
png_writer.Write()

# Read back and verify text chunks
png_reader = vtkPNGReader()
png_reader.SetFileName(filename)
png_reader.Update()

assert png_reader.GetNumberOfTextChunks() == 3, \
    f"Expected 3 text chunks, got {png_reader.GetNumberOfTextChunks()}"

begin_end = [0, 0]
png_reader.GetTextChunks(test_key, begin_end)

assert png_reader.GetTextKey(1) == test_key
assert png_reader.GetTextKey(2) == test_key
assert png_reader.GetTextValue(1) == test_value
assert png_reader.GetTextValue(2) == test_value
assert png_reader.GetTextKey(0) == long_key[:-1]

# Clean up temp files
os.remove(filename)
os.rmdir(temp_dir)

# Render the source image
image_actor = vtkImageActor()
image_actor.GetMapper().SetInputConnection(image_reader.GetOutputPort())

# Renderer
renderer = vtkRenderer()
renderer.AddActor(image_actor)
renderer.SetBackground(0.2, 0.2, 0.2)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("png text chunks")
render_window.SetMultiSamples(0)
render_window.SetSize(400, 400)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.ResetCamera()

interactor.Initialize()
interactor.Start()
