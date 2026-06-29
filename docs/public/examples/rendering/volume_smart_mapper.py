#!/usr/bin/env python
# Demonstrate volume rendering with vtkSmartVolumeMapper on analytic data.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonDataModel import vtkPiecewiseFunction
from vtkmodules.vtkImagingCore import vtkRTAnalyticSource
from vtkmodules.vtkRenderingAnnotation import vtkCubeAxesActor
from vtkmodules.vtkRenderingCore import (
    vtkColorTransferFunction,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
    vtkVolume,
    vtkVolumeProperty,
)
from vtkmodules.vtkRenderingVolumeOpenGL2 import vtkSmartVolumeMapper

# Analytic source.
source = vtkRTAnalyticSource()
source.Update()

# Smart volume mapper.
mapper = vtkSmartVolumeMapper()
mapper.SetInputConnection(source.GetOutputPort())

# Volume actor.
volume = vtkVolume()
volume.SetMapper(mapper)
volume.GetProperty().SetScalarOpacityUnitDistance(10)

# Color transfer function.
color_tf = vtkColorTransferFunction()
color_tf.AddRGBPoint(0.0, 0.0, 0.0, 0.0)
color_tf.AddRGBPoint(64.0, 1.0, 0.0, 0.0)
color_tf.AddRGBPoint(128.0, 0.0, 0.0, 1.0)
color_tf.AddRGBPoint(192.0, 0.0, 1.0, 0.0)
color_tf.AddRGBPoint(255.0, 0.0, 0.2, 0.0)

# Opacity transfer function.
opacity_tf = vtkPiecewiseFunction()
opacity_tf.AddPoint(20, 0.0)
opacity_tf.AddPoint(255, 0.2)

# Volume property.
volume_property = vtkVolumeProperty()
volume_property.SetColor(color_tf)
volume_property.SetScalarOpacity(opacity_tf)
volume_property.ShadeOn()
volume_property.SetInterpolationTypeToLinear()

volume.SetProperty(volume_property)

# Rendering pipeline.
renderer = vtkRenderer()
renderer.AddActor(volume)

# Cube axes.
cube_axes = vtkCubeAxesActor()
cube_axes.SetCamera(renderer.GetActiveCamera())
cube_axes.SetBounds(source.GetOutput().GetBounds())
renderer.AddActor(cube_axes)

renderer.SetBackground(0.7, 0.7, 0.7)

render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("volume smart mapper")
render_window.SetMultiSamples(0)

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.ResetCamera()

interactor.Initialize()
interactor.Start()
