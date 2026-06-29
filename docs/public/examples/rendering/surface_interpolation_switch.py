#!/usr/bin/env python

# Demonstrate switching surface interpolation from Phong to flat on a sphere with normals.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersCore import vtkPolyDataNormals
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Sphere with point and cell normals
sphere = vtkSphereSource()

normals = vtkPolyDataNormals()
normals.SetInputConnection(sphere.GetOutputPort())
normals.SetComputePointNormals(True)
normals.SetComputeCellNormals(True)
normals.Update()

mapper = vtkPolyDataMapper()
mapper.SetInputData(normals.GetOutput())

actor = vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetRepresentationToSurface()
actor.GetProperty().SetInterpolationToPhong()

renderer = vtkRenderer()
renderer.SetBackground(0.0, 0.0, 0.0)
renderer.AddActor(actor)

render_window = vtkRenderWindow()
render_window.SetSize(600, 300)
render_window.AddRenderer(renderer)
render_window.SetWindowName("surface interpolation switch")

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# First render with Phong interpolation
render_window.Render()

# Switch to flat interpolation
actor.GetProperty().SetInterpolationToFlat()
mapper.Update()

render_window.Render()
interactor.Initialize()
interactor.Start()
