#!/usr/bin/env python

# Demonstrate vtkPointInterpolator2D with a Gaussian kernel by reading DEM
# terrain data, interpolating elevation onto a plane, and rendering with
# contour lines and a lookup table.

import os

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import (
    vtkLookupTable,
    vtkMath,
)
from vtkmodules.vtkCommonSystem import vtkTimerLog
from vtkmodules.vtkFiltersCore import vtkContourFilter
from vtkmodules.vtkFiltersPoints import (
    vtkGaussianKernel,
    vtkPointInterpolator2D,
)
from vtkmodules.vtkFiltersSources import vtkPlaneSource
from vtkmodules.vtkIOImage import vtkDEMReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Parameters
res = 200
math = vtkMath()

# Read DEM terrain data
dem_reader = vtkDEMReader()
dem_reader.SetFileName(os.path.join(data_dir, "SainteHelens.dem"))
dem_reader.Update()

terrain_bounds = dem_reader.GetOutput().GetBounds()
center = dem_reader.GetOutput().GetCenter()

# Create a plane to interpolate onto
plane = vtkPlaneSource()
plane.SetResolution(res, res)
plane.SetOrigin(terrain_bounds[0], terrain_bounds[2], terrain_bounds[4])
plane.SetPoint1(terrain_bounds[1], terrain_bounds[2], terrain_bounds[4])
plane.SetPoint2(terrain_bounds[0], terrain_bounds[3], terrain_bounds[4])
plane.Update()

# Gaussian kernel
gaussian_kernel = vtkGaussianKernel()
gaussian_kernel.SetSharpness(2)
gaussian_kernel.SetRadius(200)

interpolator = vtkPointInterpolator2D()
interpolator.SetInputConnection(plane.GetOutputPort())
interpolator.SetSourceConnection(dem_reader.GetOutputPort())
interpolator.SetKernel(gaussian_kernel)
interpolator.SetNullPointsStrategyToClosestPoint()
interpolator.GetLocator().SetNumberOfPointsPerBucket(1)
interpolator.InterpolateZOff()

timer = vtkTimerLog()
timer.StartTimer()
interpolator.Update()
timer.StopTimer()
print("Interpolate Terrain Points (Gaussian): {0}".format(timer.GetElapsedTime()))

scalar_range = interpolator.GetOutput().GetPointData().GetArray("Elevation").GetRange()

# Lookup table
lookup_table = vtkLookupTable()
lookup_table.SetHueRange(0.6, 0)
lookup_table.SetSaturationRange(1.0, 0)
lookup_table.SetValueRange(0.5, 1.0)

interpolator_mapper = vtkPolyDataMapper()
interpolator_mapper.SetInputConnection(interpolator.GetOutputPort())
interpolator_mapper.SetScalarModeToUsePointFieldData()
interpolator_mapper.SelectColorArray("Elevation")
interpolator_mapper.SetScalarRange(scalar_range)
interpolator_mapper.SetLookupTable(lookup_table)

interpolator_actor = vtkActor()
interpolator_actor.SetMapper(interpolator_mapper)

# Contours
contour_filter = vtkContourFilter()
contour_filter.SetInputConnection(interpolator.GetOutputPort())
contour_filter.GenerateValues(20, scalar_range)

contour_mapper = vtkPolyDataMapper()
contour_mapper.SetInputConnection(contour_filter.GetOutputPort())

contour_actor = vtkActor()
contour_actor.SetMapper(contour_mapper)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(interpolator_actor)
renderer.AddActor(contour_actor)
renderer.SetBackground(0.1, 0.2, 0.4)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(300, 300)
render_window.SetWindowName("interpolator2d dem")

# Scene
camera = renderer.GetActiveCamera()
camera.SetFocalPoint(center)
focal_point = camera.GetFocalPoint()
camera.SetPosition(focal_point[0] + 0.2, focal_point[1] + 0.1, focal_point[2] + 1)
renderer.ResetCamera()

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
