#!/usr/bin/env python

# Demonstrate vtkEllipsoidalGaussianKernel by interpolating a single point
# with scalar and normal data onto a volume, then extracting an isosurface
# showing the anisotropic kernel shape.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import (
    vtkFloatArray,
    vtkPoints,
)
from vtkmodules.vtkCommonDataModel import (
    vtkImageData,
    vtkPolyData,
)
from vtkmodules.vtkFiltersCore import vtkFlyingEdges3D
from vtkmodules.vtkFiltersModeling import vtkOutlineFilter
from vtkmodules.vtkFiltersPoints import (
    vtkEllipsoidalGaussianKernel,
    vtkPointInterpolator,
)
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Parameters
res = 250

# Create a volume to interpolate onto
volume = vtkImageData()
volume.SetDimensions(res, res, res)
volume.SetOrigin(0, 0, 0)
volume.SetSpacing(1, 1, 1)
scalars_array = vtkFloatArray()
scalars_array.SetName("scalars")
scalars_array.Allocate(res ** 3)
volume.GetPointData().SetScalars(scalars_array)

center = volume.GetCenter()

# Create a single point with a normal and scalar
one_points = vtkPoints()
one_points.SetNumberOfPoints(1)
one_points.SetPoint(0, center)

one_scalars = vtkFloatArray()
one_scalars.SetNumberOfTuples(1)
one_scalars.SetTuple1(0, 5.0)
one_scalars.SetName("scalarPt")

one_normals = vtkFloatArray()
one_normals.SetNumberOfComponents(3)
one_normals.SetNumberOfTuples(1)
one_normals.SetTuple3(0, 1, 1, 1)
one_normals.SetName("normalPt")

one_data = vtkPolyData()
one_data.SetPoints(one_points)
one_data.GetPointData().SetScalars(one_scalars)
one_data.GetPointData().SetNormals(one_normals)

# Ellipsoidal Gaussian interpolation
e_kernel = vtkEllipsoidalGaussianKernel()
e_kernel.SetKernelFootprintToRadius()
e_kernel.SetRadius(50.0)
e_kernel.UseScalarsOn()
e_kernel.UseNormalsOn()
e_kernel.SetScaleFactor(0.5)
e_kernel.SetEccentricity(3)
e_kernel.NormalizeWeightsOff()

interpolator = vtkPointInterpolator()
interpolator.SetInputData(volume)
interpolator.SetSourceData(one_data)
interpolator.SetKernel(e_kernel)
interpolator.Update()

# Extract isosurface
contour = vtkFlyingEdges3D()
contour.SetInputConnection(interpolator.GetOutputPort())
contour.SetValue(0, 10)

interpolator_mapper = vtkPolyDataMapper()
interpolator_mapper.SetInputConnection(contour.GetOutputPort())

interpolator_actor = vtkActor()
interpolator_actor.SetMapper(interpolator_mapper)

# Outline
outline = vtkOutlineFilter()
outline.SetInputData(volume)

outline_mapper = vtkPolyDataMapper()
outline_mapper.SetInputConnection(outline.GetOutputPort())

outline_actor = vtkActor()
outline_actor.SetMapper(outline_mapper)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(interpolator_actor)
renderer.SetBackground(1, 1, 1)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(300, 300)
render_window.SetWindowName("ellipsoidal gaussian kernel")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
