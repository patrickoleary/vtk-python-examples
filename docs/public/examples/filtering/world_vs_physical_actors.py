#!/usr/bin/env python

# Test world vs physical coordinate system actors with camera travel matrix.

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

renwin_width = 512
renwin_height = 512

# Two cone sources
cone_1 = vtkConeSource()
cone_1.SetResolution(32)

cone_2 = vtkConeSource()
cone_2.SetResolution(32)

mapper_1 = vtkPolyDataMapper()
mapper_1.SetInputConnection(cone_1.GetOutputPort())

mapper_2 = vtkPolyDataMapper()
mapper_2.SetInputConnection(cone_2.GetOutputPort())

renderer = vtkRenderer()

# Red cone in world coordinates
world_actor = vtkActor()
world_actor.SetMapper(mapper_1)
world_actor.GetProperty().SetColor(1.0, 0.0, 0.0)
world_actor.SetCoordinateSystemToWorld()
world_actor.SetCoordinateSystemRenderer(renderer)

# Green cone in physical coordinates
physical_actor = vtkActor()
physical_actor.SetMapper(mapper_2)
physical_actor.GetProperty().SetColor(0.0, 1.0, 0.0)
physical_actor.SetCoordinateSystemToPhysical()
physical_actor.SetCoordinateSystemRenderer(renderer)

renderer.AddActor(world_actor)
renderer.AddActor(physical_actor)

render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("world vs physical actors")
render_window.SetMultiSamples(0)
render_window.SetSize(renwin_width, renwin_height)

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
model_matrix = vtkMatrix4x4()
tform = vtkTransform()
tform.Identity()
tform.Translate(0.5, 0.5, 0)
model_matrix.Multiply4x4(model_matrix, tform.GetMatrix(), model_matrix)

camera = renderer.GetActiveCamera()
camera.SetModelTransformMatrix(model_matrix)
camera.Modified()

physical_to_world = vtkMatrix4x4()
physical_to_world.DeepCopy(model_matrix)
physical_to_world.Invert()
render_window.SetPhysicalToWorldMatrix(physical_to_world)

render_window.Render()
renderer.ResetCamera()

interactor.Initialize()
interactor.Start()
