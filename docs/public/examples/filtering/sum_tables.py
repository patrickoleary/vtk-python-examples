#!/usr/bin/env python

# Visualize the result of vtkSumTables by creating two tables with
# numeric columns, summing them, and displaying the result as a
# bar-chart-style representation using positioned quads.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import (
    vtkDoubleArray,
    vtkIntArray,
    vtkUnsignedShortArray,
)
from vtkmodules.vtkCommonDataModel import vtkTable
from vtkmodules.vtkFiltersGeneral import vtkSumTables
from vtkmodules.vtkFiltersSources import vtkPlaneSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
    vtkTextActor,
)

# Build table 1
dbl_1 = vtkDoubleArray()
dbl_1.SetName("dbl")
dbl_1.SetNumberOfTuples(4)
for i, v in enumerate([-1.5, 0, 2.5, 4.25]):
    dbl_1.SetValue(i, v)

int_1 = vtkIntArray()
int_1.SetName("int")
int_1.SetNumberOfTuples(4)
for i, v in enumerate([-1, 0, 3, 5]):
    int_1.SetValue(i, v)

ush_1 = vtkUnsignedShortArray()
ush_1.SetName("ush")
ush_1.SetNumberOfTuples(4)
for i, v in enumerate([1, 0, 3, 5]):
    ush_1.SetValue(i, v)

table_1 = vtkTable()
table_1.AddColumn(dbl_1)
table_1.AddColumn(int_1)
table_1.AddColumn(ush_1)

# Build table 2
dbl_2 = vtkDoubleArray()
dbl_2.SetName("dbl")
dbl_2.SetNumberOfTuples(4)
for i, v in enumerate([-5.25, 1, 3.5, 1.25]):
    dbl_2.SetValue(i, v)

int_2 = vtkIntArray()
int_2.SetName("int")
int_2.SetNumberOfTuples(4)
for i, v in enumerate([-2, 0, 13, 25]):
    int_2.SetValue(i, v)

ush_2 = vtkUnsignedShortArray()
ush_2.SetName("ush")
ush_2.SetNumberOfTuples(4)
for i, v in enumerate([3, 4, 5, 0]):
    ush_2.SetValue(i, v)

table_2 = vtkTable()
table_2.AddColumn(dbl_2)
table_2.AddColumn(int_2)
table_2.AddColumn(ush_2)

# Sum the tables
sum_tables = vtkSumTables()
sum_tables.SetInputDataObject(0, table_1)
sum_tables.SetInputDataObject(1, table_2)
sum_tables.Update()

result = sum_tables.GetOutputDataObject(0)

# Visualize the sum result as colored bars (one plane per value)
dbl_col = result.GetColumnByName("dbl")
int_col = result.GetColumnByName("int")
ush_col = result.GetColumnByName("ush")

# dbl column bars (col_idx=0, red)
bar_dbl_0 = vtkPlaneSource()
bar_dbl_0.SetOrigin(0.0, 0, 0)
bar_dbl_0.SetPoint1(0.25, 0, 0)
bar_dbl_0.SetPoint2(0.0, dbl_col.GetTuple1(0) * 0.1, 0)
bar_dbl_0_mapper = vtkPolyDataMapper()
bar_dbl_0_mapper.SetInputConnection(bar_dbl_0.GetOutputPort())
bar_dbl_0_actor = vtkActor()
bar_dbl_0_actor.SetMapper(bar_dbl_0_mapper)
bar_dbl_0_actor.GetProperty().SetColor(1.0, 0.3, 0.3)

bar_dbl_1 = vtkPlaneSource()
bar_dbl_1.SetOrigin(0.3, 0, 0)
bar_dbl_1.SetPoint1(0.55, 0, 0)
bar_dbl_1.SetPoint2(0.3, dbl_col.GetTuple1(1) * 0.1, 0)
bar_dbl_1_mapper = vtkPolyDataMapper()
bar_dbl_1_mapper.SetInputConnection(bar_dbl_1.GetOutputPort())
bar_dbl_1_actor = vtkActor()
bar_dbl_1_actor.SetMapper(bar_dbl_1_mapper)
bar_dbl_1_actor.GetProperty().SetColor(1.0, 0.3, 0.3)

bar_dbl_2 = vtkPlaneSource()
bar_dbl_2.SetOrigin(0.6, 0, 0)
bar_dbl_2.SetPoint1(0.85, 0, 0)
bar_dbl_2.SetPoint2(0.6, dbl_col.GetTuple1(2) * 0.1, 0)
bar_dbl_2_mapper = vtkPolyDataMapper()
bar_dbl_2_mapper.SetInputConnection(bar_dbl_2.GetOutputPort())
bar_dbl_2_actor = vtkActor()
bar_dbl_2_actor.SetMapper(bar_dbl_2_mapper)
bar_dbl_2_actor.GetProperty().SetColor(1.0, 0.3, 0.3)

bar_dbl_3 = vtkPlaneSource()
bar_dbl_3.SetOrigin(0.9, 0, 0)
bar_dbl_3.SetPoint1(1.15, 0, 0)
bar_dbl_3.SetPoint2(0.9, dbl_col.GetTuple1(3) * 0.1, 0)
bar_dbl_3_mapper = vtkPolyDataMapper()
bar_dbl_3_mapper.SetInputConnection(bar_dbl_3.GetOutputPort())
bar_dbl_3_actor = vtkActor()
bar_dbl_3_actor.SetMapper(bar_dbl_3_mapper)
bar_dbl_3_actor.GetProperty().SetColor(1.0, 0.3, 0.3)

# int column bars (col_idx=1, green)
bar_int_0 = vtkPlaneSource()
bar_int_0.SetOrigin(1.5, 0, 0)
bar_int_0.SetPoint1(1.75, 0, 0)
bar_int_0.SetPoint2(1.5, int_col.GetTuple1(0) * 0.1, 0)
bar_int_0_mapper = vtkPolyDataMapper()
bar_int_0_mapper.SetInputConnection(bar_int_0.GetOutputPort())
bar_int_0_actor = vtkActor()
bar_int_0_actor.SetMapper(bar_int_0_mapper)
bar_int_0_actor.GetProperty().SetColor(0.3, 1.0, 0.3)

bar_int_1 = vtkPlaneSource()
bar_int_1.SetOrigin(1.8, 0, 0)
bar_int_1.SetPoint1(2.05, 0, 0)
bar_int_1.SetPoint2(1.8, int_col.GetTuple1(1) * 0.1, 0)
bar_int_1_mapper = vtkPolyDataMapper()
bar_int_1_mapper.SetInputConnection(bar_int_1.GetOutputPort())
bar_int_1_actor = vtkActor()
bar_int_1_actor.SetMapper(bar_int_1_mapper)
bar_int_1_actor.GetProperty().SetColor(0.3, 1.0, 0.3)

bar_int_2 = vtkPlaneSource()
bar_int_2.SetOrigin(2.1, 0, 0)
bar_int_2.SetPoint1(2.35, 0, 0)
bar_int_2.SetPoint2(2.1, int_col.GetTuple1(2) * 0.1, 0)
bar_int_2_mapper = vtkPolyDataMapper()
bar_int_2_mapper.SetInputConnection(bar_int_2.GetOutputPort())
bar_int_2_actor = vtkActor()
bar_int_2_actor.SetMapper(bar_int_2_mapper)
bar_int_2_actor.GetProperty().SetColor(0.3, 1.0, 0.3)

bar_int_3 = vtkPlaneSource()
bar_int_3.SetOrigin(2.4, 0, 0)
bar_int_3.SetPoint1(2.65, 0, 0)
bar_int_3.SetPoint2(2.4, int_col.GetTuple1(3) * 0.1, 0)
bar_int_3_mapper = vtkPolyDataMapper()
bar_int_3_mapper.SetInputConnection(bar_int_3.GetOutputPort())
bar_int_3_actor = vtkActor()
bar_int_3_actor.SetMapper(bar_int_3_mapper)
bar_int_3_actor.GetProperty().SetColor(0.3, 1.0, 0.3)

# ush column bars (col_idx=2, blue)
bar_ush_0 = vtkPlaneSource()
bar_ush_0.SetOrigin(3.0, 0, 0)
bar_ush_0.SetPoint1(3.25, 0, 0)
bar_ush_0.SetPoint2(3.0, ush_col.GetTuple1(0) * 0.1, 0)
bar_ush_0_mapper = vtkPolyDataMapper()
bar_ush_0_mapper.SetInputConnection(bar_ush_0.GetOutputPort())
bar_ush_0_actor = vtkActor()
bar_ush_0_actor.SetMapper(bar_ush_0_mapper)
bar_ush_0_actor.GetProperty().SetColor(0.3, 0.3, 1.0)

bar_ush_1 = vtkPlaneSource()
bar_ush_1.SetOrigin(3.3, 0, 0)
bar_ush_1.SetPoint1(3.55, 0, 0)
bar_ush_1.SetPoint2(3.3, ush_col.GetTuple1(1) * 0.1, 0)
bar_ush_1_mapper = vtkPolyDataMapper()
bar_ush_1_mapper.SetInputConnection(bar_ush_1.GetOutputPort())
bar_ush_1_actor = vtkActor()
bar_ush_1_actor.SetMapper(bar_ush_1_mapper)
bar_ush_1_actor.GetProperty().SetColor(0.3, 0.3, 1.0)

bar_ush_2 = vtkPlaneSource()
bar_ush_2.SetOrigin(3.6, 0, 0)
bar_ush_2.SetPoint1(3.85, 0, 0)
bar_ush_2.SetPoint2(3.6, ush_col.GetTuple1(2) * 0.1, 0)
bar_ush_2_mapper = vtkPolyDataMapper()
bar_ush_2_mapper.SetInputConnection(bar_ush_2.GetOutputPort())
bar_ush_2_actor = vtkActor()
bar_ush_2_actor.SetMapper(bar_ush_2_mapper)
bar_ush_2_actor.GetProperty().SetColor(0.3, 0.3, 1.0)

bar_ush_3 = vtkPlaneSource()
bar_ush_3.SetOrigin(3.9, 0, 0)
bar_ush_3.SetPoint1(4.15, 0, 0)
bar_ush_3.SetPoint2(3.9, ush_col.GetTuple1(3) * 0.1, 0)
bar_ush_3_mapper = vtkPolyDataMapper()
bar_ush_3_mapper.SetInputConnection(bar_ush_3.GetOutputPort())
bar_ush_3_actor = vtkActor()
bar_ush_3_actor.SetMapper(bar_ush_3_mapper)
bar_ush_3_actor.GetProperty().SetColor(0.3, 0.3, 1.0)

# Add a label
label = vtkTextActor()
label.SetInput("vtkSumTables: dbl / int / ush")
label.GetTextProperty().SetFontSize(14)
label.GetTextProperty().SetColor(1, 1, 1)
label.SetPosition(10, 10)

# Renderer
renderer = vtkRenderer()
renderer.SetBackground(0.1, 0.2, 0.4)
renderer.AddActor(bar_dbl_0_actor)
renderer.AddActor(bar_dbl_1_actor)
renderer.AddActor(bar_dbl_2_actor)
renderer.AddActor(bar_dbl_3_actor)
renderer.AddActor(bar_int_0_actor)
renderer.AddActor(bar_int_1_actor)
renderer.AddActor(bar_int_2_actor)
renderer.AddActor(bar_int_3_actor)
renderer.AddActor(bar_ush_0_actor)
renderer.AddActor(bar_ush_1_actor)
renderer.AddActor(bar_ush_2_actor)
renderer.AddActor(bar_ush_3_actor)
renderer.AddViewProp(label)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(400, 300)
render_window.SetWindowName("sum tables")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.ResetCamera()

interactor.Initialize()
interactor.Start()
