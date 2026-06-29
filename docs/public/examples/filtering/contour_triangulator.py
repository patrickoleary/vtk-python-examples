#!/usr/bin/env python

# Demonstrate vtkContourTriangulator by reading a PNG image, extracting
# contours with vtkContourFilter, and triangulating the contour polygons.

import os

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersCore import vtkContourFilter
from vtkmodules.vtkFiltersGeneral import vtkContourTriangulator
from vtkmodules.vtkIOImage import vtkPNGReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkDataSetMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Data directory
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Read PNG image
reader = vtkPNGReader()
reader.SetFileName(os.path.join(data_dir, "fullhead15.png"))
reader.Update()

# Extract contours
contour = vtkContourFilter()
contour.SetInputConnection(reader.GetOutputPort())
contour.SetValue(0, 500)

# Contour lines actor
iso_mapper = vtkDataSetMapper()
iso_mapper.SetInputConnection(contour.GetOutputPort())
iso_mapper.ScalarVisibilityOff()

iso_actor = vtkActor()
iso_actor.SetMapper(iso_mapper)
iso_actor.GetProperty().SetColor(0, 0, 0)

# Triangulate contours
triangulator = vtkContourTriangulator()
triangulator.SetInputConnection(contour.GetOutputPort())

# Triangulated polygons actor
poly_mapper = vtkDataSetMapper()
poly_mapper.SetInputConnection(triangulator.GetOutputPort())
poly_mapper.ScalarVisibilityOff()

poly_actor = vtkActor()
poly_actor.SetMapper(poly_mapper)
poly_actor.GetProperty().SetColor(1.0, 1.0, 1.0)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(poly_actor)
renderer.AddActor(iso_actor)
renderer.SetBackground(0.5, 0.5, 0.5)

# Window
render_window = vtkRenderWindow()
render_window.SetMultiSamples(0)
render_window.AddRenderer(renderer)
render_window.SetSize(300, 300)
render_window.SetWindowName("contour triangulator")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.ResetCamera()
renderer.GetActiveCamera().Azimuth(180)

interactor.Initialize()
interactor.Start()
