#!/usr/bin/env python

# Demonstrate vtkArrayRenderer for rendering DG cell grids with custom shaders.

import os
import sys

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import vtkStringToken
from vtkmodules.vtkFiltersCellGrid import vtkCellGridComputeSides
from vtkmodules.vtkFiltersSources import vtkCubeSource, vtkOutlineCornerFilter
from vtkmodules.vtkInteractionWidgets import vtkCameraOrientationWidget
from vtkmodules.vtkIOCellGrid import vtkCellGridReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)
from vtkmodules.vtkRenderingOpenGL2 import vtkArrayRenderer

# Import shader sources from the shaders subdirectory
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from shaders import vertShaderSource, fragShaderSource

# Data path
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))
filename = os.path.join(data_dir, "dgTetrahedra.dg")

cell_att_name = vtkStringToken("scalar2")
cell_att_type = vtkStringToken("DG HGRAD C1")

# Pipeline
reader = vtkCellGridReader()
reader.SetFileName(filename)
compute_sides = vtkCellGridComputeSides()
compute_sides.SetInputConnection(reader.GetOutputPort())
compute_sides.Update()

# Grab the cell-grid surface
cell_grid = compute_sides.GetOutputDataObject(0)
bounds = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
cell_grid.GetBounds(bounds)

# Mapper + Actor
array_renderer = vtkArrayRenderer()
array_renderer.SetInputDataObject(0, cell_grid)
array_renderer.SetNumberOfElements(1)
array_renderer.SetElementType(vtkArrayRenderer.Triangle)
array_renderer.SetVertexShaderSource(vertShaderSource)
array_renderer.SetFragmentShaderSource(fragShaderSource)

# Bind tetrahedron-specific metadata textures
side_offsets = cell_grid.GetCellType("vtkDGTet").GetSideOffsetsAndShapes()
array_renderer.BindArrayToTexture("side_offsets", side_offsets)
side_local = cell_grid.GetCellType("vtkDGTet").GetSideConnectivity()
array_renderer.BindArrayToTexture("side_local", side_local)
cell_parametrics = cell_grid.GetCellType("vtkDGTet").GetReferencePoints()
array_renderer.BindArrayToTexture("cell_parametrics", cell_parametrics)

# Bind (cell, side) tuples
side_conn = cell_grid.GetAttributes(vtkStringToken("triangle sides of vtkDGTet")).GetScalars()
array_renderer.BindArrayToTexture(vtkStringToken("sides"), side_conn)
array_renderer.SetNumberOfInstances(side_conn.GetNumberOfTuples())

dg_actor = vtkActor()
dg_actor.SetMapper(array_renderer)

# Bind attribute data (connectivity and value arrays)
field_range = [1, -1]
for att_id in cell_grid.GetUnorderedCellAttributeIds():
    cell_att = cell_grid.GetCellAttributeById(att_id)
    conn = cell_att.GetArrayForCellTypeAndRole("vtkDGTet", "connectivity")
    vals = cell_att.GetArrayForCellTypeAndRole("vtkDGTet", "values")
    if cell_att.GetName() == cell_att_name:
        cname = vtkStringToken("field_conn")
        vname = vtkStringToken("field_vals")
        array_renderer.BindArrayToTexture(cname, conn, True)
        array_renderer.BindArrayToTexture(vname, vals, True)
        array_renderer.PrepareColormap(None)
        cell_grid.GetCellAttributeRange(cell_att, 0, field_range, True)
        if field_range[0] > field_range[1]:
            field_range = [-1e-11, 1e-11]
        dg_actor.GetShaderProperty().GetFragmentCustomUniforms().SetUniform3f(
            "field_range", (field_range[0], field_range[1], field_range[1] - field_range[0]))
    elif cell_att == cell_grid.GetShapeAttribute():
        cname = vtkStringToken("shape_conn")
        vname = vtkStringToken("shape_vals")
        array_renderer.BindArrayToTexture(cname, conn, True)
        array_renderer.BindArrayToTexture(vname, vals, False)

# Unit cube outline
cube_source = vtkCubeSource()
corner_filter = vtkOutlineCornerFilter()
corner_filter.SetInputConnection(cube_source.GetOutputPort())

cube_mapper = vtkPolyDataMapper()
cube_mapper.SetInputConnection(corner_filter.GetOutputPort())

cube_actor = vtkActor()
cube_actor.SetMapper(cube_mapper)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(dg_actor)
renderer.AddActor(cube_actor)
renderer.SetBackground(0.5, 0.5, 0.8)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("array")

# Interactor
interactor = render_window.MakeRenderWindowInteractor()

# Scene
renderer.ResetCamera()
orientation_widget = vtkCameraOrientationWidget()
orientation_widget.SetParentRenderer(renderer)
orientation_widget.On()

interactor.Initialize()
interactor.Start()
