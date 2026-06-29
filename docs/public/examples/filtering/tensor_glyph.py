#!/usr/bin/env python

# Visualize tensor data using vtkTensorGlyph with five different glyph
# configurations: color off, no eigenvalue extraction, three glyphs,
# symmetric three glyphs, and 6-component symmetric tensors.

import os

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersCore import (
    vtkPolyDataNormals,
    vtkTensorGlyph,
)
from vtkmodules.vtkFiltersModeling import vtkOutlineFilter
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkIOLegacy import vtkDataSetReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Data file path (relative to this script)
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Reader: tensor data
reader = vtkDataSetReader()
reader.SetFileName(os.path.join(data_dir, "tensors.vtk"))

# Glyph source
glyph_source = vtkSphereSource()
glyph_source.SetRadius(0.5)
glyph_source.SetCenter(0.5, 0.0, 0.0)

# --- Glyph 1: color off ---
glyph_1 = vtkTensorGlyph()
glyph_1.SetInputConnection(reader.GetOutputPort())
glyph_1.SetSourceConnection(glyph_source.GetOutputPort())
glyph_1.SetScaleFactor(0.25)
glyph_1.ColorGlyphsOff()

normals_1 = vtkPolyDataNormals()
normals_1.SetInputConnection(glyph_1.GetOutputPort())

mapper_1 = vtkPolyDataMapper()
mapper_1.SetInputConnection(normals_1.GetOutputPort())

actor_1 = vtkActor()
actor_1.SetMapper(mapper_1)

outline_1 = vtkOutlineFilter()
outline_1.SetInputConnection(reader.GetOutputPort())

outline_mapper_1 = vtkPolyDataMapper()
outline_mapper_1.SetInputConnection(outline_1.GetOutputPort())

outline_actor_1 = vtkActor()
outline_actor_1.SetMapper(outline_mapper_1)

# --- Glyph 2: no eigenvalue extraction ---
glyph_2 = vtkTensorGlyph()
glyph_2.SetInputConnection(reader.GetOutputPort())
glyph_2.SetSourceConnection(glyph_source.GetOutputPort())
glyph_2.SetScaleFactor(0.25)
glyph_2.ExtractEigenvaluesOff()

normals_2 = vtkPolyDataNormals()
normals_2.SetInputConnection(glyph_2.GetOutputPort())

mapper_2 = vtkPolyDataMapper()
mapper_2.SetInputConnection(normals_2.GetOutputPort())

actor_2 = vtkActor()
actor_2.SetMapper(mapper_2)
actor_2.SetPosition(2.0, 0.0, 0.0)

outline_actor_2 = vtkActor()
outline_actor_2.SetMapper(outline_mapper_1)
outline_actor_2.SetPosition(2.0, 0.0, 0.0)

# --- Glyph 3: three glyphs, color by eigenvalues ---
glyph_3 = vtkTensorGlyph()
glyph_3.SetInputConnection(reader.GetOutputPort())
glyph_3.SetSourceConnection(glyph_source.GetOutputPort())
glyph_3.SetScaleFactor(0.25)
glyph_3.SetColorModeToEigenvalues()
glyph_3.ThreeGlyphsOn()

normals_3 = vtkPolyDataNormals()
normals_3.SetInputConnection(glyph_3.GetOutputPort())

mapper_3 = vtkPolyDataMapper()
mapper_3.SetInputConnection(normals_3.GetOutputPort())

actor_3 = vtkActor()
actor_3.SetMapper(mapper_3)
actor_3.SetPosition(0.0, 2.0, 0.0)

outline_actor_3 = vtkActor()
outline_actor_3.SetMapper(outline_mapper_1)
outline_actor_3.SetPosition(0.0, 2.0, 0.0)

# --- Glyph 4: symmetric three glyphs ---
glyph_4 = vtkTensorGlyph()
glyph_4.SetInputConnection(reader.GetOutputPort())
glyph_4.SetSourceConnection(glyph_source.GetOutputPort())
glyph_4.SetScaleFactor(0.25)
glyph_4.SetColorModeToEigenvalues()
glyph_4.ThreeGlyphsOn()
glyph_4.SymmetricOn()

normals_4 = vtkPolyDataNormals()
normals_4.SetInputConnection(glyph_4.GetOutputPort())

mapper_4 = vtkPolyDataMapper()
mapper_4.SetInputConnection(normals_4.GetOutputPort())

actor_4 = vtkActor()
actor_4.SetMapper(mapper_4)
actor_4.SetPosition(2.0, 2.0, 0.0)

outline_actor_4 = vtkActor()
outline_actor_4.SetMapper(outline_mapper_1)
outline_actor_4.SetPosition(2.0, 2.0, 0.0)

# --- Glyph 5: 6-component symmetric tensors ---
glyph_5 = vtkTensorGlyph()
glyph_5.SetInputConnection(reader.GetOutputPort())
glyph_5.SetSourceConnection(glyph_source.GetOutputPort())
glyph_5.SetScaleFactor(0.25)
glyph_5.SetInputArrayToProcess(0, 0, 0, 0, "symTensors1")

normals_5 = vtkPolyDataNormals()
normals_5.SetInputConnection(glyph_5.GetOutputPort())

mapper_5 = vtkPolyDataMapper()
mapper_5.SetInputConnection(normals_5.GetOutputPort())

actor_5 = vtkActor()
actor_5.SetMapper(mapper_5)
actor_5.SetPosition(4.0, 2.0, 0.0)

outline_actor_5 = vtkActor()
outline_actor_5.SetMapper(outline_mapper_1)
outline_actor_5.SetPosition(4.0, 2.0, 0.0)

# Update scalar ranges
glyph_1.Update()
scalars_1 = glyph_1.GetOutput().GetPointData().GetScalars()
if scalars_1:
    mapper_1.SetScalarRange(scalars_1.GetRange())

glyph_2.Update()
scalars_2 = glyph_2.GetOutput().GetPointData().GetScalars()
if scalars_2:
    mapper_2.SetScalarRange(scalars_2.GetRange())

glyph_3.Update()
scalars_3 = glyph_3.GetOutput().GetPointData().GetScalars()
if scalars_3:
    mapper_3.SetScalarRange(scalars_3.GetRange())

glyph_4.Update()
scalars_4 = glyph_4.GetOutput().GetPointData().GetScalars()
if scalars_4:
    mapper_4.SetScalarRange(scalars_4.GetRange())

glyph_5.Update()
scalars_5 = glyph_5.GetOutput().GetPointData().GetScalars()
if scalars_5:
    mapper_5.SetScalarRange(scalars_5.GetRange())

# Renderer
renderer = vtkRenderer()
renderer.SetBackground(0.5, 0.5, 0.5)
renderer.AddActor(actor_1)
renderer.AddActor(outline_actor_1)
renderer.AddActor(actor_2)
renderer.AddActor(outline_actor_2)
renderer.AddActor(actor_3)
renderer.AddActor(outline_actor_3)
renderer.AddActor(actor_4)
renderer.AddActor(outline_actor_4)
renderer.AddActor(actor_5)
renderer.AddActor(outline_actor_5)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("tensor glyph")

# Scene
renderer.ResetCamera()
camera = renderer.GetActiveCamera()
camera.Azimuth(-20)
camera.Elevation(20)
camera.Zoom(1.1)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
