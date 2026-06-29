#!/usr/bin/env python

# Import an invalid glTF file to test error handling (should not segfault).

import os

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkIOImport import vtkGLTFImporter
from vtkmodules.vtkRenderingCore import (
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Source
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Import invalid glTF
gltf_importer = vtkGLTFImporter()
gltf_importer.SetFileName(os.path.join(data_dir, "glTF", "invalid.gltf"))

# Renderer
renderer = vtkRenderer()
renderer.SetBackground(0.2, 0.3, 0.4)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("gltf importer-invalid")
render_window.SetMultiSamples(0)
render_window.SetSize(300, 300)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

gltf_importer.SetRenderWindow(render_window)
gltf_importer.Update()

interactor.Initialize()
interactor.Start()
