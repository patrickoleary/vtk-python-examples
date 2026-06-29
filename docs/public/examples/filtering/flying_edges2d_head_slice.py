#!/usr/bin/env python

# Generate 2D iso-contours from a CT head slice using vtkFlyingEdges2D,
# with contour values derived from the image scalar range.

import os

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersCore import vtkFlyingEdges2D
from vtkmodules.vtkFiltersModeling import vtkOutlineFilter
from vtkmodules.vtkIOImage import vtkPNGReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Data file path (relative to this script)
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Reader: load CT head slice
reader = vtkPNGReader()
reader.SetFileName(os.path.join(data_dir, "fullhead15.png"))
reader.Update()

scalar_range = reader.GetOutput().GetPointData().GetScalars().GetRange()

# Flying edges 2D iso-contours using full scalar range
iso = vtkFlyingEdges2D()
iso.SetInputConnection(reader.GetOutputPort())
iso.GenerateValues(12, scalar_range)

iso_mapper = vtkPolyDataMapper()
iso_mapper.SetInputConnection(iso.GetOutputPort())
iso_mapper.SetScalarRange(scalar_range)

iso_actor = vtkActor()
iso_actor.SetMapper(iso_mapper)
iso_actor.GetProperty().SetColor(1, 1, 1)

# Outline
outline = vtkOutlineFilter()
outline.SetInputConnection(reader.GetOutputPort())

outline_mapper = vtkPolyDataMapper()
outline_mapper.SetInputConnection(outline.GetOutputPort())

outline_actor = vtkActor()
outline_actor.SetMapper(outline_mapper)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(outline_actor)
renderer.AddActor(iso_actor)
renderer.SetBackground(0, 0, 0)

# Window
render_window = vtkRenderWindow()
render_window.SetMultiSamples(0)
render_window.AddRenderer(renderer)
render_window.SetSize(300, 300)
render_window.SetWindowName("flying edges2d head slice")

# Scene
renderer.ResetCamera()

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
