#!/usr/bin/env python
# Demonstrate a 2D histogram chart colored by magnitude of a vector array.

import math

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingContextOpenGL2  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkChartsCore import vtkChartHistogram2D, vtkPlotHistogram2D
from vtkmodules.vtkCommonCore import vtkDoubleArray
from vtkmodules.vtkCommonDataModel import vtkImageData
from vtkmodules.vtkRenderingContext2D import vtkContextActor
from vtkmodules.vtkRenderingCore import (
    vtkColorTransferFunction,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

EXTENT = 200
SIZE = 2 * EXTENT + 1
ARRAY_NAME = "swirl"

# Create image data.
data = vtkImageData()
data.SetExtent(-EXTENT, EXTENT, -EXTENT, EXTENT, 0, 0)

nb_points = data.GetNumberOfPoints()
dims = data.GetDimensions()

# Compute swirl array.
array = vtkDoubleArray()
array.SetName(ARRAY_NAME)
array.SetNumberOfComponents(3)
array.SetNumberOfTuples(nb_points)
for i in range(nb_points):
    ijk = [0, 0, 0]
    ijk[0] = i % dims[0]
    ijk[1] = (i // dims[0]) % dims[1]
    ijk[2] = i // (dims[0] * dims[1])
    array.SetTuple3(i, ijk[0] - EXTENT, ijk[1] - EXTENT, ijk[2])

data.GetPointData().AddArray(array)

# Set up the chart.
chart = vtkChartHistogram2D()
chart.SetInputData(data)

plot = vtkPlotHistogram2D.SafeDownCast(chart.GetPlot(0))
plot.SetArrayName(ARRAY_NAME)

# Set a transfer function for coloring by magnitude.
value_max = math.sqrt(2.0) * EXTENT
half_value_max = value_max / 2.0

transfer_function = vtkColorTransferFunction()
transfer_function.AddRGBSegment(0, 1.0, 0.0, 0.0, half_value_max, 0.0, 1.0, 0.0)
transfer_function.AddRGBSegment(half_value_max, 0.0, 1.0, 0.0, value_max, 0.0, 0.0, 1.0)
transfer_function.Build()
transfer_function.SetVectorModeToMagnitude()

chart.SetTransferFunction(transfer_function)
chart.RecalculateBounds()

# Context actor and scene wiring.
context_actor = vtkContextActor()
context_actor.GetScene().AddItem(chart)

# Renderer
renderer = vtkRenderer()
renderer.SetBackground(1.0, 1.0, 1.0)
context_actor.GetScene().SetRenderer(renderer)
renderer.AddActor(context_actor)

# Window
render_window = vtkRenderWindow()
render_window.SetSize(SIZE, SIZE)
render_window.SetMultiSamples(0)
render_window.AddRenderer(renderer)
render_window.SetWindowName("histogram2d magnitude")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
