#!/usr/bin/env python

# Read a CML molecule file and render using ball-and-stick representation.

import os

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkDomainsChemistry import vtkMoleculeMapper
from vtkmodules.vtkIOChemistry import vtkCMLMoleculeReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Source
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Read the CML file
cml_reader = vtkCMLMoleculeReader()
cml_reader.SetFileName(os.path.join(data_dir, "porphyrin.cml"))

# Molecule mapper
molecule_mapper = vtkMoleculeMapper()
molecule_mapper.SetInputConnection(cml_reader.GetOutputPort())
molecule_mapper.UseBallAndStickSettings()

# Actor
molecule_actor = vtkActor()
molecule_actor.SetMapper(molecule_mapper)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(molecule_actor)
renderer.SetBackground(0.0, 0.0, 0.0)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("cml molecule reader")
render_window.SetMultiSamples(0)
render_window.SetSize(450, 450)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.ResetCamera()
renderer.GetActiveCamera().Zoom(2.0)

interactor.Initialize()
interactor.Start()
