#!/usr/bin/env python

# Read a BMP image, convert to luminance, extract as geometry, warp
# by scalar value, and texture with the original color image.

import os
from pathlib import Path

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkFiltersCore import vtkMergeFilter
from vtkmodules.vtkFiltersGeneral import vtkWarpScalar
from vtkmodules.vtkFiltersGeometry import vtkImageDataGeometryFilter
from vtkmodules.vtkIOImage import vtkBMPReader
from vtkmodules.vtkImagingColor import vtkImageLuminance
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkDataSetMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
steel_blue_rgb = (0.235, 0.365, 0.565)

# Data directory: defaults to the folder containing this script
data_dir = Path(os.environ.get("VPE_DATA_DIR", Path(__file__).parent))

# Reader: load the BMP image
reader = vtkBMPReader()
reader.SetFileName(str(data_dir / "masonry.bmp"))

# Luminance: convert color image to grayscale
luminance = vtkImageLuminance()
luminance.SetInputConnection(reader.GetOutputPort())

# Geometry: extract the image data as a flat polygon mesh
geometry = vtkImageDataGeometryFilter()
geometry.SetInputConnection(luminance.GetOutputPort())

# Warp: displace the mesh perpendicular to the image plane by luminance
warp = vtkWarpScalar()
warp.SetInputConnection(geometry.GetOutputPort())
warp.SetScaleFactor(-0.1)

# Merge: combine the warped geometry with the original color scalars
merge = vtkMergeFilter()
merge.SetGeometryConnection(warp.GetOutputPort())
merge.SetScalarsConnection(reader.GetOutputPort())

# Mapper: map the merged data to graphics primitives
mapper = vtkDataSetMapper()
mapper.SetInputConnection(merge.GetOutputPort())
mapper.SetScalarRange(0, 255)

# Actor: assign the mapped geometry
actor = vtkActor()
actor.SetMapper(mapper)

# Renderer: assemble the scene and configure the camera
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(steel_blue_rgb)
renderer.ResetCamera()
renderer.GetActiveCamera().SetPosition(-100, -130, 325)
renderer.GetActiveCamera().SetFocalPoint(105, 114, -29)
renderer.GetActiveCamera().SetViewUp(0.51, 0.54, 0.67)
renderer.ResetCameraClippingRange()

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(512, 512)
render_window.SetWindowName("ImageWarp")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
