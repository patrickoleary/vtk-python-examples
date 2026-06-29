#!/usr/bin/env python

# Import a glTF GLB file (ABeautifulGame) and verify scene hierarchy.

import os

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import vtkIndent
from vtkmodules.vtkIOImport import vtkGLTFImporter
from vtkmodules.vtkRenderingCore import (
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Source
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Import glTF
gltf_importer = vtkGLTFImporter()
gltf_importer.SetFileName(os.path.join(data_dir, "glTF", "ABeautifulGame", "ABeautifulGame.glb"))
gltf_importer.SetCamera(-1)

# Renderer
renderer = vtkRenderer()
renderer.SetBackground(1.0, 1.0, 1.0)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("gltf importer hierarchy")
render_window.SetMultiSamples(0)
render_window.SetSize(300, 300)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

gltf_importer.SetRenderWindow(render_window)
gltf_importer.Update()

# Print hierarchy for verification
hierarchy = gltf_importer.GetSceneHierarchy()
if hierarchy is not None:
    print(hierarchy.SerializeToXML(vtkIndent()))

interactor.Initialize()
interactor.Start()
