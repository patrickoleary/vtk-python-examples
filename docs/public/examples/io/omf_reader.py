#!/usr/bin/env python

# Read an OMF file and render topography, collar, assay, and block model data.

import os

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkIOOMF import vtkOMFReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkDataSetMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Source
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

omf_reader = vtkOMFReader()
omf_reader.SetFileName(os.path.join(data_dir, "omf-test-file.omf"))
omf_reader.UpdateInformation()

omf_reader.SetDataElementArrayStatus("collar", 1)
omf_reader.SetDataElementArrayStatus("wolfpass_WP_assay", 1)
omf_reader.SetDataElementArrayStatus("Topography", 1)
omf_reader.SetDataElementArrayStatus("Basement", 1)
omf_reader.SetDataElementArrayStatus("Early Diorite", 1)
omf_reader.SetDataElementArrayStatus("Intermineral diorite", 1)
omf_reader.SetDataElementArrayStatus("Dacite", 1)
omf_reader.SetDataElementArrayStatus("Cover", 1)
omf_reader.SetDataElementArrayStatus("Block Model", 1)
omf_reader.Update()

omf_output = omf_reader.GetOutput()

# Mapper / Actor - collar
collar_mapper = vtkDataSetMapper()
collar_mapper.SetInputDataObject(omf_output.GetPartitionedDataSet(0).GetPartition(0))

collar_actor = vtkActor()
collar_actor.SetMapper(collar_mapper)

# Mapper / Actor - assay
assay_mapper = vtkDataSetMapper()
assay_mapper.SetInputDataObject(omf_output.GetPartitionedDataSet(1).GetPartition(0))

assay_actor = vtkActor()
assay_actor.SetMapper(assay_mapper)

# Mapper / Actor - topography
topography_mapper = vtkDataSetMapper()
topography_mapper.SetInputDataObject(omf_output.GetPartitionedDataSet(2).GetPartition(0))

topography_actor = vtkActor()
topography_actor.SetMapper(topography_mapper)

# Mapper / Actor - basement
basement_mapper = vtkDataSetMapper()
basement_mapper.SetInputDataObject(omf_output.GetPartitionedDataSet(3).GetPartition(0))

basement_actor = vtkActor()
basement_actor.SetMapper(basement_mapper)

# Mapper / Actor - early diorite
early_diorite_mapper = vtkDataSetMapper()
early_diorite_mapper.SetInputDataObject(omf_output.GetPartitionedDataSet(4).GetPartition(0))

early_diorite_actor = vtkActor()
early_diorite_actor.SetMapper(early_diorite_mapper)

# Mapper / Actor - intermineral diorite
intermineral_diorite_mapper = vtkDataSetMapper()
intermineral_diorite_mapper.SetInputDataObject(omf_output.GetPartitionedDataSet(5).GetPartition(0))

intermineral_diorite_actor = vtkActor()
intermineral_diorite_actor.SetMapper(intermineral_diorite_mapper)

# Mapper / Actor - dacite
dacite_mapper = vtkDataSetMapper()
dacite_mapper.SetInputDataObject(omf_output.GetPartitionedDataSet(6).GetPartition(0))

dacite_actor = vtkActor()
dacite_actor.SetMapper(dacite_mapper)

# Mapper / Actor - cover
cover_mapper = vtkDataSetMapper()
cover_mapper.SetInputDataObject(omf_output.GetPartitionedDataSet(7).GetPartition(0))

cover_actor = vtkActor()
cover_actor.SetMapper(cover_mapper)

# Mapper / Actor - block model
block_model_mapper = vtkDataSetMapper()
block_model_mapper.SetInputDataObject(omf_output.GetPartitionedDataSet(8).GetPartition(0))

block_model_actor = vtkActor()
block_model_actor.SetMapper(block_model_mapper)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(collar_actor)
renderer.AddActor(assay_actor)
renderer.AddActor(topography_actor)
renderer.AddActor(basement_actor)
renderer.AddActor(early_diorite_actor)
renderer.AddActor(intermineral_diorite_actor)
renderer.AddActor(dacite_actor)
renderer.AddActor(cover_actor)
renderer.AddActor(block_model_actor)
renderer.SetBackground(0.2, 0.3, 0.4)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("omf reader")
render_window.SetMultiSamples(0)
render_window.SetSize(400, 400)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.ResetCamera()

interactor.Initialize()
interactor.Start()
