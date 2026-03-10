#!/usr/bin/env python

# Create contours from a CT head slice image using vtkMarchingSquares
# and triangulate them with vtkContourTriangulator.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import os

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
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

# Colors (normalized RGB)
dark_slate_gray_background_rgb = (0.184, 0.310, 0.310)
medium_orchid_rgb = (0.729, 0.333, 0.827)
gray_rgb = (0.500, 0.500, 0.500)

# Reader: load the CT head slice image
script_dir = os.path.dirname(os.path.abspath(__file__))
file_name = os.path.join(script_dir, "fullhead15.png")

reader = vtkPNGReader()
reader.SetFileName(file_name)
reader.Update()

# Filter: extract contours at iso value 500
iso = vtkMarchingSquares()
iso.SetInputConnection(reader.GetOutputPort())
iso.SetValue(0, 500)

# Mapper: display the contour lines
iso_mapper = vtkDataSetMapper()
iso_mapper.SetInputConnection(iso.GetOutputPort())
iso_mapper.ScalarVisibilityOff()

iso_actor = vtkActor()
iso_actor.SetMapper(iso_mapper)
iso_actor.GetProperty().SetColor(medium_orchid_rgb)

# Filter: triangulate the contour region
poly = vtkContourTriangulator()
poly.SetInputConnection(iso.GetOutputPort())

# Mapper: display the triangulated region
poly_mapper = vtkDataSetMapper()
poly_mapper.SetInputConnection(poly.GetOutputPort())
poly_mapper.ScalarVisibilityOff()

poly_actor = vtkActor()
poly_actor.SetMapper(poly_mapper)
poly_actor.GetProperty().SetColor(gray_rgb)

# Renderer: assemble the scene and configure the camera
renderer = vtkRenderer()
renderer.AddActor(poly_actor)
renderer.AddActor(iso_actor)
renderer.SetBackground(dark_slate_gray_background_rgb)
renderer.ResetCamera()
renderer.GetActiveCamera().Azimuth(180)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.SetMultiSamples(0)
render_window.AddRenderer(renderer)
render_window.SetSize(640, 480)
render_window.SetWindowName("ContourTriangulator")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
