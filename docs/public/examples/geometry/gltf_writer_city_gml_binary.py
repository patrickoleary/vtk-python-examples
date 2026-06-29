#!/usr/bin/env python

# Read CityGML, write as binary GLB, re-import and render.

import os
import tempfile

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkIOCityGML import vtkCityGMLReader
from vtkmodules.vtkIOGeometry import vtkGLTFWriter
from vtkmodules.vtkIOImport import vtkGLTFImporter
from vtkmodules.vtkRenderingCore import (
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Source
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Read CityGML
citygml_reader = vtkCityGMLReader()
citygml_reader.SetFileName(os.path.join(data_dir, "CityGML", "Part-4-Buildings-V4-one.gml"))
citygml_reader.SetLOD(3)
citygml_reader.Update()
output_data = citygml_reader.GetOutputDataObject(0)

# Write as binary GLB
temp_dir = tempfile.mkdtemp()
output_name = os.path.join(temp_dir, "TestGLTFWriterCityGMLBinary.glb")

gltf_writer = vtkGLTFWriter()
gltf_writer.SetFileName(output_name)
gltf_writer.SetTextureBaseDirectory(os.path.dirname(os.path.join(data_dir, "CityGML", "Part-4-Buildings-V4-one.gml")))
gltf_writer.SetInputDataObject(output_data)
gltf_writer.Write()

# Renderer
renderer = vtkRenderer()
renderer.SetBackground(0.5, 0.7, 0.7)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("gltf writer city gml binary")
render_window.SetMultiSamples(0)
render_window.SetSize(400, 400)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Re-import the written GLB
gltf_importer = vtkGLTFImporter()
gltf_importer.SetFileName(output_name)
gltf_importer.SetCamera(-1)
gltf_importer.SetRenderWindow(render_window)
gltf_importer.Update()

# Scene
renderer.ResetCamera()
camera = renderer.GetActiveCamera()
camera.Azimuth(90)
camera.Roll(-90)
camera.Zoom(1.5)

interactor.Initialize()
interactor.Start()

# Clean up
os.remove(output_name)
os.rmdir(temp_dir)
