#!/usr/bin/env python

# Box plot comparing five random distributions using a chart overlay on the
# VTK pipeline. Raw samples are summarised into quartiles before charting.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingContextOpenGL2  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkChartsCore import vtkChartBox, vtkPlotBox
from vtkmodules.vtkCommonCore import (
    vtkFloatArray,
    vtkMinimalStandardRandomSequence,
)
from vtkmodules.vtkCommonDataModel import vtkTable
from vtkmodules.vtkFiltersStatistics import (
    vtkComputeQuartiles,
    vtkStatisticsAlgorithm,
)
from vtkmodules.vtkRenderingContext2D import vtkContextActor
from vtkmodules.vtkRenderingCore import (
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
white_smoke_rgb = (0.961, 0.961, 0.961)

# Data: generate five distributions with different spreads
rand_seq = vtkMinimalStandardRandomSequence()
rand_seq.SetSeed(42)

num_samples = 50
column_names = ["Narrow", "Medium", "Wide", "Shifted", "Bimodal"]
scales = [1.0, 2.0, 4.0, 2.0, 0.8]
offsets = [5.0, 5.0, 5.0, 10.0, 0.0]

raw_table = vtkTable()
for name in column_names:
    arr = vtkFloatArray()
    arr.SetName(name)
    raw_table.AddColumn(arr)

raw_table.SetNumberOfRows(num_samples)
for i in range(num_samples):
    for c, name in enumerate(column_names):
        if name == "Bimodal":
            center = 3.0 if (i % 2 == 0) else 7.0
            val = rand_seq.GetRangeValue(-scales[c], scales[c]) + center
        else:
            val = rand_seq.GetRangeValue(-scales[c], scales[c]) + offsets[c]
        rand_seq.Next()
        raw_table.SetValue(i, c, val)

# Statistics: compute quartile summaries from the raw samples
quartiles = vtkComputeQuartiles()
quartiles.SetInputData(vtkStatisticsAlgorithm.INPUT_DATA, raw_table)
quartiles.Update()
box_table = quartiles.GetOutput()

# Chart: create a box plot from the quartile summary table
chart = vtkChartBox()
chart.SetTitle("Distribution Comparison")
chart.SetShowLegend(True)

plot = vtkPlotBox()
plot.SetInputData(box_table)
chart.SetPlot(plot)
chart.SetColumnVisibilityAll(True)

# ContextActor: overlay the chart on the normal VTK rendering pipeline
context_actor = vtkContextActor()
context_actor.GetScene().AddItem(chart)

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.SetBackground(white_smoke_rgb)
renderer.AddActor(context_actor)
context_actor.GetScene().SetRenderer(renderer)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(640, 480)
render_window.SetMultiSamples(0)
render_window.SetWindowName("BoxPlot")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()