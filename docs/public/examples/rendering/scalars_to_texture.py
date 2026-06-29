#!/usr/bin/env python

# Demonstrate vtkScalarsToTextureFilter converting point scalars into
# a texture image using a diverging color transfer function, displayed
# with vtkImageActor.

import os

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersTexture import vtkScalarsToTextureFilter
from vtkmodules.vtkIOXML import vtkXMLPolyDataReader
from vtkmodules.vtkRenderingCore import (
    vtkColorTransferFunction,
    vtkImageActor,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Read polydata with ACCL point scalars
reader = vtkXMLPolyDataReader()
reader.SetFileName(os.path.join(data_dir, "can_slice.vtp"))

# Diverging color transfer function
color_transfer_function = vtkColorTransferFunction()
color_transfer_function.SetVectorModeToMagnitude()
color_transfer_function.SetColorSpaceToDiverging()
color_transfer_function.AddRGBPoint(0.0, 59.0 / 255.0, 76.0 / 255.0, 192.0 / 255.0)
color_transfer_function.AddRGBPoint(7.0e6, 221.0 / 255.0, 221.0 / 255.0, 221.0 / 255.0)
color_transfer_function.AddRGBPoint(1.4e7, 180.0 / 255.0, 4.0 / 255.0, 38.0 / 255.0)
color_transfer_function.Build()

# Scalars to texture filter
scalars_to_texture = vtkScalarsToTextureFilter()
scalars_to_texture.SetInputArrayToProcess(0, 0, 0, 0, "ACCL")  # FIELD_ASSOCIATION_POINTS = 0
scalars_to_texture.SetTextureDimensions(256, 256)
scalars_to_texture.SetTransferFunction(color_transfer_function)
scalars_to_texture.UseTransferFunctionOn()
scalars_to_texture.SetInputConnection(reader.GetOutputPort())

# Display the generated texture image
actor = vtkImageActor()
actor.GetMapper().SetInputConnection(scalars_to_texture.GetOutputPort(1))

# Renderer
renderer = vtkRenderer()
renderer.SetBackground(0.5, 0.5, 0.5)
renderer.AddActor(actor)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(300, 300)
render_window.SetWindowName("scalars to texture")

# Scene
renderer.ResetCamera()

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
