#!/usr/bin/env python
# Demonstrate vtkCellCentersPointPlacer constraining a distance widget to cell centers.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import vtkPoints
from vtkmodules.vtkCommonDataModel import (
    VTK_TETRA,
    vtkCellArray,
    vtkHexahedron,
    vtkPentagonalPrism,
    vtkPyramid,
    vtkTetra,
    vtkUnstructuredGrid,
    vtkVoxel,
    vtkWedge,
)
from vtkmodules.vtkCommonMath import vtkMatrix4x4
from vtkmodules.vtkCommonTransforms import vtkMatrixToLinearTransform
from vtkmodules.vtkFiltersGeneral import vtkTransformFilter
from vtkmodules.vtkInteractionWidgets import (
    vtkCellCentersPointPlacer,
    vtkDistanceRepresentation2D,
    vtkDistanceWidget,
    vtkPointHandleRepresentation3D,
)
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkDataSetMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Data: hexahedron
hex_points = vtkPoints()
hex_points.InsertNextPoint(0.0, 0.0, 0.0)
hex_points.InsertNextPoint(1.0, 0.0, 0.0)
hex_points.InsertNextPoint(1.0, 1.0, 0.0)
hex_points.InsertNextPoint(0.0, 1.0, 0.0)
hex_points.InsertNextPoint(0.0, 0.0, 1.0)
hex_points.InsertNextPoint(1.0, 0.0, 1.0)
hex_points.InsertNextPoint(1.0, 1.0, 1.0)
hex_points.InsertNextPoint(0.0, 1.0, 1.0)
hex_cell = vtkHexahedron()
hex_cell.GetPointIds().SetId(0, 0)
hex_cell.GetPointIds().SetId(1, 1)
hex_cell.GetPointIds().SetId(2, 2)
hex_cell.GetPointIds().SetId(3, 3)
hex_cell.GetPointIds().SetId(4, 4)
hex_cell.GetPointIds().SetId(5, 5)
hex_cell.GetPointIds().SetId(6, 6)
hex_cell.GetPointIds().SetId(7, 7)
hex_grid = vtkUnstructuredGrid()
hex_grid.SetPoints(hex_points)
hex_grid.InsertNextCell(hex_cell.GetCellType(), hex_cell.GetPointIds())

# Data: pentagonal prism
prism_points = vtkPoints()
prism_points.InsertNextPoint(1, 0, 0)
prism_points.InsertNextPoint(3, 0, 0)
prism_points.InsertNextPoint(4, 2, 0)
prism_points.InsertNextPoint(2, 4, 0)
prism_points.InsertNextPoint(0, 2, 0)
prism_points.InsertNextPoint(1, 0, 4)
prism_points.InsertNextPoint(3, 0, 4)
prism_points.InsertNextPoint(4, 2, 4)
prism_points.InsertNextPoint(2, 4, 4)
prism_points.InsertNextPoint(0, 2, 4)
prism_cell = vtkPentagonalPrism()
prism_cell.GetPointIds().SetId(0, 0)
prism_cell.GetPointIds().SetId(1, 1)
prism_cell.GetPointIds().SetId(2, 2)
prism_cell.GetPointIds().SetId(3, 3)
prism_cell.GetPointIds().SetId(4, 4)
prism_cell.GetPointIds().SetId(5, 5)
prism_cell.GetPointIds().SetId(6, 6)
prism_cell.GetPointIds().SetId(7, 7)
prism_cell.GetPointIds().SetId(8, 8)
prism_cell.GetPointIds().SetId(9, 9)
prism_grid = vtkUnstructuredGrid()
prism_grid.SetPoints(prism_points)
prism_grid.InsertNextCell(prism_cell.GetCellType(), prism_cell.GetPointIds())

# Data: pyramid
pyramid_points = vtkPoints()
pyramid_points.InsertNextPoint(1.0, 1.0, 1.0)
pyramid_points.InsertNextPoint(-1.0, 1.0, 1.0)
pyramid_points.InsertNextPoint(-1.0, -1.0, 1.0)
pyramid_points.InsertNextPoint(1.0, -1.0, 1.0)
pyramid_points.InsertNextPoint(0.0, 0.0, 0.0)
pyramid_cell = vtkPyramid()
pyramid_cell.GetPointIds().SetId(0, 0)
pyramid_cell.GetPointIds().SetId(1, 1)
pyramid_cell.GetPointIds().SetId(2, 2)
pyramid_cell.GetPointIds().SetId(3, 3)
pyramid_cell.GetPointIds().SetId(4, 4)
pyramid_grid = vtkUnstructuredGrid()
pyramid_grid.SetPoints(pyramid_points)
pyramid_grid.InsertNextCell(pyramid_cell.GetCellType(), pyramid_cell.GetPointIds())

# Data: tetrahedron
tetra_points = vtkPoints()
tetra_points.InsertNextPoint(0, 0, 0)
tetra_points.InsertNextPoint(1, 0, 0)
tetra_points.InsertNextPoint(1, 1, 0)
tetra_points.InsertNextPoint(0, 1, 1)
tetra_points.InsertNextPoint(5, 5, 5)
tetra_points.InsertNextPoint(6, 5, 5)
tetra_points.InsertNextPoint(6, 6, 5)
tetra_points.InsertNextPoint(5, 6, 6)
tetra_cell = vtkTetra()
tetra_cell.GetPointIds().SetId(0, 0)
tetra_cell.GetPointIds().SetId(1, 1)
tetra_cell.GetPointIds().SetId(2, 2)
tetra_cell.GetPointIds().SetId(3, 3)
tetra_cells = vtkCellArray()
tetra_cells.InsertNextCell(tetra_cell)
tetra_grid = vtkUnstructuredGrid()
tetra_grid.SetPoints(tetra_points)
tetra_grid.SetCells(VTK_TETRA, tetra_cells)

# Data: voxel
voxel_points = vtkPoints()
voxel_points.InsertNextPoint(0, 0, 0)
voxel_points.InsertNextPoint(1, 0, 0)
voxel_points.InsertNextPoint(0, 1, 0)
voxel_points.InsertNextPoint(1, 1, 0)
voxel_points.InsertNextPoint(0, 0, 1)
voxel_points.InsertNextPoint(1, 0, 1)
voxel_points.InsertNextPoint(0, 1, 1)
voxel_points.InsertNextPoint(1, 1, 1)
voxel_cell = vtkVoxel()
voxel_cell.GetPointIds().SetId(0, 0)
voxel_cell.GetPointIds().SetId(1, 1)
voxel_cell.GetPointIds().SetId(2, 2)
voxel_cell.GetPointIds().SetId(3, 3)
voxel_cell.GetPointIds().SetId(4, 4)
voxel_cell.GetPointIds().SetId(5, 5)
voxel_cell.GetPointIds().SetId(6, 6)
voxel_cell.GetPointIds().SetId(7, 7)
voxel_grid = vtkUnstructuredGrid()
voxel_grid.SetPoints(voxel_points)
voxel_grid.InsertNextCell(voxel_cell.GetCellType(), voxel_cell.GetPointIds())

# Data: wedge
wedge_points = vtkPoints()
wedge_points.InsertNextPoint(0, 1, 0)
wedge_points.InsertNextPoint(0, 0, 0)
wedge_points.InsertNextPoint(0, 0.5, 0.5)
wedge_points.InsertNextPoint(1, 1, 0)
wedge_points.InsertNextPoint(1, 0.0, 0.0)
wedge_points.InsertNextPoint(1, 0.5, 0.5)
wedge_cell = vtkWedge()
wedge_cell.GetPointIds().SetId(0, 0)
wedge_cell.GetPointIds().SetId(1, 1)
wedge_cell.GetPointIds().SetId(2, 2)
wedge_cell.GetPointIds().SetId(3, 3)
wedge_cell.GetPointIds().SetId(4, 4)
wedge_cell.GetPointIds().SetId(5, 5)
wedge_grid = vtkUnstructuredGrid()
wedge_grid.SetPoints(wedge_points)
wedge_grid.InsertNextCell(wedge_cell.GetCellType(), wedge_cell.GetPointIds())

# Transform + Mapper + Actor: hexahedron at grid position (0, 0)
hex_matrix = vtkMatrix4x4()
hex_matrix.SetElement(0, 3, 0)
hex_matrix.SetElement(1, 3, 0)
hex_transform = vtkMatrixToLinearTransform()
hex_transform.SetInput(hex_matrix)
hex_filter = vtkTransformFilter()
hex_filter.SetInputData(hex_grid)
hex_filter.SetTransform(hex_transform)
hex_filter.Update()
hex_mapper = vtkDataSetMapper()
hex_mapper.SetInputConnection(hex_filter.GetOutputPort())
hex_actor = vtkActor()
hex_actor.SetMapper(hex_mapper)
hex_actor.GetProperty().SetColor(1, 0, 0.5)

# Transform + Mapper + Actor: prism at grid position (1, 0)
prism_matrix = vtkMatrix4x4()
prism_matrix.SetElement(0, 3, 5)
prism_matrix.SetElement(1, 3, 0)
prism_transform = vtkMatrixToLinearTransform()
prism_transform.SetInput(prism_matrix)
prism_filter = vtkTransformFilter()
prism_filter.SetInputData(prism_grid)
prism_filter.SetTransform(prism_transform)
prism_filter.Update()
prism_mapper = vtkDataSetMapper()
prism_mapper.SetInputConnection(prism_filter.GetOutputPort())
prism_actor = vtkActor()
prism_actor.SetMapper(prism_mapper)
prism_actor.GetProperty().SetColor(0, 1, 0)

# Transform + Mapper + Actor: pyramid at grid position (2, 0)
pyramid_matrix = vtkMatrix4x4()
pyramid_matrix.SetElement(0, 3, 10)
pyramid_matrix.SetElement(1, 3, 0)
pyramid_transform = vtkMatrixToLinearTransform()
pyramid_transform.SetInput(pyramid_matrix)
pyramid_filter = vtkTransformFilter()
pyramid_filter.SetInputData(pyramid_grid)
pyramid_filter.SetTransform(pyramid_transform)
pyramid_filter.Update()
pyramid_mapper = vtkDataSetMapper()
pyramid_mapper.SetInputConnection(pyramid_filter.GetOutputPort())
pyramid_actor = vtkActor()
pyramid_actor.SetMapper(pyramid_mapper)
pyramid_actor.GetProperty().SetColor(0, 0, 1)

# Transform + Mapper + Actor: tetrahedron at grid position (0, 1)
tetra_matrix = vtkMatrix4x4()
tetra_matrix.SetElement(0, 3, 0)
tetra_matrix.SetElement(1, 3, 5)
tetra_transform = vtkMatrixToLinearTransform()
tetra_transform.SetInput(tetra_matrix)
tetra_filter = vtkTransformFilter()
tetra_filter.SetInputData(tetra_grid)
tetra_filter.SetTransform(tetra_transform)
tetra_filter.Update()
tetra_mapper = vtkDataSetMapper()
tetra_mapper.SetInputConnection(tetra_filter.GetOutputPort())
tetra_actor = vtkActor()
tetra_actor.SetMapper(tetra_mapper)
tetra_actor.GetProperty().SetColor(1, 1, 0)

# Transform + Mapper + Actor: voxel at grid position (1, 1)
voxel_matrix = vtkMatrix4x4()
voxel_matrix.SetElement(0, 3, 5)
voxel_matrix.SetElement(1, 3, 5)
voxel_transform = vtkMatrixToLinearTransform()
voxel_transform.SetInput(voxel_matrix)
voxel_filter = vtkTransformFilter()
voxel_filter.SetInputData(voxel_grid)
voxel_filter.SetTransform(voxel_transform)
voxel_filter.Update()
voxel_mapper = vtkDataSetMapper()
voxel_mapper.SetInputConnection(voxel_filter.GetOutputPort())
voxel_actor = vtkActor()
voxel_actor.SetMapper(voxel_mapper)
voxel_actor.GetProperty().SetColor(1, 0, 1)

# Transform + Mapper + Actor: wedge at grid position (2, 1)
wedge_matrix = vtkMatrix4x4()
wedge_matrix.SetElement(0, 3, 10)
wedge_matrix.SetElement(1, 3, 5)
wedge_transform = vtkMatrixToLinearTransform()
wedge_transform.SetInput(wedge_matrix)
wedge_filter = vtkTransformFilter()
wedge_filter.SetInputData(wedge_grid)
wedge_filter.SetTransform(wedge_transform)
wedge_filter.Update()
wedge_mapper = vtkDataSetMapper()
wedge_mapper.SetInputConnection(wedge_filter.GetOutputPort())
wedge_actor = vtkActor()
wedge_actor.SetMapper(wedge_mapper)
wedge_actor.GetProperty().SetColor(0, 1, 1)

# Point placer constrained to cell centers
point_placer = vtkCellCentersPointPlacer()
point_placer.AddProp(hex_actor)
point_placer.AddProp(prism_actor)
point_placer.AddProp(pyramid_actor)
point_placer.AddProp(tetra_actor)
point_placer.AddProp(voxel_actor)
point_placer.AddProp(wedge_actor)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(hex_actor)
renderer.AddActor(prism_actor)
renderer.AddActor(pyramid_actor)
renderer.AddActor(tetra_actor)
renderer.AddActor(voxel_actor)
renderer.AddActor(wedge_actor)
renderer.SetBackground(0.2, 0.3, 0.4)
renderer.ResetCamera()
renderer.GetActiveCamera().Azimuth(30)
renderer.GetActiveCamera().Elevation(-30)
renderer.ResetCameraClippingRange()

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("cell centers point placer")
render_window.SetSize(600, 600)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Widget
widget = vtkDistanceWidget()
widget.CreateDefaultRepresentation()

distance_rep = vtkDistanceRepresentation2D()
distance_rep.GetAxis().GetProperty().SetColor(1.0, 0.0, 0.0)

handle_rep = vtkPointHandleRepresentation3D()
handle_rep.GetProperty().SetLineWidth(4.0)
handle_rep.GetProperty().SetColor(0.8, 0.2, 0)
distance_rep.SetHandleRepresentation(handle_rep)
widget.SetRepresentation(distance_rep)

# Constrain handles to cell centers
distance_rep.InstantiateHandleRepresentation()
distance_rep.GetPoint1Representation().SetPointPlacer(point_placer)
distance_rep.GetPoint2Representation().SetPointPlacer(point_placer)

# Disable smooth motion for snap-to-center behavior
distance_rep.GetPoint1Representation().SmoothMotionOff()
distance_rep.GetPoint2Representation().SmoothMotionOff()

widget.SetInteractor(interactor)
widget.SetEnabled(1)

interactor.Initialize()
interactor.Start()
