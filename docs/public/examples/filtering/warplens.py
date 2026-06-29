#!/usr/bin/env python

# Apply lens distortion correction to an image using vtkWarpLens.

import os

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersCore import (
    vtkStripper,
    vtkTriangleFilter,
)
from vtkmodules.vtkFiltersGeneral import vtkWarpLens
from vtkmodules.vtkFiltersGeometry import vtkGeometryFilter
from vtkmodules.vtkIOImage import vtkPNGReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Data directory
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Read the image
png_reader = vtkPNGReader()
png_reader.SetFileName(os.path.join(data_dir, "camscene.png"))
png_reader.Update()

x_width = png_reader.GetOutput().GetDimensions()[0]
y_height = png_reader.GetOutput().GetDimensions()[1]

# Warp with lens distortion parameters
wl = vtkWarpLens()
wl.SetInputConnection(png_reader.GetOutputPort())
wl.SetPrincipalPoint(2.4507, 1.7733)
wl.SetFormatWidth(4.792)
wl.SetFormatHeight(3.6)
wl.SetImageWidth(x_width)
wl.SetImageHeight(y_height)
wl.SetK1(0.01307)
wl.SetK2(0.0003102)
wl.SetP1(1.953e-005)
wl.SetP2(-9.655e-005)

gf = vtkGeometryFilter()
gf.SetInputConnection(wl.GetOutputPort())

tf = vtkTriangleFilter()
tf.SetInputConnection(gf.GetOutputPort())

strip = vtkStripper()
strip.SetInputConnection(tf.GetOutputPort())
strip.SetMaximumLength(250)

mapper = vtkPolyDataMapper()
mapper.SetInputConnection(strip.GetOutputPort())

plane_actor = vtkActor()
plane_actor.SetMapper(mapper)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(plane_actor)
renderer.SetBackground(0.1, 0.2, 0.4)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(300, 300)
render_window.SetWindowName("warplens")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.ResetCamera()
renderer.GetActiveCamera().Zoom(1.4)

interactor.Initialize()
interactor.Start()
