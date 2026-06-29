#!/usr/bin/env python

# Demonstrate point and cell labeling with a selection window on a sphere.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import vtkPoints
from vtkmodules.vtkCommonDataModel import (
    vtkCellArray,
    vtkPolyData,
)
from vtkmodules.vtkFiltersCore import (
    vtkCellCenters,
    vtkGenerateIds,
)
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkActor2D,
    vtkPolyDataMapper,
    vtkPolyDataMapper2D,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
    vtkSelectVisiblePoints,
)
from vtkmodules.vtkRenderingLabel import vtkLabeledDataMapper

# Selection window bounds
xmin = 200
x_length = 100
xmax = xmin + x_length
ymin = 200
y_length = 100
ymax = ymin + y_length

# Create a selection rectangle overlay
rect_points = vtkPoints()
rect_points.InsertPoint(0, xmin, ymin, 0)
rect_points.InsertPoint(1, xmax, ymin, 0)
rect_points.InsertPoint(2, xmax, ymax, 0)
rect_points.InsertPoint(3, xmin, ymax, 0)

rect_cells = vtkCellArray()
rect_cells.InsertNextCell(5)
rect_cells.InsertCellPoint(0)
rect_cells.InsertCellPoint(1)
rect_cells.InsertCellPoint(2)
rect_cells.InsertCellPoint(3)
rect_cells.InsertCellPoint(0)

select_rect = vtkPolyData()
select_rect.SetPoints(rect_points)
select_rect.SetLines(rect_cells)

rect_mapper = vtkPolyDataMapper2D()
rect_mapper.SetInputData(select_rect)

rect_actor = vtkActor2D()
rect_actor.SetMapper(rect_mapper)

# Create a sphere
sphere = vtkSphereSource()

sphere_mapper = vtkPolyDataMapper()
sphere_mapper.SetInputConnection(sphere.GetOutputPort())

sphere_actor = vtkActor()
sphere_actor.SetMapper(sphere_mapper)

# Generate ids for labeling
id_generator = vtkGenerateIds()
id_generator.SetInputConnection(sphere.GetOutputPort())
id_generator.PointIdsOn()
id_generator.CellIdsOn()
id_generator.FieldDataOn()

# Renderer (functional exception: needed by vtkSelectVisiblePoints)
renderer = vtkRenderer()
renderer.SetBackground(1, 1, 1)

# Point labels — visible points in selection window
visible_points = vtkSelectVisiblePoints()
visible_points.SetInputConnection(id_generator.GetOutputPort())
visible_points.SetRenderer(renderer)
visible_points.SelectionWindowOn()
visible_points.SetSelection(xmin, xmin + x_length, ymin, ymin + y_length)

point_label_mapper = vtkLabeledDataMapper()
point_label_mapper.SetInputConnection(visible_points.GetOutputPort())
point_label_mapper.SetLabelModeToLabelFieldData()
point_label_mapper.SetFieldDataName("vtkPointIds")

point_labels = vtkActor2D()
point_labels.SetMapper(point_label_mapper)

# Cell labels — visible cell centers in selection window
cell_centers = vtkCellCenters()
cell_centers.SetInputConnection(id_generator.GetOutputPort())

visible_cells = vtkSelectVisiblePoints()
visible_cells.SetInputConnection(cell_centers.GetOutputPort())
visible_cells.SetRenderer(renderer)
visible_cells.SelectionWindowOn()
visible_cells.SetSelection(xmin, xmin + x_length, ymin, ymin + y_length)

cell_label_mapper = vtkLabeledDataMapper()
cell_label_mapper.SetInputConnection(visible_cells.GetOutputPort())
cell_label_mapper.SetLabelModeToLabelFieldData()
cell_label_mapper.SetFieldDataName("vtkCellIds")
cell_label_mapper.GetLabelTextProperty().SetColor(0, 1, 0)

cell_labels = vtkActor2D()
cell_labels.SetMapper(cell_label_mapper)

# Add actors to renderer
renderer.AddActor(sphere_actor)
renderer.AddViewProp(rect_actor)
renderer.AddViewProp(point_labels)
renderer.AddViewProp(cell_labels)

# Render window
render_window = vtkRenderWindow()
render_window.SetSize(500, 500)
render_window.AddRenderer(renderer)
render_window.SetWindowName("labeled mesh")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
