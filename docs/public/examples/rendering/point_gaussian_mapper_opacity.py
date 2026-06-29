#!/usr/bin/env python

# Demonstrate point Gaussian mapper with opacity function and custom splat shader for square shape.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonDataModel import vtkPiecewiseFunction
from vtkmodules.vtkFiltersGeneral import vtkRandomAttributeGenerator
from vtkmodules.vtkFiltersSources import vtkPointSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkColorTransferFunction,
    vtkPointGaussianMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

desired_points = 10000

points = vtkPointSource()
points.SetNumberOfPoints(desired_points)
points.SetRadius(pow(desired_points, 0.33) * 10.0)
points.Update()

# Generate random attributes
random_attr = vtkRandomAttributeGenerator()
random_attr.SetInputConnection(points.GetOutputPort())
random_attr.SetDataTypeToFloat()
random_attr.GeneratePointScalarsOn()
random_attr.GeneratePointVectorsOn()
random_attr.GeneratePointArrayOn()
random_attr.Update()

output = random_attr.GetOutput()
output.GetPointData().SetScalars(output.GetPointData().GetArray("RandomPointArray"))

# Point Gaussian mapper with square splat shader
mapper = vtkPointGaussianMapper()
mapper.SetInputConnection(random_attr.GetOutputPort())
mapper.SetColorModeToMapScalars()
mapper.SetScalarModeToUsePointFieldData()
mapper.SelectColorArray("RandomPointVectors")
mapper.SetInterpolateScalarsBeforeMapping(0)
mapper.SetScaleArray("RandomPointScalars")
mapper.SetScaleArrayComponent(1)
mapper.SetOpacityArray("RandomPointArray")
mapper.SetOpacityArrayComponent(0)
mapper.EmissiveOff()

# Custom splat shader: square shape with cutout
mapper.SetSplatShaderCode(
    "//VTK::Color::Impl\n"
    "  if (abs(offsetVCVSOutput.x) > 1.0 || abs(offsetVCVSOutput.y) > 1.0) { discard; }\n"
    "  if (abs(offsetVCVSOutput.x) < 0.6 && abs(offsetVCVSOutput.y) < 0.6) { discard; }\n"
)
mapper.SetBoundScale(1.5)

# Color transfer function
ctf = vtkColorTransferFunction()
ctf.AddHSVPoint(0.0, 0.1, 0.7, 1.0)
ctf.AddHSVPoint(1.0, 0.9, 0.7, 1.0)
ctf.SetColorSpaceToHSV()
ctf.HSVWrapOff()
mapper.SetLookupTable(ctf)

# Opacity transfer function
otf = vtkPiecewiseFunction()
otf.AddPoint(0.0, 0.3)
otf.AddPoint(1.0, 1.0)
mapper.SetScalarOpacityFunction(otf)

actor = vtkActor()
actor.SetMapper(mapper)

renderer = vtkRenderer()
renderer.SetBackground(0.0, 0.0, 0.0)
renderer.AddActor(actor)

render_window = vtkRenderWindow()
render_window.SetSize(300, 300)
render_window.SetMultiSamples(0)
render_window.AddRenderer(renderer)
render_window.SetWindowName("point gaussian mapper opacity")

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
# Pipeline exception: render needed before camera zoom for point gaussian
render_window.Render()
renderer.GetActiveCamera().SetPosition(0, 0, 1)
renderer.GetActiveCamera().SetFocalPoint(0, 0, 0)
renderer.GetActiveCamera().SetViewUp(0, 1, 0)
renderer.ResetCamera()
renderer.GetActiveCamera().Zoom(10.0)

interactor.Initialize()
interactor.Start()
