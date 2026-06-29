#!/usr/bin/env python

# Demonstrate vtkPointGaussianMapper with random point splats and a color transfer function.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersSources import vtkPointSource
from vtkmodules.vtkFiltersGeneral import vtkRandomAttributeGenerator
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkColorTransferFunction,
    vtkPointGaussianMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

desired_points = int(1.0e4)

# Random point cloud
points = vtkPointSource()
points.SetNumberOfPoints(desired_points)
points.SetRadius(pow(desired_points, 0.33) * 20.0)
points.Update()

# Generate random scalar and vector attributes
random_attr = vtkRandomAttributeGenerator()
random_attr.SetInputConnection(points.GetOutputPort())
random_attr.SetDataTypeToFloat()
random_attr.GeneratePointScalarsOn()
random_attr.GeneratePointVectorsOn()
random_attr.Update()

# Point gaussian mapper with splat rendering
mapper = vtkPointGaussianMapper()
mapper.SetInputConnection(random_attr.GetOutputPort())
mapper.SetColorModeToMapScalars()
mapper.SetScalarModeToUsePointFieldData()
mapper.SelectColorArray("RandomPointVectors")
mapper.SetInterpolateScalarsBeforeMapping(0)
mapper.SetScaleArray("RandomPointVectors")
mapper.SetScaleArrayComponent(3)

# HSV color transfer function
ctf = vtkColorTransferFunction()
ctf.AddHSVPoint(0.0, 0.1, 1.0, 0.8)
ctf.AddHSVPoint(1.0, 0.2, 0.5, 1.0)
ctf.SetColorSpaceToRGB()
mapper.SetLookupTable(ctf)

actor = vtkActor()
actor.SetMapper(mapper)

# Rendering pipeline
renderer = vtkRenderer()
renderer.SetBackground(0.0, 0.0, 0.0)
renderer.AddActor(actor)

render_window = vtkRenderWindow()
render_window.SetSize(300, 300)
render_window.SetMultiSamples(0)
render_window.AddRenderer(renderer)
render_window.SetWindowName("point gaussian mapper")

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.GetActiveCamera().SetPosition(0, 0, 1)
renderer.GetActiveCamera().SetFocalPoint(0, 0, 0)
renderer.GetActiveCamera().SetViewUp(0, 1, 0)
renderer.ResetCamera()
renderer.GetActiveCamera().Zoom(10.0)

interactor.Initialize()
interactor.Start()
