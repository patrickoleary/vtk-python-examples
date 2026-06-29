#!/usr/bin/env python

# Demonstrate GPU volume ray casting with maximum intensity projection on independent components.

import os

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
import vtkmodules.vtkRenderingVolumeOpenGL2  # noqa: F401

from vtkmodules.vtkCommonDataModel import vtkPiecewiseFunction
from vtkmodules.vtkIOXML import vtkXMLImageDataReader
from vtkmodules.vtkRenderingCore import (
    vtkColorTransferFunction,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
    vtkVolume,
)
from vtkmodules.vtkRenderingVolume import vtkGPUVolumeRayCastMapper

data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Read 4-component vase dataset
reader = vtkXMLImageDataReader()
reader.SetFileName(os.path.join(data_dir, "vase_4comp.vti"))

# Opacity transfer functions per component
opacity_func_0 = vtkPiecewiseFunction()
opacity_func_0.AddPoint(0.0, 0.0)
opacity_func_0.AddPoint(60.0, 0.1)
opacity_func_0.AddPoint(255.0, 0.0)

opacity_func_1 = vtkPiecewiseFunction()
opacity_func_1.AddPoint(0.0, 0.0)
opacity_func_1.AddPoint(60.0, 0.0)
opacity_func_1.AddPoint(120.0, 0.1)
opacity_func_1.AddPoint(255.0, 0.0)

opacity_func_2 = vtkPiecewiseFunction()
opacity_func_2.AddPoint(0.0, 0.0)
opacity_func_2.AddPoint(120.0, 0.0)
opacity_func_2.AddPoint(180.0, 0.1)
opacity_func_2.AddPoint(255.0, 0.0)

opacity_func_3 = vtkPiecewiseFunction()
opacity_func_3.AddPoint(0.0, 0.0)
opacity_func_3.AddPoint(180.0, 0.0)
opacity_func_3.AddPoint(255.0, 0.1)

# Color transfer functions per component
color_0 = vtkColorTransferFunction()
color_0.AddRGBPoint(0.0, 1.0, 0.0, 0.0)
color_0.AddRGBPoint(60.0, 1.0, 0.0, 0.0)

color_1 = vtkColorTransferFunction()
color_1.AddRGBPoint(60.0, 0.0, 0.0, 1.0)
color_1.AddRGBPoint(120.0, 0.0, 0.0, 1.0)

color_2 = vtkColorTransferFunction()
color_2.AddRGBPoint(120.0, 0.0, 1.0, 0.0)
color_2.AddRGBPoint(180.0, 0.0, 1.0, 0.0)

color_3 = vtkColorTransferFunction()
color_3.AddRGBPoint(180.0, 0.0, 0.0, 0.0)
color_3.AddRGBPoint(239.0, 0.0, 0.0, 0.0)

# Volume mapper + Volume
volume_mapper = vtkGPUVolumeRayCastMapper()
volume_mapper.SetBlendModeToMaximumIntensity()
volume_mapper.SetSampleDistance(0.1)
volume_mapper.SetAutoAdjustSampleDistances(0)
volume_mapper.SetInputConnection(reader.GetOutputPort())

volume = vtkVolume()
volume.SetMapper(volume_mapper)

volume_property = volume.GetProperty()
volume_property.SetIndependentComponents(1)
volume_property.SetScalarOpacity(0, opacity_func_0)
volume_property.SetScalarOpacity(1, opacity_func_1)
volume_property.SetScalarOpacity(2, opacity_func_2)
volume_property.SetScalarOpacity(3, opacity_func_3)
volume_property.SetColor(0, color_0)
volume_property.SetColor(1, color_1)
volume_property.SetColor(2, color_2)
volume_property.SetColor(3, color_3)

renderer = vtkRenderer()
renderer.AddViewProp(volume)
renderer.SetBackground(0.1, 0.4, 0.2)

render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("gpu ray cast independent component mip")

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.ResetCamera()

interactor.Initialize()
interactor.Start()
