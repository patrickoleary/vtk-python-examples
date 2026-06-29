#!/usr/bin/env python
# Demonstrate vtkHeatmapItem with scalar color legend via vtkContextActor.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingContextOpenGL2  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import vtkIntArray, vtkStringArray
from vtkmodules.vtkCommonDataModel import vtkTable
from vtkmodules.vtkRenderingContext2D import vtkContextActor, vtkContextScene, vtkContextTransform
from vtkmodules.vtkViewsInfovis import vtkHeatmapItem
from vtkmodules.vtkRenderingCore import (
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Build table with integer scalar column.
table = vtkTable()

table_names = vtkStringArray()
table_names.SetNumberOfTuples(3)
table_names.SetValue(0, "3")
table_names.SetValue(1, "2")
table_names.SetValue(2, "1")
table_names.SetName("names")

column = vtkIntArray()
column.SetNumberOfTuples(3)
column.SetName("values")
column.SetValue(0, 3)
column.SetValue(1, 2)
column.SetValue(2, 1)

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
render_window.SetWindowName("heatmap scalar legend")
render_window.SetMultiSamples(0)
render_window.SetSize(400, 400)

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
