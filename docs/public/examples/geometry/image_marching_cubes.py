#!/usr/bin/env python

# Demonstrate vtkImageMarchingCubes by reading a volume dataset, extracting
# an isosurface at a specified value, and rendering with an outline.

import os
from math import cos, pi, sin

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonColor import vtkNamedColors
from vtkmodules.vtkFiltersGeneral import vtkImageMarchingCubes
from vtkmodules.vtkFiltersModeling import vtkOutlineFilter
from vtkmodules.vtkIOImage import vtkImageReader2
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))
named_colors = vtkNamedColors()

# Data direction matrix
angle = pi / 2
direction = [
    -1, 0, 0,
    0, cos(angle), -sin(angle),
    0, -sin(angle), -cos(angle),
]

# Read volume data
reader = vtkImageReader2()
reader.SetDataScalarTypeToUnsignedShort()
reader.SetFilePrefix(os.path.join(data_dir, "headsq", "quarter"))
reader.SetDataExtent(0, 63, 0, 63, 1, 93)
reader.SetDataSpacing(3.2, 3.2, 1.5)
reader.SetDataOrigin(0.0, 0.0, 0.0)
reader.SetDataDirection(direction)

# Extract isosurface
iso = vtkImageMarchingCubes()
iso.SetInputConnection(reader.GetOutputPort())
iso.SetValue(0, 1150)
iso.SetInputMemoryLimit(100)

# Isosurface mapper and actor
iso_mapper = vtkPolyDataMapper()
iso_mapper.SetInputConnection(iso.GetOutputPort())
iso_mapper.ScalarVisibilityOff()

rgb = [0.0, 0.0, 0.0]
named_colors.GetColorRGB("antique_white", rgb)

iso_actor = vtkActor()
iso_actor.SetMapper(iso_mapper)
iso_actor.GetProperty().SetColor(rgb)

# Outline
outline = vtkOutlineFilter()
outline.SetInputConnection(reader.GetOutputPort())

outline_mapper = vtkPolyDataMapper()
outline_mapper.SetInputConnection(outline.GetOutputPort())

outline_actor = vtkActor()
outline_actor.SetMapper(outline_mapper)
outline_actor.VisibilityOff()

# Renderer
renderer = vtkRenderer()
renderer.AddActor(outline_actor)
renderer.AddActor(iso_actor)
renderer.SetBackground(0.2, 0.3, 0.4)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(200, 200)
render_window.SetWindowName("image marching cubes")

# Scene
renderer.ResetCamera()

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
