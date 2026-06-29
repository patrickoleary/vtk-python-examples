#!/usr/bin/env python
# Demonstrate vtkMoleculeMapper with ball-and-stick rendering of a PDB protein.

import os

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkDomainsChemistry import vtkMoleculeMapper
from vtkmodules.vtkIOChemistry import vtkPDBReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkLight,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Read protein from PDB file.
reader = vtkPDBReader()
reader.SetFileName(os.path.join(data_dir, "2LYZ.pdb"))
reader.Update()

# Molecule mapper with ball-and-stick settings (output port 1 is molecule).
mol_mapper = vtkMoleculeMapper()
mol_mapper.SetInputConnection(reader.GetOutputPort(1))
mol_mapper.UseBallAndStickSettings()

# Actor with material properties.
actor = vtkActor()
actor.SetMapper(mol_mapper)
actor.GetProperty().SetAmbient(0.0)
actor.GetProperty().SetDiffuse(1.0)
actor.GetProperty().SetSpecular(0.0)
actor.GetProperty().SetSpecularPower(40)

# Camera light.
light = vtkLight()
light.SetLightTypeToCameraLight()
light.SetPosition(1.0, 1.0, 1.0)

# Rendering pipeline.
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.ResetCamera()
renderer.GetActiveCamera().Zoom(1.7)
renderer.SetBackground(0.0, 0.0, 0.0)

render_window = vtkRenderWindow()
render_window.SetSize(450, 450)
render_window.AddRenderer(renderer)
render_window.SetWindowName("pdb ball and stick")
render_window.Render()

# Reset camera to standard position.
renderer.GetActiveCamera().SetPosition(0, 0, 1)
renderer.GetActiveCamera().SetFocalPoint(0, 0, 0)
renderer.GetActiveCamera().SetViewUp(0, 1, 0)
renderer.ResetCamera()
renderer.GetActiveCamera().Zoom(1.7)

render_window.SetMultiSamples(0)

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
