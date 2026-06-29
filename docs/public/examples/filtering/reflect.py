#!/usr/bin/env python

# Reflect a cone through X-max, Y-max, and Z-max planes using
# vtkReflectionFilter, producing eight mirrored copies.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersGeneral import vtkReflectionFilter
from vtkmodules.vtkFiltersSources import vtkConeSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkDataSetMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Create a cone and reflect through three planes
cone = vtkConeSource()

reflect = vtkReflectionFilter()
reflect.SetInputConnection(cone.GetOutputPort())
reflect.SetPlaneToXMax()

reflect_2 = vtkReflectionFilter()
reflect_2.SetInputConnection(reflect.GetOutputPort())
reflect_2.SetPlaneToYMax()

reflect_3 = vtkReflectionFilter()
reflect_3.SetInputConnection(reflect_2.GetOutputPort())
reflect_3.SetPlaneToZMax()

mapper = vtkDataSetMapper()
mapper.SetInputConnection(reflect_3.GetOutputPort())

actor = vtkActor()
actor.SetMapper(mapper)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(0.1, 0.2, 0.4)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(200, 200)
render_window.SetWindowName("reflect")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
