#!/usr/bin/env python

# Import a 3DS file and render the scene with a gradient background.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import os
from pathlib import Path

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkIOImport import vtk3DSImporter
from vtkmodules.vtkRenderingCore import (
    vtkCamera,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
gold_rgb = (1.0, 0.843, 0.0)
wheat_rgb = (0.961, 0.871, 0.702)

# Data file: set VPE_DATA_DIR env var to override, otherwise look next to this script
data_dir = Path(os.environ.get("VPE_DATA_DIR", Path(__file__).parent))
file_name = str(data_dir / "iflamingo.3ds")

# Importer: reads the 3DS file and creates the actors, cameras, and lights.
# vtk3DSImporter is a reader, filter, mapper, and actor all in one.
importer = vtk3DSImporter()
importer.SetFileName(file_name)
importer.ComputeNormalsOn()

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.SetBackground(wheat_rgb)
renderer.SetBackground2(gold_rgb)
renderer.GradientBackgroundOn()

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("3ds importer")
render_window.SetMultiSamples(0)
render_window.SetSize(640, 480)

# Connect the importer to the render window and import the scene
importer.SetRenderWindow(render_window)
importer.Update()

# Scene: position the camera after import populates the scene
camera = vtkCamera()
camera.SetPosition(0, -1, 0)
camera.SetFocalPoint(0, 0, 0)
camera.SetViewUp(0, 0, 1)
camera.Azimuth(150)
camera.Elevation(30)
renderer.SetActiveCamera(camera)
renderer.ResetCamera()

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

render_window_interactor.Initialize()
render_window_interactor.Start()
