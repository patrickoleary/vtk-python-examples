#!/usr/bin/env python

# Demonstrate 2D image warping with cubic interpolation using
# vtkThinPlateSplineTransform, vtkTransformToGrid, and vtkGridTransform.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

import os

from vtkmodules.vtkCommonCore import (
    vtkLookupTable,
    vtkPoints,
)
from vtkmodules.vtkCommonTransforms import vtkThinPlateSplineTransform
from vtkmodules.vtkFiltersHybrid import (
    vtkGridTransform,
    vtkTransformToGrid,
)
from vtkmodules.vtkIOImage import vtkBMPReader
from vtkmodules.vtkImagingCore import (
    vtkImageBlend,
    vtkImageMapToColors,
    vtkImageReslice,
)
from vtkmodules.vtkImagingSources import vtkImageGridSource
from vtkmodules.vtkInteractionStyle import vtkInteractorStyleImage
from vtkmodules.vtkRenderingCore import (
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)
from vtkmodules.vtkRenderingCore import vtkImageSlice, vtkImageSliceMapper

data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Create a grid image
image_grid = vtkImageGridSource()
image_grid.SetGridSpacing(16, 16, 0)
image_grid.SetGridOrigin(0, 0, 0)
image_grid.SetDataExtent(0, 255, 0, 255, 0, 0)
image_grid.SetDataScalarTypeToUnsignedChar()

table = vtkLookupTable()
table.SetTableRange(0, 1)
table.SetValueRange(1.0, 0.0)
table.SetSaturationRange(0.0, 0.0)
table.SetHueRange(0.0, 0.0)
table.SetAlphaRange(0.0, 1.0)
table.Build()

alpha = vtkImageMapToColors()
alpha.SetInputConnection(image_grid.GetOutputPort())
alpha.SetLookupTable(table)

# Read masonry image
reader = vtkBMPReader()
reader.SetFileName(os.path.join(data_dir, "masonry.bmp"))

# Blend grid overlay with masonry image
blend = vtkImageBlend()
blend.AddInputConnection(reader.GetOutputPort())
blend.AddInputConnection(alpha.GetOutputPort())

# Create ThinPlateSpline transform with 8 landmarks
p1 = vtkPoints()
p1.SetNumberOfPoints(8)
p1.SetPoint(0, 0, 0, 0)
p1.SetPoint(1, 0, 255, 0)
p1.SetPoint(2, 255, 0, 0)
p1.SetPoint(3, 255, 255, 0)
p1.SetPoint(4, 96, 96, 0)
p1.SetPoint(5, 96, 159, 0)
p1.SetPoint(6, 159, 159, 0)
p1.SetPoint(7, 159, 96, 0)

p2 = vtkPoints()
p2.SetNumberOfPoints(8)
p2.SetPoint(0, 0, 0, 0)
p2.SetPoint(1, 0, 255, 0)
p2.SetPoint(2, 255, 0, 0)
p2.SetPoint(3, 255, 255, 0)
p2.SetPoint(4, 96, 159, 0)
p2.SetPoint(5, 159, 159, 0)
p2.SetPoint(6, 159, 96, 0)
p2.SetPoint(7, 96, 96, 0)

thin_plate = vtkThinPlateSplineTransform()
thin_plate.SetSourceLandmarks(p2)
thin_plate.SetTargetLandmarks(p1)
thin_plate.SetBasisToR2LogR()

# Convert thin plate spline into a grid
transform_to_grid = vtkTransformToGrid()
transform_to_grid.SetInput(thin_plate)
transform_to_grid.SetGridSpacing(16, 16, 1)
transform_to_grid.SetGridOrigin(-0.5, -0.5, 0)
transform_to_grid.SetGridExtent(0, 16, 0, 16, 0, 0)
transform_to_grid.Update()

transform = vtkGridTransform()
transform.SetDisplacementGridConnection(transform_to_grid.GetOutputPort())
transform.SetInterpolationModeToCubic()

# Invert the transform before passing to vtkImageReslice
transform.Inverse()

# Apply the grid warp to the image
reslice = vtkImageReslice()
reslice.SetInputConnection(blend.GetOutputPort())
reslice.SetResliceTransform(transform)
reslice.SetInterpolationModeToLinear()

# Display using vtkImageSliceMapper + vtkImageSlice
image_mapper = vtkImageSliceMapper()
image_mapper.SetInputConnection(reslice.GetOutputPort())

image_slice = vtkImageSlice()
image_slice.SetMapper(image_mapper)
image_slice.GetProperty().SetColorWindow(255.0)
image_slice.GetProperty().SetColorLevel(127.5)

# Renderer
renderer = vtkRenderer()
renderer.AddViewProp(image_slice)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(256, 256)
render_window.SetWindowName("grid warp cubic")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)
interactor_style_image = vtkInteractorStyleImage()
interactor.SetInteractorStyle(interactor_style_image)

# Scene
renderer.GetActiveCamera().ParallelProjectionOn()
renderer.ResetCamera()

interactor.Initialize()
interactor.Start()
