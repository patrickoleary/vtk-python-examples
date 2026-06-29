#!/usr/bin/env python

# Demonstrate vtkFacetReader loading and rendering a .facet file.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

import os

from vtkmodules.vtkFiltersHybrid import vtkFacetReader
from vtkmodules.vtkRenderingCore import (
    vtkCamera,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)
from vtkmodules.vtkRenderingLOD import vtkLODActor

data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Read facet file
facet_reader = vtkFacetReader()
facet_reader.SetFileName(os.path.join(data_dir, "clown.facet"))

mapper = vtkPolyDataMapper()
mapper.SetInputConnection(facet_reader.GetOutputPort())
mapper.UseLookupTableScalarRangeOff()
mapper.SetScalarVisibility(1)
mapper.SetScalarModeToDefault()

actor = vtkLODActor()
actor.SetMapper(mapper)
actor.GetProperty().SetRepresentationToSurface()
actor.GetProperty().SetInterpolationToGouraud()
actor.GetProperty().SetAmbient(0.15)
actor.GetProperty().SetDiffuse(0.85)
actor.GetProperty().SetSpecular(0.1)
actor.GetProperty().SetSpecularPower(100)
actor.GetProperty().SetSpecularColor(1, 1, 1)
actor.GetProperty().SetColor(1, 1, 1)
actor.SetNumberOfCloudPoints(30000)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(0, 0, 0)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(300, 300)
render_window.SetWindowName("facet reader")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
camera = vtkCamera()
camera.SetClippingRange(3, 6)
camera.SetFocalPoint(0.1, 0.03, -0.5)
camera.SetPosition(4.4, -0.5, -0.5)
camera.SetViewUp(0, 0, -1)
renderer.SetActiveCamera(camera)

interactor.Initialize()
interactor.Start()
