#!/usr/bin/env python

# Read a single DICOM image file and display it using the standard
# VTK pipeline with parallel projection and 2D image interaction.

import os
from pathlib import Path

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkIOImage import vtkDICOMImageReader
from vtkmodules.vtkInteractionStyle import vtkInteractorStyleImage
from vtkmodules.vtkRenderingCore import (
    vtkImageActor,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
background_rgb = (0.200, 0.302, 0.400)

# Data directory: defaults to the folder containing this script
data_dir = Path(os.environ.get("VPE_DATA_DIR", Path(__file__).parent))

# Reader: load a single DICOM image from file
reader = vtkDICOMImageReader()
reader.SetFileName(str(data_dir / "prostate.img"))
reader.Update()

# Actor: display the image as a 2D texture
actor = vtkImageActor()
actor.GetMapper().SetInputConnection(reader.GetOutputPort())
scalar_range = reader.GetOutput().GetScalarRange()
actor.GetProperty().SetColorWindow(scalar_range[1] - scalar_range[0])
actor.GetProperty().SetColorLevel((scalar_range[1] + scalar_range[0]) / 2.0)

# Renderer: assemble the scene and configure the camera
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(background_rgb)
renderer.ResetCamera()
renderer.GetActiveCamera().ParallelProjectionOn()

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(640, 480)
render_window.SetWindowName("ReadDICOM")

# Interactor: handle mouse and keyboard events with 2D image interaction
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)
render_window_interactor.SetInteractorStyle(vtkInteractorStyleImage())

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
