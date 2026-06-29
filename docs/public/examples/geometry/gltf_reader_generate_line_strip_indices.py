#!/usr/bin/env python

# Read a glTF file with LINE_STRIP primitive mode (generated indices) and render.

import os

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkIOGeometry import vtkGLTFReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkCompositePolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Source
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Read glTF file
gltf_reader = vtkGLTFReader()
gltf_reader.SetFileName(os.path.join(data_dir, "glTF", "PrimitiveModes", "Mesh_PrimitiveMode_LINE_STRIP.gltf"))
gltf_reader.Update()

# Mapper
composite_mapper = vtkCompositePolyDataMapper()
composite_mapper.SetInputConnection(gltf_reader.GetOutputPort())

# Actor
gltf_actor = vtkActor()
gltf_actor.SetMapper(composite_mapper)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(gltf_actor)
renderer.SetBackground(0.0, 0.0, 0.2)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("gltf reader generate line strip indices")
render_window.SetMultiSamples(0)
render_window.SetSize(300, 300)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.ResetCamera()

interactor.Initialize()
interactor.Start()
