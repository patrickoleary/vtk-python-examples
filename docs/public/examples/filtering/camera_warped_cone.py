#!/usr/bin/env python

# Test camera distortion using a user transform on a cone.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonMath import vtkMatrix4x4
from vtkmodules.vtkCommonTransforms import vtkTransform
from vtkmodules.vtkFiltersSources import vtkConeSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Cone geometry
cone = vtkConeSource()
cone.SetResolution(8)

cone_mapper = vtkPolyDataMapper()
cone_mapper.SetInputConnection(cone.GetOutputPort())

cone_actor = vtkActor()
cone_actor.SetMapper(cone_mapper)

# Create a transform that squashes the X axis by 0.5
matrix = vtkMatrix4x4()
matrix.SetElement(0, 0, 0.5)

transform = vtkTransform()
transform.SetMatrix(matrix)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(cone_actor)

render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("camera warped cone")
render_window.SetMultiSamples(0)
render_window.SetSize(300, 300)

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.ResetCamera()
renderer.GetActiveCamera().SetUserTransform(transform)

interactor.Initialize()
interactor.Start()
