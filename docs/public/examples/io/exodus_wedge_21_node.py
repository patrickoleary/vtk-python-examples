#!/usr/bin/env python

# Read a 21-node wedge Exodus file and render the surface.

import os

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersGeometry import vtkDataSetSurfaceFilter
from vtkmodules.vtkIOExodus import vtkExodusIIReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkCompositePolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Source
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Read the Exodus file
exodus_reader = vtkExodusIIReader()
exodus_reader.SetFileName(os.path.join(data_dir, "wedge21.g"))
exodus_reader.Update()

# Surface filter
surface_filter = vtkDataSetSurfaceFilter()
surface_filter.SetInputConnection(exodus_reader.GetOutputPort())

# Composite mapper
composite_mapper = vtkCompositePolyDataMapper()
composite_mapper.SetInputConnection(surface_filter.GetOutputPort())

# Actor
exodus_actor = vtkActor()
exodus_actor.SetMapper(composite_mapper)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(exodus_actor)
renderer.SetBackground(1, 1, 1)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("exodus wedge 21 node")
render_window.SetMultiSamples(0)
render_window.SetSize(300, 300)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
camera = renderer.GetActiveCamera()
camera.SetPosition(10.0, 10.0, 5.0)
camera.SetViewUp(0.0, 0.4, 1.0)
renderer.ResetCamera()

interactor.Initialize()
interactor.Start()
