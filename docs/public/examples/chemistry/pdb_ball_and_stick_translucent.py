#!/usr/bin/env python
# Demonstrate vtkMoleculeMapper with translucent ball-and-stick rendering of caffeine.

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

# Read caffeine from PDB file.
reader = vtkPDBReader()
reader.SetFileName(os.path.join(data_dir, "caffeine.pdb"))
reader.Update()

# Molecule mapper with ball-and-stick settings (output port 1 is molecule).
mol_mapper = vtkMoleculeMapper()
mol_mapper.SetInputConnection(reader.GetOutputPort(1))
mol_mapper.UseBallAndStickSettings()

# Translucent actor.
actor = vtkActor()
actor.SetMapper(mol_mapper)
actor.GetProperty().SetOpacity(0.4)

# Rendering pipeline.
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(1.0, 1.0, 1.0)

render_window = vtkRenderWindow()
render_window.SetSize(450, 450)
render_window.AddRenderer(renderer)
render_window.SetWindowName("pdb ball and stick translucent")

# Two lights.
light_1 = vtkLight()
light_1.SetFocalPoint(0, 0, 0)
light_1.SetPosition(0, 1, 0.2)
light_1.SetColor(0.95, 0.97, 1.0)
light_1.SetIntensity(0.8)
renderer.AddLight(light_1)

light_2 = vtkLight()
light_2.SetFocalPoint(0, 0, 0)
light_2.SetPosition(1.0, 1.0, 1.0)
light_2.SetColor(1.0, 0.8, 0.7)
light_2.SetIntensity(0.3)
renderer.AddLight(light_2)

# Camera setup.
renderer.GetActiveCamera().SetPosition(0, 0, 1)
renderer.GetActiveCamera().SetFocalPoint(0, 0, 0)
renderer.GetActiveCamera().SetViewUp(0, 1, 0)
renderer.ResetCamera()
renderer.GetActiveCamera().Zoom(3.0)

render_window.SetMultiSamples(0)

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
