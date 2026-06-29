#!/usr/bin/env python

# Render DG cell grids (hexahedra, tetrahedra, wedges, etc.) using vtkCellGridMapper.

import os

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonDataModel import vtkCellGridSidesQuery
from vtkmodules.vtkFiltersCellGrid import vtkCellGridComputeSides
from vtkmodules.vtkIOCellGrid import vtkCellGridReader
from vtkmodules.vtkRenderingCellGrid import vtkRenderingCellGrid
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkCellGridMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Register render responder for DG cells
vtkRenderingCellGrid.RegisterCellsAndResponders()

# Data path
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Read hexahedra cell grid
cell_grid_reader = vtkCellGridReader()
cell_grid_reader.SetFileName(os.path.join(data_dir, "dgHexahedra.dg"))

# Compute sides for surface rendering
compute_sides = vtkCellGridComputeSides()
compute_sides.SetInputConnection(cell_grid_reader.GetOutputPort())
compute_sides.SetOutputDimensionControl(vtkCellGridSidesQuery.NextLowestDimension)
compute_sides.PreserveRenderableInputsOff()
compute_sides.OmitSidesForRenderableInputsOff()
compute_sides.Update()

# Mapper with scalar coloring
cell_grid_mapper = vtkCellGridMapper()
cell_grid_mapper.SetInputConnection(compute_sides.GetOutputPort())
cell_grid_mapper.ScalarVisibilityOn()
cell_grid_mapper.SetScalarMode(4)  # VTK_SCALAR_MODE_USE_CELL_FIELD_DATA
cell_grid_mapper.SetArrayName("scalar1")

cell_grid_actor = vtkActor()
cell_grid_actor.SetMapper(cell_grid_mapper)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(cell_grid_actor)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("cellgrid rendering")
render_window.SetMultiSamples(0)
render_window.SetSize(300, 300)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.GetActiveCamera().Azimuth(20)
renderer.GetActiveCamera().Elevation(30)
renderer.ResetCamera()

interactor.Initialize()
interactor.Start()
