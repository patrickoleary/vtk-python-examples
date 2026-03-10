#!/usr/bin/env python

# Volume render a numpy array with three overlapping colored cubes.

import numpy as np

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
from vtkmodules.vtkRenderingVolumeOpenGL2 import vtkOpenGLRayCastImageDisplayHelper  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkCommonDataModel import vtkPiecewiseFunction
from vtkmodules.vtkIOImage import vtkImageImport
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
misty_rose_rgb = (1.0, 0.894, 0.882)

# Numpy data: three overlapping cubes in a 75^3 volume.
# Each cube has a different scalar value (50, 100, 150).
data_matrix = np.zeros([75, 75, 75], dtype=np.uint8)
data_matrix[0:35, 0:35, 0:35] = 50
data_matrix[25:55, 25:55, 25:55] = 100
data_matrix[45:74, 45:74, 45:74] = 150

# ImageImport: transfer the numpy array into VTK as a vtkImageData.
# The array is converted to raw bytes and copied into the importer.
importer = vtkImageImport()
data_string = data_matrix.tobytes()
importer.CopyImportVoidPointer(data_string, len(data_string))
importer.SetDataScalarTypeToUnsignedChar()
importer.SetNumberOfScalarComponents(1)
importer.SetDataExtent(0, 74, 0, 74, 0, 74)
importer.SetWholeExtent(0, 74, 0, 74, 0, 74)

# OpacityFunction: map scalar values to opacity.
# Background (0) is transparent; cubes have increasing opacity.
opacity = vtkPiecewiseFunction()
opacity.AddPoint(0, 0.0)
opacity.AddPoint(50, 0.05)
opacity.AddPoint(100, 0.1)
opacity.AddPoint(150, 0.2)

# ColorFunction: map scalar values to RGB colors.
# Cubes are red, green, and blue respectively.
color_func = vtkColorTransferFunction()
color_func.AddRGBPoint(50, 1.0, 0.0, 0.0)
color_func.AddRGBPoint(100, 0.0, 1.0, 0.0)
color_func.AddRGBPoint(150, 0.0, 0.0, 1.0)

# VolumeProperty: combine the color and opacity transfer functions
volume_property = vtkVolumeProperty()
volume_property.SetColor(color_func)
volume_property.SetScalarOpacity(opacity)

# VolumeMapper: ray-cast the image data
volume_mapper = vtkFixedPointVolumeRayCastMapper()
volume_mapper.SetInputConnection(importer.GetOutputPort())

# Volume: pair the mapper and property
volume = vtkVolume()
volume.SetMapper(volume_mapper)
volume.SetProperty(volume_property)

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.AddVolume(volume)
renderer.SetBackground(misty_rose_rgb)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(640, 480)
render_window.SetWindowName("VTKWithNumpy")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
