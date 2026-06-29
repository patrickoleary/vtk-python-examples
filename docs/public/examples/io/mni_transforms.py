#!/usr/bin/env python

# Write and read MNI transforms (thin plate spline and grid), apply to an image.

import os
import tempfile

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import (
    vtkLookupTable,
    vtkPoints,
)
from vtkmodules.vtkCommonTransforms import (
    vtkGeneralTransform,
    vtkThinPlateSplineTransform,
    vtkTransform,
)
from vtkmodules.vtkFiltersHybrid import (
    vtkGridTransform,
    vtkTransformToGrid,
)
from vtkmodules.vtkIOImage import vtkBMPReader
from vtkmodules.vtkIOMINC import (
    vtkMNITransformReader,
    vtkMNITransformWriter,
)
from vtkmodules.vtkImagingCore import (
    vtkImageBlend,
    vtkImageMapToColors,
    vtkImageReslice,
)
from vtkmodules.vtkImagingSources import vtkImageGridSource
from vtkmodules.vtkRenderingCore import (
    vtkImageActor,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Source
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))
temp_dir = tempfile.mkdtemp()

# Create an image grid overlay
grid_source = vtkImageGridSource()
grid_source.SetGridSpacing(16, 16, 0)
grid_source.SetGridOrigin(0, 0, 0)
grid_source.SetDataExtent(0, 255, 0, 255, 0, 0)
grid_source.SetDataScalarTypeToUnsignedChar()

alpha_lut = vtkLookupTable()
alpha_lut.SetTableRange(0, 1)
alpha_lut.SetValueRange(1.0, 0.0)
alpha_lut.SetSaturationRange(0.0, 0.0)
alpha_lut.SetHueRange(0.0, 0.0)
alpha_lut.SetAlphaRange(0.0, 1.0)
alpha_lut.Build()

alpha_colors = vtkImageMapToColors()
alpha_colors.SetInputConnection(grid_source.GetOutputPort())
alpha_colors.SetLookupTable(alpha_lut)

# Read the background image
bmp_reader = vtkBMPReader()
bmp_reader.SetFileName(os.path.join(data_dir, "masonry.bmp"))

image_blend = vtkImageBlend()
image_blend.AddInputConnection(bmp_reader.GetOutputPort())
image_blend.AddInputConnection(alpha_colors.GetOutputPort())

# Create a ThinPlateSpline transform
source_points = vtkPoints()
source_points.SetNumberOfPoints(8)
source_points.SetPoint(0, 0, 0, 0)
source_points.SetPoint(1, 0, 255, 0)
source_points.SetPoint(2, 255, 0, 0)
source_points.SetPoint(3, 255, 255, 0)
source_points.SetPoint(4, 96, 96, 0)
source_points.SetPoint(5, 96, 159, 0)
source_points.SetPoint(6, 159, 159, 0)
source_points.SetPoint(7, 159, 96, 0)

target_points = vtkPoints()
target_points.SetNumberOfPoints(8)
target_points.SetPoint(0, 0, 0, 0)
target_points.SetPoint(1, 0, 255, 0)
target_points.SetPoint(2, 255, 0, 0)
target_points.SetPoint(3, 255, 255, 0)
target_points.SetPoint(4, 96, 159, 0)
target_points.SetPoint(5, 159, 159, 0)
target_points.SetPoint(6, 159, 96, 0)
target_points.SetPoint(7, 96, 96, 0)

tps_transform = vtkThinPlateSplineTransform()
tps_transform.SetSourceLandmarks(source_points)
tps_transform.SetTargetLandmarks(target_points)
tps_transform.SetBasisToR2LogR()

# Write the TPS transform
tps_file = os.path.join(temp_dir, "mni-thinplatespline.xfm")
tps_writer = vtkMNITransformWriter()
tps_writer.SetFileName(tps_file)
tps_writer.SetTransform(tps_transform)
tps_writer.Write()

# Read TPS back
tps_transform_reader = vtkMNITransformReader()
tps_transform_reader.SetFileName(tps_file)
tps_read_transform = tps_transform_reader.GetTransform()

# Make a linear transform
linear_transform = vtkTransform()
linear_transform.PostMultiply()
linear_transform.Translate(-127.5, -127.5, 0)
linear_transform.RotateZ(30)
linear_transform.Translate(+127.5, +127.5, 0)

# Remove the linear part from TPS
tps_general_transform = vtkGeneralTransform()
tps_general_transform.SetInput(tps_read_transform)
tps_general_transform.PreMultiply()
tps_general_transform.Concatenate(linear_transform.GetInverse().GetMatrix())

# Convert to grid transform
grid_converter = vtkTransformToGrid()
grid_converter.SetInput(tps_general_transform)
grid_converter.SetGridSpacing(16, 16, 1)
grid_converter.SetGridOrigin(-64.5, -64.5, 0)
grid_converter.SetGridExtent(0, 24, 0, 24, 0, 0)
grid_converter.Update()

grid_transform = vtkGridTransform()
grid_transform.SetDisplacementGridConnection(grid_converter.GetOutputPort())
grid_transform.SetInterpolationModeToCubic()

# Add back the linear part
grid_general_transform = vtkGeneralTransform()
grid_general_transform.SetInput(grid_transform)
grid_general_transform.PreMultiply()
grid_general_transform.Concatenate(linear_transform.GetMatrix())

# Invert for reslice
grid_general_transform.Inverse()

# Write grid transform
grid_file = os.path.join(temp_dir, "mni-grid.xfm")
grid_transform_writer = vtkMNITransformWriter()
grid_transform_writer.SetFileName(grid_file)
grid_transform_writer.SetComments("TestMNITransforms output transform")
grid_transform_writer.SetTransform(grid_general_transform)
grid_transform_writer.Write()

# Read grid transform back
grid_transform_reader = vtkMNITransformReader()
grid_transform_reader.SetFileName(grid_file)
read_transform = grid_transform_reader.GetTransform()

# Apply the grid warp to the image
image_reslice = vtkImageReslice()
image_reslice.SetInputConnection(image_blend.GetOutputPort())
image_reslice.SetResliceTransform(read_transform)
image_reslice.SetInterpolationModeToLinear()

# Display with standard rendering pipeline
image_actor = vtkImageActor()
image_actor.GetMapper().SetInputConnection(image_reslice.GetOutputPort())

renderer = vtkRenderer()
renderer.AddActor(image_actor)

render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("mni transforms")
render_window.SetMultiSamples(0)
render_window.SetSize(256, 256)

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.GetActiveCamera().ParallelProjectionOn()
renderer.ResetCamera()

interactor.Initialize()
interactor.Start()

# Clean up temp files
for f in [tps_file, grid_file]:
    if os.path.exists(f):
        os.remove(f)
grid_mnc = os.path.join(temp_dir, "mni-grid_grid.mnc")
if os.path.exists(grid_mnc):
    os.remove(grid_mnc)
os.rmdir(temp_dir)
