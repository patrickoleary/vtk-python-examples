#!/usr/bin/env python

# Demonstrate vtkPointInterpolator with four different kernels (Voronoi,
# Gaussian, Shepard, Linear) on a PLOT3D combustor dataset, interpolating
# onto a probe plane and rendering in a 2x2 viewport grid.

import os

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonDataModel import vtkStaticPointLocator
from vtkmodules.vtkCommonSystem import vtkTimerLog
from vtkmodules.vtkFiltersCore import vtkStructuredGridOutlineFilter
from vtkmodules.vtkFiltersPoints import (
    vtkGaussianKernel,
    vtkLinearKernel,
    vtkPointInterpolator,
    vtkShepardKernel,
    vtkVoronoiKernel,
)
from vtkmodules.vtkFiltersSources import vtkPlaneSource
from vtkmodules.vtkIOParallel import vtkMultiBlockPLOT3DReader
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

# Read PLOT3D combustor data
plot3d_reader = vtkMultiBlockPLOT3DReader()
plot3d_reader.SetXYZFileName(os.path.join(data_dir, "combxyz.bin"))
plot3d_reader.SetQFileName(os.path.join(data_dir, "combq.bin"))
plot3d_reader.SetScalarFunctionNumber(100)
plot3d_reader.SetVectorFunctionNumber(202)
plot3d_reader.Update()

output = plot3d_reader.GetOutput().GetBlock(0)
center = output.GetCenter()

# Probe plane
plane = vtkPlaneSource()
plane.SetResolution(res, res)
plane.SetOrigin(0, 0, 0)
plane.SetPoint1(10, 0, 0)
plane.SetPoint2(0, 10, 0)
plane.SetCenter(center)
plane.SetNormal(0, 1, 0)

# Reuse locator
locator = vtkStaticPointLocator()
locator.SetDataSet(output)
locator.BuildLocator()

timer = vtkTimerLog()

# --- Voronoi kernel ---
voronoi_kernel = vtkVoronoiKernel()

interpolator_0 = vtkPointInterpolator()
interpolator_0.SetInputConnection(plane.GetOutputPort())
interpolator_0.SetSourceData(output)
interpolator_0.SetKernel(voronoi_kernel)
interpolator_0.SetLocator(locator)

timer.StartTimer()
interpolator_0.Update()
timer.StopTimer()
print("Interpolate Points (Voronoi): {0}".format(timer.GetElapsedTime()))

interpolator_mapper_0 = vtkPolyDataMapper()
interpolator_mapper_0.SetInputConnection(interpolator_0.GetOutputPort())

interpolator_actor_0 = vtkActor()
interpolator_actor_0.SetMapper(interpolator_mapper_0)

outline_0 = vtkStructuredGridOutlineFilter()
outline_0.SetInputData(output)
outline_mapper_0 = vtkPolyDataMapper()
outline_mapper_0.SetInputConnection(outline_0.GetOutputPort())
outline_actor_0 = vtkActor()
outline_actor_0.SetMapper(outline_mapper_0)

# --- Gaussian kernel ---
gaussian_kernel = vtkGaussianKernel()
gaussian_kernel.SetSharpness(4)
gaussian_kernel.SetRadius(0.5)

interpolator_1 = vtkPointInterpolator()
interpolator_1.SetInputConnection(plane.GetOutputPort())
interpolator_1.SetSourceData(output)
interpolator_1.SetKernel(gaussian_kernel)
interpolator_1.SetLocator(locator)
interpolator_1.SetNullPointsStrategyToNullValue()

timer.StartTimer()
interpolator_1.Update()
timer.StopTimer()
print("Interpolate Points (Gaussian): {0}".format(timer.GetElapsedTime()))

interpolator_mapper_1 = vtkPolyDataMapper()
interpolator_mapper_1.SetInputConnection(interpolator_1.GetOutputPort())

interpolator_actor_1 = vtkActor()
interpolator_actor_1.SetMapper(interpolator_mapper_1)

outline_1 = vtkStructuredGridOutlineFilter()
outline_1.SetInputData(output)
outline_mapper_1 = vtkPolyDataMapper()
outline_mapper_1.SetInputConnection(outline_1.GetOutputPort())
outline_actor_1 = vtkActor()
outline_actor_1.SetMapper(outline_mapper_1)

# --- Shepard kernel ---
shepard_kernel = vtkShepardKernel()
shepard_kernel.SetPowerParameter(2)
shepard_kernel.SetRadius(0.5)

interpolator_2 = vtkPointInterpolator()
interpolator_2.SetInputConnection(plane.GetOutputPort())
interpolator_2.SetSourceData(output)
interpolator_2.SetKernel(shepard_kernel)
interpolator_2.SetLocator(locator)
interpolator_2.SetNullPointsStrategyToMaskPoints()

timer.StartTimer()
interpolator_2.Update()
timer.StopTimer()
print("Interpolate Points (Shepard): {0}".format(timer.GetElapsedTime()))

interpolator_mapper_2 = vtkPolyDataMapper()
interpolator_mapper_2.SetInputConnection(interpolator_2.GetOutputPort())

interpolator_actor_2 = vtkActor()
interpolator_actor_2.SetMapper(interpolator_mapper_2)

outline_2 = vtkStructuredGridOutlineFilter()
outline_2.SetInputData(output)
outline_mapper_2 = vtkPolyDataMapper()
outline_mapper_2.SetInputConnection(outline_2.GetOutputPort())
outline_actor_2 = vtkActor()
outline_actor_2.SetMapper(outline_mapper_2)

# --- Linear kernel ---
linear_kernel = vtkLinearKernel()
linear_kernel.SetRadius(0.5)

interpolator_3 = vtkPointInterpolator()
interpolator_3.SetInputConnection(plane.GetOutputPort())
interpolator_3.SetSourceData(output)
interpolator_3.SetKernel(linear_kernel)
interpolator_3.SetLocator(locator)
interpolator_3.SetNullPointsStrategyToNullValue()
interpolator_3.AddExcludedArray("StagnationEnergy")

timer.StartTimer()
interpolator_3.Update()
timer.StopTimer()
print("Interpolate Points (Linear): {0}".format(timer.GetElapsedTime()))

interpolator_mapper_3 = vtkPolyDataMapper()
interpolator_mapper_3.SetInputConnection(interpolator_3.GetOutputPort())

interpolator_actor_3 = vtkActor()
interpolator_actor_3.SetMapper(interpolator_mapper_3)

outline_3 = vtkStructuredGridOutlineFilter()
outline_3.SetInputData(output)
outline_mapper_3 = vtkPolyDataMapper()
outline_mapper_3.SetInputConnection(outline_3.GetOutputPort())
outline_actor_3 = vtkActor()
outline_actor_3.SetMapper(outline_mapper_3)

# Renderers
renderer_0 = vtkRenderer()
renderer_0.SetViewport(0, 0, 0.5, 0.5)
renderer_0.AddActor(interpolator_actor_0)
renderer_0.AddActor(outline_actor_0)
renderer_0.SetBackground(0.1, 0.2, 0.4)

renderer_1 = vtkRenderer()
renderer_1.SetViewport(0.5, 0, 1, 0.5)
renderer_1.AddActor(interpolator_actor_1)
renderer_1.AddActor(outline_actor_1)
renderer_1.SetBackground(0.1, 0.2, 0.4)

renderer_2 = vtkRenderer()
renderer_2.SetViewport(0, 0.5, 0.5, 1)
renderer_2.AddActor(interpolator_actor_2)
renderer_2.AddActor(outline_actor_2)
renderer_2.SetBackground(0.1, 0.2, 0.4)

renderer_3 = vtkRenderer()
renderer_3.SetViewport(0.5, 0.5, 1, 1)
renderer_3.AddActor(interpolator_actor_3)
renderer_3.AddActor(outline_actor_3)
renderer_3.SetBackground(0.1, 0.2, 0.4)

# Window
render_window = vtkRenderWindow()
render_window.SetMultiSamples(0)
render_window.AddRenderer(renderer_0)
render_window.AddRenderer(renderer_1)
render_window.AddRenderer(renderer_2)
render_window.AddRenderer(renderer_3)
render_window.SetSize(500, 500)
render_window.SetWindowName("interpolator")

# Scene
camera = renderer_0.GetActiveCamera()
camera.SetClippingRange(3.95297, 50)
camera.SetFocalPoint(8.88908, 0.595038, 29.3342)
camera.SetPosition(-12.3332, 31.7479, 41.2387)
camera.SetViewUp(0.060772, -0.319905, 0.945498)

renderer_1.SetActiveCamera(camera)
renderer_2.SetActiveCamera(camera)
renderer_3.SetActiveCamera(camera)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
