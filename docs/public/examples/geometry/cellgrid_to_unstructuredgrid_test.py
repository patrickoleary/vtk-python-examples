#!/usr/bin/env python

# Demonstrate vtkCellGridToUnstructuredGrid converting DG hexahedral
# cell centers to an unstructured grid, with arrow glyphs showing
# HCurl vector attributes.

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
from vtkmodules.vtkFiltersSources import vtkArrowSource
from vtkmodules.vtkIOCellGrid import vtkCellGridReader
from vtkmodules.vtkRenderingCellGrid import vtkRenderingCellGrid
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkCellGridMapper,
    vtkGlyph3DMapper,
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

flag_edges_verts = vtkCellGridSidesQuery.EdgesOfInputs | vtkCellGridSidesQuery.VerticesOfInputs
flag_edges_only = vtkCellGridSidesQuery.EdgesOfInputs

# Compute sides (edges + vertices for shape, edges only for display)
edge_sides = vtkCellGridComputeSides()
edge_sides.SetOutputDimensionControl(flag_edges_verts)
edge_sides.SetInputConnection(reader.GetOutputPort())
edge_sides.Update()

# Compute cell centers and convert to unstructured grid
cell_centers = vtkCellGridCellCenters()
cell_centers.SetInputConnection(edge_sides.GetOutputPort())

grid_converter = vtkCellGridToUnstructuredGrid()
grid_converter.SetInputConnection(cell_centers.GetOutputPort())
grid_converter.Update()

# Shape actor (edges)
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

# Arrow glyph source for vector visualization
arrow_source = vtkArrowSource()
arrow_source.SetTipResolution(64)
arrow_source.SetShaftResolution(64)

# Glyph mapper showing curl1 vectors at cell centers
glyph_mapper = vtkGlyph3DMapper()
glyph_mapper.SetInputConnection(grid_converter.GetOutputPort())
glyph_mapper.SetSourceConnection(arrow_source.GetOutputPort())
glyph_mapper.SetArrayComponent(-1)
glyph_mapper.SetOrient(True)
glyph_mapper.SetOrientationArray("curl1")
glyph_mapper.SetScaling(True)
glyph_mapper.SetScaleMode(vtkGlyph3DMapper.SCALE_BY_MAGNITUDE)
glyph_mapper.SetScaleArray("curl1")
glyph_mapper.SetScaleFactor(0.25)
glyph_mapper.SelectColorArray("scalar1")

glyph_prop = vtkProperty()
glyph_prop.SetLineWidth(5)
glyph_prop.SetPointSize(4)
glyph_prop.SetColor(0.5, 0.5, 0.75)

glyph_actor = vtkActor()
glyph_actor.SetMapper(glyph_mapper)
glyph_actor.SetProperty(glyph_prop)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(shape_actor)
renderer.AddActor(glyph_actor)
renderer.SetBackground(1.0, 1.0, 1.0)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("cellgrid to unstructuredgrid test")

# Scene
renderer.ResetCamera()
renderer.GetActiveCamera().Zoom(2.0)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
