#!/usr/bin/env python

# Demonstrate how to change the point size of rendered vertices.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkFiltersSources import vtkPointSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
yellow = (1.000, 1.000, 0.000)
royal_blue = (0.255, 0.412, 0.882)

# Source: generate random point cloud
source = vtkPointSource()
source.SetCenter(0.0, 0.0, 0.0)
source.SetNumberOfPoints(10)
source.SetRadius(5.0)

# Mapper: map point data to graphics primitives
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(source.GetOutputPort())

# Actor: assign the mapped geometry and set point size
actor = vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetColor(yellow)
actor.GetProperty().SetPointSize(5)

# Renderer: assemble the scene and configure the camera
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(royal_blue)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("PointSize")
render_window.SetSize(640, 480)

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Start()
