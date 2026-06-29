#!/usr/bin/env python

# Demonstrate vtkMemoryLimitImageDataStreamer by reading head MRI slices,
# mapping scalars to RGBA colors via a lookup table with cycling hue
# range, streaming with a memory limit, and displaying a 2D slice using
# a standard rendering pipeline with parallel projection.

import os

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import vtkLookupTable
from vtkmodules.vtkFiltersParallelImaging import vtkMemoryLimitImageDataStreamer
from vtkmodules.vtkIOImage import vtkImageReader
from vtkmodules.vtkImagingCore import vtkImageMapToColors
from vtkmodules.vtkRenderingCore import (
    vtkActor2D,
    vtkImageMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Read head MRI slices
reader = vtkImageReader()
reader.ReleaseDataFlagOff()
reader.SetDataByteOrderToLittleEndian()
reader.SetDataExtent(0, 63, 0, 63, 1, 93)
reader.SetFilePrefix(os.path.join(data_dir, "headsq", "quarter"))
reader.SetDataMask(0x7fff)

# Lookup table with cycling hue range
range_start = 0.0
range_end = 0.2

lookup_table = vtkLookupTable()
lookup_table.SetTableRange(0, 1800)
lookup_table.SetSaturationRange(1, 1)
lookup_table.SetHueRange(range_start, range_end)
lookup_table.SetValueRange(1, 1)
lookup_table.SetAlphaRange(1, 1)
lookup_table.Build()

# Map scalars to RGBA colors
map_to_rgba = vtkImageMapToColors()
map_to_rgba.SetInputConnection(reader.GetOutputPort())
map_to_rgba.SetOutputFormatToRGBA()
map_to_rgba.SetLookupTable(lookup_table)

# Stream with memory limit
streamer = vtkMemoryLimitImageDataStreamer()
streamer.SetInputConnection(map_to_rgba.GetOutputPort())
streamer.SetMemoryLimit(100)
streamer.UpdateWholeExtent()

# Display a 2D slice using standard pipeline with parallel projection
image_mapper = vtkImageMapper()
image_mapper.SetInputConnection(streamer.GetOutputPort())
image_mapper.SetColorWindow(255.0)
image_mapper.SetColorLevel(127.5)
image_mapper.SetZSlice(50)

actor = vtkActor2D()
actor.SetMapper(image_mapper)

# Renderer
renderer = vtkRenderer()
renderer.AddViewProp(actor)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(300, 300)
render_window.SetWindowName("image streamer")

# Scene
renderer.GetActiveCamera().ParallelProjectionOn()

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
