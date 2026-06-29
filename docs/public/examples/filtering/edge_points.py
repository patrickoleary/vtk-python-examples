#!/usr/bin/env python

# Generate edge points on CT head data using vtkEdgePoints.

import os

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonColor import vtkNamedColors
from vtkmodules.vtkFiltersGeneral import vtkEdgePoints
from vtkmodules.vtkIOImage import vtkVolume16Reader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkDataSetMapper,
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
v16.SetDataByteOrderToLittleEndian()
v16.SetFilePrefix(os.path.join(data_dir, "headsq", "quarter"))
v16.SetDataSpacing(3.2, 3.2, 1.5)
v16.SetImageRange(30, 50)
v16.SetDataMask(0x7fff)

# Create points on edges
edge_points = vtkEdgePoints()
edge_points.SetInputConnection(v16.GetOutputPort())
edge_points.SetValue(1150)

mapper = vtkDataSetMapper()
mapper.SetInputConnection(edge_points.GetOutputPort())
mapper.ScalarVisibilityOff()

colors.GetColorRGB("raw_sienna", rgb)
head_actor = vtkActor()
head_actor.SetMapper(mapper)
head_actor.GetProperty().SetColor(rgb)

# Renderer
colors.GetColorRGB("slate_grey", rgb)
renderer = vtkRenderer()
renderer.AddActor(head_actor)
renderer.SetBackground(rgb)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(300, 300)
render_window.SetWindowName("edge points")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.GetActiveCamera().SetPosition(99.8847, 537.86, 22.4716)
renderer.GetActiveCamera().SetFocalPoint(99.8847, 109.81, 15)
renderer.GetActiveCamera().SetViewAngle(20)
renderer.GetActiveCamera().SetViewUp(0, -1, 0)
renderer.ResetCameraClippingRange()

interactor.Initialize()
interactor.Start()
