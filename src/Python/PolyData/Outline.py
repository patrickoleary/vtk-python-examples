#!/usr/bin/env python

# Display a cone with an axis-aligned bounding-box outline using vtkOutlineFilter.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkFiltersModeling import vtkOutlineFilter
from vtkmodules.vtkFiltersSources import vtkConeSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
misty_rose_rgb = (1.000, 0.894, 0.882)
gold_rgb = (1.000, 0.843, 0.000)
midnight_blue_rgb = (0.098, 0.098, 0.439)

# Source: high-resolution cone
cone_source = vtkConeSource()
cone_source.SetCenter(0, 0, 0)
cone_source.SetResolution(100)

# Mapper & Actor: map cone surface to graphics primitives
cone_mapper = vtkPolyDataMapper()
cone_mapper.SetInputConnection(cone_source.GetOutputPort())

cone_actor = vtkActor()
cone_actor.SetMapper(cone_mapper)
cone_actor.GetProperty().SetColor(misty_rose_rgb)

# Filter: bounding-box outline
outline = vtkOutlineFilter()
outline.SetInputConnection(cone_source.GetOutputPort())

# Mapper & Actor: map outline wireframe to graphics primitives
outline_mapper = vtkPolyDataMapper()
outline_mapper.SetInputConnection(outline.GetOutputPort())

outline_actor = vtkActor()
outline_actor.SetMapper(outline_mapper)
outline_actor.GetProperty().SetColor(gold_rgb)

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.AddActor(cone_actor)
renderer.AddActor(outline_actor)
renderer.SetBackground(midnight_blue_rgb)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(640, 480)
render_window.SetWindowName("Outline")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window.Render()
render_window_interactor.Start()
