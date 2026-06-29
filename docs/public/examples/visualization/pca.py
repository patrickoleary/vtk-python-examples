#!/usr/bin/env python

# Demonstrate vtkPCAAnalysisFilter visualizing shape variation from a set of
# aligned objects using Procrustes alignment and PCA modes.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import vtkFloatArray
from vtkmodules.vtkCommonDataModel import vtkPolyData
from vtkmodules.vtkCommonTransforms import vtkTransform
from vtkmodules.vtkFiltersCore import vtkPolyDataNormals
from vtkmodules.vtkFiltersGeneral import (
    vtkMultiBlockDataGroupFilter,
    vtkTransformPolyDataFilter,
)
from vtkmodules.vtkFiltersHybrid import (
    vtkPCAAnalysisFilter,
    vtkProcrustesAlignmentFilter,
)
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
sphere.SetPhiResolution(36)
sphere.SetThetaResolution(36)
sphere.Update()

transform_1 = vtkTransform()
transform_1.Translate(0.2, 0.1, 0.3)
transform_1.Scale(1.3, 1.1, 0.8)

transform_2 = vtkTransform()
transform_2.Translate(0.3, 0.7, 0.1)
transform_2.Scale(1.0, 0.1, 1.8)

transformer_1 = vtkTransformPolyDataFilter()
transformer_1.SetInputConnection(sphere.GetOutputPort())
transformer_1.SetTransform(transform_1)
transformer_1.Update()

transformer_2 = vtkTransformPolyDataFilter()
transformer_2.SetInputConnection(sphere.GetOutputPort())
transformer_2.SetTransform(transform_2)
transformer_2.Update()

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

# -- Procrustes alignment (rigid body) --
group = vtkMultiBlockDataGroupFilter()
group.AddInputConnection(sphere.GetOutputPort())
group.AddInputConnection(transformer_1.GetOutputPort())
group.AddInputConnection(transformer_2.GetOutputPort())

procrustes = vtkProcrustesAlignmentFilter()
procrustes.SetInputConnection(group.GetOutputPort())
procrustes.GetLandmarkTransform().SetModeToRigidBody()
procrustes.Update()

# -- Viewport 1: aligned shapes --
mapper_1a = vtkPolyDataMapper()
mapper_1a.SetInputData(procrustes.GetOutput().GetBlock(0))
actor_1a = vtkActor()
actor_1a.SetMapper(mapper_1a)
actor_1a.GetProperty().SetDiffuseColor(1.0000, 0.3882, 0.2784)

mapper_1b = vtkPolyDataMapper()
mapper_1b.SetInputData(procrustes.GetOutput().GetBlock(1))
actor_1b = vtkActor()
actor_1b.SetMapper(mapper_1b)
actor_1b.GetProperty().SetDiffuseColor(0.3882, 1.0000, 0.2784)

mapper_1c = vtkPolyDataMapper()
mapper_1c.SetInputData(procrustes.GetOutput().GetBlock(2))
actor_1c = vtkActor()
actor_1c.SetMapper(mapper_1c)
actor_1c.GetProperty().SetDiffuseColor(0.3882, 0.2784, 1.0000)

# -- PCA analysis --
pca = vtkPCAAnalysisFilter()
pca.SetInputConnection(procrustes.GetOutputPort())
pca.Update()

# -- Viewport 2: first mode (-3, 0, +3 std deviations) --
params = vtkFloatArray()
params.SetNumberOfComponents(1)
params.SetNumberOfTuples(1)

params.SetTuple1(0, 0.0)
shape_2a = vtkPolyData()
shape_2a.DeepCopy(sphere.GetOutput())
pca.GetParameterisedShape(params, shape_2a)
normals_2a = vtkPolyDataNormals()
normals_2a.SetInputData(shape_2a)
mapper_2a = vtkPolyDataMapper()
mapper_2a.SetInputConnection(normals_2a.GetOutputPort())
actor_2a = vtkActor()
actor_2a.SetMapper(mapper_2a)
actor_2a.GetProperty().SetDiffuseColor(1, 1, 1)

params.SetTuple1(0, -3.0)
shape_2b = vtkPolyData()
shape_2b.DeepCopy(sphere.GetOutput())
pca.GetParameterisedShape(params, shape_2b)
normals_2b = vtkPolyDataNormals()
normals_2b.SetInputData(shape_2b)
mapper_2b = vtkPolyDataMapper()
mapper_2b.SetInputConnection(normals_2b.GetOutputPort())
actor_2b = vtkActor()
actor_2b.SetMapper(mapper_2b)
actor_2b.GetProperty().SetDiffuseColor(1, 1, 1)

params.SetTuple1(0, 3.0)
shape_2c = vtkPolyData()
shape_2c.DeepCopy(sphere.GetOutput())
pca.GetParameterisedShape(params, shape_2c)
normals_2c = vtkPolyDataNormals()
normals_2c.SetInputData(shape_2c)
mapper_2c = vtkPolyDataMapper()
mapper_2c.SetInputConnection(normals_2c.GetOutputPort())
actor_2c = vtkActor()
actor_2c.SetMapper(mapper_2c)
actor_2c.GetProperty().SetDiffuseColor(1, 1, 1)

# -- Viewport 3: second mode --
params_4 = vtkFloatArray()
params_4.SetNumberOfComponents(1)
params_4.SetNumberOfTuples(2)
params_4.SetTuple1(0, 0.0)

params_4.SetTuple1(1, -3.0)
shape_3a = vtkPolyData()
shape_3a.DeepCopy(sphere.GetOutput())
pca.GetParameterisedShape(params_4, shape_3a)
normals_3a = vtkPolyDataNormals()
normals_3a.SetInputData(shape_3a)
mapper_3a = vtkPolyDataMapper()
mapper_3a.SetInputConnection(normals_3a.GetOutputPort())
actor_3a = vtkActor()
actor_3a.SetMapper(mapper_3a)
actor_3a.GetProperty().SetDiffuseColor(1, 1, 1)

params_4.SetTuple1(1, 0.0)
shape_3b = vtkPolyData()
shape_3b.DeepCopy(sphere.GetOutput())
pca.GetParameterisedShape(params_4, shape_3b)
normals_3b = vtkPolyDataNormals()
normals_3b.SetInputData(shape_3b)
mapper_3b = vtkPolyDataMapper()
mapper_3b.SetInputConnection(normals_3b.GetOutputPort())
actor_3b = vtkActor()
actor_3b.SetMapper(mapper_3b)
actor_3b.GetProperty().SetDiffuseColor(1, 1, 1)

params_4.SetTuple1(1, 3.0)
shape_3c = vtkPolyData()
shape_3c.DeepCopy(sphere.GetOutput())
pca.GetParameterisedShape(params_4, shape_3c)
normals_3c = vtkPolyDataNormals()
normals_3c.SetInputData(shape_3c)
mapper_3c = vtkPolyDataMapper()
mapper_3c.SetInputConnection(normals_3c.GetOutputPort())
actor_3c = vtkActor()
actor_3c.SetMapper(mapper_3c)
actor_3c.GetProperty().SetDiffuseColor(1, 1, 1)

# -- Renderers --
renderer_0 = vtkRenderer()
renderer_0.AddActor(actor_0a)
renderer_0.AddActor(actor_0b)
renderer_0.AddActor(actor_0c)
renderer_0.SetBackground(1, 1, 1)
renderer_0.SetViewport(0.0, 0.0, 0.25, 1.0)

renderer_1 = vtkRenderer()
renderer_1.AddActor(actor_1a)
renderer_1.AddActor(actor_1b)
renderer_1.AddActor(actor_1c)
renderer_1.SetBackground(1, 1, 1)
renderer_1.SetViewport(0.25, 0.0, 0.5, 1.0)

renderer_2 = vtkRenderer()
renderer_2.AddActor(actor_2a)
renderer_2.AddActor(actor_2b)
renderer_2.AddActor(actor_2c)
renderer_2.SetBackground(1, 1, 1)
renderer_2.SetViewport(0.5, 0.0, 0.75, 1.0)

renderer_3 = vtkRenderer()
renderer_3.AddActor(actor_3a)
renderer_3.AddActor(actor_3b)
renderer_3.AddActor(actor_3c)
renderer_3.SetBackground(1, 1, 1)
renderer_3.SetViewport(0.75, 0.0, 1.0, 1.0)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer_0)
render_window.AddRenderer(renderer_1)
render_window.AddRenderer(renderer_2)
render_window.AddRenderer(renderer_3)
render_window.SetSize(600, 200)
render_window.SetWindowName("pca")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer_0.ResetCamera()
renderer_0.GetActiveCamera().SetPosition(1, -1, 0)
renderer_0.ResetCamera()

renderer_1.ResetCamera()
renderer_1.GetActiveCamera().SetPosition(1, -1, 0)
renderer_1.ResetCamera()

renderer_2.ResetCamera()
renderer_2.GetActiveCamera().SetPosition(1, -1, 0)
renderer_2.ResetCamera()

renderer_3.ResetCamera()
renderer_3.GetActiveCamera().SetPosition(1, -1, 0)
renderer_3.ResetCamera()

interactor.Initialize()
interactor.Start()
