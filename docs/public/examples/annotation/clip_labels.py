#!/usr/bin/env python

# Test that clipping planes affect labels displayed by vtkLabeledDataMapper.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonDataModel import (
    vtkPlane,
    vtkPlaneCollection,
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
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
    vtkSelectVisiblePoints,
)
from vtkmodules.vtkRenderingLabel import vtkLabeledDataMapper

# Selection window bounds
xmin = 0
ymin = 0
xmax = 400
ymax = 400

# Create a sphere
sphere = vtkSphereSource()

# Generate data arrays containing point and cell ids
id_generator = vtkGenerateIds()
id_generator.SetInputConnection(sphere.GetOutputPort())
id_generator.PointIdsOn()
id_generator.CellIdsOn()
id_generator.FieldDataOn()

# Sphere mapper and actor
sphere_mapper = vtkPolyDataMapper()
sphere_mapper.SetInputConnection(sphere.GetOutputPort())

sphere_actor = vtkActor()
sphere_actor.SetMapper(sphere_mapper)

# Clipping planes
clip_plane_1 = vtkPlane()
clip_plane_1.SetOrigin(-0.1, 0.0, 0.0)
clip_plane_1.SetNormal(1, 0, 0.0)

clip_plane_2 = vtkPlane()
clip_plane_2.SetOrigin(0.1, 0.0, 0.0)
clip_plane_2.SetNormal(-1, 0, 0.0)

clip_plane_collection = vtkPlaneCollection()
clip_plane_collection.AddItem(clip_plane_1)
clip_plane_collection.AddItem(clip_plane_2)

# Renderer (functional exception: needed by vtkSelectVisiblePoints)
renderer = vtkRenderer()
renderer.SetBackground(1, 1, 1)
renderer.AddActor(sphere_actor)

# Point labels — visible points in selection window
visible_points = vtkSelectVisiblePoints()
visible_points.SetInputConnection(id_generator.GetOutputPort())
visible_points.SetRenderer(renderer)
visible_points.SelectionWindowOn()
visible_points.SetSelection(xmin, xmax, ymin, ymax)

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
visible_cells.SetSelection(xmin, xmax, ymin, ymax)

cell_label_mapper = vtkLabeledDataMapper()
cell_label_mapper.SetInputConnection(visible_cells.GetOutputPort())
cell_label_mapper.SetLabelModeToLabelFieldData()
cell_label_mapper.SetFieldDataName("vtkCellIds")
cell_label_mapper.GetLabelTextProperty().SetColor(0, 1, 0)

cell_labels = vtkActor2D()
cell_labels.SetMapper(cell_label_mapper)

# Render window
render_window = vtkRenderWindow()
render_window.SetSize(xmax, ymax)
render_window.AddRenderer(renderer)
render_window.SetWindowName("clip labels")

# Functional render: establish depth buffer for visible point selection
render_window.Render()

# Apply clipping planes and add label actors after initial render
sphere_mapper.SetClippingPlanes(clip_plane_collection)
point_label_mapper.SetClippingPlanes(clip_plane_collection)
cell_label_mapper.SetClippingPlanes(clip_plane_collection)

renderer.AddViewProp(point_labels)
renderer.AddViewProp(cell_labels)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
