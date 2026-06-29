#!/usr/bin/env python

# Demonstrate changing renderers with the same SSAA pass on a dragon model.

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
actor.GetProperty().SetLineWidth(2)

# SSAA pass
basic_passes = vtkRenderStepsPass()
ssaa = vtkSSAAPass()
ssaa.SetDelegatePass(basic_passes)

# First renderer
renderer_0 = vtkRenderer()
renderer_0.AddActor(actor)
renderer_0.SetPass(ssaa)

render_window = vtkRenderWindow()
render_window.SetSize(500, 500)
render_window.SetMultiSamples(0)
render_window.SetAlphaBitPlanes(1)
render_window.AddRenderer(renderer_0)
render_window.SetWindowName("ssaa pass change renderers")

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

renderer_0.ResetCamera()
render_window.Render()

# Switch to second renderer with same SSAA pass
renderer_1 = vtkRenderer()
render_window.RemoveRenderer(renderer_0)
render_window.AddRenderer(renderer_1)
renderer_1.SetPass(ssaa)
renderer_1.AddActor(actor)
renderer_1.ResetCamera()

render_window.Render()
interactor.Initialize()
interactor.Start()
