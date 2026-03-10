#!/usr/bin/env python

# Import a glTF scene file and render it with a gradient background.

import os
from pathlib import Path

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkIOImport import vtkGLTFImporter
from vtkmodules.vtkRenderingCore import (
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
background_top_rgb = (0.319, 0.431, 0.549)
background_bottom_rgb = (0.200, 0.302, 0.400)

# Data directory: defaults to the folder containing this script
data_dir = Path(os.environ.get("VPE_DATA_DIR", Path(__file__).parent))

# Renderer: assemble the scene with a gradient background
renderer = vtkRenderer()
renderer.SetBackground(background_bottom_rgb)
renderer.SetBackground2(background_top_rgb)
renderer.GradientBackgroundOn()

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(640, 480)
render_window.SetWindowName("GLTFImporter")

# Importer: read the glTF file and populate the render window
importer = vtkGLTFImporter()
importer.SetFileName(str(data_dir / "headMesh.gltf"))
importer.SetRenderWindow(render_window)
importer.Update()

# Camera: frame the imported geometry
renderer.ResetCamera()

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
