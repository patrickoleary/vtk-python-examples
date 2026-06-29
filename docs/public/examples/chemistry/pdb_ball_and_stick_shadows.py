#!/usr/bin/env python
# Demonstrate vtkMoleculeMapper with ball-and-stick rendering, shadows, and a ground plane.

import os

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkDomainsChemistry import vtkMoleculeMapper
from vtkmodules.vtkFiltersSources import vtkPlaneSource
from vtkmodules.vtkIOChemistry import vtkPDBReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkLight,
    vtkPolyDataMapper,
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
actor.GetProperty().SetAmbient(0.3)
actor.GetProperty().SetDiffuse(0.7)
actor.GetProperty().SetSpecular(0.4)
actor.GetProperty().SetSpecularPower(40)

# Rendering pipeline.
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.ResetCamera()
renderer.GetActiveCamera().Zoom(1.7)
renderer.SetBackground(0.4, 0.5, 0.6)

render_window = vtkRenderWindow()
render_window.SetSize(450, 450)
render_window.AddRenderer(renderer)
render_window.SetWindowName("pdb ball and stick shadows")

# Ground plane below molecule.
bounds = mol_mapper.GetBounds()
plane = vtkPlaneSource()
plane.SetOrigin(bounds[0], bounds[2], bounds[4])
plane.SetPoint1(bounds[1], bounds[2], bounds[4])
plane.SetPoint2(bounds[0], bounds[2], bounds[5])

plane_mapper = vtkPolyDataMapper()
plane_mapper.SetInputConnection(plane.GetOutputPort())

plane_actor = vtkActor()
plane_actor.SetMapper(plane_mapper)
renderer.AddActor(plane_actor)

# Two lights for shadow casting.
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

# Enable shadows.
renderer.UseShadowsOn()

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
