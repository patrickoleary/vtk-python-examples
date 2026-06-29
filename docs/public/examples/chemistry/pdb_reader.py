#!/usr/bin/env python

# Read a PDB file and render the protein structure.

import os

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

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

# Read PDB file
pdb_reader = vtkPDBReader()
pdb_reader.SetFileName(os.path.join(data_dir, "6VWW.pdb"))
pdb_reader.Update()

# Mapper + Actor
protein_mapper = vtkPolyDataMapper()
protein_mapper.SetInputConnection(pdb_reader.GetOutputPort())
protein_mapper.SetScalarModeToUsePointFieldData()
protein_mapper.SelectColorArray("rgb_colors")
protein_mapper.SetColorModeToDirectScalars()

protein_actor = vtkActor()
protein_actor.SetMapper(protein_mapper)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(protein_actor)
renderer.SetBackground(0.2, 0.3, 0.4)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("pdb reader")
render_window.SetMultiSamples(0)
render_window.SetSize(600, 600)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.ResetCamera()

interactor.Initialize()
interactor.Start()
