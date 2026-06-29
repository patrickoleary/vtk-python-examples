#!/usr/bin/env python

# Write a PLY file with alpha from elevation, then read and render it.

import os
import tempfile

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import vtkLookupTable
from vtkmodules.vtkFiltersCore import vtkElevationFilter
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
ply_output_file = os.path.join(temp_dir, "plyAlpha.ply")

sphere_source = vtkSphereSource()
sphere_source.SetPhiResolution(20)
sphere_source.SetThetaResolution(20)

# Filter
elevation_filter = vtkElevationFilter()
elevation_filter.SetInputConnection(sphere_source.GetOutputPort())
elevation_filter.SetLowPoint(-0.5, -0.5, -0.5)
elevation_filter.SetHighPoint(0.5, 0.5, 0.5)

alpha_lut = vtkLookupTable()
alpha_lut.SetTableRange(0, 1)
alpha_lut.SetAlphaRange(0, 1.0)
alpha_lut.Build()

ply_writer = vtkPLYWriter()
ply_writer.SetFileName(ply_output_file)
ply_writer.SetFileTypeToBinary()
ply_writer.EnableAlphaOn()
ply_writer.SetColorModeToDefault()
ply_writer.SetArrayName("Elevation")
ply_writer.SetLookupTable(alpha_lut)
ply_writer.SetInputConnection(elevation_filter.GetOutputPort())
ply_writer.Write()

readback_reader = vtkPLYReader()
readback_reader.SetFileName(ply_output_file)

# Mapper
alpha_mapper = vtkPolyDataMapper()
alpha_mapper.SetInputConnection(readback_reader.GetOutputPort())
alpha_mapper.ScalarVisibilityOn()

# Actor
alpha_actor = vtkActor()
alpha_actor.SetMapper(alpha_mapper)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(alpha_actor)
renderer.SetBackground(0, 0, 0)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("ply writer alpha")
render_window.SetMultiSamples(0)
render_window.SetSize(300, 300)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
interactor.Initialize()
interactor.Start()
