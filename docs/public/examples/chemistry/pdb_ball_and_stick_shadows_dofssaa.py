#!/usr/bin/env python
# Demonstrate vtkOpenGLMoleculeMapper with shadows, depth of field, and SSAA passes.

import os

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import vtkLookupTable
from vtkmodules.vtkDomainsChemistry import vtkMoleculeMapper, vtkPeriodicTable
from vtkmodules.vtkDomainsChemistryOpenGL2 import vtkOpenGLMoleculeMapper
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
from vtkmodules.vtkRenderingOpenGL2 import (
    vtkCameraPass,
    vtkDepthOfFieldPass,
    vtkRenderPassCollection,
    vtkSSAAPass,
    vtkSequencePass,
    vtkShadowMapPass,
)

data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Read protein from PDB file.
reader = vtkPDBReader()
reader.SetFileName(os.path.join(data_dir, "2LYZ.pdb"))
reader.Update()

# OpenGL molecule mapper with VDW radii, no bonds.
mol_mapper = vtkOpenGLMoleculeMapper()
mol_mapper.SetInputConnection(reader.GetOutputPort(1))
mol_mapper.SetRenderBonds(False)
mol_mapper.SetAtomicRadiusType(vtkMoleculeMapper.VDWRadius)
mol_mapper.SetAtomicRadiusScaleFactor(0.9)

# Desaturate the default periodic table lookup table.
periodic_table = vtkPeriodicTable()
lookup_table = vtkLookupTable()
periodic_table.GetDefaultLUT(lookup_table)
num_colors = lookup_table.GetNumberOfColors()
for i in range(num_colors):
    rgb = lookup_table.GetTableValue(i)
    lookup_table.SetTableValue(i, 0.45 + rgb[0] * 0.55, 0.45 + rgb[1] * 0.55, 0.45 + rgb[2] * 0.55)
mol_mapper.SetLookupTable(lookup_table)

# Actor with material properties.
actor = vtkActor()
actor.SetMapper(mol_mapper)
actor.GetProperty().SetAmbient(0.3)
actor.GetProperty().SetDiffuse(0.7)
actor.GetProperty().SetSpecular(0.4)
actor.GetProperty().SetSpecularPower(40)

# Shader replacement for ambient color.
shader_property = actor.GetShaderProperty()
shader_property.AddFragmentShaderReplacement(
    "//VTK::Color::Impl",
    True,
    "//VTK::Color::Impl\n  ambientColor = diffuseColor*0.2;\n",
    False,
)

# Rendering pipeline.
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.ResetCamera()
renderer.GetActiveCamera().Zoom(1.7)
renderer.GetActiveCamera().SetFocalDisk(renderer.GetActiveCamera().GetDistance() * 0.05)
renderer.SetBackground2(0.2, 0.2, 0.3)
renderer.SetBackground(0.1, 0.1, 0.15)
renderer.GradientBackgroundOn()

render_window = vtkRenderWindow()
render_window.SetSize(600, 600)
render_window.AddRenderer(renderer)
render_window.SetWindowName("pdb ball and stick shadows dofssaa")

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

# Lights with shadow attenuation.
light_1 = vtkLight()
light_1.SetFocalPoint(0, 0, 0)
light_1.SetPosition(-0.3, 0.9, 0.3)
light_1.SetIntensity(0.5)
light_1.SetShadowAttenuation(0.6)
renderer.AddLight(light_1)

light_2 = vtkLight()
light_2.SetFocalPoint(0, 0, 0)
light_2.SetPosition(0.3, 0.9, 0.3)
light_2.SetIntensity(0.5)
light_2.SetShadowAttenuation(0.6)
renderer.AddLight(light_2)

# Shadow map pass pipeline.
shadows = vtkShadowMapPass()

sequence_pass = vtkSequencePass()
passes = vtkRenderPassCollection()
passes.AddItem(shadows.GetShadowMapBakerPass())
passes.AddItem(shadows)
sequence_pass.SetPasses(passes)

camera_pass = vtkCameraPass()
camera_pass.SetDelegatePass(sequence_pass)

# Depth of field pass.
dof_pass = vtkDepthOfFieldPass()
dof_pass.SetDelegatePass(camera_pass)

# SSAA pass.
ssaa_pass = vtkSSAAPass()
ssaa_pass.SetDelegatePass(dof_pass)

# Set render pass pipeline on OpenGL renderer.
renderer.SetPass(ssaa_pass)

render_window.Render()

# Reset camera to final position.
renderer.GetActiveCamera().SetPosition(0, 0, 1)
renderer.GetActiveCamera().SetFocalPoint(0, 0, 0)
renderer.GetActiveCamera().SetViewUp(0, 1, 0)
renderer.ResetCamera()
renderer.GetActiveCamera().Elevation(40.0)
renderer.GetActiveCamera().Zoom(2.0)

render_window.SetMultiSamples(0)

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
