#!/usr/bin/env python

# Compute exp(-r)*cos(10*r) on a plane, warp by scalar, and color by
# the derivative. A Bessel-like function visualization.

import math

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import (
    vtkFloatArray,
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

# Create a plane and scale it
plane = vtkPlaneSource()
plane.SetResolution(300, 300)

transform = vtkTransform()
transform.Scale(10.0, 10.0, 1.0)

trans_f = vtkTransformPolyDataFilter()
trans_f.SetInputConnection(plane.GetOutputPort())
trans_f.SetTransform(transform)
trans_f.Update()

# Compute exp(-r)*cos(10r) and its derivative
input_pd = trans_f.GetOutput()
num_pts = input_pd.GetNumberOfPoints()

new_pts = vtkPoints()
new_pts.SetNumberOfPoints(num_pts)

derivs = vtkFloatArray()
derivs.SetNumberOfTuples(num_pts)

x = [0.0, 0.0, 0.0]
for i in range(num_pts):
    input_pd.GetPoint(i, x)
    r = math.sqrt(x[0] * x[0] + x[1] * x[1])
    x[2] = math.exp(-r) * math.cos(10.0 * r)
    new_pts.SetPoint(i, x)
    deriv = -math.exp(-r) * (math.cos(10.0 * r) + 10.0 * math.sin(10.0 * r))
    derivs.SetValue(i, deriv)

bessel = vtkPolyData()
bessel.CopyStructure(input_pd)
bessel.SetPoints(new_pts)
bessel.GetPointData().SetScalars(derivs)

# Warp by scalar
warp = vtkWarpScalar()
warp.SetInputData(bessel)
warp.XYPlaneOn()
warp.SetScaleFactor(0.5)

# Mapper and actor
mapper = vtkDataSetMapper()
mapper.SetInputConnection(warp.GetOutputPort())
scalar_range = bessel.GetScalarRange()
mapper.SetScalarRange(scalar_range[0], scalar_range[1])

carpet = vtkActor()
carpet.SetMapper(mapper)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(carpet)
renderer.SetBackground(1, 1, 1)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(300, 300)
render_window.SetWindowName("exp cos")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.ResetCamera()
renderer.GetActiveCamera().Zoom(1.4)
renderer.GetActiveCamera().Elevation(-55)
renderer.GetActiveCamera().Azimuth(25)
renderer.ResetCameraClippingRange()

interactor.Initialize()
interactor.Start()
