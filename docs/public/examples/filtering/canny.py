#!/usr/bin/env python

# Canny edge detection pipeline: read an image, smooth, compute gradient,
# non-maximum suppression, link and threshold edgels, then sub-pixel position.

import os

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonExecutionModel import vtkImageToStructuredPoints
from vtkmodules.vtkFiltersCore import (
    vtkStripper,
    vtkThreshold,
)
from vtkmodules.vtkFiltersGeneral import (
    vtkLinkEdgels,
    vtkSubPixelPositionEdgels,
)
from vtkmodules.vtkFiltersGeometry import vtkGeometryFilter
from vtkmodules.vtkIOImage import vtkPNMReader
from vtkmodules.vtkImagingCore import (
    vtkImageCast,
    vtkImageConstantPad,
)
from vtkmodules.vtkImagingColor import vtkImageLuminance
from vtkmodules.vtkImagingGeneral import (
    vtkImageGaussianSmooth,
    vtkImageGradient,
)
from vtkmodules.vtkImagingMath import vtkImageMagnitude
from vtkmodules.vtkImagingMorphological import vtkImageNonMaximumSuppression
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Data directory
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Read the image
image_in = vtkPNMReader()
image_in.SetFileName(os.path.join(data_dir, "earth.ppm"))

# Convert to luminance
luminance = vtkImageLuminance()
luminance.SetInputConnection(image_in.GetOutputPort())

# Cast to float
image_cast = vtkImageCast()
image_cast.SetOutputScalarTypeToFloat()
image_cast.SetInputConnection(luminance.GetOutputPort())

# Smooth the image
gaussian_smooth = vtkImageGaussianSmooth()
gaussian_smooth.SetInputConnection(image_cast.GetOutputPort())
gaussian_smooth.SetDimensionality(2)
gaussian_smooth.SetRadiusFactors(1, 1, 0)

# Compute gradient
img_gradient = vtkImageGradient()
img_gradient.SetInputConnection(gaussian_smooth.GetOutputPort())
img_gradient.SetDimensionality(2)

img_magnitude = vtkImageMagnitude()
img_magnitude.SetInputConnection(img_gradient.GetOutputPort())
img_magnitude.Update()

# Non-maximum suppression
non_max = vtkImageNonMaximumSuppression()
non_max.SetMagnitudeInputData(img_magnitude.GetOutput())
non_max.SetVectorInputData(img_gradient.GetOutput())
non_max.SetDimensionality(2)

pad = vtkImageConstantPad()
pad.SetInputConnection(img_gradient.GetOutputPort())
pad.SetOutputNumberOfScalarComponents(3)
pad.SetConstant(0)
pad.Update()

image_to_sp_1 = vtkImageToStructuredPoints()
image_to_sp_1.SetInputConnection(non_max.GetOutputPort())
image_to_sp_1.SetVectorInputData(pad.GetOutput())

# Link edgels
img_link = vtkLinkEdgels()
img_link.SetInputConnection(image_to_sp_1.GetOutputPort())
img_link.SetGradientThreshold(2)

# Threshold links
threshold_edgels = vtkThreshold()
threshold_edgels.SetInputConnection(img_link.GetOutputPort())
threshold_edgels.SetThresholdFunction(vtkThreshold.THRESHOLD_UPPER)
threshold_edgels.SetUpperThreshold(10.0)
threshold_edgels.AllScalarsOff()

geometry_filter = vtkGeometryFilter()
geometry_filter.SetInputConnection(threshold_edgels.GetOutputPort())

image_to_sp = vtkImageToStructuredPoints()
image_to_sp.SetInputConnection(img_magnitude.GetOutputPort())
image_to_sp.SetVectorInputData(pad.GetOutput())
image_to_sp.Update()

# Sub-pixel position edgels
sub_pixel = vtkSubPixelPositionEdgels()
sub_pixel.SetInputConnection(geometry_filter.GetOutputPort())
sub_pixel.SetGradMapsData(image_to_sp.GetOutput())

strip = vtkStripper()
strip.SetInputConnection(sub_pixel.GetOutputPort())

mapper = vtkPolyDataMapper()
mapper.SetInputConnection(strip.GetOutputPort())
mapper.ScalarVisibilityOff()

plane_actor = vtkActor()
plane_actor.SetMapper(mapper)
plane_actor.GetProperty().SetAmbient(1.0)
plane_actor.GetProperty().SetDiffuse(0.0)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(plane_actor)

# Window
render_window = vtkRenderWindow()
render_window.SetMultiSamples(0)
render_window.AddRenderer(renderer)
render_window.SetSize(600, 300)
render_window.SetWindowName("canny")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.ResetCamera()
renderer.GetActiveCamera().Zoom(2.8)

interactor.Initialize()
interactor.Start()
