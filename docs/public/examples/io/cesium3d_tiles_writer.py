#!/usr/bin/env python

# Write 3D Tiles from OBJ and CityGML buildings, then import and render the church model.

import os
import tempfile

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import vtkStringArray
from vtkmodules.vtkCommonDataModel import vtkFieldData, vtkMultiBlockDataSet
from vtkmodules.vtkIOCesium3DTiles import vtkCesium3DTilesWriter
from vtkmodules.vtkIOCityGML import vtkCityGMLReader
from vtkmodules.vtkIOGeometry import vtkOBJReader
from vtkmodules.vtkIOImport import vtkGLTFImporter
from vtkmodules.vtkRenderingCore import (
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Source
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))
temp_dir = tempfile.mkdtemp()

# --- Test Jacksonville Buildings (OBJ) ---
print("Test jacksonville buildings")

obj_reader = vtkOBJReader()
obj_reader.SetFileName(os.path.join(data_dir, "jacksonville-triangle.obj"))
obj_reader.Update()

# Parse offset from OBJ comment
obj_comment = obj_reader.GetComment()
obj_offset = [0.0, 0.0, 0.0]
if obj_comment:
    parts = obj_comment.split()
    idx = 0
    for i in range(3):
        if idx + 2 < len(parts):
            obj_offset[i] = float(parts[idx + 2])
            idx += 3

# Set texture URI field on poly data
obj_poly = obj_reader.GetOutput()
obj_texture_file = os.path.splitext(os.path.join(data_dir, "jacksonville-triangle.obj"))[0] + ".png"
if os.path.isfile(obj_texture_file):
    field_data = obj_poly.GetFieldData()
    if not field_data:
        field_data = vtkFieldData()
        obj_poly.SetFieldData(field_data)
    string_array = vtkStringArray()
    string_array.SetNumberOfTuples(1)
    string_array.SetValue(0, obj_texture_file)
    string_array.SetName("texture_uri")
    field_data.AddArray(string_array)

# Build multi-block for Jacksonville
jax_building = vtkMultiBlockDataSet()
jax_building.SetBlock(0, obj_poly)
jax_root = vtkMultiBlockDataSet()
jax_root.SetBlock(0, jax_building)

jax_writer = vtkCesium3DTilesWriter()
jax_writer.SetInputDataObject(jax_root)
jax_writer.SetContentGLTF(True)
jax_writer.ContentGLTFSaveGLBOff()
jax_writer.SetInputType(vtkCesium3DTilesWriter.Buildings)
jax_writer.SetDirectoryName(os.path.join(temp_dir, "jacksonville-3dtiles"))
jax_writer.SetTextureBaseDirectory(data_dir)
jax_writer.SetOffset(obj_offset)
jax_writer.SetSaveTextures(False)
jax_writer.SetNumberOfFeaturesPerTile(1)
jax_writer.SetSaveTiles(True)
jax_writer.SetCRS("+proj=utm +zone=17")
jax_writer.Write()

# --- Test Berlin Buildings (CityGML) ---
print("Test berlin buildings (citygml)")

berlin_reader = vtkCityGMLReader()
berlin_reader.SetFileName(os.path.join(data_dir, "berlin-triangle.gml"))
berlin_reader.SetNumberOfBuildings(1)
berlin_reader.SetLOD(2)
berlin_reader.Update()

berlin_writer = vtkCesium3DTilesWriter()
berlin_writer.SetInputDataObject(berlin_reader.GetOutput())
berlin_writer.SetContentGLTF(True)
berlin_writer.ContentGLTFSaveGLBOff()
berlin_writer.SetInputType(vtkCesium3DTilesWriter.Buildings)
berlin_writer.SetDirectoryName(os.path.join(temp_dir, "berlin-3dtiles"))
berlin_writer.SetTextureBaseDirectory(data_dir)
berlin_writer.SetOffset([0.0, 0.0, 0.0])
berlin_writer.SetSaveTextures(False)
berlin_writer.SetNumberOfFeaturesPerTile(1)
berlin_writer.SetSaveTiles(True)
berlin_writer.SetCRS("+proj=utm +zone=33")
berlin_writer.Write()

# --- Test Church Buildings (CityGML) with rendering ---
print("Test merge textures church (citygml)")

church_reader = vtkCityGMLReader()
church_reader.SetFileName(os.path.join(data_dir, "CityGML", "Part-4-Buildings-V4-one.gml"))
church_reader.SetNumberOfBuildings(1)
church_reader.SetLOD(3)
church_reader.Update()

church_writer = vtkCesium3DTilesWriter()
church_writer.SetInputDataObject(church_reader.GetOutput())
church_writer.SetContentGLTF(True)
church_writer.ContentGLTFSaveGLBOff()
church_writer.SetInputType(vtkCesium3DTilesWriter.Buildings)
church_writer.SetDirectoryName(os.path.join(temp_dir, "church-3dtiles"))
church_writer.SetTextureBaseDirectory(os.path.join(data_dir, "CityGML"))
church_writer.SetOffset([435200.0, 3354000.0, 0.0])
church_writer.SetSaveTextures(True)
church_writer.SetNumberOfFeaturesPerTile(1)
church_writer.SetSaveTiles(True)
church_writer.SetCRS("+proj=utm +zone=17")
church_writer.Write()

# Renderer
renderer = vtkRenderer()
renderer.SetBackground(0.5, 0.7, 0.7)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("cesium3d tiles writer")
render_window.SetMultiSamples(0)
render_window.SetSize(400, 400)

# Import the generated GLTF
gltf_importer = vtkGLTFImporter()
gltf_importer.SetFileName(os.path.join(temp_dir, "church-3dtiles", "0", "0.gltf"))
gltf_importer.SetRenderWindow(render_window)
gltf_importer.Update()

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.ResetCamera()
renderer.GetActiveCamera().Azimuth(90)
renderer.GetActiveCamera().Roll(-90)
renderer.GetActiveCamera().Zoom(1.5)

interactor.Initialize()
interactor.Start()
