#!/usr/bin/env python

# Contour a quadratic tetrahedron dataset loaded from a VTK file,
# displaying both the wireframe mesh and the contour surface.

import os

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersCore import vtkContourFilter
from vtkmodules.vtkIOLegacy import vtkUnstructuredGridReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkDataSetMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Data file path (relative to this script)
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Read quadratic tetrahedra
reader = vtkUnstructuredGridReader()
reader.SetFileName(os.path.join(data_dir, "quadTetEdgeTest.vtk"))

# Contour the quadratic tet
tet_contours = vtkContourFilter()
tet_contours.SetInputConnection(reader.GetOutputPort())
tet_contours.SetValue(0, 0.5)

tet_contour_mapper = vtkDataSetMapper()
tet_contour_mapper.SetInputConnection(tet_contours.GetOutputPort())
tet_contour_mapper.ScalarVisibilityOff()

tet_mapper = vtkDataSetMapper()
tet_mapper.SetInputConnection(reader.GetOutputPort())
tet_mapper.ScalarVisibilityOff()

tet_actor = vtkActor()
tet_actor.SetMapper(tet_mapper)
tet_actor.GetProperty().SetRepresentationToWireframe()
tet_actor.GetProperty().SetAmbient(1.0)

tet_contour_actor = vtkActor()
tet_contour_actor.SetMapper(tet_contour_mapper)
tet_contour_actor.GetProperty().SetAmbient(1.0)

# Remove all cullers so single vertex actors will render
renderer = vtkRenderer()
renderer.GetCullers().RemoveAllItems()
renderer.SetBackground(0.1, 0.2, 0.3)
renderer.AddActor(tet_actor)
renderer.AddActor(tet_contour_actor)

# Window
render_window = vtkRenderWindow()
render_window.SetMultiSamples(0)
render_window.AddRenderer(renderer)
render_window.SetSize(400, 250)
render_window.SetWindowName("contour quadratic tetra")

# Scene
renderer.ResetCamera()
renderer.GetActiveCamera().Dolly(1.5)
renderer.ResetCameraClippingRange()

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
