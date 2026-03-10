#!/usr/bin/env python

# Use a camera orientation widget to interactively control the camera.

import os
from pathlib import Path

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkIOXML import vtkXMLPolyDataReader
from vtkmodules.vtkInteractionWidgets import vtkCameraOrientationWidget
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
beige_rgb = (0.961, 0.961, 0.863)
dim_gray_rgb = (0.412, 0.412, 0.412)

# Data: read cow.vtp
data_dir = Path(os.environ.get("VPE_DATA_DIR", Path(__file__).parent))
file_path = data_dir / "cow.vtp"

# Reader: load XML poly data
reader = vtkXMLPolyDataReader()
reader.SetFileName(str(file_path))

# Mapper: map polygon data to graphics primitives
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(reader.GetOutputPort())

# Actor: assign the mapped geometry
actor = vtkActor()
actor.GetProperty().SetColor(beige_rgb)
actor.SetMapper(mapper)

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(dim_gray_rgb)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.SetSize(600, 600)
render_window.SetWindowName("CameraOrientationWidget")
render_window.AddRenderer(renderer)

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# CameraOrientationWidget: orientation gizmo for camera control
cow = vtkCameraOrientationWidget()
cow.SetParentRenderer(renderer)
cow.On()

# Launch the interactive visualization
render_window.Render()
render_window_interactor.Initialize()
render_window_interactor.Start()
