#!/usr/bin/env python

# Test vtkRotationFilter creating rotated copies of a cone.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersGeneral import vtkRotationFilter
from vtkmodules.vtkFiltersSources import vtkConeSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkDataSetMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Cone source
cone = vtkConeSource()
cone.SetRadius(0.05)
cone.SetHeight(0.25)
cone.SetResolution(256)
cone.SetCenter(0.15, 0.0, 0.15)

# Rotation filter
rotate = vtkRotationFilter()
rotate.SetInputConnection(cone.GetOutputPort())
rotate.SetAxisToZ()
rotate.SetCenter(0.0, 0.0, 0.0)
rotate.SetAngle(45)
rotate.SetNumberOfCopies(7)
rotate.CopyInputOn()

mapper = vtkDataSetMapper()
mapper.SetInputConnection(rotate.GetOutputPort())

actor = vtkActor()
actor.SetMapper(mapper)

renderer = vtkRenderer()
renderer.AddActor(actor)

render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("rotate")
render_window.SetMultiSamples(0)
render_window.SetSize(512, 512)

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
