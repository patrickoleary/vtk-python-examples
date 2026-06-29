#!/usr/bin/env python

# Read an XYZ molecule file with vtkXYZMolReader2 and render with ball-and-stick.

import os

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkDomainsChemistry import vtkMoleculeMapper, vtkSimpleBondPerceiver
from vtkmodules.vtkIOChemistry import vtkXYZMolReader2
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Source
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Read XYZ file
xyz_reader = vtkXYZMolReader2()
xyz_reader.SetFileName(os.path.join(data_dir, "nanowireTB23K298.xyz"))
xyz_reader.Update()

# Perceive bonds
bond_perceiver = vtkSimpleBondPerceiver()
bond_perceiver.SetInputConnection(xyz_reader.GetOutputPort())
bond_perceiver.SetTolerance(0.7)
bond_perceiver.Update()

# Molecule mapper + actor
molecule_mapper = vtkMoleculeMapper()
molecule_mapper.SetInputConnection(bond_perceiver.GetOutputPort())
molecule_mapper.UseBallAndStickSettings()

molecule_actor = vtkActor()
molecule_actor.SetMapper(molecule_mapper)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(molecule_actor)
renderer.SetBackground(0.9, 0.9, 0.9)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("molecule xyz")
render_window.SetMultiSamples(0)
render_window.SetSize(600, 600)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.ResetCamera()

interactor.Initialize()
interactor.Start()
