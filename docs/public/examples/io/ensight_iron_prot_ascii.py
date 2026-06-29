#!/usr/bin/env python

# Read EnSight ironProt ASCII case file, contour at 200, and render.

import os

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersCore import vtkContourFilter
from vtkmodules.vtkIOEnSight import vtkGenericEnSightReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkCompositePolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Source
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Read EnSight case file
ensight_reader = vtkGenericEnSightReader()
ensight_reader.SetCaseFileName(os.path.join(data_dir, "EnSight", "ironProt_ascii.case"))

# Contour
contour_filter = vtkContourFilter()
contour_filter.SetInputConnection(ensight_reader.GetOutputPort())
contour_filter.SetValue(0, 200)
contour_filter.SetComputeScalars(1)

# Mapper
composite_mapper = vtkCompositePolyDataMapper()
composite_mapper.SetInputConnection(contour_filter.GetOutputPort())
composite_mapper.SetScalarRange(0, 1)
composite_mapper.SetScalarVisibility(1)

# Actor
ensight_actor = vtkActor()
ensight_actor.SetMapper(composite_mapper)
ensight_actor.GetProperty().SetRepresentationToSurface()
ensight_actor.GetProperty().SetInterpolationToGouraud()

# Renderer
renderer = vtkRenderer()
renderer.AddActor(ensight_actor)
renderer.SetBackground(0, 0, 0)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("ensight iron prot ascii")
render_window.SetMultiSamples(0)
render_window.SetSize(300, 300)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
camera = renderer.GetActiveCamera()
camera.SetPosition(-54.8012, 109.471, 231.412)
camera.SetFocalPoint(33, 33, 33)
camera.SetViewUp(0.157687, 0.942832, -0.293604)
camera.SetViewAngle(30)
camera.SetClippingRange(124.221, 363.827)

interactor.Initialize()
interactor.Start()
