#!/usr/bin/env python

# Demonstrate vtkCellGridCellCenters computing cell centers on a DG
# hexahedral mesh, rendering cell edges with center glyphs.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

import os

from vtkmodules.vtkCommonDataModel import vtkCellGridSidesQuery
from vtkmodules.vtkFiltersCellGrid import (
    vtkCellGridCellCenters,
    vtkCellGridComputeSides,
    vtkCellGridToUnstructuredGrid,
    vtkFiltersCellGrid,
)
from vtkmodules.vtkIOCellGrid import vtkCellGridReader
from vtkmodules.vtkRenderingCellGrid import vtkRenderingCellGrid
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkCellGridMapper,
    vtkProperty,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Register render responders for DG cells
vtkRenderingCellGrid.RegisterCellsAndResponders()
vtkFiltersCellGrid.RegisterCellsAndResponders()

data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Read DG hexahedral cell grid
reader = vtkCellGridReader()
reader.SetFileName(os.path.join(data_dir, "dgHexahedra.dg"))

# Compute sides (surfaces then edges)
surface_sides = vtkCellGridComputeSides()
surface_sides.SetInputConnection(reader.GetOutputPort())

edge_sides = vtkCellGridComputeSides()
edge_sides.SetOutputDimensionControl(vtkCellGridSidesQuery.EdgesOfInputs)
edge_sides.OmitSidesForRenderableInputsOff()
edge_sides.SetInputConnection(surface_sides.GetOutputPort())
edge_sides.Update()

# Compute cell centers
cell_centers = vtkCellGridCellCenters()
cell_centers.SetInputConnection(reader.GetOutputPort())
cell_centers.Update()

# Convert centers to unstructured grid for verification
grid_converter = vtkCellGridToUnstructuredGrid()
grid_converter.SetInputConnection(cell_centers.GetOutputPort())
grid_converter.Update()

# Shape mapper (edges)
shape_mapper = vtkCellGridMapper()
shape_mapper.SetInputConnection(edge_sides.GetOutputPort())
shape_mapper.ScalarVisibilityOff()

shape_prop = vtkProperty()
shape_prop.SetOpacity(1.0)
shape_prop.SetLineWidth(1)
shape_prop.SetPointSize(8)
shape_prop.SetColor(0, 0, 0)

shape_actor = vtkActor()
shape_actor.SetMapper(shape_mapper)
shape_actor.SetProperty(shape_prop)

# Center mapper (cell centers as points)
center_mapper = vtkCellGridMapper()
center_mapper.SetInputConnection(cell_centers.GetOutputPort())
center_mapper.ScalarVisibilityOff()

center_prop = vtkProperty()
center_prop.SetOpacity(1.0)
center_prop.SetLineWidth(5)
center_prop.SetPointSize(8)
center_prop.SetColor(1, 0, 0)

center_actor = vtkActor()
center_actor.SetMapper(center_mapper)
center_actor.SetProperty(center_prop)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(shape_actor)
renderer.AddActor(center_actor)
renderer.SetBackground(1.0, 1.0, 1.0)

# Window
render_window = vtkRenderWindow()
render_window.SetMultiSamples(0)
render_window.AddRenderer(renderer)
render_window.SetWindowName("cellgrid cell centers")

# Scene
bounds = [0, 0, 0, 0, 0, 0]
edge_sides.GetOutputDataObject(0).GetBounds(bounds)

camera = renderer.GetActiveCamera()
camera.SetViewUp(0, 1, 0)
camera.SetPosition(5, 2.5, 2.25)
camera.SetFocalPoint(2, 1, 1)
camera.SetDistance(7)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
