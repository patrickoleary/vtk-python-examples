#!/usr/bin/env python

# Demonstrate vtkCellGridTransform applying a rotation to a DG
# hexahedral mesh, with arrow glyphs showing transformed HCurl
# vector attributes alongside the original mesh.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

import os

from vtkmodules.vtkCommonDataModel import vtkCellGridSidesQuery
from vtkmodules.vtkCommonTransforms import vtkTransform
from vtkmodules.vtkFiltersCellGrid import (
    vtkCellGridCellCenters,
    vtkCellGridComputeSides,
    vtkCellGridToUnstructuredGrid,
    vtkCellGridTransform,
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

flag_edges_only = vtkCellGridSidesQuery.EdgesOfInputs

# Read DG hexahedral cell grid
reader = vtkCellGridReader()
reader.SetFileName(os.path.join(data_dir, "dgHexahedra.dg"))

# Original mesh edges (before transform)
original_sides = vtkCellGridComputeSides()
original_sides.SetOutputDimensionControl(flag_edges_only)
original_sides.SetInputConnection(reader.GetOutputPort())

# Apply rotation transform
rotation_transform = vtkTransform()
rotation_transform.RotateZ(-60)

cell_grid_transform = vtkCellGridTransform()
cell_grid_transform.SetTransform(rotation_transform)
cell_grid_transform.SetInputConnection(reader.GetOutputPort())

# Transformed mesh edges
transformed_sides = vtkCellGridComputeSides()
transformed_sides.SetOutputDimensionControl(flag_edges_only)
transformed_sides.SetInputConnection(cell_grid_transform.GetOutputPort())

# Transformed mesh sides for center computation
transform_edge_sides = vtkCellGridComputeSides()
transform_edge_sides.SetOutputDimensionControl(flag_edges_only)
transform_edge_sides.SetInputConnection(cell_grid_transform.GetOutputPort())

# Compute cell centers and convert to unstructured grid
cell_centers = vtkCellGridCellCenters()
cell_centers.SetInputConnection(transform_edge_sides.GetOutputPort())

grid_converter = vtkCellGridToUnstructuredGrid()
grid_converter.SetInputConnection(cell_centers.GetOutputPort())
grid_converter.Update()

# Original shape actor (black edges)
shape_mapper_2 = vtkCellGridMapper()
shape_mapper_2.SetInputConnection(original_sides.GetOutputPort())
shape_mapper_2.ScalarVisibilityOff()

shape_prop_2 = vtkProperty()
shape_prop_2.SetOpacity(1.0)
shape_prop_2.SetLineWidth(1)
shape_prop_2.SetPointSize(8)
shape_prop_2.SetColor(0, 0, 0)

shape_actor_2 = vtkActor()
shape_actor_2.SetMapper(shape_mapper_2)
shape_actor_2.SetProperty(shape_prop_2)

# Transformed shape actor (black edges)
shape_mapper = vtkCellGridMapper()
shape_mapper.SetInputConnection(transform_edge_sides.GetOutputPort())
shape_mapper.ScalarVisibilityOff()

shape_prop = vtkProperty()
shape_prop.SetOpacity(1.0)
shape_prop.SetLineWidth(1)
shape_prop.SetPointSize(8)
shape_prop.SetColor(0, 0, 0)

shape_actor = vtkActor()
shape_actor.SetMapper(shape_mapper)
shape_actor.SetProperty(shape_prop)

# Arrow glyph source for HCurl vector visualization
arrow_source = vtkArrowSource()
arrow_source.SetTipResolution(64)
arrow_source.SetShaftResolution(64)

# Glyph mapper showing curl1 vectors at transformed cell centers
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
renderer.AddActor(shape_actor_2)
renderer.AddActor(glyph_actor)
renderer.SetBackground(1.0, 1.0, 1.0)

# Window
render_window = vtkRenderWindow()
render_window.SetMultiSamples(0)
render_window.AddRenderer(renderer)
render_window.SetWindowName("cellgrid transform")

# Scene
renderer.ResetCamera()
renderer.GetActiveCamera().Zoom(2.0)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
