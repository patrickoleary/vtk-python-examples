#!/usr/bin/env python

# Wrap a tube around a line segment using vtkTubeFilter.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkFiltersCore import vtkTubeFilter
from vtkmodules.vtkFiltersSources import vtkLineSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
red_rgb = (1.000, 0.000, 0.000)
dark_slate_gray_rgb = (0.184, 0.310, 0.310)

# Source: a simple line
line_source = vtkLineSource()
line_source.SetPoint1(1.0, 0.0, 0.0)
line_source.SetPoint2(0.0, 1.0, 0.0)

# Mapper & Actor: map the thin line to graphics primitives
line_mapper = vtkPolyDataMapper()
line_mapper.SetInputConnection(line_source.GetOutputPort())

line_actor = vtkActor()
line_actor.SetMapper(line_mapper)
line_actor.GetProperty().SetColor(red_rgb)

# Filter: tube around the line
tube_filter = vtkTubeFilter()
tube_filter.SetInputConnection(line_source.GetOutputPort())
tube_filter.SetRadius(0.025)
tube_filter.SetNumberOfSides(50)

# Mapper & Actor: map the translucent tube to graphics primitives
tube_mapper = vtkPolyDataMapper()
tube_mapper.SetInputConnection(tube_filter.GetOutputPort())

tube_actor = vtkActor()
tube_actor.SetMapper(tube_mapper)
tube_actor.GetProperty().SetOpacity(0.5)

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.AddActor(line_actor)
renderer.AddActor(tube_actor)
renderer.SetBackground(dark_slate_gray_rgb)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(640, 480)
render_window.SetWindowName("TubeFilter")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window.Render()
render_window_interactor.Start()
