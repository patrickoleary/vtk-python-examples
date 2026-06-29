#!/usr/bin/env python

# Create extruded clip art from a beach photograph by thresholding,
# seed connectivity, smoothing, clipping, decimating, and extruding
# the resulting geometry with texture mapping.

import os

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonExecutionModel import vtkCastToConcrete
from vtkmodules.vtkFiltersCore import (
    vtkClipPolyData,
    vtkDecimatePro,
    vtkPolyDataNormals,
    vtkStripper,
    vtkTriangleFilter,
)
from vtkmodules.vtkFiltersGeometry import vtkImageDataGeometryFilter
from vtkmodules.vtkFiltersModeling import vtkLinearExtrusionFilter
from vtkmodules.vtkFiltersTexture import vtkTextureMapToPlane
from vtkmodules.vtkIOImage import vtkTIFFReader
from vtkmodules.vtkImagingColor import vtkImageRGBToHSV
from vtkmodules.vtkImagingCore import (
    vtkImageThreshold,
    vtkImageConstantPad,
    vtkImageExtractComponents,
    vtkImageShrink3D,
)
from vtkmodules.vtkImagingGeneral import vtkImageGaussianSmooth
from vtkmodules.vtkImagingMorphological import vtkImageSeedConnectivity
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
    vtkTexture,
)

# Data file path (relative to this script)
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Read the beach image
image_in = vtkTIFFReader()
image_in.SetFileName(os.path.join(data_dir, "beach.tif"))
image_in.SetOrientationType(4)
image_in.GetExecutive().SetReleaseDataFlag(0, 0)
image_in.Update()

# Compute power-of-two padding dimensions
org_x = (image_in.GetExecutive().GetWholeExtent(
    image_in.GetOutputInformation(0))[1]
    - image_in.GetExecutive().GetWholeExtent(
        image_in.GetOutputInformation(0))[0] + 1)
org_y = (image_in.GetExecutive().GetWholeExtent(
    image_in.GetOutputInformation(0))[3]
    - image_in.GetExecutive().GetWholeExtent(
        image_in.GetOutputInformation(0))[2] + 1)

pad_x = 1 << ((org_x - 1).bit_length())
pad_y = 1 << ((org_y - 1).bit_length())

# Pad image to power-of-two for texture
image_power_of_2 = vtkImageConstantPad()
image_power_of_2.SetInputConnection(image_in.GetOutputPort())
image_power_of_2.SetOutputWholeExtent(0, pad_x - 1, 0, pad_y - 1, 0, 0)

# Convert to HSV and extract value channel
to_hsv = vtkImageRGBToHSV()
to_hsv.SetInputConnection(image_in.GetOutputPort())
to_hsv.GetExecutive().SetReleaseDataFlag(0, 0)

extract_image = vtkImageExtractComponents()
extract_image.SetInputConnection(to_hsv.GetOutputPort())
extract_image.SetComponents(2)
extract_image.GetExecutive().SetReleaseDataFlag(0, 0)

# Threshold the value channel
threshold_1 = vtkImageThreshold()
threshold_1.SetInputConnection(extract_image.GetOutputPort())
threshold_1.ThresholdByUpper(230)
threshold_1.SetInValue(255)
threshold_1.SetOutValue(0)
threshold_1.ReplaceInOn()
threshold_1.ReplaceOutOn()
threshold_1.Update()

extent = threshold_1.GetExecutive().GetWholeExtent(
    threshold_1.GetOutputInformation(0))

# Seed connectivity from corners
connect = vtkImageSeedConnectivity()
connect.SetInputConnection(threshold_1.GetOutputPort())
connect.SetInputConnectValue(255)
connect.SetOutputConnectedValue(255)
connect.SetOutputUnconnectedValue(0)
connect.AddSeed(extent[0], extent[2])
connect.AddSeed(extent[1], extent[2])
connect.AddSeed(extent[1], extent[3])
connect.AddSeed(extent[0], extent[3])

# Smooth
smooth = vtkImageGaussianSmooth()
smooth.SetDimensionality(2)
smooth.SetStandardDeviation(1, 1)
smooth.SetInputConnection(connect.GetOutputPort())

# Shrink
shrink = vtkImageShrink3D()
shrink.SetInputConnection(smooth.GetOutputPort())
shrink.SetShrinkFactors(2, 2, 1)
shrink.AveragingOn()

# Convert to geometry
geometry = vtkImageDataGeometryFilter()
geometry.SetInputConnection(shrink.GetOutputPort())

# Texture coordinates
geometry_texture = vtkTextureMapToPlane()
geometry_texture.SetInputConnection(geometry.GetOutputPort())
geometry_texture.SetOrigin(0, 0, 0)
geometry_texture.SetPoint1(pad_x - 1, 0, 0)
geometry_texture.SetPoint2(0, pad_y - 1, 0)

# Cast to concrete polydata
geometry_pd = vtkCastToConcrete()
geometry_pd.SetInputConnection(geometry_texture.GetOutputPort())
geometry_pd.Update()

# Clip the geometry
clip = vtkClipPolyData()
clip.SetInputData(geometry_pd.GetPolyDataOutput())
clip.SetValue(5.5)
clip.GenerateClipScalarsOff()
clip.InsideOutOn()
clip.GetOutput().GetPointData().CopyScalarsOff()
clip.Update()

# Triangulate
triangles = vtkTriangleFilter()
triangles.SetInputConnection(clip.GetOutputPort())

# Decimate
decimate = vtkDecimatePro()
decimate.SetInputConnection(triangles.GetOutputPort())
decimate.BoundaryVertexDeletionOn()
decimate.SetDegree(25)
decimate.PreserveTopologyOn()

# Extrude
extrude = vtkLinearExtrusionFilter()
extrude.SetInputConnection(decimate.GetOutputPort())
extrude.SetExtrusionType(2)
extrude.SetScaleFactor(-20)

# Normals
normals = vtkPolyDataNormals()
normals.SetInputConnection(extrude.GetOutputPort())
normals.SetFeatureAngle(80)

# Mapper
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(normals.GetOutputPort())
mapper.ScalarVisibilityOff()

# Texture from padded image
image_texture = vtkTexture()
image_texture.InterpolateOn()
image_texture.SetInputConnection(image_power_of_2.GetOutputPort())

# Actor
clipart = vtkActor()
clipart.SetMapper(mapper)
clipart.SetTexture(image_texture)
clipart.GetProperty().SetDiffuseColor(1, 1, 1)
clipart.GetProperty().SetSpecular(0.5)
clipart.GetProperty().SetSpecularPower(30)
clipart.GetProperty().SetDiffuse(0.9)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(clipart)
renderer.SetBackground(0.2, 0.3, 0.4)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(320, 256)
render_window.SetWindowName("clip art")

# Scene
renderer.ResetCamera()
camera = renderer.GetActiveCamera()
camera.Azimuth(30)
camera.Elevation(-30)
camera.Dolly(1.5)
renderer.ResetCameraClippingRange()

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
