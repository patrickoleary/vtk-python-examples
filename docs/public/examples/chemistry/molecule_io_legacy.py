#!/usr/bin/env python
# Demonstrate molecule round-trip through legacy IO writer/reader with lattice info.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonDataModel import vtkMolecule, vtkVector3d
from vtkmodules.vtkDomainsChemistry import vtkMoleculeMapper
from vtkmodules.vtkIOLegacy import vtkGenericDataObjectReader, vtkGenericDataObjectWriter
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkLight,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Build molecule.
mol = vtkMolecule()
mol.Initialize()

o1 = mol.AppendAtom(8, 3.0088731969, 1.1344098673, 0.9985902874)
o2 = mol.AppendAtom(8, -0.2616286966, 2.7806709534, 0.7027800226)
c1 = mol.AppendAtom(6, -2.0738607910, 1.2298524695, 0.3421802228)
c2 = mol.AppendAtom(6, -1.4140240045, 0.1045928523, 0.0352265378)
c3 = mol.AppendAtom(6, 0.0000000000, 0.0000000000, 0.0000000000)
c4 = mol.AppendAtom(6, 1.2001889412, 0.0000000000, 0.0000000000)
c5 = mol.AppendAtom(6, -1.4612030913, 2.5403617582, 0.6885503164)
c6 = mol.AppendAtom(6, 2.6528126498, 0.1432895796, 0.0427014196)
h1 = mol.AppendAtom(1, -3.1589178142, 1.2268537165, 0.3536340040)
h2 = mol.AppendAtom(1, -1.9782163251, -0.7930325394, -0.1986937306)
h3 = mol.AppendAtom(1, 3.0459155564, 0.4511167867, -0.9307386568)
h4 = mol.AppendAtom(1, 3.1371551056, -0.7952192984, 0.3266426961)
h5 = mol.AppendAtom(1, 2.3344947615, 1.8381683043, 0.9310726537)
h6 = mol.AppendAtom(1, -2.1991803919, 3.3206134015, 0.9413825084)

mol.AppendBond(c1, c5, 1)
mol.AppendBond(c1, c2, 2)
mol.AppendBond(c2, c3, 1)
mol.AppendBond(c3, c4, 3)
mol.AppendBond(c4, c6, 1)
mol.AppendBond(c5, o2, 2)
mol.AppendBond(c6, o1, 1)
mol.AppendBond(c5, h6, 1)
mol.AppendBond(c1, h1, 1)
mol.AppendBond(c2, h2, 1)
mol.AppendBond(c6, h3, 1)
mol.AppendBond(c6, h4, 1)
mol.AppendBond(o1, h5, 1)

# Set lattice info.
mol.SetLattice(vtkVector3d(8.0, 0.0, 0.0), vtkVector3d(0.0, 6.0, 0.0), vtkVector3d(0.0, 0.0, 4.0))
mol.SetLatticeOrigin(vtkVector3d(-4.0, -2.0, -2.0))

# Write molecule to string via legacy writer.
writer = vtkGenericDataObjectWriter()
writer.SetInputData(mol)
writer.WriteToOutputStringOn()
writer.Write()

# Read molecule back via legacy reader.
reader = vtkGenericDataObjectReader()
reader.ReadFromInputStringOn()
reader.SetInputString(writer.GetOutputString())
reader.Update()

# Molecule mapper with ball-and-stick settings.
mol_mapper = vtkMoleculeMapper()
mol_mapper.SetInputConnection(reader.GetOutputPort())
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
renderer.SetBackground(0.0, 0.0, 0.0)

render_window = vtkRenderWindow()
render_window.SetSize(450, 450)
render_window.SetMultiSamples(0)
render_window.AddRenderer(renderer)
render_window.SetWindowName("molecule io legacy")

render_window.Render()
renderer.ResetCameraClippingRange()

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
