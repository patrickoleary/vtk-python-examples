#!/usr/bin/env python

# Interpolate a scalar field from scattered points onto a sphere surface
# using vtkPointInterpolator with a Gaussian kernel. The scattered source
# points are shown as splats alongside the interpolated surface.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import math

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkCommonCore import (
    vtkFloatArray,
    vtkMinimalStandardRandomSequence,
    vtkPoints,
)
from vtkmodules.vtkCommonDataModel import (
    vtkImageData,
    vtkPolyData,
)
from vtkmodules.vtkFiltersCore import vtkResampleWithDataSet
from vtkmodules.vtkFiltersPoints import (
    vtkGaussianKernel,
    vtkPointInterpolator,
)
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPointGaussianMapper,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
slate_gray_background_rgb = (0.439, 0.502, 0.565)

# Generate 200 random scattered source points with a scalar value
rng = vtkMinimalStandardRandomSequence()
rng.SetSeed(42)

source_points = vtkPoints()
source_scalars = vtkFloatArray()
source_scalars.SetName("val")
for _ in range(200):
    rng.Next()
    x = rng.GetRangeValue(-1.0, 1.0)
    rng.Next()
    y = rng.GetRangeValue(-1.0, 1.0)
    rng.Next()
    z = rng.GetRangeValue(-1.0, 1.0)
    source_points.InsertNextPoint(x, y, z)
    source_scalars.InsertNextValue(math.sqrt(x * x + y * y + z * z))

source_poly = vtkPolyData()
source_poly.SetPoints(source_points)
source_poly.GetPointData().AddArray(source_scalars)
source_poly.GetPointData().SetActiveScalars("val")
scalar_range = source_scalars.GetRange()

# Probe surface: a tessellated sphere
probe_sphere = vtkSphereSource()
probe_sphere.SetThetaResolution(40)
probe_sphere.SetPhiResolution(40)
probe_sphere.SetRadius(0.8)
probe_sphere.Update()

probe_surface = probe_sphere.GetOutput()
bounds = probe_surface.GetBounds()

# ImageData volume enclosing the probe surface for interpolation
volume = vtkImageData()
volume.SetDimensions(51, 51, 51)
volume.SetSpacing(
    (bounds[1] - bounds[0]) / 50.0,
    (bounds[3] - bounds[2]) / 50.0,
    (bounds[5] - bounds[4]) / 50.0,
)
volume.SetOrigin(bounds[0], bounds[2], bounds[4])

# Gaussian kernel for smooth interpolation
gaussian_kernel = vtkGaussianKernel()
gaussian_kernel.SetSharpness(2)
gaussian_kernel.SetRadius(1.0)

# PointInterpolator: interpolate source scalars onto the volume grid
interpolator = vtkPointInterpolator()
interpolator.SetInputData(volume)
interpolator.SetSourceData(source_poly)
interpolator.SetKernel(gaussian_kernel)

# Resample: project the interpolated volume onto the probe surface
resample = vtkResampleWithDataSet()
resample.SetInputData(probe_surface)
resample.SetSourceConnection(interpolator.GetOutputPort())

# Mapper: map the interpolated surface to graphics primitives
surface_mapper = vtkPolyDataMapper()
surface_mapper.SetInputConnection(resample.GetOutputPort())
surface_mapper.SetScalarRange(scalar_range)

surface_actor = vtkActor()
surface_actor.SetMapper(surface_mapper)

# Mapper: show source points as Gaussian splats
point_mapper = vtkPointGaussianMapper()
point_mapper.SetInputData(source_poly)
point_mapper.SetScalarRange(scalar_range)
point_mapper.SetScaleFactor(0.03)
point_mapper.EmissiveOff()
point_mapper.SetSplatShaderCode(
    "//VTK::Color::Impl\n"
    "float dist = dot(offsetVCVSOutput.xy,offsetVCVSOutput.xy);\n"
    "if (dist > 1.0) {\n"
    "  discard;\n"
    "} else {\n"
    "  float scale = (1.0 - dist);\n"
    "  ambientColor *= scale;\n"
    "  diffuseColor *= scale;\n"
    "}\n"
)

point_actor = vtkActor()
point_actor.SetMapper(point_mapper)

# Renderer: assemble the scene and configure the camera
renderer = vtkRenderer()
renderer.AddActor(surface_actor)
renderer.AddActor(point_actor)
renderer.SetBackground(slate_gray_background_rgb)
renderer.ResetCamera()

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(640, 480)
render_window.SetWindowName("PointInterpolator")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
