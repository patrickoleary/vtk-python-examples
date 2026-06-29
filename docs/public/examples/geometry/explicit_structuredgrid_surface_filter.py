#!/usr/bin/env python

# Demonstrate vtkExplicitStructuredGridSurfaceFilter on an explicit
# structured grid converted from an unstructured grid file.

import os

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersGeometry import vtkExplicitStructuredGridSurfaceFilter
from vtkmodules.vtkFiltersCore import vtkUnstructuredGridToExplicitStructuredGrid
from vtkmodules.vtkIOXML import vtkXMLUnstructuredGridReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkDataSetMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Read unstructured grid
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

# Surface filter
surf = vtkExplicitStructuredGridSurfaceFilter()
surf.SetInputConnection(esg_convertor.GetOutputPort())
surf.Update()

# Mapper
mapper = vtkDataSetMapper()
mapper.SetInputConnection(surf.GetOutputPort())

actor = vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetOpacity(0.5)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(actor)

# Window
render_window = vtkRenderWindow()
render_window.SetSize(300, 300)
render_window.AddRenderer(renderer)
render_window.SetWindowName("explicit structuredgrid surface filter")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.ResetCamera()

interactor.Initialize()
interactor.Start()
