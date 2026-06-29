#!/usr/bin/env python

# Demonstrate FXAA combined with EDL shading render pass on a cylinder.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersSources import vtkCylinderSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)
from vtkmodules.vtkRenderingOpenGL2 import (
    vtkEDLShading,
    vtkOpenGLFXAAPass,
    vtkRenderStepsPass,
)

# Cylinder
cylinder = vtkCylinderSource()
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(cylinder.GetOutputPort())
actor = vtkActor()
actor.SetMapper(mapper)

# Renderer with FXAA + EDL pass chain
renderer = vtkRenderer()
renderer.SetBackground(1.0, 1.0, 1.0)
renderer.AddActor(actor)

basic_passes = vtkRenderStepsPass()
edl = vtkEDLShading()
edl.SetDelegatePass(basic_passes)
fxaa = vtkOpenGLFXAAPass()
fxaa.SetDelegatePass(edl)
renderer.SetPass(fxaa)

# Render window
render_window = vtkRenderWindow()
render_window.SetMultiSamples(0)
render_window.AddRenderer(renderer)
render_window.SetWindowName("fxaa with edl pass")

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.ResetCamera()
camera = renderer.GetActiveCamera()
camera.SetViewUp(-0.45365, 0.78693, -0.418262)
camera.SetPosition(-0.388464, 0.574701, 0.0925649)
camera.SetFocalPoint(-0.50418, 0.453051, -0.0108049)
renderer.ResetCameraClippingRange()

interactor.Initialize()
interactor.Start()
