#!/usr/bin/env python

# Read a Cesium B3DM (GLB) file and render with textures.

import os

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import vtkInformation
from vtkmodules.vtkIOGeometry import vtkGLTFReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkProp,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Source
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))
gltf_reader = vtkGLTFReader()
gltf_reader.SetFileName(os.path.join(data_dir, "jacksonville-gltf", "9", "9.glb"))
gltf_reader.Update()
multi_block = gltf_reader.GetOutput()

# Texture coordinate flip matrix
texture_transform = [1, 0, 0, 0, 0, -1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1]

# Leaf polydata is nested: multi_block -> scene -> mesh_group -> polydata
mesh_group = multi_block.GetBlock(0).GetBlock(0)

# Mapper + Actor 0
mapper_0 = vtkPolyDataMapper()
mapper_0.SetInputDataObject(mesh_group.GetBlock(0))
actor_0 = vtkActor()
actor_0.SetMapper(mapper_0)
information_0 = vtkInformation()
actor_0.SetPropertyKeys(information_0)
information_0.Set(vtkProp.GENERAL_TEXTURE_TRANSFORM(), texture_transform, 16)
actor_0.SetTexture(gltf_reader.GetTexture(0).GetVTKTexture())

# Mapper + Actor 1
mapper_1 = vtkPolyDataMapper()
mapper_1.SetInputDataObject(mesh_group.GetBlock(1))
actor_1 = vtkActor()
actor_1.SetMapper(mapper_1)
information_1 = vtkInformation()
actor_1.SetPropertyKeys(information_1)
information_1.Set(vtkProp.GENERAL_TEXTURE_TRANSFORM(), texture_transform, 16)
actor_1.SetTexture(gltf_reader.GetTexture(1).GetVTKTexture())

# Mapper + Actor 2
mapper_2 = vtkPolyDataMapper()
mapper_2.SetInputDataObject(mesh_group.GetBlock(2))
actor_2 = vtkActor()
actor_2.SetMapper(mapper_2)
information_2 = vtkInformation()
actor_2.SetPropertyKeys(information_2)
information_2.Set(vtkProp.GENERAL_TEXTURE_TRANSFORM(), texture_transform, 16)
actor_2.SetTexture(gltf_reader.GetTexture(2).GetVTKTexture())

# Renderer
renderer = vtkRenderer()
renderer.AddActor(actor_0)
renderer.AddActor(actor_1)
renderer.AddActor(actor_2)
renderer.SetBackground(0.5, 0.7, 0.7)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("cesium b3dm reader")
render_window.SetMultiSamples(0)
render_window.SetSize(400, 400)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.ResetCamera()
renderer.GetActiveCamera().Zoom(1.1)

interactor.Initialize()
interactor.Start()
