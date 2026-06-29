#!/usr/bin/env python

# Write a sphere to PLY in multiple color modes, read back, and render.

import os
import tempfile

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import vtkLookupTable
from vtkmodules.vtkFiltersCore import vtkPointDataToCellData, vtkSimpleElevationFilter
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkIOPLY import vtkPLYReader, vtkPLYWriter
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Source
temp_dir = tempfile.mkdtemp()
ply_filename = os.path.join(temp_dir, "plyWriter.ply")

sphere_source = vtkSphereSource()
sphere_source.SetPhiResolution(10)
sphere_source.SetThetaResolution(20)

# Filter
elevation_filter = vtkSimpleElevationFilter()
elevation_filter.SetInputConnection(sphere_source.GetOutputPort())

point_to_cell = vtkPointDataToCellData()
point_to_cell.SetInputConnection(elevation_filter.GetOutputPort())

# Write 1: uniform cell color (red)
cell_color_writer = vtkPLYWriter()
cell_color_writer.SetInputConnection(point_to_cell.GetOutputPort())
cell_color_writer.SetFileName(ply_filename)
cell_color_writer.SetFileTypeToBinary()
cell_color_writer.SetDataByteOrderToLittleEndian()
cell_color_writer.SetColorModeToUniformCellColor()
cell_color_writer.SetColor(255, 0, 0)
cell_color_writer.Write()

cell_color_reader = vtkPLYReader()
cell_color_reader.SetFileName(ply_filename)
cell_color_reader.Update()

cell_color_mapper = vtkPolyDataMapper()
cell_color_mapper.SetInputConnection(cell_color_reader.GetOutputPort())

cell_color_actor = vtkActor()
cell_color_actor.SetMapper(cell_color_mapper)

# Write 2: map through lookup table
elevation_lut = vtkLookupTable()
elevation_lut.Build()

lut_writer = vtkPLYWriter()
lut_writer.SetInputConnection(point_to_cell.GetOutputPort())
lut_writer.SetFileName(ply_filename)
lut_writer.SetFileTypeToBinary()
lut_writer.SetDataByteOrderToLittleEndian()
lut_writer.SetColorModeToDefault()
lut_writer.SetLookupTable(elevation_lut)
lut_writer.SetArrayName("Elevation")
lut_writer.SetComponent(0)
lut_writer.Write()

lut_reader = vtkPLYReader()
lut_reader.SetFileName(ply_filename)
lut_reader.Update()

lut_mapper = vtkPolyDataMapper()
lut_mapper.SetInputConnection(lut_reader.GetOutputPort())

lut_actor = vtkActor()
lut_actor.SetMapper(lut_mapper)
lut_actor.AddPosition(1, 0, 0)

# Write 3: read previous RGB and re-write
rgb_input_reader = vtkPLYReader()
rgb_input_reader.SetFileName(ply_filename)
rgb_input_reader.Update()

rgb_writer = vtkPLYWriter()
rgb_writer.SetInputConnection(rgb_input_reader.GetOutputPort())
rgb_writer.SetFileName(ply_filename)
rgb_writer.SetFileTypeToBinary()
rgb_writer.SetDataByteOrderToLittleEndian()
rgb_writer.SetColorModeToDefault()
rgb_writer.SetArrayName("RGB")
rgb_writer.SetComponent(0)
rgb_writer.Write()

rgb_reader = vtkPLYReader()
rgb_reader.SetFileName(ply_filename)
rgb_reader.Update()

rgb_mapper = vtkPolyDataMapper()
rgb_mapper.SetInputConnection(rgb_reader.GetOutputPort())

rgb_actor = vtkActor()
rgb_actor.SetMapper(rgb_mapper)
rgb_actor.AddPosition(2, 0, 0)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(cell_color_actor)
renderer.AddActor(lut_actor)
renderer.AddActor(rgb_actor)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("ply read write")
render_window.SetMultiSamples(0)
render_window.SetSize(330, 120)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
render_window.Render()
renderer.GetActiveCamera().Zoom(3.0)

interactor.Initialize()
interactor.Start()
