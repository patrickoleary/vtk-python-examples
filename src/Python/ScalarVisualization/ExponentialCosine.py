#!/usr/bin/env python

# Warp a plane with an exponential cosine function and color by derivative.

import math

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkCommonCore import (
    vtkDoubleArray,
    vtkPoints,
)
from vtkmodules.vtkCommonDataModel import vtkPolyData
from vtkmodules.vtkCommonTransforms import vtkTransform
from vtkmodules.vtkFiltersGeneral import (
    vtkTransformPolyDataFilter,
    vtkWarpScalar,
)
from vtkmodules.vtkFiltersSources import vtkPlaneSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkDataSetMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
beige = (0.961, 0.961, 0.863)

# Source: create a high-resolution plane and scale it
plane = vtkPlaneSource()
plane.SetResolution(300, 300)

transform = vtkTransform()
transform.Scale(10.0, 10.0, 1.0)

trans_filter = vtkTransformPolyDataFilter()
trans_filter.SetInputConnection(plane.GetOutputPort())
trans_filter.SetTransform(transform)
trans_filter.Update()

# Compute: evaluate exponential cosine function and its derivative
input_pd = trans_filter.GetOutput()
num_pts = input_pd.GetNumberOfPoints()

new_pts = vtkPoints()
new_pts.SetNumberOfPoints(num_pts)

derivs = vtkDoubleArray()
derivs.SetNumberOfTuples(num_pts)

bessel = vtkPolyData()
bessel.CopyStructure(input_pd)
bessel.SetPoints(new_pts)
bessel.GetPointData().SetScalars(derivs)

x = [0.0] * 3
for i in range(num_pts):
    input_pd.GetPoint(i, x)
    r = (x[0] * x[0] + x[1] * x[1]) ** 0.5
    x[2] = math.exp(-r) * math.cos(10.0 * r)
    new_pts.SetPoint(i, x)
    deriv = -math.exp(-r) * (math.cos(10.0 * r) + 10.0 * math.sin(10.0 * r))
    derivs.SetValue(i, deriv)

# Filter: warp the plane by the computed function values
warp = vtkWarpScalar()
warp.SetInputData(bessel)
warp.XYPlaneOn()
warp.SetScaleFactor(0.5)

# Mapper: map the warped surface to graphics primitives
mapper = vtkDataSetMapper()
mapper.SetInputConnection(warp.GetOutputPort())
scalar_range = bessel.GetScalarRange()
mapper.SetScalarRange(scalar_range[0], scalar_range[1])

# Actor: display the warped surface
carpet = vtkActor()
carpet.SetMapper(mapper)

# Renderer: assemble the scene and configure the camera
renderer = vtkRenderer()
renderer.AddActor(carpet)
renderer.SetBackground(beige)
renderer.ResetCamera()
renderer.GetActiveCamera().Zoom(1.35)
renderer.GetActiveCamera().Elevation(-55)
renderer.GetActiveCamera().Azimuth(25)
renderer.ResetCameraClippingRange()

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("ExponentialCosine")
render_window.SetSize(640, 480)

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Start()
