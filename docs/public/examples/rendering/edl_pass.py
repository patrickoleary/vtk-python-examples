#!/usr/bin/env python

# Demonstrate Eye-Dome Lighting (EDL) shading render pass on dragon mesh.

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
from vtkmodules.vtkRenderingOpenGL2 import vtkEDLShading, vtkRenderStepsPass

# Read dragon mesh
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))
reader = vtkPLYReader()
reader.SetFileName(os.path.join(data_dir, "dragon.ply"))
reader.Update()

mapper = vtkPolyDataMapper()
mapper.SetInputConnection(reader.GetOutputPort())

actor = vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetAmbientColor(0.135, 0.2225, 0.3)
actor.GetProperty().SetDiffuseColor(0.54, 0.89, 0.63)
actor.GetProperty().SetDiffuse(0.7)
actor.GetProperty().SetAmbient(0.7)
actor.GetProperty().LightingOff()

# Renderer with EDL pass
renderer = vtkRenderer()
renderer.SetBackground(0.3, 0.4, 0.6)
renderer.AddActor(actor)

basic_passes = vtkRenderStepsPass()
edl = vtkEDLShading()
edl.SetDelegatePass(basic_passes)
renderer.SetPass(edl)

render_window = vtkRenderWindow()
render_window.SetSize(600, 600)
render_window.SetMultiSamples(0)
render_window.AddRenderer(renderer)
render_window.SetWindowName("edl pass")

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.GetActiveCamera().SetPosition(-0.2, 0.2, 1)
renderer.GetActiveCamera().SetFocalPoint(0, 0, 0)
renderer.GetActiveCamera().SetViewUp(0, 1, 0)
renderer.GetActiveCamera().OrthogonalizeViewUp()
renderer.ResetCamera()

interactor.Initialize()
interactor.Start()
