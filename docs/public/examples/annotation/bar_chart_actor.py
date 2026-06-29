#!/usr/bin/env python

# Test vtkBarChartActor with random data and colored bars.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import vtkFloatArray, vtkMath
from vtkmodules.vtkCommonDataModel import vtkTable
from vtkmodules.vtkRenderingAnnotation import vtkBarChartActor
from vtkmodules.vtkRenderingCore import (
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

num_tuples = 6

# Random bar data
bitter = vtkFloatArray()
bitter.SetNumberOfTuples(num_tuples)
for i in range(num_tuples):
    bitter.SetTuple1(i, vtkMath.Random(7, 100))

table = vtkTable()
table.AddColumn(bitter)

# Bar chart actor
bar_chart_actor = vtkBarChartActor()
bar_chart_actor.SetInput(table)
bar_chart_actor.SetTitle("Bar Chart")
bar_chart_actor.GetPositionCoordinate().SetValue(0.05, 0.05, 0.0)
bar_chart_actor.GetPosition2Coordinate().SetValue(0.95, 0.85, 0.0)
bar_chart_actor.GetProperty().SetColor(1, 1, 1)
bar_chart_actor.GetLegendActor().SetNumberOfEntries(num_tuples)

for i in range(num_tuples):
    red = vtkMath.Random(0, 1)
    green = vtkMath.Random(0, 1)
    blue = vtkMath.Random(0, 1)
    bar_chart_actor.SetBarColor(i, red, green, blue)

bar_chart_actor.SetBarLabel(0, "oil")
bar_chart_actor.SetBarLabel(1, "gas")
bar_chart_actor.SetBarLabel(2, "water")
bar_chart_actor.SetBarLabel(3, "snake oil")
bar_chart_actor.SetBarLabel(4, "tequila")
bar_chart_actor.SetBarLabel(5, "beer")
bar_chart_actor.LegendVisibilityOn()

bar_chart_actor.GetTitleTextProperty().SetColor(1, 1, 0)
bar_chart_actor.GetLabelTextProperty().SetColor(1, 0, 0)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(bar_chart_actor)
renderer.SetBackground(0, 0, 0)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("bar chart actor")
render_window.SetMultiSamples(0)
render_window.SetSize(500, 200)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
