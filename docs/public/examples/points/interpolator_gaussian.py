#!/usr/bin/env python

# Demonstrate vtkPointInterpolator with a Gaussian kernel by interpolating
# PLOT3D combustor data onto a volume probe and rendering with a dataset
# mapper.

import os

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonDataModel import (
    vtkImageData,
    vtkStaticPointLocator,
)
from vtkmodules.vtkCommonSystem import vtkTimerLog
from vtkmodules.vtkFiltersCore import vtkStructuredGridOutlineFilter
from vtkmodules.vtkFiltersPoints import (
    vtkGaussianKernel,
    vtkPointInterpolator,
)
from vtkmodules.vtkIOParallel import vtkMultiBlockPLOT3DReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkDataSetMapper,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Parameters
res = 40

# Read PLOT3D combustor data
plot3d_reader = vtkMultiBlockPLOT3DReader()
plot3d_reader.SetXYZFileName(os.path.join(data_dir, "combxyz.bin"))
plot3d_reader.SetQFileName(os.path.join(data_dir, "combq.bin"))
plot3d_reader.SetScalarFunctionNumber(100)
plot3d_reader.SetVectorFunctionNumber(202)
plot3d_reader.Update()

output = plot3d_reader.GetOutput().GetBlock(0)
bounds = output.GetBounds()

# Create a probe volume
probe = vtkImageData()
probe.SetDimensions(res, res, res)
probe.SetOrigin(bounds[0], bounds[2], bounds[4])
probe.SetSpacing(
    (bounds[1] - bounds[0]) / (res - 1),
    (bounds[3] - bounds[2]) / (res - 1),
    (bounds[5] - bounds[4]) / (res - 1),
)

# Reuse locator
locator = vtkStaticPointLocator()
locator.SetDataSet(output)
locator.BuildLocator()

# Gaussian kernel
gaussian_kernel = vtkGaussianKernel()
gaussian_kernel.SetRadius(0.5)
gaussian_kernel.SetSharpness(4)
print("Radius: {0}".format(gaussian_kernel.GetRadius()))

interpolator = vtkPointInterpolator()
interpolator.SetInputData(probe)
interpolator.SetSourceData(output)
interpolator.SetKernel(gaussian_kernel)
interpolator.SetLocator(locator)
interpolator.SetNullPointsStrategyToClosestPoint()

timer = vtkTimerLog()
timer.StartTimer()
interpolator.Update()
timer.StopTimer()
print("Interpolate Points (Volume probe): {0}".format(timer.GetElapsedTime()))

interpolator_mapper = vtkDataSetMapper()
interpolator_mapper.SetInputConnection(interpolator.GetOutputPort())

interpolator_actor = vtkActor()
interpolator_actor.SetMapper(interpolator_mapper)

# Outline
outline = vtkStructuredGridOutlineFilter()
outline.SetInputData(output)

outline_mapper = vtkPolyDataMapper()
outline_mapper.SetInputConnection(outline.GetOutputPort())

outline_actor = vtkActor()
outline_actor.SetMapper(outline_mapper)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(interpolator_actor)
renderer.AddActor(outline_actor)
renderer.SetBackground(0.1, 0.2, 0.4)

# Window
render_window = vtkRenderWindow()
render_window.SetMultiSamples(0)
render_window.AddRenderer(renderer)
render_window.SetSize(250, 250)
render_window.SetWindowName("interpolator gaussian")

# Scene
camera = renderer.GetActiveCamera()
camera.SetClippingRange(3.95297, 50)
camera.SetFocalPoint(8.88908, 0.595038, 29.3342)
camera.SetPosition(-12.3332, 31.7479, 41.2387)
camera.SetViewUp(0.060772, -0.319905, 0.945498)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
