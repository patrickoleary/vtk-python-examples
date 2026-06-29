#!/usr/bin/env python

# Demonstrate vtkFitToHeightMapFilter by creating a random height field
# image, draping a plane source over it using point projection and cell
# average height strategies in side-by-side renderers.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import vtkFloatArray, vtkLookupTable, vtkMath
from vtkmodules.vtkCommonDataModel import vtkImageData
from vtkmodules.vtkFiltersCore import vtkTriangleFilter
from vtkmodules.vtkFiltersGeneral import vtkWarpScalar
from vtkmodules.vtkFiltersGeometry import vtkImageDataGeometryFilter
from vtkmodules.vtkFiltersModeling import vtkFitToHeightMapFilter
from vtkmodules.vtkFiltersSources import vtkPlaneSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Image dimensions
i_dim = 5
j_dim = 7
img_size = i_dim * j_dim

# Lookup table
lookup_table = vtkLookupTable()
lookup_table.SetHueRange(0.6, 0)
lookup_table.SetSaturationRange(1.0, 0)
lookup_table.SetValueRange(0.5, 1.0)

# Create an image with random heights
image = vtkImageData()
image.SetDimensions(i_dim, j_dim, 1)
image.SetSpacing(1, 1, 1)
image.SetOrigin(0, 0, 0)

math = vtkMath()
math.RandomSeed(31415)
heights = vtkFloatArray()
heights.SetNumberOfTuples(img_size)
for i in range(img_size):
    heights.SetTuple1(i, math.Random(0, 1))
image.GetPointData().SetScalars(heights)

scalar_low = image.GetScalarRange()[0]
scalar_high = image.GetScalarRange()[1]

# Warp the image to create a terrain surface
surface = vtkImageDataGeometryFilter()
surface.SetInputData(image)

triangle_filter = vtkTriangleFilter()
triangle_filter.SetInputConnection(surface.GetOutputPort())

warp = vtkWarpScalar()
warp.SetInputConnection(triangle_filter.GetOutputPort())
warp.SetScaleFactor(1)
warp.UseNormalOn()
warp.SetNormal(0, 0, 1)

# Terrain actor
img_mapper = vtkPolyDataMapper()
img_mapper.SetInputConnection(warp.GetOutputPort())
img_mapper.SetScalarRange(scalar_low, scalar_high)
img_mapper.SetLookupTable(lookup_table)

img_actor = vtkActor()
img_actor.SetMapper(img_mapper)

# Plane to drape over terrain
plane = vtkPlaneSource()
plane.SetOrigin(-0.1, -0.1, 0)
plane.SetPoint1(i_dim - 1 + 0.1, -0.1, 0)
plane.SetPoint2(-0.1, j_dim - 1 + 0.1, 0)
plane.SetResolution(40, 20)

# Fit using point projection strategy
fit = vtkFitToHeightMapFilter()
fit.SetInputConnection(plane.GetOutputPort())
fit.SetHeightMapData(image)
fit.SetFittingStrategyToPointProjection()
fit.UseHeightMapOffsetOn()
fit.Update()

mapper = vtkPolyDataMapper()
mapper.SetInputConnection(fit.GetOutputPort())
mapper.ScalarVisibilityOff()

actor = vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetColor(1, 0, 0)

# Fit using cell average height strategy
fit_2 = vtkFitToHeightMapFilter()
fit_2.SetInputConnection(plane.GetOutputPort())
fit_2.SetHeightMapData(image)
fit_2.SetFittingStrategyToCellAverageHeight()
fit_2.UseHeightMapOffsetOn()
fit_2.Update()

mapper_2 = vtkPolyDataMapper()
mapper_2.SetInputConnection(fit_2.GetOutputPort())
mapper_2.ScalarVisibilityOff()

actor_2 = vtkActor()
actor_2.SetMapper(mapper_2)
actor_2.GetProperty().SetColor(1, 0, 0)

# Two renderers side by side
renderer_0 = vtkRenderer()
renderer_0.SetViewport(0, 0, 0.5, 1)
renderer_0.AddActor(actor)
renderer_0.AddActor(img_actor)

renderer_1 = vtkRenderer()
renderer_1.SetViewport(0.5, 0, 1, 1)
renderer_1.AddActor(actor_2)
renderer_1.AddActor(img_actor)


# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer_0)
render_window.AddRenderer(renderer_1)
render_window.SetWindowName("fit to height map draping")

# Scene
renderer_0.GetActiveCamera().SetPosition(1, 1, 1)
renderer_0.ResetCamera()
renderer_1.SetActiveCamera(renderer_0.GetActiveCamera())

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
