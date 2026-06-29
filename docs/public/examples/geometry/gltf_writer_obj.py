#!/usr/bin/env python

# Read OBJ, write as glTF, re-import and render.

import os
import shutil
import tempfile

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonDataModel import vtkMultiBlockDataSet
from vtkmodules.vtkIOGeometry import (
    vtkGLTFWriter,
    vtkOBJReader,
)
from vtkmodules.vtkIOImport import vtkGLTFImporter
from vtkmodules.vtkRenderingCore import (
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Source
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Read OBJ file
obj_file = os.path.join(data_dir, "jacksonville_15.obj")
obj_reader = vtkOBJReader()
obj_reader.SetFileName(obj_file)
obj_reader.Update()

# Build multi-block structure
building = vtkMultiBlockDataSet()
building.SetBlock(0, obj_reader.GetOutput())

root = vtkMultiBlockDataSet()
root.SetBlock(0, building)

# Write as glTF
temp_dir = tempfile.mkdtemp()
output_name = os.path.join(temp_dir, "TestGLTFWriterObj.gltf")

gltf_writer = vtkGLTFWriter()
gltf_writer.SetFileName(output_name)
gltf_writer.SetTextureBaseDirectory(data_dir)
gltf_writer.SetInputDataObject(root)
gltf_writer.Write()

# Renderer
renderer = vtkRenderer()
renderer.SetBackground(0.5, 0.7, 0.7)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("gltf writer obj")
render_window.SetMultiSamples(0)
render_window.SetSize(400, 400)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Re-import the written glTF
gltf_importer = vtkGLTFImporter()
gltf_importer.SetFileName(output_name)
gltf_importer.SetCamera(-1)
gltf_importer.SetRenderWindow(render_window)
gltf_importer.Update()

# Scene
renderer.ResetCamera()

interactor.Initialize()
interactor.Start()

# Clean up
shutil.rmtree(temp_dir)
