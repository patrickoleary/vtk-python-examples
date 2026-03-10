#!/usr/bin/env python

# Import a 3DS file and render the scene with a gradient background.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
import os
from pathlib import Path

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

# Camera: position the view
camera = vtkCamera()
camera.SetPosition(0, -1, 0)
camera.SetFocalPoint(0, 0, 0)
camera.SetViewUp(0, 0, 1)
camera.Azimuth(150)
camera.Elevation(30)

renderer.SetActiveCamera(camera)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(640, 480)
render_window.SetWindowName("3DSImporter")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Connect the importer to the render window and import the scene
importer.SetRenderWindow(render_window)
importer.Update()

# Reset after import: the importer added actors the renderer didn't know
# about at creation time, so recompute the camera bounds.
renderer.ResetCamera()

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
