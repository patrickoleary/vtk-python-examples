#!/usr/bin/env python

# Demonstrate vtkPointInterpolator2D by reading a DEM terrain dataset,
# warping it to 3D, generating a random point cloud with implicit function
# attributes, and interpolating those attributes onto the terrain surface.

import os

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import (
    vtkMath,
    vtkPoints,
)
from vtkmodules.vtkCommonDataModel import (
    vtkPolyData,
    vtkSphere,
)
from vtkmodules.vtkCommonSystem import vtkTimerLog
from vtkmodules.vtkFiltersGeneral import (
    vtkSampleImplicitFunctionFilter,
    vtkWarpScalar,
)
from vtkmodules.vtkFiltersGeometry import vtkImageDataGeometryFilter
from vtkmodules.vtkFiltersModeling import vtkOutlineFilter
from vtkmodules.vtkFiltersPoints import (
    vtkPointInterpolator2D,
    vtkVoronoiKernel,
)
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
n_pts = 1000000
math = vtkMath()

# Read DEM terrain data
dem_reader = vtkDEMReader()
dem_reader.SetFileName(os.path.join(data_dir, "SainteHelens.dem"))
dem_reader.Update()

# Convert to geometry and warp
geom = vtkImageDataGeometryFilter()
geom.SetInputConnection(dem_reader.GetOutputPort())

warp = vtkWarpScalar()
warp.SetInputConnection(geom.GetOutputPort())
warp.SetNormal(0, 0, 1)
warp.UseNormalOn()
warp.SetScaleFactor(2)
warp.Update()

terrain_bounds = warp.GetOutput().GetBounds()
center = warp.GetOutput().GetCenter()

# Random point cloud with implicit function attributes
points = vtkPoints()
points.SetDataTypeToFloat()
points.SetNumberOfPoints(n_pts)
for i in range(0, n_pts):
    points.SetPoint(i, math.Random(terrain_bounds[0], terrain_bounds[1]), math.Random(terrain_bounds[2], terrain_bounds[3]), math.Random(terrain_bounds[4], terrain_bounds[5]))

source = vtkPolyData()
source.SetPoints(points)

sphere = vtkSphere()
sphere.SetCenter(center[0], center[1] - 7500, center[2])

sample_filter = vtkSampleImplicitFunctionFilter()
sample_filter.SetInputData(source)
sample_filter.SetImplicitFunction(sphere)
sample_filter.Update()

# Voronoi kernel interpolation
voronoi_kernel = vtkVoronoiKernel()

interpolator_1 = vtkPointInterpolator2D()
interpolator_1.SetInputConnection(warp.GetOutputPort())
interpolator_1.SetSourceConnection(sample_filter.GetOutputPort())
interpolator_1.SetKernel(voronoi_kernel)
interpolator_1.SetNullPointsStrategyToClosestPoint()

timer = vtkTimerLog()
timer.StartTimer()
interpolator_1.Update()
timer.StopTimer()
print("Interpolate Terrain Points (Gaussian): {0}".format(timer.GetElapsedTime()))

scalar_range = sample_filter.GetOutput().GetScalarRange()

interpolator_mapper = vtkPolyDataMapper()
interpolator_mapper.SetInputConnection(interpolator_1.GetOutputPort())
interpolator_mapper.SetScalarRange(scalar_range)

interpolator_actor = vtkActor()
interpolator_actor.SetMapper(interpolator_mapper)

# Outline
outline_1 = vtkOutlineFilter()
outline_1.SetInputConnection(warp.GetOutputPort())

outline_mapper_1 = vtkPolyDataMapper()
outline_mapper_1.SetInputConnection(outline_1.GetOutputPort())

outline_actor_1 = vtkActor()
outline_actor_1.SetMapper(outline_mapper_1)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(interpolator_actor)
renderer.AddActor(outline_actor_1)
renderer.SetBackground(0.1, 0.2, 0.4)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(250, 250)
render_window.SetWindowName("interpolator2d")

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
