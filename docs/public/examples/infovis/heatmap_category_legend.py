#!/usr/bin/env python
# Demonstrate vtkHeatmapItem with category legend via vtkContextActor.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingContextOpenGL2  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import vtkStringArray
from vtkmodules.vtkCommonDataModel import vtkTable
from vtkmodules.vtkRenderingContext2D import vtkContextActor, vtkContextScene, vtkContextTransform
from vtkmodules.vtkViewsInfovis import vtkHeatmapItem
from vtkmodules.vtkRenderingCore import (
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Build table with string category columns.
table = vtkTable()

table_names = vtkStringArray()
table_names.SetNumberOfTuples(4)
table_names.SetValue(0, "c")
table_names.SetValue(1, "b")
table_names.SetValue(2, "a")
table_names.SetValue(3, "a")
table_names.SetName("names")

column = vtkStringArray()
column.SetNumberOfTuples(4)
column.SetName("values")
column.SetValue(0, "c")
column.SetValue(1, "b")
column.SetValue(2, "a")
column.SetValue(3, "a")

table.AddColumn(table_names)
table.AddColumn(column)

# Heatmap item.
heatmap = vtkHeatmapItem()
heatmap.SetTable(table)

# Context actor pipeline.
context_actor = vtkContextActor()
context_transform = vtkContextTransform()
context_transform.SetInteractive(True)
context_transform.AddItem(heatmap)
context_transform.Translate(125, 125)
context_actor.GetScene().AddItem(context_transform)

# Standard rendering pipeline.
renderer = vtkRenderer()
renderer.SetBackground(1.0, 1.0, 1.0)
renderer.AddActor(context_actor)
context_actor.GetScene().SetRenderer(renderer)

render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("heatmap category legend")
render_window.SetMultiSamples(0)
render_window.SetSize(400, 400)

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
