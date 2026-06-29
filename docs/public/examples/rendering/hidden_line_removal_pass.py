#!/usr/bin/env python

# Demonstrate hidden line removal on a wireframe Exodus II model.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

import os

from vtkmodules.vtkFiltersGeometry import vtkCompositeDataGeometryFilter
from vtkmodules.vtkIOExodus import vtkExodusIIReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkCompositePolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Read Exodus II data
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))
reader = vtkExodusIIReader()
reader.SetFileName(os.path.join(data_dir, "can.ex2"))

# Convert composite data to polydata
geom_filter = vtkCompositeDataGeometryFilter()
geom_filter.SetInputConnection(reader.GetOutputPort())

mapper = vtkCompositePolyDataMapper()
mapper.SetInputConnection(geom_filter.GetOutputPort())

actor = vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetColor(1.0, 0.0, 0.0)
actor.GetProperty().SetRepresentationToWireframe()
actor.GetProperty().LightingOff()

# Renderer with hidden line removal
renderer = vtkRenderer()
renderer.UseHiddenLineRemovalOn()
renderer.AddActor(actor)
renderer.SetBackground(1.0, 1.0, 1.0)
renderer.SetBackground2(0.3, 0.1, 0.2)
renderer.GradientBackgroundOn()

render_window = vtkRenderWindow()
render_window.SetSize(500, 500)
render_window.SetMultiSamples(0)
render_window.AddRenderer(renderer)
render_window.SetWindowName("hidden line removal pass")

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.GetActiveCamera().ParallelProjectionOn()
renderer.GetActiveCamera().SetPosition(-340.0, -70.0, -50.0)
renderer.GetActiveCamera().SetFocalPoint(-2.5, 3.0, -5.0)
renderer.GetActiveCamera().SetViewUp(0, 0.5, -1)
renderer.GetActiveCamera().SetParallelScale(12)

interactor.Initialize()
interactor.Start()
