#!/usr/bin/env python

# Demonstrate vtkContourTriangulator with vtkMarchingSquares by reading
# a PNG image, extracting contours with marching squares, and
# triangulating the contour polygons.

import os

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersCore import vtkMarchingSquares
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

# Extract contours with marching squares
iso = vtkMarchingSquares()
iso.SetInputConnection(reader.GetOutputPort())
iso.SetValue(0, 500)

# Contour lines actor
iso_mapper = vtkDataSetMapper()
iso_mapper.SetInputConnection(iso.GetOutputPort())
iso_mapper.ScalarVisibilityOff()

iso_actor = vtkActor()
iso_actor.SetMapper(iso_mapper)
iso_actor.GetProperty().SetColor(0, 0, 0)

# Triangulate contours
triangulator = vtkContourTriangulator()
triangulator.SetInputConnection(iso.GetOutputPort())

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
render_window.SetWindowName("contour triangulator marching")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.ResetCamera()
renderer.GetActiveCamera().Azimuth(180)

interactor.Initialize()
interactor.Start()
