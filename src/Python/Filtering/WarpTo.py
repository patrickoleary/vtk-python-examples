#!/usr/bin/env python

# Create a tube around a line, then warp the geometry toward a target
# point using vtkWarpTo to demonstrate geometric deformation.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkFiltersCore import vtkTubeFilter
from vtkmodules.vtkFiltersGeneral import vtkWarpTo
from vtkmodules.vtkFiltersSources import vtkLineSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkDataSetMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
gold_rgb = (1.0, 0.843, 0.0)
green_rgb = (0.0, 0.5, 0.0)

# Source: generate a vertical line from (0,0,0) to (0,1,0)
line_source = vtkLineSource()
line_source.SetPoint1(0.0, 0.0, 0.0)
line_source.SetPoint2(0.0, 1.0, 0.0)
line_source.SetResolution(20)

# Filter: wrap a tube (cylinder) around the line
tube_filter = vtkTubeFilter()
tube_filter.SetInputConnection(line_source.GetOutputPort())
tube_filter.SetRadius(0.01)
tube_filter.SetNumberOfSides(50)

# Filter: warp the tube geometry toward a target point
warp_to = vtkWarpTo()
warp_to.SetInputConnection(tube_filter.GetOutputPort())
warp_to.SetPosition(10, 1, 0)
warp_to.SetScaleFactor(5)
warp_to.AbsoluteOn()

# Mapper: map the warped geometry to graphics primitives
mapper = vtkDataSetMapper()
mapper.SetInputConnection(warp_to.GetOutputPort())
mapper.ScalarVisibilityOff()

# Actor: assign the mapped geometry
actor = vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetColor(gold_rgb)

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(green_rgb)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(640, 480)
render_window.SetWindowName("WarpTo")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
