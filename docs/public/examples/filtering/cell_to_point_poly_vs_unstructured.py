#!/usr/bin/env python

# Compare cell-to-point data conversion on polydata vs unstructured grid.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonDataModel import vtkSphere
from vtkmodules.vtkFiltersCore import (
    vtkCellDataToPointData,
    vtkPointDataToCellData,
    vtkSimpleElevationFilter,
)
from vtkmodules.vtkFiltersExtraction import vtkExtractGeometry
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkDataSetMapper,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Control resolution
resolution = 20

# Source: generate a sphere with elevation-based scalars
sphere = vtkSphereSource()
sphere.SetThetaResolution(resolution)
sphere.SetPhiResolution(int(resolution / 2))
sphere.GenerateNormalsOff()

elevation = vtkSimpleElevationFilter()
elevation.SetInputConnection(sphere.GetOutputPort())

# Convert point data to cell data (strip point scalars)
point_to_cell = vtkPointDataToCellData()
point_to_cell.SetInputConnection(elevation.GetOutputPort())
point_to_cell.PassPointDataOff()

# Left viewport: cell data directly
mapper_0 = vtkPolyDataMapper()
mapper_0.SetInputConnection(point_to_cell.GetOutputPort())

actor_0 = vtkActor()
actor_0.SetMapper(mapper_0)

# Middle viewport: cell-to-point on polydata
cell_to_point_1 = vtkCellDataToPointData()
cell_to_point_1.SetInputConnection(point_to_cell.GetOutputPort())

mapper_1 = vtkPolyDataMapper()
mapper_1.SetInputConnection(cell_to_point_1.GetOutputPort())

actor_1 = vtkActor()
actor_1.SetMapper(mapper_1)

# Right viewport: cell-to-point on unstructured grid
implicit_sphere = vtkSphere()
implicit_sphere.SetCenter(0, 0, 0)
implicit_sphere.SetRadius(10000000)

extract = vtkExtractGeometry()
extract.SetImplicitFunction(implicit_sphere)
extract.SetInputConnection(point_to_cell.GetOutputPort())
extract.ExtractInsideOn()
extract.Update()

cell_to_point_2 = vtkCellDataToPointData()
cell_to_point_2.SetInputConnection(extract.GetOutputPort())

mapper_2 = vtkDataSetMapper()
mapper_2.SetInputConnection(cell_to_point_2.GetOutputPort())

actor_2 = vtkActor()
actor_2.SetMapper(mapper_2)

# Renderers
background = (0.1, 0.2, 0.4)

renderer_0 = vtkRenderer()
renderer_0.SetViewport(0, 0, 0.33, 1.0)
renderer_0.AddActor(actor_0)
renderer_0.SetBackground(background)

renderer_1 = vtkRenderer()
renderer_1.SetViewport(0.33, 0, 0.66, 1.0)
renderer_1.AddActor(actor_1)
renderer_1.SetBackground(background)

renderer_2 = vtkRenderer()
renderer_2.SetViewport(0.66, 0, 1.0, 1.0)
renderer_2.AddActor(actor_2)
renderer_2.SetBackground(background)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer_0)
render_window.AddRenderer(renderer_1)
render_window.AddRenderer(renderer_2)
render_window.SetSize(600, 200)
render_window.SetWindowName("cell to point poly vs unstructured")

# Scene
renderer_0.GetActiveCamera().SetPosition(1, 0, 0)
renderer_0.GetActiveCamera().SetFocalPoint(0, 0, 0)
renderer_0.ResetCamera()
renderer_1.SetActiveCamera(renderer_0.GetActiveCamera())
renderer_2.SetActiveCamera(renderer_0.GetActiveCamera())

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
