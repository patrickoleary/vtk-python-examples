#!/usr/bin/env python

# Demonstrate vtkConeSource at varying resolutions (0, 1, 2, 8) with
# different colors, arranged horizontally in a single renderer.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersSources import vtkConeSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Cones with varying resolution
cone_0 = vtkConeSource()
cone_0.SetResolution(0)

cone_1 = vtkConeSource()
cone_1.SetResolution(1)

cone_2 = vtkConeSource()
cone_2.SetResolution(2)

cone_8 = vtkConeSource()
cone_8.SetResolution(8)

cone_0_mapper = vtkPolyDataMapper()
cone_0_mapper.SetInputConnection(cone_0.GetOutputPort())

cone_0_actor = vtkActor()
cone_0_actor.SetMapper(cone_0_mapper)
cone_0_actor.SetPosition(-1.5, 0, 0)
cone_0_actor.GetProperty().SetDiffuseColor(1, 0, 0)

cone_1_mapper = vtkPolyDataMapper()
cone_1_mapper.SetInputConnection(cone_1.GetOutputPort())

cone_1_actor = vtkActor()
cone_1_actor.SetMapper(cone_1_mapper)
cone_1_actor.SetPosition(-0.5, 0, 0)
cone_1_actor.GetProperty().SetDiffuseColor(0, 1, 0)

cone_2_mapper = vtkPolyDataMapper()
cone_2_mapper.SetInputConnection(cone_2.GetOutputPort())

cone_2_actor = vtkActor()
cone_2_actor.SetMapper(cone_2_mapper)
cone_2_actor.SetPosition(0.5, 0, 0)

cone_8_mapper = vtkPolyDataMapper()
cone_8_mapper.SetInputConnection(cone_8.GetOutputPort())

cone_8_actor = vtkActor()
cone_8_actor.SetMapper(cone_8_mapper)
cone_8_actor.SetPosition(1.5, 0, 0)
cone_8_actor.GetProperty().BackfaceCullingOn()
cone_8_actor.GetProperty().SetDiffuseColor(0, 0, 1)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(cone_0_actor)
renderer.AddActor(cone_1_actor)
renderer.AddActor(cone_2_actor)
renderer.AddActor(cone_8_actor)
renderer.SetBackground(0.5, 0.5, 0.5)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(300, 90)
render_window.SetWindowName("cone resolution")

# Scene
renderer.ResetCamera()
renderer.GetActiveCamera().Elevation(30)
renderer.GetActiveCamera().Dolly(1.3)
renderer.ResetCameraClippingRange()

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
