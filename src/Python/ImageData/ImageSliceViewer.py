#!/usr/bin/env python

# Display the middle axial slice of a 3D medical volume (FullHead.mhd)
# using the standard VTK rendering pipeline with parallel projection
# and vtkInteractorStyleImage for proper 2D slice viewing.

import os
from pathlib import Path

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkIOImage import vtkMetaImageReader
from vtkmodules.vtkImagingCore import vtkImageCast
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

# Cast: convert to unsigned char for vtkImageActor display
cast = vtkImageCast()
cast.SetInputConnection(reader.GetOutputPort())
cast.SetOutputScalarTypeToUnsignedChar()
cast.ClampOverflowOn()

# Determine the middle axial slice
extent = reader.GetOutput().GetExtent()
mid_z = (extent[4] + extent[5]) // 2

# Actor: display the middle axial slice as a 2D image
image_actor = vtkImageActor()
image_actor.GetMapper().SetInputConnection(cast.GetOutputPort())
image_actor.SetDisplayExtent(extent[0], extent[1], extent[2], extent[3],
                             mid_z, mid_z)

# Renderer: assemble the scene and configure the camera
renderer = vtkRenderer()
renderer.AddActor(image_actor)
renderer.SetBackground(black_rgb)
renderer.ResetCamera()
renderer.GetActiveCamera().ParallelProjectionOn()

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(640, 480)
render_window.SetWindowName("ImageSliceViewer")

# Interactor: handle mouse and keyboard events with 2D image style
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetInteractorStyle(vtkInteractorStyleImage())
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
