#!/usr/bin/env python

# Demonstrate GPU volume ray casting with user-defined fragment shader replacements for depth coloring.

import os

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
import vtkmodules.vtkRenderingVolumeOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import VTK_LINEAR_INTERPOLATION
from vtkmodules.vtkCommonDataModel import vtkPiecewiseFunction
from vtkmodules.vtkIOImage import vtkNrrdReader
from vtkmodules.vtkRenderingCore import (
    vtkColorTransferFunction,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
    vtkShaderProperty,
    vtkVolume,
    vtkVolumeProperty,
)
from vtkmodules.vtkRenderingVolume import vtkGPUVolumeRayCastMapper

data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Read NRRD volume data
reader = vtkNrrdReader()
reader.SetFileName(os.path.join(data_dir, "tooth.nhdr"))
reader.Update()

scalar_range = reader.GetOutput().GetScalarRange()

# Volume property with shading
volume_property = vtkVolumeProperty()
volume_property.ShadeOn()
volume_property.SetInterpolationType(VTK_LINEAR_INTERPOLATION)

# Color transfer function
color_tf = vtkColorTransferFunction()
color_tf.AddRGBPoint(0, 0.0, 0.0, 0.0)
color_tf.AddRGBPoint(510, 0.4, 0.4, 1.0)
color_tf.AddRGBPoint(640, 1.0, 1.0, 1.0)
color_tf.AddRGBPoint(scalar_range[1], 0.9, 0.1, 0.1)

# Opacity transfer function
opacity_tf = vtkPiecewiseFunction()
opacity_tf.AddPoint(0, 0.00)
opacity_tf.AddPoint(510, 0.00)
opacity_tf.AddPoint(640, 0.5)
opacity_tf.AddPoint(scalar_range[1], 0.4)

volume_property.SetScalarOpacity(opacity_tf)
volume_property.SetColor(color_tf)
volume_property.SetShade(1)

# GPU volume mapper
volume_mapper = vtkGPUVolumeRayCastMapper()
volume_mapper.SetInputConnection(reader.GetOutputPort())
volume_mapper.SetUseJittering(1)

# User shader replacements: color by depth of translucent voxel
shader_property = vtkShaderProperty()
shader_property.AddFragmentShaderReplacement(
    "//VTK::Base::Dec",
    True,
    "//VTK::Base::Dec"
    "\n bool l_updateDepth;"
    "\n vec3 l_opaqueFragPos;",
    False,
)
shader_property.AddFragmentShaderReplacement(
    "//VTK::Base::Init",
    True,
    "//VTK::Base::Init\n"
    "\n l_updateDepth = true;"
    "\n l_opaqueFragPos = vec3(0.0);",
    False,
)
shader_property.AddFragmentShaderReplacement(
    "//VTK::Base::Impl",
    True,
    "//VTK::Base::Impl"
    "\n    if(!g_skip && g_srcColor.a > 0.0 && l_updateDepth)"
    "\n      {"
    "\n      l_opaqueFragPos = g_dataPos;"
    "\n      l_updateDepth = false;"
    "\n      }",
    False,
)
shader_property.AddFragmentShaderReplacement(
    "//VTK::RenderToImage::Exit",
    True,
    "//VTK::RenderToImage::Exit"
    "\n  if (l_opaqueFragPos == vec3(0.0))"
    "\n    {"
    "\n    fragOutput0 = vec4(0.0);"
    "\n    }"
    "\n  else"
    "\n    {"
    "\n    vec4 depthValue = in_projectionMatrix * in_modelViewMatrix *"
    "\n                      in_volumeMatrix[0] * in_textureDatasetMatrix[0] *"
    "\n                      vec4(l_opaqueFragPos, 1.0);"
    "\n    depthValue /= depthValue.w;"
    "\n    fragOutput0 = vec4(vec3(0.5 * (gl_DepthRange.far -"
    "\n                       gl_DepthRange.near) * depthValue.z + 0.5 *"
    "\n                      (gl_DepthRange.far + gl_DepthRange.near)), 1.0);"
    "\n    }",
    False,
)

# Volume
volume = vtkVolume()
volume.SetShaderProperty(shader_property)
volume.SetMapper(volume_mapper)
volume.SetProperty(volume_property)

renderer = vtkRenderer()
renderer.AddVolume(volume)

render_window = vtkRenderWindow()
render_window.SetMultiSamples(0)
render_window.SetSize(300, 300)
render_window.AddRenderer(renderer)
render_window.SetWindowName("gpu ray cast user shader")

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.GetActiveCamera().Elevation(-60.0)
renderer.ResetCamera()
renderer.GetActiveCamera().Zoom(1.3)

interactor.Initialize()
interactor.Start()
