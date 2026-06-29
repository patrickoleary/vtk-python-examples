#!/usr/bin/env python
# Demonstrate a box plot with Michelson-Morley experiment data using vtkComputeQuartiles.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingContextOpenGL2  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkChartsCore import vtkChartBox, vtkPlotBox
from vtkmodules.vtkCommonCore import vtkIntArray, vtkLookupTable, vtkStringArray
from vtkmodules.vtkCommonDataModel import vtkTable
from vtkmodules.vtkFiltersStatistics import vtkComputeQuartiles
from vtkmodules.vtkRenderingContext2D import vtkContextActor
from vtkmodules.vtkRenderingCore import (
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Michelson-Morley experiment data.
values = [
    [850, 960, 880, 890, 890],
    [740, 940, 880, 810, 840],
    [900, 960, 880, 810, 780],
    [1070, 940, 860, 820, 810],
    [930, 880, 720, 800, 760],
    [850, 800, 720, 770, 810],
    [950, 850, 620, 760, 790],
    [980, 880, 860, 740, 810],
    [980, 900, 970, 750, 820],
    [880, 840, 950, 760, 850],
    [1000, 830, 880, 910, 870],
    [980, 790, 910, 920, 870],
    [930, 810, 850, 890, 810],
    [650, 880, 870, 860, 740],
    [760, 880, 840, 880, 810],
    [810, 830, 840, 720, 940],
    [1000, 800, 850, 840, 950],
    [1000, 790, 840, 850, 800],
    [960, 760, 840, 850, 810],
    [960, 800, 840, 780, 870],
]

num_columns = 5
input_table = vtkTable()

arr_0 = vtkIntArray()
arr_0.SetName("Run 1")
input_table.AddColumn(arr_0)

arr_1 = vtkIntArray()
arr_1.SetName("Run 2")
input_table.AddColumn(arr_1)

arr_2 = vtkIntArray()
arr_2.SetName("Run 3")
input_table.AddColumn(arr_2)

arr_3 = vtkIntArray()
arr_3.SetName("Run 4")
input_table.AddColumn(arr_3)

arr_4 = vtkIntArray()
arr_4.SetName("Run 5")
input_table.AddColumn(arr_4)

input_table.SetNumberOfRows(20)
for j in range(20):
    for i in range(5):
        input_table.SetValue(j, i, values[j][i])

# Compute quartiles.
quartiles = vtkComputeQuartiles()
quartiles.SetInputData(0, input_table)
quartiles.Update()

lookup = vtkLookupTable()
lookup.SetNumberOfColors(5)
lookup.SetRange(0, 4)
lookup.Build()

# Set up the chart.
chart = vtkChartBox()
chart.GetPlot(0).SetInputData(quartiles.GetOutput())
chart.GetPlot(0).LegendVisibilityOn()
chart.SetColumnVisibilityAll(True)
chart.SetTitle("Michelson-Morley experiment")
chart.GetTitleProperties().SetVerticalJustificationToTop()
chart.GetTitleProperties().SetFontSize(20)
chart.GetTitleProperties().FrameOn()
chart.GetYAxis().SetTitle("Speed of Light (km/s - 299000)")

# Set the labels.
labels = vtkStringArray()
labels.SetNumberOfValues(5)
for i in range(5):
    labels.SetValue(i, f"Run {i + 1}")
chart.GetPlot(0).SetLabels(labels)

# Context actor and scene wiring.
context_actor = vtkContextActor()
context_actor.GetScene().AddItem(chart)

# Renderer
renderer = vtkRenderer()
renderer.SetBackground(0.8, 0.8, 0.8)
context_actor.GetScene().SetRenderer(renderer)
renderer.AddActor(context_actor)

# Window
render_window = vtkRenderWindow()
render_window.SetSize(400, 400)
render_window.SetMultiSamples(0)
render_window.AddRenderer(renderer)
render_window.SetWindowName("box plot michelson morley")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
