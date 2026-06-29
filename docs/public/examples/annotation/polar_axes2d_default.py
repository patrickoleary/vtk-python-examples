#!/usr/bin/env python

# Test vtkPolarAxesActor2D in default configuration.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersSources import vtkOutlineSource
from vtkmodules.vtkRenderingAnnotation import vtkPolarAxesActor2D
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Polar axes 2D (default)
polar_axes = vtkPolarAxesActor2D()
polar_axes.GetProperty().SetLineWidth(2)

# Outline for context
outline_source = vtkOutlineSource()

outline_mapper = vtkPolyDataMapper()
outline_mapper.SetInputConnection(outline_source.GetOutputPort())

outline_actor = vtkActor()
outline_actor.SetMapper(outline_mapper)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(polar_axes)
renderer.AddActor(outline_actor)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("polar axes2d default")
render_window.SetMultiSamples(0)
render_window.SetSize(300, 300)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.GetActiveCamera().ParallelProjectionOn()
renderer.ResetCamera()

interactor.Initialize()
interactor.Start()
