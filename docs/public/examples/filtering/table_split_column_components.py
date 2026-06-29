#!/usr/bin/env python

# Demonstrate vtkSplitColumnComponents by creating a table with single-
# and multi-component integer arrays, splitting them into individual
# columns, and rendering the result in a chart view.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingContextOpenGL2  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkChartsCore import (
    vtkChart,
    vtkChartXY,
)
from vtkmodules.vtkCommonCore import vtkIntArray
from vtkmodules.vtkCommonDataModel import vtkTable
from vtkmodules.vtkFiltersGeneral import vtkSplitColumnComponents
from vtkmodules.vtkRenderingContext2D import vtkContextActor
from vtkmodules.vtkRenderingCore import (
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Create single-component array
single = vtkIntArray()
single.SetNumberOfComponents(1)
single.SetNumberOfTuples(5)
single.SetName("Single")

# Create three-component array
multi = vtkIntArray()
multi.SetNumberOfComponents(3)
multi.SetNumberOfTuples(5)
multi.SetName("Multi")

for i in range(5):
    single.SetValue(i, i)
    multi.SetTuple3(i, i + 1, 2 * (i + 1), 3 * (i + 1))

# Build the table
table = vtkTable()
table.AddColumn(single)
table.AddColumn(multi)

# Split multi-component columns into individual columns
split = vtkSplitColumnComponents()
split.SetInputData(table)
split.Update()

# Display split columns in a chart
split_output = split.GetOutput()

chart = vtkChartXY()
chart.SetTitle("TableSplitColumnComponents")

line_0 = chart.AddPlot(vtkChart.LINE)
line_0.SetInputData(split_output, "Single", "Multi (0)")
line_0.SetColor(255, 0, 0, 255)
line_0.SetWidth(2.0)

line_1 = chart.AddPlot(vtkChart.LINE)
line_1.SetInputData(split_output, "Single", "Multi (1)")
line_1.SetColor(0, 255, 0, 255)
line_1.SetWidth(2.0)

line_2 = chart.AddPlot(vtkChart.LINE)
line_2.SetInputData(split_output, "Single", "Multi (2)")
line_2.SetColor(0, 0, 255, 255)
line_2.SetWidth(2.0)

# ContextActor: overlay the chart on the normal VTK rendering pipeline
context_actor = vtkContextActor()
context_actor.GetScene().AddItem(chart)

renderer = vtkRenderer()
renderer.SetBackground(1.0, 1.0, 1.0)
renderer.AddActor(context_actor)
context_actor.GetScene().SetRenderer(renderer)

render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(600, 400)
render_window.SetMultiSamples(0)
render_window.SetWindowName("table split column components")

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
