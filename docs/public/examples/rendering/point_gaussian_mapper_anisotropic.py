#!/usr/bin/env python

# Demonstrate anisotropic point Gaussian mapper with random scale and quaternion rotation.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

import math

from vtkmodules.vtkCommonCore import vtkFloatArray, vtkMersenneTwister
from vtkmodules.vtkFiltersSources import vtkPointSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPointGaussianMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

desired_points = 100

points = vtkPointSource()
points.SetNumberOfPoints(desired_points)
points.SetRadius(10.0)
points.Update()

poly_data = points.GetOutput()

# Scale array (3-component)
scale = vtkFloatArray()
scale.SetName("scale")
scale.SetNumberOfComponents(3)
scale.SetNumberOfTuples(desired_points)

# Orientation array (4-component quaternion)
orientation = vtkFloatArray()
orientation.SetName("rotation")
orientation.SetNumberOfComponents(4)
orientation.SetNumberOfTuples(desired_points)

# Random number generator
seq = vtkMersenneTwister()
seq.InitializeSequence(0, 0)

two_pi = math.pi * 2.0

for i in range(desired_points):
    s0 = 0.01 + seq.GetValue()
    seq.Next()
    s1 = 0.01 + seq.GetValue()
    seq.Next()
    s2 = 0.01 + seq.GetValue()
    seq.Next()

    u = seq.GetValue()
    seq.Next()
    v = seq.GetValue()
    seq.Next()
    w = seq.GetValue()
    seq.Next()

    # Random quaternion (uniform on SO(3))
    q0 = math.sqrt(1.0 - u) * math.sin(two_pi * v)
    q1 = math.sqrt(1.0 - u) * math.cos(two_pi * v)
    q2 = math.sqrt(u) * math.sin(two_pi * w)
    q3 = math.sqrt(u) * math.cos(two_pi * w)

    scale.SetTuple3(i, s0, s1, s2)
    orientation.SetTuple4(i, q0, q1, q2, q3)

poly_data.GetPointData().AddArray(scale)
poly_data.GetPointData().AddArray(orientation)

# Point Gaussian mapper with anisotropic splats
mapper = vtkPointGaussianMapper()
mapper.SetInputData(poly_data)
mapper.EmissiveOff()
mapper.SetSplatShaderCode(
    "//VTK::Color::Impl\n"
    "  float dist = sqrt(dot(offsetVCVSOutput.xy,offsetVCVSOutput.xy));\n"
    "  if (dist > 1.0) { discard; }\n"
    "  float scale = (1.0 - dist);\n"
    "  ambientColor *= scale;\n"
    "  diffuseColor *= scale;\n"
)
mapper.SetBoundScale(1.0)
mapper.AnisotropicOn()
mapper.SetScaleArray("scale")
mapper.SetRotationArray("rotation")
mapper.SetLowpassMatrix(1e-5, 0, 1e-5)

actor = vtkActor()
actor.SetMapper(mapper)

renderer = vtkRenderer()
renderer.SetBackground(0.0, 0.0, 0.0)
renderer.AddActor(actor)

render_window = vtkRenderWindow()
render_window.SetSize(300, 300)
render_window.SetMultiSamples(0)
render_window.AddRenderer(renderer)
render_window.SetWindowName("point gaussian mapper anisotropic")

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.ResetCamera()
renderer.GetActiveCamera().Zoom(2.0)

interactor.Initialize()
interactor.Start()
