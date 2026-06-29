#!/usr/bin/env python
# Demonstrate vtkCameraOrientationWidget to control camera orientation using cow.vtp data.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

import os

from vtkmodules.vtkInteractionWidgets import vtkCameraOrientationWidget
from vtkmodules.vtkIOXML import vtkXMLPolyDataReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Dataset
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))
reader = vtkXMLPolyDataReader()
reader.SetFileName(os.path.join(data_dir, "cow.vtp"))

# Mapper + Actor
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(reader.GetOutputPort())

actor = vtkActor()
actor.SetMapper(mapper)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(0.32, 0.32, 0.32)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("camera orientation widget test")
render_window.SetSize(300, 300)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Widget
cam_orient_widget = vtkCameraOrientationWidget()
cam_orient_widget.SetParentRenderer(renderer)

# Customize widget axis colors
cam_rep = cam_orient_widget.GetRepresentation()
cam_rep.SetXAxisColor([0.50, 1.00, 1.00])
cam_rep.SetYAxisColor([1.00, 0.50, 1.00])
cam_rep.SetZAxisColor([1.00, 0.75, 0.25])
cam_orient_widget.On()

interactor.Initialize()
interactor.Start()
