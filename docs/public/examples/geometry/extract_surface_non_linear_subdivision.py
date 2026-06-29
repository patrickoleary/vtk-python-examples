#!/usr/bin/env python

# Demonstrate vtkDataSetSurfaceFilter with non-linear subdivision
# on a quadratic tetrahedral mesh.

import os

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersGeometry import vtkDataSetSurfaceFilter
from vtkmodules.vtkIOXML import vtkXMLUnstructuredGridReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Read quadratic tetra mesh
reader = vtkXMLUnstructuredGridReader()
reader.SetFileName(os.path.join(data_dir, "quadraticTetra01.vtu"))

# Extract surface with non-linear subdivision
extract_surface = vtkDataSetSurfaceFilter()
extract_surface.SetInputConnection(reader.GetOutputPort())
extract_surface.SetNonlinearSubdivisionLevel(4)

# Mapper
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(extract_surface.GetOutputPort())
mapper.ScalarVisibilityOn()
mapper.SelectColorArray("scalars")
mapper.SetScalarModeToUsePointFieldData()

actor = vtkActor()
actor.SetMapper(mapper)

# Renderer
renderer = vtkRenderer()
renderer.SetBackground(0, 0, 0)
renderer.AddActor(actor)

# Window
render_window = vtkRenderWindow()
render_window.SetSize(300, 300)
render_window.AddRenderer(renderer)
render_window.SetWindowName("extract surface non linear subdivision")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.ResetCamera()

interactor.Initialize()
interactor.Start()
