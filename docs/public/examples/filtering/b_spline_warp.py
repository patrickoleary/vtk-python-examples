#!/usr/bin/env python

# Test B-spline image warping with graph paper grid and thin plate spline transform.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import (
    vtkLookupTable,
    vtkPoints,
)
from vtkmodules.vtkCommonTransforms import vtkThinPlateSplineTransform
from vtkmodules.vtkFiltersHybrid import (
    vtkBSplineTransform,
    vtkTransformToGrid,
)
from vtkmodules.vtkImagingCore import (
    vtkImageBSplineCoefficients,
    vtkImageBSplineInterpolator,
    vtkImageBlend,
    vtkImageMapToColors,
    vtkImageReslice,
)
from vtkmodules.vtkImagingSources import vtkImageGridSource
from vtkmodules.vtkInteractionStyle import vtkInteractorStyleImage
from vtkmodules.vtkRenderingCore import (
    vtkImageActor,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Create grid images for graph paper effect
image_grid_1 = vtkImageGridSource()
image_grid_1.SetGridSpacing(4, 4, 0)
image_grid_1.SetGridOrigin(0, 0, 0)
image_grid_1.SetDataExtent(0, 255, 0, 255, 0, 0)
image_grid_1.SetDataScalarTypeToUnsignedChar()

image_grid_2 = vtkImageGridSource()
image_grid_2.SetGridSpacing(16, 16, 0)
image_grid_2.SetGridOrigin(0, 0, 0)
image_grid_2.SetDataExtent(0, 255, 0, 255, 0, 0)
image_grid_2.SetDataScalarTypeToUnsignedChar()

# Lookup tables for coloring
table_1 = vtkLookupTable()
table_1.SetTableRange(0, 1)
table_1.SetValueRange(1.0, 0.7)
table_1.SetSaturationRange(0.0, 1.0)
table_1.SetHueRange(0.12, 0.12)
table_1.SetAlphaRange(1.0, 1.0)
table_1.Build()

table_2 = vtkLookupTable()
table_2.SetTableRange(0, 1)
table_2.SetValueRange(1.0, 0.0)
table_2.SetSaturationRange(0.0, 0.0)
table_2.SetHueRange(0.0, 0.0)
table_2.SetAlphaRange(0.0, 1.0)
table_2.Build()

# Map grids to colors
map_1 = vtkImageMapToColors()
map_1.SetInputConnection(image_grid_1.GetOutputPort())
map_1.SetLookupTable(table_1)

map_2 = vtkImageMapToColors()
map_2.SetInputConnection(image_grid_2.GetOutputPort())
map_2.SetLookupTable(table_2)

# Blend the two grid images
blend = vtkImageBlend()
blend.AddInputConnection(map_1.GetOutputPort())
blend.AddInputConnection(map_2.GetOutputPort())

# Create thin plate spline transform
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

thin_plate = vtkThinPlateSplineTransform()
thin_plate.SetSourceLandmarks(target_points)
thin_plate.SetTargetLandmarks(source_points)
thin_plate.SetBasisToR2LogR()

# Convert thin plate spline to B-spline grid
transform_to_grid = vtkTransformToGrid()
transform_to_grid.SetInput(thin_plate)
transform_to_grid.SetGridSpacing(16.0, 16.0, 1.0)
transform_to_grid.SetGridOrigin(0.0, 0.0, 0.0)
transform_to_grid.SetGridExtent(0, 16, 0, 16, 0, 0)

grid = vtkImageBSplineCoefficients()
grid.SetInputConnection(transform_to_grid.GetOutputPort())
grid.UpdateWholeExtent()

# Create B-spline transform with half displacement
transform = vtkBSplineTransform()
transform.SetCoefficientData(grid.GetOutput())
transform.SetDisplacementScale(0.5)
transform.SetBorderModeToZero()
transform.Inverse()

# Prefilter for B-spline interpolation
prefilter = vtkImageBSplineCoefficients()
prefilter.SetInputConnection(blend.GetOutputPort())
prefilter.SetBorderModeToRepeat()
prefilter.SetSplineDegree(3)

# B-spline interpolator
bspline_interpolator = vtkImageBSplineInterpolator()
bspline_interpolator.SetSplineDegree(3)

# Reslice with B-spline transform and interpolation
reslice = vtkImageReslice()
reslice.SetInputConnection(prefilter.GetOutputPort())
reslice.SetResliceTransform(transform)
reslice.WrapOn()
reslice.SetInterpolator(bspline_interpolator)
reslice.SetOutputSpacing(1.0, 1.0, 1.0)
reslice.SetOutputOrigin(-32.0, -32.0, 0.0)
reslice.SetOutputExtent(0, 319, 0, 319, 0, 0)

# Display
actor = vtkImageActor()
actor.GetMapper().SetInputConnection(reslice.GetOutputPort())

renderer = vtkRenderer()
renderer.AddViewProp(actor)

render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(320, 320)
render_window.SetWindowName("b spline warp")

# Scene
renderer.GetActiveCamera().ParallelProjectionOn()
renderer.ResetCamera()

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)
interactor_style_image = vtkInteractorStyleImage()
interactor.SetInteractorStyle(interactor_style_image)

interactor.Initialize()
interactor.Start()
