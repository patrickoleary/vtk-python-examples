#!/usr/bin/env python
# Demonstrate vtkMoleculeMapper with liquorice stick rendering.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonDataModel import vtkMolecule
from vtkmodules.vtkDomainsChemistry import vtkMoleculeMapper
from vtkmodules.vtkRenderingCore import (
    vtkActor,
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

# Molecule mapper with liquorice stick settings.
mol_mapper = vtkMoleculeMapper()
mol_mapper.SetInputData(mol)
mol_mapper.UseLiquoriceStickSettings()

actor = vtkActor()
actor.SetMapper(mol_mapper)

# Rendering pipeline.
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(0.0, 0.0, 0.0)

render_window = vtkRenderWindow()
render_window.SetSize(450, 450)
render_window.SetMultiSamples(0)
render_window.AddRenderer(renderer)
render_window.SetWindowName("liquorice sticks")

render_window.Render()
renderer.GetActiveCamera().Zoom(2.2)

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
