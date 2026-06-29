#!/usr/bin/env python
# Demonstrate vtkProteinRibbonFilter rendering a PDB protein structure.

import os

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkDomainsChemistry import vtkProteinRibbonFilter
from vtkmodules.vtkIOChemistry import vtkPDBReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Read protein from PDB file.
reader = vtkPDBReader()
reader.SetFileName(os.path.join(data_dir, "3GQP.pdb"))

# Protein ribbon filter.
ribbon_filter = vtkProteinRibbonFilter()
ribbon_filter.SetInputConnection(reader.GetOutputPort())
ribbon_filter.Update()

# Mapper and actor.
mapper = vtkPolyDataMapper()
mapper.SetInputData(ribbon_filter.GetOutput())

actor = vtkActor()
actor.SetMapper(mapper)

# Rendering pipeline.
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(0, 0, 0)
renderer.ResetCamera()
renderer.GetActiveCamera().Zoom(1.5)
renderer.ResetCameraClippingRange()

render_window = vtkRenderWindow()
render_window.SetSize(450, 450)
render_window.SetMultiSamples(0)
render_window.AddRenderer(renderer)
render_window.SetWindowName("protein ribbon")

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
