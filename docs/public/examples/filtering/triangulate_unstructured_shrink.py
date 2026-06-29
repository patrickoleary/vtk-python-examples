#!/usr/bin/env python

# Triangulate an unstructured grid and shrink the resulting tetrahedra
# using vtkDataSetTriangleFilter and vtkShrinkFilter.

import os

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersGeneral import (
    vtkDataSetTriangleFilter,
    vtkShrinkFilter,
)
from vtkmodules.vtkIOLegacy import vtkDataSetReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkDataSetMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Data directory
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Read unstructured grid
reader = vtkDataSetReader()
reader.SetFileName(os.path.join(data_dir, "uGridEx.vtk"))

# Triangulate
tris = vtkDataSetTriangleFilter()
tris.SetInputConnection(reader.GetOutputPort())

# Shrink
shrink = vtkShrinkFilter()
shrink.SetInputConnection(tris.GetOutputPort())
shrink.SetShrinkFactor(0.8)

mapper = vtkDataSetMapper()
mapper.SetInputConnection(shrink.GetOutputPort())
mapper.SetScalarRange(0, 26)

actor = vtkActor()
actor.SetMapper(mapper)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(1, 1, 1)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(350, 350)
render_window.SetWindowName("triangulate unstructured shrink")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.GetActiveCamera().SetPosition(-4.01115, 6.03964, 10.5393)
renderer.GetActiveCamera().SetFocalPoint(1, 0.525, 3.025)
renderer.GetActiveCamera().SetViewAngle(30)
renderer.GetActiveCamera().SetViewUp(0.114284, 0.835731, -0.537115)
renderer.GetActiveCamera().SetClippingRange(4.83787, 17.8392)

interactor.Initialize()
interactor.Start()
