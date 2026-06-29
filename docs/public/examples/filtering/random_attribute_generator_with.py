#!/usr/bin/env python

# Demonstrate vtkRandomAttributeGenerator by generating random point
# scalars, vectors, cell scalars, and cell vectors on a sphere and
# rendering the sphere colored by the random point scalars.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersGeneral import vtkRandomAttributeGenerator
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Create a sphere
sphere = vtkSphereSource()

# Generate random point and cell data
random_gen = vtkRandomAttributeGenerator()
random_gen.SetInputConnection(sphere.GetOutputPort())
random_gen.GenerateAllPointDataOn()
random_gen.GenerateAllCellDataOn()
random_gen.Update()

# Render colored by random point scalars
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(random_gen.GetOutputPort())
mapper.SetScalarModeToUsePointFieldData()
mapper.SelectColorArray("RandomPointScalars")
mapper.SetScalarRange(0, 1)

actor = vtkActor()
actor.SetMapper(mapper)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(0.1, 0.2, 0.4)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(400, 400)
render_window.SetWindowName("random attribute generator with")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.ResetCamera()

interactor.Initialize()
interactor.Start()
