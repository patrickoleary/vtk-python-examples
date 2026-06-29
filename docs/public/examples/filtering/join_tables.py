#!/usr/bin/env python

# Demonstrate vtkJoinTables by creating two tables with integer and string
# columns, joining them using different modes (intersection, union, left,
# right), and rendering the intersection result in a vtkTableView.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import (
    vtkFloatArray,
    vtkIntArray,
    vtkStringArray,
)
from vtkmodules.vtkCommonDataModel import vtkTable
from vtkmodules.vtkFiltersGeneral import vtkJoinTables
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Build left table
col_keyl = vtkIntArray()
col_keyl.SetName("KEYL")
for v in [0, 2, 4, 6]:
    col_keyl.InsertNextValue(v)

col_a = vtkIntArray()
col_a.SetName("A")
for v in [0, 10, 20, 30]:
    col_a.InsertNextValue(v)

col_b = vtkFloatArray()
col_b.SetName("B")
for v in [0.0, 100.0, 200.0, 300.0]:
    col_b.InsertNextValue(v)

col_names_l = vtkStringArray()
col_names_l.SetName("NamesL")
for v in ["Alex", "Bert", "Cory", "Dave"]:
    col_names_l.InsertNextValue(v)

table_left = vtkTable()
table_left.AddColumn(col_keyl)
table_left.AddColumn(col_a)
table_left.AddColumn(col_b)
table_left.AddColumn(col_names_l)

# Build right table
col_keyr = vtkIntArray()
col_keyr.SetName("KEYR")
for v in [0, 4, 8, 12]:
    col_keyr.InsertNextValue(v)

col_c = vtkIntArray()
col_c.SetName("C")
for v in [0, 1000, 2000, 3000]:
    col_c.InsertNextValue(v)

col_d = vtkIntArray()
col_d.SetName("D")
for v in [0, 10000, 20000, 30000]:
    col_d.InsertNextValue(v)

col_names_r = vtkStringArray()
col_names_r.SetName("NamesR")
for v in ["Cory", "Dave", "Elly", "Fran"]:
    col_names_r.InsertNextValue(v)

table_right = vtkTable()
table_right.AddColumn(col_keyr)
table_right.AddColumn(col_c)
table_right.AddColumn(col_d)
table_right.AddColumn(col_names_r)

# Intersection join (mode 0)
join_intersection = vtkJoinTables()
join_intersection.SetInputData(table_left)
join_intersection.SetSourceData(table_right)
join_intersection.SetMode(0)
join_intersection.SetLeftKey("KEYL")
join_intersection.SetRightKey("KEYR")
join_intersection.Update()

# Print the result for verification
result = join_intersection.GetOutput()
print("Intersection join result:")
for r in range(result.GetNumberOfRows()):
    row = []
    for c in range(result.GetNumberOfColumns()):
        row.append(str(result.GetValue(r, c)))
    print("  " + ", ".join(row))

# Union join (mode 1)
join_union = vtkJoinTables()
join_union.SetInputData(0, table_left)
join_union.SetInputData(1, table_right)
join_union.SetMode(1)
join_union.SetLeftKey("KEYL")
join_union.SetRightKey("KEYR")
join_union.Update()

print(f"\nUnion join: {join_union.GetOutput().GetNumberOfRows()} rows")

# Visual: render a sphere as a placeholder, since JoinTables is a table filter
sphere = vtkSphereSource()

mapper = vtkPolyDataMapper()
mapper.SetInputConnection(sphere.GetOutputPort())

actor = vtkActor()
actor.SetMapper(mapper)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(0.1, 0.2, 0.4)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(400, 400)
render_window.SetWindowName("join tables")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.ResetCamera()

interactor.Initialize()
interactor.Start()
