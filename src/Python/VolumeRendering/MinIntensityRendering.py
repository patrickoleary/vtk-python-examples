#!/usr/bin/env python

# Minimum intensity projection volume rendering of an iron protein.

import os
from pathlib import Path

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
import vtkmodules.vtkRenderingVolumeOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkCommonDataModel import vtkPiecewiseFunction
from vtkmodules.vtkIOLegacy import vtkStructuredPointsReader
from vtkmodules.vtkImagingCore import vtkImageClip
from vtkmodules.vtkRenderingCore import (
    vtkColorTransferFunction,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
    vtkVolume,
    vtkVolumeProperty,
)
from vtkmodules.vtkRenderingVolume import vtkFixedPointVolumeRayCastMapper

# Colors (normalized RGB)
midnight_blue_rgb = (0.098, 0.098, 0.439)

# Data: locate the iron protein dataset
data_dir = Path(os.environ.get("VPE_DATA_DIR", Path(__file__).parent))
file_name = str(data_dir / "ironProt.vtk")

# Source: read the structured points data
reader = vtkStructuredPointsReader()
reader.SetFileName(file_name)

# Clip: crop the volume to see the minimum intensity region
clip = vtkImageClip()
clip.SetInputConnection(reader.GetOutputPort())
clip.SetOutputWholeExtent(0, 66, 0, 66, 30, 37)
clip.ClipDataOn()

# Transfer functions: map scalar value to opacity and color
opacity_transfer_function = vtkPiecewiseFunction()
opacity_transfer_function.AddSegment(0, 1.0, 256, 0.1)

color_transfer_function = vtkColorTransferFunction()
color_transfer_function.AddRGBPoint(0, 1.0, 1.0, 1.0)
color_transfer_function.AddRGBPoint(255, 1.0, 1.0, 1.0)

# VolumeProperty: describe how the data will look
volume_property = vtkVolumeProperty()
volume_property.SetScalarOpacity(opacity_transfer_function)
volume_property.SetColor(color_transfer_function)
volume_property.SetInterpolationTypeToLinear()

# Mapper: fixed-point ray cast mapper with minimum intensity blend mode
volume_mapper = vtkFixedPointVolumeRayCastMapper()
volume_mapper.SetInputConnection(clip.GetOutputPort())
volume_mapper.SetBlendModeToMinimumIntensity()

# Volume: holds the mapper and property
volume = vtkVolume()
volume.SetMapper(volume_mapper)
volume.SetProperty(volume_property)

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.AddViewProp(volume)
renderer.SetBackground(midnight_blue_rgb)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(600, 600)
render_window.SetWindowName("MinIntensityRendering")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window.Render()
renderer.GetActiveCamera().Zoom(1.3)
render_window_interactor.Initialize()
render_window_interactor.Start()
