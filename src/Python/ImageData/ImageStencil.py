#!/usr/bin/env python

# Mask a region of a 3D medical volume (FullHead.mhd) using
# vtkImageStencil.  A spherical mask is generated with
# vtkImageEllipsoidSource and converted to a stencil via
# vtkImageToImageStencil.

import os
from pathlib import Path

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkIOImage import vtkMetaImageReader
from vtkmodules.vtkImagingCore import vtkImageCast
from vtkmodules.vtkImagingSources import vtkImageEllipsoidSource
from vtkmodules.vtkImagingStencil import (
    vtkImageStencil,
    vtkImageToImageStencil,
)
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

# Determine the volume geometry
extent = reader.GetOutput().GetExtent()

# Mask: generate a spherical binary mask using vtkImageEllipsoidSource
ellipsoid = vtkImageEllipsoidSource()
ellipsoid.SetWholeExtent(extent[0], extent[1], extent[2], extent[3],
                         extent[4], extent[5])
ellipsoid.SetCenter((extent[0] + extent[1]) / 2.0,
                    (extent[2] + extent[3]) / 2.0,
                    (extent[4] + extent[5]) / 2.0)
ellipsoid.SetRadius(80.0, 80.0, 40.0)
ellipsoid.SetInValue(255)
ellipsoid.SetOutValue(0)
ellipsoid.Update()

# Stencil source: convert the binary mask to an image stencil
stencil_source = vtkImageToImageStencil()
stencil_source.SetInputConnection(ellipsoid.GetOutputPort())
stencil_source.ThresholdByUpper(128)
stencil_source.Update()

# Filter: apply the stencil to mask the volume
stencil = vtkImageStencil()
stencil.SetInputConnection(reader.GetOutputPort())
stencil.SetStencilConnection(stencil_source.GetOutputPort())
stencil.SetBackgroundValue(0)
stencil.ReverseStencilOff()

# Cast: convert to unsigned char for display
cast = vtkImageCast()
cast.SetInputConnection(stencil.GetOutputPort())
cast.SetOutputScalarTypeToUnsignedChar()
cast.ClampOverflowOn()
cast.Update()

# Display the middle axial slice
mid_z = (extent[4] + extent[5]) // 2

# Actor: display the masked slice
image_actor = vtkImageActor()
image_actor.GetMapper().SetInputConnection(cast.GetOutputPort())
image_actor.SetDisplayExtent(extent[0], extent[1], extent[2], extent[3],
                             mid_z, mid_z)

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.AddActor(image_actor)
renderer.SetBackground(black_rgb)
renderer.ResetCamera()

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(640, 480)
render_window.SetWindowName("ImageStencil")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
