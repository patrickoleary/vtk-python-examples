#!/usr/bin/env python
# Demonstrate vtkHeatmapItem rendering a table with numeric and string columns.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingContextOpenGL2  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import vtkDoubleArray, vtkStringArray
from vtkmodules.vtkCommonDataModel import vtkTable
from vtkmodules.vtkRenderingContext2D import vtkContextActor, vtkContextScene, vtkContextTransform
from vtkmodules.vtkViewsInfovis import vtkHeatmapItem
from vtkmodules.vtkRenderingCore import (
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Build table with names and numeric/string columns.
table = vtkTable()

table_names = vtkStringArray()
table_names.SetNumberOfTuples(3)
table_names.SetValue(0, "c")
table_names.SetValue(1, "b")
table_names.SetValue(2, "a")
table_names.SetName("name")

m1 = vtkDoubleArray()
m1.SetNumberOfTuples(3)
m1.SetName("m1")
m1.SetValue(0, 1.0)
m1.SetValue(1, 3.0)
m1.SetValue(2, 1.0)

m2 = vtkDoubleArray()
m2.SetNumberOfTuples(3)
m2.SetName("m2")
m2.SetValue(0, 2.0)
m2.SetValue(1, 2.0)
m2.SetValue(2, 2.0)

m3 = vtkDoubleArray()
m3.SetNumberOfTuples(3)
m3.SetName("m3")
m3.SetValue(0, 3.0)
m3.SetValue(1, 1.0)
m3.SetValue(2, 3.0)

m4 = vtkStringArray()
m4.SetNumberOfTuples(3)
m4.SetName("m4")
m4.SetValue(0, "a")
m4.SetValue(1, "b")
m4.SetValue(2, "c")

table.AddColumn(table_names)
table.AddColumn(m1)
table.AddColumn(m2)
table.AddColumn(m3)
table.AddColumn(m4)

# Heatmap item.
heatmap = vtkHeatmapItem()
heatmap.SetTable(table)
heatmap.SetPosition(20, 5)

# Context actor pipeline.
context_actor = vtkContextActor()
context_transform = vtkContextTransform()
context_transform.SetInteractive(True)
context_transform.AddItem(heatmap)
context_transform.Scale(2, 2)
context_actor.GetScene().AddItem(context_transform)

# Standard rendering pipeline.
renderer = vtkRenderer()
renderer.SetBackground(1.0, 1.0, 1.0)
renderer.AddActor(context_actor)
context_actor.GetScene().SetRenderer(renderer)

render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("heatmap item")
render_window.SetMultiSamples(0)
render_window.SetSize(400, 200)

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
