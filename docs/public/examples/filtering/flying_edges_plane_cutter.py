#!/usr/bin/env python

# Cut a sampled sphere volume with a plane using vtkFlyingEdgesPlaneCutter.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonDataModel import (
    vtkPlane,
    vtkSphere,
)
from vtkmodules.vtkFiltersCore import vtkFlyingEdgesPlaneCutter
from vtkmodules.vtkFiltersModeling import vtkOutlineFilter
from vtkmodules.vtkImagingHybrid import vtkSampleFunction
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

resolution = 100

# Source: sample a sphere implicit function
sphere = vtkSphere()
sphere.SetCenter(0.0, 0.0, 0.0)
sphere.SetRadius(0.25)

sample = vtkSampleFunction()
sample.SetImplicitFunction(sphere)
sample.SetModelBounds(-0.5, 0.5, -0.5, 0.5, -0.5, 0.5)
sample.SetSampleDimensions(resolution, resolution, resolution)
sample.Update()

# Cut plane
plane = vtkPlane()
plane.SetOrigin(0, 0, 0)
plane.SetNormal(1, 1, 1)

# Flying edges plane cutter
cut = vtkFlyingEdgesPlaneCutter()
cut.SetInputConnection(sample.GetOutputPort())
cut.SetPlane(plane)
cut.ComputeNormalsOff()
cut.Update()

cut_mapper = vtkPolyDataMapper()
cut_mapper.SetInputConnection(cut.GetOutputPort())

cut_actor = vtkActor()
cut_actor.SetMapper(cut_mapper)
cut_actor.GetProperty().SetColor(1, 1, 1)
cut_actor.GetProperty().SetOpacity(1)

# Outline
outline = vtkOutlineFilter()
outline.SetInputConnection(sample.GetOutputPort())

outline_mapper = vtkPolyDataMapper()
outline_mapper.SetInputConnection(outline.GetOutputPort())

outline_actor = vtkActor()
outline_actor.SetMapper(outline_mapper)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(outline_actor)
renderer.AddActor(cut_actor)
renderer.SetBackground(0, 0, 0)

# Window
render_window = vtkRenderWindow()
render_window.SetMultiSamples(0)
render_window.AddRenderer(renderer)
render_window.SetSize(400, 400)
render_window.SetWindowName("flying edges plane cutter")

# Scene
renderer.ResetCamera()

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
