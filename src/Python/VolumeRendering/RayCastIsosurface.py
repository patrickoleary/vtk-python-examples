#!/usr/bin/env python

# Use volume rendering to produce an iso-surface-like image.

import os
from pathlib import Path

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkCommonDataModel import vtkPiecewiseFunction
from vtkmodules.vtkIOImage import vtkMetaImageReader
from vtkmodules.vtkInteractionStyle import vtkInteractorStyleTrackballCamera
from vtkmodules.vtkRenderingCore import (
    vtkCamera,
    vtkColorTransferFunction,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
    vtkVolume,
    vtkVolumeProperty,
)
from vtkmodules.vtkRenderingVolumeOpenGL2 import vtkOpenGLGPUVolumeRayCastMapper

# Colors (normalized RGB)
flesh_rgb = (1.0, 0.490, 0.250)
ivory_rgb = (1.0, 1.0, 0.941)
cornflower_rgb = (0.392, 0.584, 0.929)

# Data: locate the FullHead dataset
data_dir = Path(os.environ.get("VPE_DATA_DIR", Path(__file__).parent))
file_name = str(data_dir / "FullHead.mhd")

# Iso-surface values
iso1 = 500
iso2 = 1150

# Source: read the meta image data
reader = vtkMetaImageReader()
reader.SetFileName(file_name)

# Mapper: GPU volume ray cast mapper with iso-surface blend mode
volume_mapper = vtkOpenGLGPUVolumeRayCastMapper()
volume_mapper.SetInputConnection(reader.GetOutputPort())
volume_mapper.SetAutoAdjustSampleDistances(False)
volume_mapper.SetSampleDistance(0.5)
volume_mapper.SetBlendModeToIsoSurface()

# Transfer functions: color and opacity for the two iso-surfaces
color_transfer_function = vtkColorTransferFunction()
color_transfer_function.RemoveAllPoints()
color_transfer_function.AddRGBPoint(iso1, *flesh_rgb)
color_transfer_function.AddRGBPoint(iso2, *ivory_rgb)

scalar_opacity = vtkPiecewiseFunction()
scalar_opacity.AddPoint(iso1, 0.3)
scalar_opacity.AddPoint(iso2, 0.6)

# VolumeProperty: describe shading, interpolation, and transfer functions
volume_property = vtkVolumeProperty()
volume_property.ShadeOn()
volume_property.SetInterpolationTypeToLinear()
volume_property.SetColor(color_transfer_function)
volume_property.SetScalarOpacity(scalar_opacity)
volume_property.GetIsoSurfaceValues().SetValue(0, iso1)
volume_property.GetIsoSurfaceValues().SetValue(1, iso2)

# Volume: holds the mapper and property
volume = vtkVolume()
volume.SetMapper(volume_mapper)
volume.SetProperty(volume_property)

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.AddVolume(volume)
renderer.SetBackground(cornflower_rgb)
renderer.ResetCamera()

# Camera: set a good viewpoint
camera = vtkCamera()
camera.SetViewUp(0, 0, -1)
camera.SetPosition(0, -1, 0)
camera.SetFocalPoint(0, 0, 0)
renderer.SetActiveCamera(camera)
renderer.ResetCamera()
camera.Azimuth(30.0)
camera.Elevation(30.0)
camera.Dolly(1.5)
renderer.ResetCameraClippingRange()

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(800, 600)
render_window.SetWindowName("RayCastIsosurface")

# Interactor: handle mouse and keyboard events
style = vtkInteractorStyleTrackballCamera()
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)
render_window_interactor.SetInteractorStyle(style)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
