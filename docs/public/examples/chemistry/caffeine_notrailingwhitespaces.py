#!/usr/bin/env python

# Read caffeine PDB file (no trailing whitespaces variant) and render.

import os

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersCore import vtkGlyph3D, vtkTubeFilter
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkIOChemistry import vtkPDBReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Source
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Read PDB (no trailing whitespaces variant)
pdb_reader = vtkPDBReader()
pdb_reader.SetFileName(os.path.join(data_dir, "caffeine_notrailingspaces.pdb"))
pdb_reader.SetHBScale(1.0)
pdb_reader.SetBScale(1.0)

# Atom glyphs
sphere_source = vtkSphereSource()
sphere_source.SetCenter(0, 0, 0)
sphere_source.SetRadius(1)
sphere_source.SetThetaResolution(8)
sphere_source.SetPhiResolution(8)

glyph_filter = vtkGlyph3D()
glyph_filter.SetInputConnection(pdb_reader.GetOutputPort())
glyph_filter.SetOrient(1)
glyph_filter.SetColorMode(1)
glyph_filter.SetScaleMode(2)
glyph_filter.SetScaleFactor(0.25)
glyph_filter.SetSourceConnection(sphere_source.GetOutputPort())

atom_mapper = vtkPolyDataMapper()
atom_mapper.SetInputConnection(glyph_filter.GetOutputPort())
atom_mapper.UseLookupTableScalarRangeOff()
atom_mapper.SetScalarVisibility(1)
atom_mapper.SetScalarModeToDefault()

atom_actor = vtkActor()
atom_actor.SetMapper(atom_mapper)
atom_actor.GetProperty().SetAmbient(0.15)
atom_actor.GetProperty().SetDiffuse(0.85)
atom_actor.GetProperty().SetSpecular(0.1)
atom_actor.GetProperty().SetSpecularPower(100)

# Bond tubes
tube_filter = vtkTubeFilter()
tube_filter.SetInputConnection(pdb_reader.GetOutputPort())
tube_filter.SetNumberOfSides(8)
tube_filter.SetCapping(0)
tube_filter.SetRadius(0.2)
tube_filter.SetVaryRadius(0)
tube_filter.SetRadiusFactor(10)

bond_mapper = vtkPolyDataMapper()
bond_mapper.SetInputConnection(tube_filter.GetOutputPort())
bond_mapper.UseLookupTableScalarRangeOff()
bond_mapper.SetScalarVisibility(1)
bond_mapper.SetScalarModeToDefault()

bond_actor = vtkActor()
bond_actor.SetMapper(bond_mapper)
bond_actor.GetProperty().SetAmbient(0.15)
bond_actor.GetProperty().SetDiffuse(0.85)
bond_actor.GetProperty().SetSpecular(0.1)
bond_actor.GetProperty().SetSpecularPower(100)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(atom_actor)
renderer.AddActor(bond_actor)
renderer.SetBackground(0, 0, 0)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("caffeine notrailingwhitespaces")
render_window.SetMultiSamples(0)
render_window.SetSize(300, 300)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.ResetCamera()

interactor.Initialize()
interactor.Start()
