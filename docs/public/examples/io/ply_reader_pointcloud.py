#!/usr/bin/env python

# Read a PLY point cloud and render with sphere glyphs.

import os

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersCore import vtkGlyph3D
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkIOPLY import vtkPLYReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Source
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

ply_reader = vtkPLYReader()
ply_reader.SetFileName(os.path.join(data_dir, "PointCloud.ply"))
ply_reader.Update()

bounds = ply_reader.GetOutput().GetBounds()
range_x = bounds[1] - bounds[0]
radius = range_x * 0.05

sphere_source = vtkSphereSource()
sphere_source.SetRadius(radius)

# Filter
sphere_glyph = vtkGlyph3D()
sphere_glyph.SetInputConnection(ply_reader.GetOutputPort())
sphere_glyph.SetSourceConnection(sphere_source.GetOutputPort())
sphere_glyph.ScalingOff()
sphere_glyph.SetColorModeToColorByScalar()
sphere_glyph.Update()

# Mapper / Actor - points
point_mapper = vtkPolyDataMapper()
point_mapper.SetInputConnection(ply_reader.GetOutputPort())
point_mapper.ScalarVisibilityOn()

point_actor = vtkActor()
point_actor.SetMapper(point_mapper)

# Mapper / Actor - glyphs
glyph_mapper = vtkPolyDataMapper()
glyph_mapper.SetInputConnection(sphere_glyph.GetOutputPort())

glyph_actor = vtkActor()
glyph_actor.SetMapper(glyph_mapper)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(point_actor)
renderer.AddActor(glyph_actor)
renderer.SetBackground(0.4, 0.5, 0.7)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("ply reader pointcloud")
render_window.SetMultiSamples(0)
render_window.SetSize(300, 300)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
interactor.Initialize()
interactor.Start()
