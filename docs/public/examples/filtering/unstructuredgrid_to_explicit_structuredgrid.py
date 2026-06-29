#!/usr/bin/env python

# Convert an unstructured grid to an explicit structured grid using
# vtkUnstructuredGridToExplicitStructuredGrid.

import os

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersCore import vtkUnstructuredGridToExplicitStructuredGrid
from vtkmodules.vtkIOXML import vtkXMLUnstructuredGridReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkDataSetMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Data directory
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Read the unstructured grid
reader = vtkXMLUnstructuredGridReader()
reader.SetFileName(os.path.join(data_dir, "explicitStructuredGrid.vtu"))
reader.Update()

# Convert to explicit structured grid
esg_convertor = vtkUnstructuredGridToExplicitStructuredGrid()
esg_convertor.SetInputConnection(reader.GetOutputPort())
esg_convertor.SetWholeExtent(0, 5, 0, 13, 0, 3)
esg_convertor.SetInputArrayToProcess(0, 0, 0, 1, "BLOCK_I")
esg_convertor.SetInputArrayToProcess(1, 0, 0, 1, "BLOCK_J")
esg_convertor.SetInputArrayToProcess(2, 0, 0, 1, "BLOCK_K")
esg_convertor.Update()

mapper = vtkDataSetMapper()
mapper.SetInputConnection(esg_convertor.GetOutputPort())

actor = vtkActor()
actor.SetMapper(mapper)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(actor)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(300, 300)
render_window.SetWindowName("unstructuredgrid to explicit structuredgrid")

# Scene
renderer.ResetCamera()

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
