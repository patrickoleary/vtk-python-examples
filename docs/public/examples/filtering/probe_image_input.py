#!/usr/bin/env python

# Probe a wavelet image through a Delaunay-triangulated point cloud
# and render the result using ray-cast volume rendering.

import math

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
import vtkmodules.vtkRenderingVolumeOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import (
    vtkFloatArray,
    vtkMath,
)
from vtkmodules.vtkCommonDataModel import (
    vtkImageData,
    vtkPiecewiseFunction,
)
from vtkmodules.vtkFiltersCore import (
    vtkDelaunay3D,
    vtkProbeFilter,
)
from vtkmodules.vtkFiltersSources import vtkPointSource
from vtkmodules.vtkImagingCore import vtkRTAnalyticSource  # noqa: E402
from vtkmodules.vtkRenderingCore import (
    vtkColorTransferFunction,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
    vtkVolume,
    vtkVolumeProperty,
)
from vtkmodules.vtkRenderingVolumeOpenGL2 import vtkSmartVolumeMapper

dim = 48
center = [dim / 2.0, dim / 2.0, dim / 2.0]
extent = [0, dim - 1, 0, dim - 1, 0, dim - 1]

# Source: wavelet image
image_source = vtkRTAnalyticSource()
image_source.SetWholeExtent(extent[0], extent[1], extent[2], extent[3], extent[4], extent[5])
image_source.SetCenter(center)
image_source.Update()

image_data = image_source.GetOutput()
scalar_range = image_data.GetScalarRange()
origin = image_data.GetOrigin()
spacing = image_data.GetSpacing()

# Create an unstructured grid via point cloud + Delaunay
vtkMath.RandomSeed(0)
point_source = vtkPointSource()
point_source.SetCenter(center)
point_source.SetRadius(center[0])
point_source.SetNumberOfPoints(24 * 24 * 24)

delaunay = vtkDelaunay3D()
delaunay.SetInputConnection(point_source.GetOutputPort())

# Probe image data onto unstructured grid
probe_1 = vtkProbeFilter()
probe_1.SetSourceData(image_data)
probe_1.SetInputConnection(delaunay.GetOutputPort())

# Probe unstructured grid back onto image geometry
output_data = vtkImageData()
output_data.SetExtent(extent)
output_data.SetOrigin(origin)
output_data.SetSpacing(spacing)
scalars = vtkFloatArray()
scalars.SetName("scalars")
scalars.Allocate(dim * dim * dim)
output_data.GetPointData().SetScalars(scalars)

probe_2 = vtkProbeFilter()
probe_2.SetSourceConnection(probe_1.GetOutputPort())
probe_2.SetInputData(output_data)

# Volume rendering
volume_mapper = vtkSmartVolumeMapper()
volume_mapper.SetInputConnection(probe_2.GetOutputPort())
volume_mapper.SetRequestedRenderModeToRayCast()

# Color transfer function
volume_color = vtkColorTransferFunction()
volume_color.AddRGBPoint(scalar_range[0], 0.0, 0.0, 1.0)
volume_color.AddRGBPoint((scalar_range[0] + scalar_range[1]) * 0.5, 0.0, 1.0, 0.0)
volume_color.AddRGBPoint(scalar_range[1], 1.0, 0.0, 0.0)

# Opacity transfer function
volume_opacity = vtkPiecewiseFunction()
volume_opacity.AddPoint(scalar_range[0], 0.0)
volume_opacity.AddPoint((scalar_range[0] + scalar_range[1]) * 0.5, 0.0)
volume_opacity.AddPoint(scalar_range[1], 1.0)

# Volume property
volume_property = vtkVolumeProperty()
volume_property.SetColor(volume_color)
volume_property.SetScalarOpacity(volume_opacity)
volume_property.SetInterpolationTypeToLinear()
volume_property.ShadeOn()
volume_property.SetAmbient(0.5)
volume_property.SetDiffuse(0.8)
volume_property.SetSpecular(0.2)

# Volume
volume = vtkVolume()
volume.SetMapper(volume_mapper)
volume.SetProperty(volume_property)

# Renderer
renderer = vtkRenderer()
renderer.AddViewProp(volume)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(300, 300)
render_window.SetWindowName("probe image input")

# Scene
renderer.ResetCamera()

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
