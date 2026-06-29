#!/usr/bin/env python

# Create a letter "B" outline by reading a PGM image, smoothing it,
# converting to geometry, and clipping to extract the letter shape.

import os

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

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

# Data file path (relative to this script)
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Read the PGM image of letter B
image_in = vtkPNMReader()
image_in.SetFileName(os.path.join(data_dir, "B.pgm"))

# Gaussian smooth
gaussian = vtkImageGaussianSmooth()
gaussian.SetStandardDeviations(2, 2)
gaussian.SetDimensionality(2)
gaussian.SetRadiusFactors(1, 1)
gaussian.SetInputConnection(image_in.GetOutputPort())

# Convert image to geometry
geometry = vtkImageDataGeometryFilter()
geometry.SetInputConnection(gaussian.GetOutputPort())

# Clip to extract the letter shape
clipper = vtkClipPolyData()
clipper.SetInputConnection(geometry.GetOutputPort())
clipper.SetValue(127.5)
clipper.GenerateClipScalarsOff()
clipper.InsideOutOn()
clipper.GetOutput().GetPointData().CopyScalarsOff()
clipper.Update()

mapper = vtkPolyDataMapper()
mapper.SetInputConnection(clipper.GetOutputPort())
mapper.ScalarVisibilityOff()

letter = vtkActor()
letter.SetMapper(mapper)
letter.GetProperty().SetDiffuseColor(0, 0, 0)
letter.GetProperty().SetRepresentationToWireframe()

# Renderer
renderer = vtkRenderer()
renderer.AddActor(letter)
renderer.SetBackground(1, 1, 1)
# Window
render_window = vtkRenderWindow()
render_window.SetMultiSamples(0)
render_window.AddRenderer(renderer)
render_window.SetSize(320, 320)
render_window.SetWindowName("create bfont")

# Scene
renderer.ResetCamera()
renderer.GetActiveCamera().Dolly(1.2)
renderer.ResetCameraClippingRange()

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
