#!/usr/bin/env python

# Generate an isosurface from a CT head volume using
# vtkSynchronizedTemplates3D with triangle generation.

import os

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersCore import vtkSynchronizedTemplates3D
from vtkmodules.vtkIOImage import vtkImageReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Data file path (relative to this script)
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Reader: load 16-bit CT head volume
reader = vtkImageReader()
reader.SetDataByteOrderToLittleEndian()
reader.SetDataExtent(0, 63, 0, 63, 1, 93)
reader.SetDataSpacing(3.2, 3.2, 1.5)
reader.SetFilePrefix(os.path.join(data_dir, "headsq", "quarter"))
reader.SetDataMask(0x7fff)

# Isosurface with triangle generation
sync_templates = vtkSynchronizedTemplates3D()
sync_templates.SetInputConnection(reader.GetOutputPort())
sync_templates.SetValue(0, 1150)
sync_templates.GenerateTrianglesOn()

mapper = vtkPolyDataMapper()
mapper.SetInputConnection(sync_templates.GetOutputPort())
mapper.ScalarVisibilityOff()

actor = vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetColor(1, 0.7, 0.6)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(0.5, 0.5, 0.6)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(400, 400)
render_window.SetWindowName("synchronized templates3d")

# Scene
camera = renderer.GetActiveCamera()
camera.SetPosition(99.8847, 537.926, 15)
camera.SetFocalPoint(99.8847, 109.81, 15)
camera.SetViewAngle(20)
camera.SetViewUp(0, 0, -1)
renderer.ResetCameraClippingRange()

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
