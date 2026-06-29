#!/usr/bin/env python
# Demonstrate parallel coordinates chart with multiple float arrays on a table.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingContextOpenGL2  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import vtkFloatArray
from vtkmodules.vtkCommonDataModel import vtkTable
from vtkmodules.vtkChartsCore import vtkChartParallelCoordinates
from vtkmodules.vtkRenderingContext2D import vtkContextActor
from vtkmodules.vtkRenderingCore import (
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Build table with float arrays.
table = vtkTable()
array1 = vtkFloatArray()
array1.SetName("Array1")
table.AddColumn(array1)
array2 = vtkFloatArray()
array2.SetName("Array2")
table.AddColumn(array2)
array3 = vtkFloatArray()
array3.SetName("Array3")
table.AddColumn(array3)
array4 = vtkFloatArray()
array4.SetName("Array4")
table.AddColumn(array4)
array5 = vtkFloatArray()
array5.SetName("Array5")
table.AddColumn(array5)
array6 = vtkFloatArray()
array6.SetName("Array6")
table.AddColumn(array6)

data = [
    [0, 0, 0, 0, 0, 3],
    [1, -1, 1, 2, 1, 6],
    [2, -2, 4, 4, 0.5, 2],
    [3, -3, 9, 6, 0.33, 4],
    [4, -4, 16, 8, 0.25, 9],
]
table.SetNumberOfRows(len(data))
for i, row in enumerate(data):
    for j, val in enumerate(row):
        table.SetValue(i, j, val)

# Parallel coordinates chart.
chart = vtkChartParallelCoordinates()
chart.GetPlot(0).SetInputData(table)

# Context actor with scene wiring.
context_actor = vtkContextActor()
context_actor.GetScene().AddItem(chart)

# Renderer.
renderer = vtkRenderer()
renderer.SetBackground(1.0, 1.0, 1.0)
context_actor.GetScene().SetRenderer(renderer)
renderer.AddActor(context_actor)

# Render window.
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("parallel coordinates view")
render_window.SetMultiSamples(0)
render_window.SetSize(600, 300)

# Interactor.
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
