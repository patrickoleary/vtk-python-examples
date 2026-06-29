#!/usr/bin/env python
# Demonstrate vtkQuadricClustering on a sphere source.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonColor import vtkNamedColors
from vtkmodules.vtkFiltersCore import vtkQuadricClustering
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

colors = vtkNamedColors()

# Create a high-resolution sphere.
sphere = vtkSphereSource()
sphere.SetPhiResolution(150)
sphere.SetThetaResolution(150)

# Decimate with quadric clustering.
mesh = vtkQuadricClustering()
mesh.SetInputConnection(sphere.GetOutputPort())
mesh.SetNumberOfXDivisions(10)
mesh.SetNumberOfYDivisions(10)
mesh.SetNumberOfZDivisions(10)

# Mapper and actor.
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(mesh.GetOutputPort())

tomato_rgb = [0.0, 0.0, 0.0]
colors.GetColorRGB("tomato", tomato_rgb)

actor = vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetDiffuseColor(tomato_rgb)
actor.GetProperty().SetDiffuse(0.8)
actor.GetProperty().SetSpecular(0.4)
actor.GetProperty().SetSpecularPower(30)

renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(1, 1, 1)

render_window = vtkRenderWindow()
render_window.SetSize(300, 300)
render_window.AddRenderer(renderer)
render_window.SetWindowName("quadric clustering data model")

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
