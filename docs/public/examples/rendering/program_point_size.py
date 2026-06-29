#!/usr/bin/env python

# Demonstrate programmatic point size using a vertex shader replacement.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

sphere = vtkSphereSource()
sphere.SetThetaResolution(16)
sphere.SetPhiResolution(16)

mapper = vtkPolyDataMapper()
mapper.SetInputConnection(sphere.GetOutputPort())
mapper.UseProgramPointSizeOn()

actor = vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetRepresentationToPoints()

# Shader replacement: point size varies with depth
sp = actor.GetShaderProperty()
sp.AddVertexShaderReplacement(
    "//VTK::ValuePass::Impl", True,
    "gl_PointSize = (1.0 - gl_Position.z) * 8.0;\n"
    "///VTK::ValuePass::Impl\n",
    False,
)

renderer = vtkRenderer()
renderer.SetBackground(0.0, 0.0, 0.0)
renderer.AddActor(actor)

render_window = vtkRenderWindow()
render_window.SetSize(300, 300)
render_window.SetMultiSamples(0)
render_window.AddRenderer(renderer)
render_window.SetWindowName("program point size")

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.ResetCamera()
renderer.GetActiveCamera().Elevation(-45)
renderer.GetActiveCamera().OrthogonalizeViewUp()
renderer.GetActiveCamera().Zoom(1.5)
renderer.ResetCameraClippingRange()

interactor.Initialize()
interactor.Start()
