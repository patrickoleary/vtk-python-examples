#!/usr/bin/env python

# Clip regions from a quantized PNG image using vtkDiscreteFlyingEdgesClipper2D.

import os

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersGeneral import vtkDiscreteFlyingEdgesClipper2D
from vtkmodules.vtkIOImage import vtkPNGReader
from vtkmodules.vtkImagingCore import vtkImageExtractComponents
from vtkmodules.vtkImagingColor import vtkImageQuantizeRGBToIndex
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Data directory
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Read the PNG image
red = vtkPNGReader()
red.SetFileName(os.path.join(data_dir, "RedCircle.png"))
red.Update()

# Extract RGB components
extract = vtkImageExtractComponents()
extract.SetInputConnection(red.GetOutputPort())
extract.SetComponents(0, 1, 2)

# Quantize into an index image
quantize = vtkImageQuantizeRGBToIndex()
quantize.SetInputConnection(extract.GetOutputPort())
quantize.SetNumberOfColors(3)

# Clip discrete regions
discrete = vtkDiscreteFlyingEdgesClipper2D()
discrete.SetInputConnection(quantize.GetOutputPort())
discrete.SetValue(0, 1)

# Display clipped polygons
poly_mapper = vtkPolyDataMapper()
poly_mapper.SetInputConnection(discrete.GetOutputPort())

poly_actor = vtkActor()
poly_actor.SetMapper(poly_mapper)

# Renderer
renderer = vtkRenderer()
renderer.SetBackground(1, 1, 1)
renderer.AddActor(poly_actor)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(400, 400)
render_window.SetWindowName("discrete flying edges clipper2d")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
