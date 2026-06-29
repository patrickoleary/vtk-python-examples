#!/usr/bin/env python

# Extract contours from a quantized PNG image using vtkDiscreteFlyingEdges2D
# and fill them as polygons via vtkContourLoopExtraction.

import os

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersCore import vtkTriangleFilter
from vtkmodules.vtkFiltersGeneral import vtkDiscreteFlyingEdges2D
from vtkmodules.vtkFiltersModeling import vtkContourLoopExtraction
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

# Discrete flying edges 2D
discrete = vtkDiscreteFlyingEdges2D()
discrete.SetInputConnection(quantize.GetOutputPort())
discrete.SetValue(0, 0)

# Extract contour loops as polygons
poly_loops = vtkContourLoopExtraction()
poly_loops.SetInputConnection(discrete.GetOutputPort())

# Triangulate concave polygons for correct rendering
tri_filter = vtkTriangleFilter()
tri_filter.SetInputConnection(poly_loops.GetOutputPort())

# Contour lines
line_mapper = vtkPolyDataMapper()
line_mapper.SetInputConnection(discrete.GetOutputPort())
line_mapper.ScalarVisibilityOff()

line_actor = vtkActor()
line_actor.SetMapper(line_mapper)
line_actor.GetProperty().SetColor(0, 0, 0)

# Filled polygons
poly_mapper = vtkPolyDataMapper()
poly_mapper.SetInputConnection(tri_filter.GetOutputPort())

poly_actor = vtkActor()
poly_actor.SetMapper(poly_mapper)

# Renderer
renderer = vtkRenderer()
renderer.SetBackground(1, 1, 1)
renderer.AddActor(line_actor)
renderer.AddActor(poly_actor)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(400, 400)
render_window.SetWindowName("discrete flying edges2d")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
