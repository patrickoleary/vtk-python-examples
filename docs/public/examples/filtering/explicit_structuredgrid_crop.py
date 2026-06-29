#!/usr/bin/env python

# Read an unstructured grid, convert to explicit structured grid,
# and crop it to a smaller extent.

import os

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersCore import (
    vtkExplicitStructuredGridCrop,
    vtkUnstructuredGridToExplicitStructuredGrid,
)
from vtkmodules.vtkIOXML import vtkXMLUnstructuredGridReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkDataSetMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Data file path (relative to this script)
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Reader: load the unstructured grid
reader = vtkXMLUnstructuredGridReader()
reader.SetFileName(os.path.join(data_dir, "explicitStructuredGrid.vtu"))
reader.Update()

# Filter: convert unstructured grid to explicit structured grid
esg_converter = vtkUnstructuredGridToExplicitStructuredGrid()
esg_converter.SetInputConnection(reader.GetOutputPort())
esg_converter.SetWholeExtent(0, 5, 0, 13, 0, 3)
esg_converter.SetInputArrayToProcess(0, 0, 0, 1, "BLOCK_I")
esg_converter.SetInputArrayToProcess(1, 0, 0, 1, "BLOCK_J")
esg_converter.SetInputArrayToProcess(2, 0, 0, 1, "BLOCK_K")
esg_converter.Update()

# Filter: crop the explicit structured grid
crop = vtkExplicitStructuredGridCrop()
crop.SetInputConnection(esg_converter.GetOutputPort())
crop.SetOutputWholeExtent(0, 5, 0, 6, 0, 3)
crop.Update()

# Mapper
mapper = vtkDataSetMapper()
mapper.SetInputConnection(crop.GetOutputPort())

# Actor
actor = vtkActor()
actor.SetMapper(mapper)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(actor)

# Window
render_window = vtkRenderWindow()
render_window.SetSize(300, 300)
render_window.AddRenderer(renderer)
render_window.SetWindowName("explicit structuredgrid crop")

# Scene
renderer.ResetCamera()

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
