#!/usr/bin/env python

# Demonstrate SSAA (super-sample anti-aliasing) render pass on a dragon model.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

import os

from vtkmodules.vtkIOPLY import vtkPLYReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)
from vtkmodules.vtkRenderingOpenGL2 import vtkRenderStepsPass, vtkSSAAPass

data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Dragon model
reader = vtkPLYReader()
reader.SetFileName(os.path.join(data_dir, "dragon.ply"))
reader.Update()

mapper = vtkPolyDataMapper()
mapper.SetInputConnection(reader.GetOutputPort())

actor = vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetAmbientColor(0.2, 0.2, 1.0)
actor.GetProperty().SetDiffuseColor(1.0, 0.65, 0.7)
actor.GetProperty().SetSpecularColor(1.0, 1.0, 1.0)
actor.GetProperty().SetSpecular(0.5)
actor.GetProperty().SetDiffuse(0.7)
actor.GetProperty().SetAmbient(0.5)
actor.GetProperty().SetSpecularPower(20.0)
actor.GetProperty().SetOpacity(1.0)

# Renderer with SSAA pass
renderer = vtkRenderer()
renderer.AddActor(actor)

basic_passes = vtkRenderStepsPass()
ssaa = vtkSSAAPass()
ssaa.SetDelegatePass(basic_passes)
renderer.SetPass(ssaa)

render_window = vtkRenderWindow()
render_window.SetSize(500, 500)
render_window.SetMultiSamples(0)
render_window.SetAlphaBitPlanes(1)
render_window.AddRenderer(renderer)
render_window.SetWindowName("ssaa pass")

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.GetActiveCamera().SetPosition(0, 0, 1)
renderer.GetActiveCamera().SetFocalPoint(0, 0, 0)
renderer.GetActiveCamera().SetViewUp(0, 1, 0)
renderer.ResetCamera()

interactor.Initialize()
interactor.Start()
