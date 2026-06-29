#!/usr/bin/env python

# Demonstrate vtkBox implicit function by sampling it across a volume,
# generating contours with vtkContourFilter, and rendering with an outline.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonDataModel import vtkBox
from vtkmodules.vtkFiltersCore import vtkContourFilter
from vtkmodules.vtkFiltersModeling import vtkOutlineFilter
from vtkmodules.vtkImagingHybrid import vtkSampleFunction
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkCamera,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Define a box implicit function
box = vtkBox()
box.SetXMin(0, 2, 4)
box.SetXMax(2, 4, 6)

# Sample the implicit function
sample = vtkSampleFunction()
sample.SetSampleDimensions(30, 30, 30)
sample.SetImplicitFunction(box)
sample.SetModelBounds(0, 1.5, 1, 5, 2, 8)
sample.ComputeNormalsOn()

# Generate contours
contours = vtkContourFilter()
contours.SetInputConnection(sample.GetOutputPort())
contours.GenerateValues(5, -0.5, 1.5)

# Contour mapper and actor
cont_mapper = vtkPolyDataMapper()
cont_mapper.SetInputConnection(contours.GetOutputPort())
cont_mapper.SetScalarRange(-0.5, 1.5)

cont_actor = vtkActor()
cont_actor.SetMapper(cont_mapper)

# Outline
outline = vtkOutlineFilter()
outline.SetInputConnection(sample.GetOutputPort())

outline_mapper = vtkPolyDataMapper()
outline_mapper.SetInputConnection(outline.GetOutputPort())

outline_actor = vtkActor()
outline_actor.SetMapper(outline_mapper)
outline_actor.GetProperty().SetColor(0, 0, 0)

# Renderer
renderer = vtkRenderer()
renderer.SetBackground(1, 1, 1)
renderer.AddActor(cont_actor)
renderer.AddActor(outline_actor)

# Window
render_window = vtkRenderWindow()
render_window.SetMultiSamples(0)
render_window.AddRenderer(renderer)
render_window.SetSize(500, 500)
render_window.SetWindowName("box function")

# Scene
camera = vtkCamera()
camera.SetClippingRange(6.31875, 20.689)
camera.SetFocalPoint(0.75, 3, 5)
camera.SetPosition(9.07114, -4.10065, -1.38712)
camera.SetViewAngle(30)
camera.SetViewUp(-0.580577, -0.802756, 0.13606)
renderer.SetActiveCamera(camera)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
