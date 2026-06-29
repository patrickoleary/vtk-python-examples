#!/usr/bin/env python
# Demonstrate vtkTensorProbeWidget with a synthetic polyline trajectory.

import os

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkInteractionWidgets import (
    vtkTensorProbeRepresentation,
    vtkTensorProbeWidget,
)
from vtkmodules.vtkIOXML import vtkXMLPolyDataReader
from vtkmodules.vtkRenderingCore import (
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Source
reader = vtkXMLPolyDataReader()
reader.SetFileName(os.path.join(data_dir, "SyntheticPolyline.vtp"))
reader.Update()

poly_data = reader.GetOutput()

# Renderer
renderer = vtkRenderer()

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("tensor probe widget")
render_window.SetMultiSamples(0)
render_window.SetSize(512, 512)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Widget
tensor_widget = vtkTensorProbeWidget()
tensor_widget.SetInteractor(interactor)

tensor_rep = vtkTensorProbeRepresentation.SafeDownCast(tensor_widget.GetRepresentation())
tensor_rep.SetTrajectory(poly_data)

tensor_widget.EnabledOn()

# Scene
renderer.ResetCamera()
renderer.GetActiveCamera().SetPosition(4.50141, 2.82662, 0.42005)
renderer.GetActiveCamera().SetViewUp(-0.529751, 0.83346, -0.157189)
renderer.GetActiveCamera().SetFocalPoint(3.06943, 2.31262, 2.5207)
renderer.ResetCameraClippingRange()

interactor.Initialize()
interactor.Start()
