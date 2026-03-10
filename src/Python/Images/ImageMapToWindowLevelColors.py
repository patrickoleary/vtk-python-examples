#!/usr/bin/env python

# Display a medical volume slice using window/level grayscale mapping
# via vtkImageMapToWindowLevelColors.

import os
from pathlib import Path

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkIOImage import vtkMetaImageReader
from vtkmodules.vtkImagingColor import vtkImageMapToWindowLevelColors
from vtkmodules.vtkInteractionStyle import vtkInteractorStyleImage
from vtkmodules.vtkRenderingCore import (
    vtkImageActor,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
black_rgb = (0.0, 0.0, 0.0)

# Data directory: defaults to the folder containing this script
data_dir = Path(os.environ.get("VPE_DATA_DIR", Path(__file__).parent))

# Reader: load the 3D medical volume
reader = vtkMetaImageReader()
reader.SetFileName(str(data_dir / "FullHead.mhd"))
reader.Update()

# WindowLevel: map scalars to grayscale using radiology-style window/level
window_level = vtkImageMapToWindowLevelColors()
window_level.SetWindow(2000)
window_level.SetLevel(1000)
window_level.SetInputConnection(reader.GetOutputPort())

# Choose the middle axial slice
extent = reader.GetOutput().GetExtent()
mid_z = (extent[4] + extent[5]) // 2

# Actor: display the window/level mapped slice
actor = vtkImageActor()
actor.GetMapper().SetInputConnection(window_level.GetOutputPort())
actor.SetDisplayExtent(extent[0], extent[1], extent[2], extent[3], mid_z, mid_z)
actor.GetProperty().SetInterpolationTypeToNearest()

# Renderer: assemble the scene with parallel projection for 2D viewing
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(black_rgb)
renderer.ResetCamera()
renderer.GetActiveCamera().ParallelProjectionOn()

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(640, 480)
render_window.SetWindowName("ImageMapToWindowLevelColors")

# Interactor: handle mouse and keyboard events with 2D image style
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetInteractorStyle(vtkInteractorStyleImage())
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
