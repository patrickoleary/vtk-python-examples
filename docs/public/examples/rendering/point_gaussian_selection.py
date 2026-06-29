#!/usr/bin/env python

# Demonstrate vtkPointGaussianMapper with hardware selection.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import vtkLookupTable
from vtkmodules.vtkFiltersGeneral import vtkRandomAttributeGenerator
from vtkmodules.vtkFiltersSources import vtkPointSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPointGaussianMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

desired_points = 1000

# Point source
points = vtkPointSource()
points.SetNumberOfPoints(desired_points)
points.SetRadius(pow(desired_points, 0.33) * 20.0)
points.Update()

# Random attributes
random_attr = vtkRandomAttributeGenerator()
random_attr.SetInputConnection(points.GetOutputPort())
random_attr.SetDataTypeToFloat()
random_attr.GeneratePointScalarsOn()
random_attr.GeneratePointVectorsOn()
random_attr.Update()

# Point gaussian mapper
mapper = vtkPointGaussianMapper()
mapper.SetInputConnection(random_attr.GetOutputPort())
mapper.SetColorModeToMapScalars()
mapper.SetScalarModeToUsePointFieldData()
mapper.SelectColorArray("RandomPointVectors")
mapper.SetInterpolateScalarsBeforeMapping(0)
mapper.SetScaleArray("RandomPointVectors")
mapper.SetScaleArrayComponent(3)

lut = vtkLookupTable()
lut.SetHueRange(0.1, 0.2)
lut.SetSaturationRange(1.0, 0.5)
lut.SetValueRange(0.8, 1.0)
mapper.SetLookupTable(lut)

actor = vtkActor()
actor.SetMapper(mapper)

renderer = vtkRenderer()
renderer.SetBackground(0.0, 0.0, 0.0)
renderer.AddActor(actor)

render_window = vtkRenderWindow()
render_window.SetSize(300, 300)
render_window.SetMultiSamples(0)
render_window.AddRenderer(renderer)
render_window.SetWindowName("point gaussian selection")

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
# Pipeline exception: render needed before camera zoom for hardware selection
render_window.Render()
renderer.GetActiveCamera().Zoom(3.5)

interactor.Initialize()
interactor.Start()
