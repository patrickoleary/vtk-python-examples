#!/usr/bin/env python

# Demonstrate vtkProcrustesAlignmentFilter with StartFromCentroid enabled,
# comparing rigid body and similarity alignment in a 3-viewport layout.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonTransforms import vtkTransform
from vtkmodules.vtkFiltersGeneral import (
    vtkMultiBlockDataGroupFilter,
    vtkTransformPolyDataFilter,
)
from vtkmodules.vtkFiltersHybrid import vtkProcrustesAlignmentFilter
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Create a sphere and two distorted copies
sphere = vtkSphereSource()

transform_1 = vtkTransform()
transform_1.Translate(0.2, 0.1, 0.3)
transform_1.Scale(1.3, 1.1, 0.8)

transform_2 = vtkTransform()
transform_2.Translate(0.3, 0.7, 0.1)
transform_2.Scale(1.0, 0.1, 1.8)

transformer_1 = vtkTransformPolyDataFilter()
transformer_1.SetInputConnection(sphere.GetOutputPort())
transformer_1.SetTransform(transform_1)

transformer_2 = vtkTransformPolyDataFilter()
transformer_2.SetInputConnection(sphere.GetOutputPort())
transformer_2.SetTransform(transform_2)

# -- Viewport 0: original shapes --
mapper_0a = vtkPolyDataMapper()
mapper_0a.SetInputConnection(sphere.GetOutputPort())
actor_0a = vtkActor()
actor_0a.SetMapper(mapper_0a)
actor_0a.GetProperty().SetDiffuseColor(1.0000, 0.3882, 0.2784)

mapper_0b = vtkPolyDataMapper()
mapper_0b.SetInputConnection(transformer_1.GetOutputPort())
actor_0b = vtkActor()
actor_0b.SetMapper(mapper_0b)
actor_0b.GetProperty().SetDiffuseColor(0.3882, 1.0000, 0.2784)

mapper_0c = vtkPolyDataMapper()
mapper_0c.SetInputConnection(transformer_2.GetOutputPort())
actor_0c = vtkActor()
actor_0c.SetMapper(mapper_0c)
actor_0c.GetProperty().SetDiffuseColor(0.3882, 0.2784, 1.0000)

# -- Procrustes rigid body alignment with centroid start --
group = vtkMultiBlockDataGroupFilter()
group.AddInputConnection(sphere.GetOutputPort())
group.AddInputConnection(transformer_1.GetOutputPort())
group.AddInputConnection(transformer_2.GetOutputPort())

procrustes_1 = vtkProcrustesAlignmentFilter()
procrustes_1.SetInputConnection(group.GetOutputPort())
procrustes_1.GetLandmarkTransform().SetModeToRigidBody()
procrustes_1.StartFromCentroidOn()
procrustes_1.Update()

# -- Viewport 1: rigid body aligned shapes --
mapper_1a = vtkPolyDataMapper()
mapper_1a.SetInputData(procrustes_1.GetOutput().GetBlock(0))
actor_1a = vtkActor()
actor_1a.SetMapper(mapper_1a)
actor_1a.GetProperty().SetDiffuseColor(1.0000, 0.3882, 0.2784)

mapper_1b = vtkPolyDataMapper()
mapper_1b.SetInputData(procrustes_1.GetOutput().GetBlock(1))
actor_1b = vtkActor()
actor_1b.SetMapper(mapper_1b)
actor_1b.GetProperty().SetDiffuseColor(0.3882, 1.0000, 0.2784)

mapper_1c = vtkPolyDataMapper()
mapper_1c.SetInputData(procrustes_1.GetOutput().GetBlock(2))
actor_1c = vtkActor()
actor_1c.SetMapper(mapper_1c)
actor_1c.GetProperty().SetDiffuseColor(0.3882, 0.2784, 1.0000)

# -- Procrustes similarity alignment (default) --
procrustes_2 = vtkProcrustesAlignmentFilter()
procrustes_2.SetInputConnection(group.GetOutputPort())
procrustes_2.Update()

# -- Viewport 2: similarity aligned shapes --
mapper_2a = vtkPolyDataMapper()
mapper_2a.SetInputData(procrustes_2.GetOutput().GetBlock(0))
actor_2a = vtkActor()
actor_2a.SetMapper(mapper_2a)
actor_2a.GetProperty().SetDiffuseColor(1.0000, 0.3882, 0.2784)

mapper_2b = vtkPolyDataMapper()
mapper_2b.SetInputData(procrustes_2.GetOutput().GetBlock(1))
actor_2b = vtkActor()
actor_2b.SetMapper(mapper_2b)
actor_2b.GetProperty().SetDiffuseColor(0.3882, 1.0000, 0.2784)

mapper_2c = vtkPolyDataMapper()
mapper_2c.SetInputData(procrustes_2.GetOutput().GetBlock(2))
actor_2c = vtkActor()
actor_2c.SetMapper(mapper_2c)
actor_2c.GetProperty().SetDiffuseColor(0.3882, 0.2784, 1.0000)

# -- Renderers --
renderer_0 = vtkRenderer()
renderer_0.AddActor(actor_0a)
renderer_0.AddActor(actor_0b)
renderer_0.AddActor(actor_0c)
renderer_0.SetBackground(1, 1, 1)
renderer_0.SetViewport(0.0, 0.0, 0.33, 1.0)

renderer_1 = vtkRenderer()
renderer_1.AddActor(actor_1a)
renderer_1.AddActor(actor_1b)
renderer_1.AddActor(actor_1c)
renderer_1.SetBackground(1, 1, 1)
renderer_1.SetViewport(0.33, 0.0, 0.66, 1.0)

renderer_2 = vtkRenderer()
renderer_2.AddActor(actor_2a)
renderer_2.AddActor(actor_2b)
renderer_2.AddActor(actor_2c)
renderer_2.SetBackground(1, 1, 1)
renderer_2.SetViewport(0.66, 0.0, 1.0, 1.0)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer_0)
render_window.AddRenderer(renderer_1)
render_window.AddRenderer(renderer_2)
render_window.SetSize(300, 100)
render_window.SetWindowName("procrustes rigid centroid")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer_0.ResetCamera()
renderer_0.GetActiveCamera().SetPosition(1, -1, 0)
renderer_0.ResetCamera()

# Share camera from renderer_0 (matches original test)
renderer_1.SetActiveCamera(renderer_0.GetActiveCamera())

renderer_2.ResetCamera()
renderer_2.GetActiveCamera().SetPosition(1, -1, 0)
renderer_2.ResetCamera()

interactor.Initialize()
interactor.Start()
