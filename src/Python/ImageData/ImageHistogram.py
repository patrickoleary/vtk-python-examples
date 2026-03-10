#!/usr/bin/env python

# Compute and display a histogram of scalar values from a 3D medical
# volume (FullHead.mhd).  The left viewport shows the middle axial slice
# colored with a discrete lookup table derived from histogram bins.
# The right viewport shows the histogram as a bar chart using
# vtkChartXY / vtkPlotBar rendered through vtkContextActor.

import os
from pathlib import Path

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingContextOpenGL2  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkChartsCore import vtkChartXY
from vtkmodules.vtkCommonCore import vtkFloatArray, vtkIntArray, vtkLookupTable
from vtkmodules.vtkCommonDataModel import vtkTable
from vtkmodules.vtkIOImage import vtkMetaImageReader
from vtkmodules.vtkImagingCore import vtkImageMapToColors
from vtkmodules.vtkImagingStatistics import vtkImageAccumulate
from vtkmodules.vtkRenderingContext2D import vtkContextActor
from vtkmodules.vtkRenderingCore import (
    vtkColorTransferFunction,
    vtkImageActor,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
black_rgb = (0.0, 0.0, 0.0)
white_rgb = (1.0, 1.0, 1.0)

# Data directory: defaults to the folder containing this script
data_dir = Path(os.environ.get("VPE_DATA_DIR", Path(__file__).parent))

# Reader: load the 3D medical volume
reader = vtkMetaImageReader()
reader.SetFileName(str(data_dir / "FullHead.mhd"))
reader.Update()

# Histogram: compute scalar distribution with 256 bins
num_bins = 256
histogram = vtkImageAccumulate()
histogram.SetInputConnection(reader.GetOutputPort())
histogram.SetComponentExtent(0, num_bins - 1, 0, 0, 0, 0)
histogram.SetComponentOrigin(0, 0, 0)
histogram.SetComponentSpacing(1, 1, 1)
histogram.Update()

# Extract bin counts into arrays for the chart
bin_values = vtkFloatArray()
bin_values.SetName("Scalar Value")
bin_values.SetNumberOfTuples(num_bins)

count_values = vtkIntArray()
count_values.SetName("Frequency")
count_values.SetNumberOfTuples(num_bins)

hist_output = histogram.GetOutput()
for i in range(num_bins):
    bin_values.SetValue(i, float(i))
    count_values.SetValue(i, int(hist_output.GetScalarComponentAsDouble(i, 0, 0, 0)))

# Table: assemble the histogram data for the chart
table = vtkTable()
table.AddColumn(bin_values)
table.AddColumn(count_values)

# Lookup table: build a discrete colormap from cool-to-warm
ctf = vtkColorTransferFunction()
ctf.SetColorSpaceToDiverging()
ctf.AddRGBPoint(0.0, 0.230, 0.299, 0.754)
ctf.AddRGBPoint(128.0, 0.865, 0.865, 0.865)
ctf.AddRGBPoint(255.0, 0.706, 0.016, 0.150)

lut = vtkLookupTable()
lut.SetNumberOfTableValues(num_bins)
lut.SetRange(0, num_bins - 1)
for i in range(num_bins):
    rgb = ctf.GetColor(float(i))
    lut.SetTableValue(i, rgb[0], rgb[1], rgb[2], 1.0)
lut.Build()

# Map: apply the discrete colormap to the volume slice
map_to_colors = vtkImageMapToColors()
map_to_colors.SetInputConnection(reader.GetOutputPort())
map_to_colors.SetLookupTable(lut)
map_to_colors.SetOutputFormatToRGB()

# Display the middle axial slice
extent = reader.GetOutput().GetExtent()
mid_z = (extent[4] + extent[5]) // 2

# Actor: display the colormapped slice in the left viewport
slice_actor = vtkImageActor()
slice_actor.GetMapper().SetInputConnection(map_to_colors.GetOutputPort())
slice_actor.SetDisplayExtent(extent[0], extent[1], extent[2], extent[3],
                             mid_z, mid_z)

# Renderer 1: left viewport — colormapped slice
renderer_left = vtkRenderer()
renderer_left.AddActor(slice_actor)
renderer_left.SetViewport(0.0, 0.0, 0.5, 1.0)
renderer_left.SetBackground(black_rgb)
renderer_left.ResetCamera()

# Chart: build a bar chart of the histogram
chart = vtkChartXY()
chart.SetTitle("Scalar Histogram")
chart.GetAxis(0).SetTitle("Frequency")
chart.GetAxis(1).SetTitle("Scalar Value")

plot = chart.AddPlot(0)
plot.SetInputData(table, 0, 1)
plot.SetColor(70, 130, 180, 255)

# Context actor: host the chart in a standard renderer
context_actor = vtkContextActor()
context_actor.GetScene().AddItem(chart)

# Renderer 2: right viewport — histogram chart
renderer_right = vtkRenderer()
renderer_right.AddActor(context_actor)
renderer_right.SetViewport(0.5, 0.0, 1.0, 1.0)
renderer_right.SetBackground(white_rgb)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer_left)
render_window.AddRenderer(renderer_right)
render_window.SetSize(1200, 500)
render_window.SetWindowName("ImageHistogram")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
