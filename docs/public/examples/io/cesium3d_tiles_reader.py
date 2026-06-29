#!/usr/bin/env python

# Read a Cesium 3D Tiles tileset and render with textures.

import os

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import vtkInformation
from vtkmodules.vtkIOCesium3DTiles import vtkCesium3DTilesReader
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
tileset_reader = vtkCesium3DTilesReader()
tileset_reader.SetFileName(os.path.join(data_dir, "jacksonville-gltf", "tileset.json"))
tileset_reader.Update()

output_data = tileset_reader.GetOutput()

# Renderer
renderer = vtkRenderer()
renderer.SetBackground(0.5, 0.7, 0.7)

# Texture coordinate flip matrix
texture_transform = [1, 0, 0, 0, 0, -1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1]

# Partitioned dataset 0, partition 0
pds_0 = output_data.GetPartitionedDataSet(0)
gltf_reader_0 = vtkGLTFReader.SafeDownCast(tileset_reader.GetTileReader(0))

mapper_0_0 = vtkPolyDataMapper()
mapper_0_0.SetInputDataObject(pds_0.GetPartition(0))
actor_0_0 = vtkActor()
actor_0_0.SetMapper(mapper_0_0)
information_0_0 = vtkInformation()
actor_0_0.SetPropertyKeys(information_0_0)
information_0_0.Set(vtkProp.GENERAL_TEXTURE_TRANSFORM(), texture_transform, 16)
actor_0_0.SetTexture(gltf_reader_0.GetTexture(0).GetVTKTexture())
renderer.AddActor(actor_0_0)

# Partitioned dataset 0, partition 1
mapper_0_1 = vtkPolyDataMapper()
mapper_0_1.SetInputDataObject(pds_0.GetPartition(1))
actor_0_1 = vtkActor()
actor_0_1.SetMapper(mapper_0_1)
information_0_1 = vtkInformation()
actor_0_1.SetPropertyKeys(information_0_1)
information_0_1.Set(vtkProp.GENERAL_TEXTURE_TRANSFORM(), texture_transform, 16)
actor_0_1.SetTexture(gltf_reader_0.GetTexture(1).GetVTKTexture())
renderer.AddActor(actor_0_1)

# Partitioned dataset 0, partition 2
mapper_0_2 = vtkPolyDataMapper()
mapper_0_2.SetInputDataObject(pds_0.GetPartition(2))
actor_0_2 = vtkActor()
actor_0_2.SetMapper(mapper_0_2)
information_0_2 = vtkInformation()
actor_0_2.SetPropertyKeys(information_0_2)
information_0_2.Set(vtkProp.GENERAL_TEXTURE_TRANSFORM(), texture_transform, 16)
actor_0_2.SetTexture(gltf_reader_0.GetTexture(2).GetVTKTexture())
renderer.AddActor(actor_0_2)

# Partitioned dataset 1, partition 0
pds_1 = output_data.GetPartitionedDataSet(1)
gltf_reader_1 = vtkGLTFReader.SafeDownCast(tileset_reader.GetTileReader(1))

mapper_1_0 = vtkPolyDataMapper()
mapper_1_0.SetInputDataObject(pds_1.GetPartition(0))
actor_1_0 = vtkActor()
actor_1_0.SetMapper(mapper_1_0)
information_1_0 = vtkInformation()
actor_1_0.SetPropertyKeys(information_1_0)
information_1_0.Set(vtkProp.GENERAL_TEXTURE_TRANSFORM(), texture_transform, 16)
actor_1_0.SetTexture(gltf_reader_1.GetTexture(0).GetVTKTexture())
renderer.AddActor(actor_1_0)

# Partitioned dataset 2, partition 0
pds_2 = output_data.GetPartitionedDataSet(2)
gltf_reader_2 = vtkGLTFReader.SafeDownCast(tileset_reader.GetTileReader(2))

mapper_2_0 = vtkPolyDataMapper()
mapper_2_0.SetInputDataObject(pds_2.GetPartition(0))
actor_2_0 = vtkActor()
actor_2_0.SetMapper(mapper_2_0)
information_2_0 = vtkInformation()
actor_2_0.SetPropertyKeys(information_2_0)
information_2_0.Set(vtkProp.GENERAL_TEXTURE_TRANSFORM(), texture_transform, 16)
actor_2_0.SetTexture(gltf_reader_2.GetTexture(0).GetVTKTexture())
renderer.AddActor(actor_2_0)

# Partitioned dataset 2, partition 1
mapper_2_1 = vtkPolyDataMapper()
mapper_2_1.SetInputDataObject(pds_2.GetPartition(1))
actor_2_1 = vtkActor()
actor_2_1.SetMapper(mapper_2_1)
information_2_1 = vtkInformation()
actor_2_1.SetPropertyKeys(information_2_1)
information_2_1.Set(vtkProp.GENERAL_TEXTURE_TRANSFORM(), texture_transform, 16)
actor_2_1.SetTexture(gltf_reader_2.GetTexture(1).GetVTKTexture())
renderer.AddActor(actor_2_1)

# Partitioned dataset 2, partition 2
mapper_2_2 = vtkPolyDataMapper()
mapper_2_2.SetInputDataObject(pds_2.GetPartition(2))
actor_2_2 = vtkActor()
actor_2_2.SetMapper(mapper_2_2)
information_2_2 = vtkInformation()
actor_2_2.SetPropertyKeys(information_2_2)
information_2_2.Set(vtkProp.GENERAL_TEXTURE_TRANSFORM(), texture_transform, 16)
actor_2_2.SetTexture(gltf_reader_2.GetTexture(2).GetVTKTexture())
renderer.AddActor(actor_2_2)

# Partitioned dataset 3, partition 0
pds_3 = output_data.GetPartitionedDataSet(3)
gltf_reader_3 = vtkGLTFReader.SafeDownCast(tileset_reader.GetTileReader(3))

mapper_3_0 = vtkPolyDataMapper()
mapper_3_0.SetInputDataObject(pds_3.GetPartition(0))
actor_3_0 = vtkActor()
actor_3_0.SetMapper(mapper_3_0)
information_3_0 = vtkInformation()
actor_3_0.SetPropertyKeys(information_3_0)
information_3_0.Set(vtkProp.GENERAL_TEXTURE_TRANSFORM(), texture_transform, 16)
actor_3_0.SetTexture(gltf_reader_3.GetTexture(0).GetVTKTexture())
renderer.AddActor(actor_3_0)

# Partitioned dataset 3, partition 1
mapper_3_1 = vtkPolyDataMapper()
mapper_3_1.SetInputDataObject(pds_3.GetPartition(1))
actor_3_1 = vtkActor()
actor_3_1.SetMapper(mapper_3_1)
information_3_1 = vtkInformation()
actor_3_1.SetPropertyKeys(information_3_1)
information_3_1.Set(vtkProp.GENERAL_TEXTURE_TRANSFORM(), texture_transform, 16)
actor_3_1.SetTexture(gltf_reader_3.GetTexture(1).GetVTKTexture())
renderer.AddActor(actor_3_1)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("cesium3d tiles reader")
render_window.SetMultiSamples(0)
render_window.SetSize(400, 400)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.ResetCamera()
renderer.GetActiveCamera().Elevation(-45)
renderer.GetActiveCamera().Azimuth(-45)
renderer.GetActiveCamera().Zoom(1.2)

interactor.Initialize()
interactor.Start()
