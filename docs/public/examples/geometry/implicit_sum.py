#!/usr/bin/env python
# Demonstrate adding two implicit models (cone and sphere) to produce a combined surface.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonDataModel import vtkCone, vtkImplicitSum, vtkSphere
from vtkmodules.vtkFiltersCore import vtkContourFilter
from vtkmodules.vtkImagingHybrid import vtkSampleFunction
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Create implicit functions.
geom_object_1 = vtkCone()
geom_object_2 = vtkSphere()
geom_object_2.SetRadius(0.5)
geom_object_2.SetCenter(0.5, 0, 0)

# Combine with weighted sum.
implicit_sum = vtkImplicitSum()
implicit_sum.SetNormalizeByWeight(1)
implicit_sum.AddFunction(geom_object_1, 2)
implicit_sum.AddFunction(geom_object_2, 1)

# Sample the implicit function.
sample = vtkSampleFunction()
sample.SetImplicitFunction(implicit_sum)
sample.SetSampleDimensions(60, 60, 60)
sample.ComputeNormalsOn()

# Extract the zero-level isosurface.
surface = vtkContourFilter()
surface.SetInputConnection(sample.GetOutputPort())
surface.SetValue(0, 0.0)

# Mapper and actor.
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(surface.GetOutputPort())
mapper.ScalarVisibilityOff()

actor = vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetDiffuseColor(0.2, 0.4, 0.6)
actor.GetProperty().SetSpecular(0.4)
actor.GetProperty().SetDiffuse(0.7)
actor.GetProperty().SetSpecularPower(40)

renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(1, 1, 1)

render_window = vtkRenderWindow()
render_window.SetSize(300, 300)
render_window.AddRenderer(renderer)
render_window.SetWindowName("implicit sum")

renderer.ResetCamera()
renderer.GetActiveCamera().Azimuth(60)
renderer.GetActiveCamera().Elevation(-10)
renderer.GetActiveCamera().Dolly(1.5)
renderer.ResetCameraClippingRange()

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
