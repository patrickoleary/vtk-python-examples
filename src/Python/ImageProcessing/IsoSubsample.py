#!/usr/bin/env python

# Demonstrate aliasing that occurs when a high-frequency signal is
# subsampled.  The left viewport shows an isosurface of the skull
# after subsampling (aliased).  The right viewport shows the same
# isosurface after a low-pass Gaussian filter before subsampling.

import os
from pathlib import Path

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkFiltersGeneral import vtkImageMarchingCubes
from vtkmodules.vtkIOImage import vtkMetaImageReader
from vtkmodules.vtkImagingCore import vtkImageShrink3D
from vtkmodules.vtkImagingGeneral import vtkImageGaussianSmooth
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
ivory_rgb = (1.0, 1.0, 0.9412)
black_rgb = (0.0, 0.0, 0.0)

# Data directory: defaults to the folder containing this script
data_dir = Path(os.environ.get("VPE_DATA_DIR", Path(__file__).parent))

# Reader: load the 3D medical volume
reader = vtkMetaImageReader()
reader.SetFileName(str(data_dir / "FullHead.mhd"))
reader.Update()

# Smoothed pipeline: Gaussian smooth then subsample then isosurface
smooth = vtkImageGaussianSmooth()
smooth.SetDimensionality(3)
smooth.SetInputConnection(reader.GetOutputPort())
smooth.SetStandardDeviations(1.75, 1.75, 0.0)
smooth.SetRadiusFactor(2)

subsample_smoothed = vtkImageShrink3D()
subsample_smoothed.SetInputConnection(smooth.GetOutputPort())
subsample_smoothed.SetShrinkFactors(4, 4, 1)

iso_smoothed = vtkImageMarchingCubes()
iso_smoothed.SetInputConnection(smooth.GetOutputPort())
iso_smoothed.SetValue(0, 1150)

mapper_smoothed = vtkPolyDataMapper()
mapper_smoothed.SetInputConnection(iso_smoothed.GetOutputPort())
mapper_smoothed.ScalarVisibilityOff()

actor_smoothed = vtkActor()
actor_smoothed.SetMapper(mapper_smoothed)
actor_smoothed.GetProperty().SetColor(ivory_rgb)

# Unsmoothed pipeline: subsample then isosurface (aliased)
subsample = vtkImageShrink3D()
subsample.SetInputConnection(reader.GetOutputPort())
subsample.SetShrinkFactors(4, 4, 1)

iso = vtkImageMarchingCubes()
iso.SetInputConnection(subsample.GetOutputPort())
iso.SetValue(0, 1150)

mapper_aliased = vtkPolyDataMapper()
mapper_aliased.SetInputConnection(iso.GetOutputPort())
mapper_aliased.ScalarVisibilityOff()

actor_aliased = vtkActor()
actor_aliased.SetMapper(mapper_aliased)
actor_aliased.GetProperty().SetColor(ivory_rgb)

# Renderer 1: left viewport — aliased (subsampled without smoothing)
renderer_left = vtkRenderer()
renderer_left.SetViewport(0.0, 0.0, 0.5, 1.0)
renderer_left.AddActor(actor_aliased)
renderer_left.GetActiveCamera().SetFocalPoint(0.0, 0.0, 0.0)
renderer_left.GetActiveCamera().SetPosition(0.0, -1.0, 0.0)
renderer_left.GetActiveCamera().SetViewUp(0.0, 0.0, -1.0)
renderer_left.ResetCamera()
renderer_left.GetActiveCamera().Azimuth(-20.0)
renderer_left.GetActiveCamera().Elevation(20.0)
renderer_left.ResetCameraClippingRange()
renderer_left.SetBackground(black_rgb)

# Renderer 2: right viewport — smoothed before subsampling
renderer_right = vtkRenderer()
renderer_right.SetViewport(0.5, 0.0, 1.0, 1.0)
renderer_right.AddActor(actor_smoothed)
renderer_right.SetActiveCamera(renderer_left.GetActiveCamera())
renderer_right.SetBackground(black_rgb)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer_left)
render_window.AddRenderer(renderer_right)
render_window.SetSize(640, 480)
render_window.SetWindowName("IsoSubsample")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
