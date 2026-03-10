#!/usr/bin/env python

# Clip a scanned image to create a letter B wireframe.

import os
from pathlib import Path

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkFiltersCore import vtkClipPolyData
from vtkmodules.vtkFiltersGeometry import vtkImageDataGeometryFilter
from vtkmodules.vtkIOImage import vtkPNMReader
from vtkmodules.vtkImagingGeneral import vtkImageGaussianSmooth
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
lamp_black = (0.180, 0.282, 0.227)
white_smoke = (0.961, 0.961, 0.961)

# Data file
data_dir = Path(os.environ.get("VPE_DATA_DIR", Path(__file__).parent))
file_name = str(data_dir / "B.pgm")

# Reader: load the scanned PGM image
image_in = vtkPNMReader()
image_in.SetFileName(file_name)

# Filter: smooth the image with a Gaussian kernel
gaussian = vtkImageGaussianSmooth()
gaussian.SetStandardDeviations(2, 2)
gaussian.SetDimensionality(2)
gaussian.SetRadiusFactors(1, 1)
gaussian.SetInputConnection(image_in.GetOutputPort())

# Filter: convert image data to polygonal geometry
geometry = vtkImageDataGeometryFilter()
geometry.SetInputConnection(gaussian.GetOutputPort())

# Filter: clip the geometry at half-intensity threshold
clipper = vtkClipPolyData()
clipper.SetInputConnection(geometry.GetOutputPort())
clipper.SetValue(127.5)
clipper.GenerateClipScalarsOff()
clipper.InsideOutOn()
clipper.GetOutput().GetPointData().CopyScalarsOff()
clipper.Update()

# Mapper: map clipped geometry to graphics primitives
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(clipper.GetOutputPort())
mapper.ScalarVisibilityOff()

# Actor: display the letter as wireframe
letter_actor = vtkActor()
letter_actor.SetMapper(mapper)
letter_actor.GetProperty().SetDiffuseColor(lamp_black)
letter_actor.GetProperty().SetRepresentationToWireframe()

# Renderer: assemble the scene and configure the camera
renderer = vtkRenderer()
renderer.AddActor(letter_actor)
renderer.SetBackground(white_smoke)
renderer.ResetCamera()
renderer.GetActiveCamera().Dolly(1.2)
renderer.ResetCameraClippingRange()

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("CreateBFont")
render_window.SetSize(640, 480)

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Start()
