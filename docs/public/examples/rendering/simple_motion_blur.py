#!/usr/bin/env python

# Demonstrate simple motion blur render pass with three dragon models.

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
from vtkmodules.vtkRenderingOpenGL2 import vtkRenderStepsPass, vtkSimpleMotionBlurPass

data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Dragon model
reader = vtkPLYReader()
reader.SetFileName(os.path.join(data_dir, "dragon.ply"))
reader.Update()

mapper = vtkPolyDataMapper()
mapper.SetInputConnection(reader.GetOutputPort())

# Dragon 1: warm colors
actor_0 = vtkActor()
actor_0.SetMapper(mapper)
actor_0.GetProperty().SetAmbientColor(1.0, 0.0, 0.0)
actor_0.GetProperty().SetDiffuseColor(1.0, 0.8, 0.3)
actor_0.GetProperty().SetSpecular(0.0)
actor_0.GetProperty().SetDiffuse(0.5)
actor_0.GetProperty().SetAmbient(0.3)
actor_0.SetPosition(-0.1, 0.0, -0.1)

# Dragon 2: cool colors
actor_1 = vtkActor()
actor_1.SetMapper(mapper)
actor_1.GetProperty().SetAmbientColor(0.2, 0.2, 1.0)
actor_1.GetProperty().SetDiffuseColor(0.2, 1.0, 0.8)
actor_1.GetProperty().SetSpecularColor(1.0, 1.0, 1.0)
actor_1.GetProperty().SetSpecular(0.2)
actor_1.GetProperty().SetDiffuse(0.9)
actor_1.GetProperty().SetAmbient(0.1)
actor_1.GetProperty().SetSpecularPower(10.0)

# Dragon 3: blue-ish
actor_2 = vtkActor()
actor_2.SetMapper(mapper)
actor_2.GetProperty().SetDiffuseColor(0.5, 0.65, 1.0)
actor_2.GetProperty().SetSpecularColor(1.0, 1.0, 1.0)
actor_2.GetProperty().SetSpecular(0.7)
actor_2.GetProperty().SetDiffuse(0.4)
actor_2.GetProperty().SetSpecularPower(60.0)
actor_2.SetPosition(0.1, 0.0, 0.1)

# Renderer with motion blur pass
renderer = vtkRenderer()
renderer.SetBackground(0.3, 0.4, 0.6)
renderer.AddActor(actor_0)
renderer.AddActor(actor_1)
renderer.AddActor(actor_2)

basic_passes = vtkRenderStepsPass()
motion = vtkSimpleMotionBlurPass()
motion.SetDelegatePass(basic_passes)
renderer.SetPass(motion)

render_window = vtkRenderWindow()
render_window.SetSize(500, 500)
render_window.SetMultiSamples(0)
render_window.AddRenderer(renderer)
render_window.SetWindowName("simple motion blur")

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.GetActiveCamera().SetPosition(0, 0, 1)
renderer.GetActiveCamera().SetFocalPoint(0, 0, 0)
renderer.GetActiveCamera().SetViewUp(0, 1, 0)
renderer.ResetCamera()
renderer.GetActiveCamera().Azimuth(15.0)
renderer.GetActiveCamera().Zoom(1.8)

# Pipeline exception: multiple renders to accumulate motion blur
render_window.Render()
for i in range(30):
    renderer.GetActiveCamera().Azimuth(10.0 / 30)
    renderer.GetActiveCamera().Elevation(10.0 / 30)
    render_window.Render()

interactor.Initialize()
interactor.Start()
