#!/usr/bin/env python

# Generate an isosurface of iron protein data using
# vtkRecursiveDividingCubes with an outline.

import os

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonColor import vtkNamedColors
from vtkmodules.vtkFiltersGeneral import vtkRecursiveDividingCubes
from vtkmodules.vtkFiltersModeling import vtkOutlineFilter
from vtkmodules.vtkIOLegacy import vtkStructuredPointsReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkCamera,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Data directory
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

colors = vtkNamedColors()
rgb = [0.0, 0.0, 0.0]

# Read structured points
reader = vtkStructuredPointsReader()
reader.SetFileName(os.path.join(data_dir, "ironProt.vtk"))

# Recursive dividing cubes
iso = vtkRecursiveDividingCubes()
iso.SetInputConnection(reader.GetOutputPort())
iso.SetValue(128)
iso.SetDistance(0.5)
iso.SetIncrement(2)

iso_mapper = vtkPolyDataMapper()
iso_mapper.SetInputConnection(iso.GetOutputPort())
iso_mapper.ScalarVisibilityOff()

colors.GetColorRGB("bisque", rgb)
iso_actor = vtkActor()
iso_actor.SetMapper(iso_mapper)
iso_actor.GetProperty().SetColor(rgb)

# Outline
outline = vtkOutlineFilter()
outline.SetInputConnection(reader.GetOutputPort())

outline_mapper = vtkPolyDataMapper()
outline_mapper.SetInputConnection(outline.GetOutputPort())

colors.GetColorRGB("black", rgb)
outline_actor = vtkActor()
outline_actor.SetMapper(outline_mapper)
outline_actor.GetProperty().SetColor(rgb)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(outline_actor)
renderer.AddActor(iso_actor)
renderer.SetBackground(0.1, 0.2, 0.4)

# Window
render_window = vtkRenderWindow()
render_window.SetMultiSamples(0)
render_window.AddRenderer(renderer)
render_window.SetSize(250, 250)
render_window.SetWindowName("recursive dc")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
cam = vtkCamera()
cam.SetClippingRange(19.1589, 957.946)
cam.SetFocalPoint(33.7014, 26.706, 30.5867)
cam.SetPosition(150.841, 89.374, -107.462)
cam.SetViewUp(-0.190015, 0.944614, 0.267578)
cam.Dolly(3)
renderer.SetActiveCamera(cam)

interactor.Initialize()
interactor.Start()
