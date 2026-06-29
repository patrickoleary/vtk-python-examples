#!/usr/bin/env python

# Compute displacement gradient, small strain, and Green-Lagrange strain
# tensors on a hexahedron using vtkCellDerivatives and visualize the
# deformed mesh with strain magnitude coloring.

import math

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

import numpy as np

from vtkmodules.vtkCommonCore import (
    vtkFloatArray,
    vtkPoints,
)
from vtkmodules.vtkCommonDataModel import (
    vtkCellArray,
    vtkHexahedron,
    vtkUnstructuredGrid,
)
from vtkmodules.vtkFiltersGeneral import (
    vtkCellDerivatives,
    vtkWarpVector,
)
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkDataSetMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Create a simple hexahedron
points = vtkPoints()
points.SetNumberOfPoints(8)
points.InsertPoint(0, 0, 0, 0)
points.InsertPoint(1, 1, 0, 0)
points.InsertPoint(2, 1, 1, 0)
points.InsertPoint(3, 0, 1, 0)
points.InsertPoint(4, 0, 0, 1)
points.InsertPoint(5, 1, 0, 1)
points.InsertPoint(6, 1, 1, 1)
points.InsertPoint(7, 0, 1, 1)

hexahedron = vtkHexahedron()
for k in range(8):
    hexahedron.GetPointIds().SetId(k, k)

cell_array = vtkCellArray()
cell_array.InsertNextCell(hexahedron)

# Build displacement from a shear + extension deformation gradient
# F = [[2, 1, 0], [0, 1, 0], [0, 0, 1]]
f_matrix = np.array([[2, 1, 0], [0, 1, 0], [0, 0, 1]], dtype=float)
gu = f_matrix - np.eye(3)

farray_disp = vtkFloatArray()
farray_disp.SetName("displacement")
farray_disp.SetNumberOfComponents(3)
farray_disp.SetNumberOfTuples(8)

for k in range(8):
    pt = np.array(points.GetPoint(k))
    disp = gu @ pt
    farray_disp.SetTuple(k, disp.tolist())

ugrid = vtkUnstructuredGrid()
ugrid.SetPoints(points)
ugrid.SetCells(hexahedron.GetCellType(), cell_array)
ugrid.GetPointData().AddArray(farray_disp)
ugrid.GetPointData().SetActiveVectors("displacement")

# Compute Green-Lagrange strain tensor
cell_derivatives = vtkCellDerivatives()
cell_derivatives.SetVectorModeToPassVectors()
cell_derivatives.SetTensorModeToComputeGreenLagrangeStrain()
cell_derivatives.SetInputData(ugrid)
cell_derivatives.Update()

# Warp the mesh by displacement to show deformed shape
warper = vtkWarpVector()
warper.SetInputData(ugrid)
warper.SetScaleFactor(1.0)
warper.Update()

# Map the deformed mesh
deformed_mapper = vtkDataSetMapper()
deformed_mapper.SetInputConnection(warper.GetOutputPort())

deformed_actor = vtkActor()
deformed_actor.SetMapper(deformed_mapper)
deformed_actor.GetProperty().SetColor(1.0, 0.4, 0.4)
deformed_actor.GetProperty().EdgeVisibilityOn()
deformed_actor.GetProperty().SetEdgeColor(0, 0, 0)
deformed_actor.GetProperty().SetLineWidth(2)

# Map the original mesh as wireframe reference
original_mapper = vtkDataSetMapper()
original_mapper.SetInputData(ugrid)

original_actor = vtkActor()
original_actor.SetMapper(original_mapper)
original_actor.GetProperty().SetRepresentationToWireframe()
original_actor.GetProperty().SetColor(0.5, 0.5, 0.5)
original_actor.GetProperty().SetLineWidth(2)

# Also show the strain result mesh
strain_mapper = vtkDataSetMapper()
strain_mapper.SetInputConnection(cell_derivatives.GetOutputPort())
strain_mapper.SetScalarModeToUseCellFieldData()
strain_mapper.SelectColorArray("GreenLagrangeStrain")
strain_mapper.SetScalarRange(0, 1)

strain_actor = vtkActor()
strain_actor.SetMapper(strain_mapper)
strain_actor.AddPosition(2.5, 0, 0)
strain_actor.GetProperty().EdgeVisibilityOn()
strain_actor.GetProperty().SetEdgeColor(0, 0, 0)
strain_actor.GetProperty().SetLineWidth(2)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(original_actor)
renderer.AddActor(deformed_actor)
renderer.AddActor(strain_actor)
renderer.SetBackground(0.1, 0.2, 0.4)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(600, 400)
render_window.SetWindowName("green lagrange strain")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.ResetCamera()
renderer.GetActiveCamera().Azimuth(30)
renderer.GetActiveCamera().Elevation(20)
renderer.ResetCameraClippingRange()

interactor.Initialize()
interactor.Start()
