#!/usr/bin/env python

# Demonstrate vtkIntersectionPolyDataFilter on two triangulated polydata
# that nearly share a vertex, verifying the intersection handles edge
# cases and rendering both surfaces with the intersection line.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import vtkPoints
from vtkmodules.vtkCommonDataModel import (
    VTK_TRIANGLE,
    vtkCellArray,
    vtkPolyData,
)
from vtkmodules.vtkFiltersGeneral import vtkIntersectionPolyDataFilter
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# First triangle
points_0 = vtkPoints()
points_0.InsertNextPoint(-30.125, 29.3125, -27.1875)
points_0.InsertNextPoint(-29.9375, 29.375, -27.3125)
points_0.InsertNextPoint(-30.0625, 28.5, -27.25)

cells_0 = vtkCellArray()
cells_0.InsertNextCell(3, [0, 1, 2])

poly_0 = vtkPolyData()
poly_0.SetPoints(points_0)
poly_0.SetPolys(cells_0)

# Second triangle (shares a near-coincident vertex)
points_1 = vtkPoints()
points_1.InsertNextPoint(-29.9375, 29.3125, -27.3125)
points_1.InsertNextPoint(-29.875, 29.8125, -27.5)
points_1.InsertNextPoint(-29.75, 27.6875, -27.4375)

cells_1 = vtkCellArray()
cells_1.InsertNextCell(3, [0, 1, 2])

poly_1 = vtkPolyData()
poly_1.SetPoints(points_1)
poly_1.SetPolys(cells_1)

# Compute intersection
intersection = vtkIntersectionPolyDataFilter()
intersection.SetInputData(0, poly_0)
intersection.SetInputData(1, poly_1)
intersection.Update()

# Render first triangle
mapper_0 = vtkPolyDataMapper()
mapper_0.SetInputData(poly_0)
mapper_0.ScalarVisibilityOff()

actor_0 = vtkActor()
actor_0.SetMapper(mapper_0)
actor_0.GetProperty().SetColor(1, 0, 0)
actor_0.GetProperty().SetOpacity(0.5)

# Render second triangle
mapper_1 = vtkPolyDataMapper()
mapper_1.SetInputData(poly_1)
mapper_1.ScalarVisibilityOff()

actor_1 = vtkActor()
actor_1.SetMapper(mapper_1)
actor_1.GetProperty().SetColor(0, 1, 0)
actor_1.GetProperty().SetOpacity(0.5)

# Render intersection line (if any)
intersection_mapper = vtkPolyDataMapper()
intersection_mapper.SetInputConnection(intersection.GetOutputPort())
intersection_mapper.ScalarVisibilityOff()

intersection_actor = vtkActor()
intersection_actor.SetMapper(intersection_mapper)
intersection_actor.GetProperty().SetColor(1, 1, 0)
intersection_actor.GetProperty().SetLineWidth(3.0)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(actor_0)
renderer.AddActor(actor_1)
renderer.AddActor(intersection_actor)
renderer.SetBackground(0.1, 0.2, 0.3)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(400, 400)
render_window.SetWindowName("intersection near vertex")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.ResetCamera()

interactor.Initialize()
interactor.Start()
