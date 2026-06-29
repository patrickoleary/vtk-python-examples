#!/usr/bin/env python

# Generate an isosurface from CT head data using vtkMarchingContourFilter
# with an outline.

import os

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonColor import vtkNamedColors
from vtkmodules.vtkFiltersGeneral import vtkMarchingContourFilter
from vtkmodules.vtkFiltersModeling import vtkOutlineFilter
from vtkmodules.vtkIOImage import vtkVolume16Reader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Data directory
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

colors = vtkNamedColors()
rgb = [0.0, 0.0, 0.0]

# Read CT head slices
v16 = vtkVolume16Reader()
v16.SetDataDimensions(64, 64)
v16.GetOutput().SetOrigin(0.0, 0.0, 0.0)
v16.SetDataByteOrderToLittleEndian()
v16.SetFilePrefix(os.path.join(data_dir, "headsq", "quarter"))
v16.SetImageRange(1, 93)
v16.SetDataSpacing(3.2, 3.2, 1.5)
v16.Update()

# Marching contour filter
iso = vtkMarchingContourFilter()
iso.SetInputConnection(v16.GetOutputPort())
iso.SetValue(0, 1125)

iso_mapper = vtkPolyDataMapper()
iso_mapper.SetInputConnection(iso.GetOutputPort())
iso_mapper.ScalarVisibilityOff()

colors.GetColorRGB("antique_white", rgb)
iso_actor = vtkActor()
iso_actor.SetMapper(iso_mapper)
iso_actor.GetProperty().SetColor(rgb)

# Outline
outline = vtkOutlineFilter()
outline.SetInputConnection(v16.GetOutputPort())

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
render_window.SetWindowName("mcubes")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.ResetCamera()
renderer.GetActiveCamera().Elevation(90)
renderer.GetActiveCamera().SetViewUp(0, 0, -1)
renderer.GetActiveCamera().Dolly(1.5)
renderer.ResetCameraClippingRange()

interactor.Initialize()
interactor.Start()
