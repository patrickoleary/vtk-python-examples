#!/usr/bin/env python

# Demonstrate SSAO using renderer convenience API on a dragon with ground plane.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

import os

from vtkmodules.vtkFiltersSources import vtkPlaneSource
from vtkmodules.vtkIOPLY import vtkPLYReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Dragon model
reader = vtkPLYReader()
reader.SetFileName(os.path.join(data_dir, "dragon.ply"))
reader.Update()

mapper = vtkPolyDataMapper()
mapper.SetInputConnection(reader.GetOutputPort())

actor = vtkActor()
actor.SetMapper(mapper)

# Ground plane under dragon
ply_bounds = mapper.GetBounds()
plane = vtkPlaneSource()
plane.SetOrigin(-0.2, ply_bounds[2], -0.2)
plane.SetPoint1(-0.2, ply_bounds[2], 0.2)
plane.SetPoint2(0.2, ply_bounds[2], -0.2)

plane_mapper = vtkPolyDataMapper()
plane_mapper.SetInputConnection(plane.GetOutputPort())

plane_actor = vtkActor()
plane_actor.SetMapper(plane_mapper)

# Renderer with SSAO via convenience API
renderer = vtkRenderer()
renderer.SetBackground(0.3, 0.4, 0.6)
renderer.AddActor(actor)
renderer.AddActor(plane_actor)
renderer.SetUseSSAO(True)
renderer.SetSSAORadius(0.05)
renderer.SetSSAOKernelSize(128)

render_window = vtkRenderWindow()
render_window.SetSize(600, 600)
render_window.SetMultiSamples(0)
render_window.AddRenderer(renderer)
render_window.SetWindowName("ssao pass with renderer")

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.GetActiveCamera().SetPosition(-0.2, 0.8, 1)
renderer.GetActiveCamera().SetFocalPoint(0, 0, 0)
renderer.GetActiveCamera().SetViewUp(0, 1, 0)
renderer.GetActiveCamera().OrthogonalizeViewUp()
renderer.ResetCamera()
renderer.GetActiveCamera().Zoom(2.5)

interactor.Initialize()
interactor.Start()
