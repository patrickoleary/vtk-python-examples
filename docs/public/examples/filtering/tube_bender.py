#!/usr/bin/env python

# Demonstrate vtkTubeBender to smooth bends in a tube created from a
# polyline with sharp turns.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkCommonCore import vtkPoints
from vtkmodules.vtkCommonDataModel import vtkCellArray, vtkPolyData
from vtkmodules.vtkFiltersCore import vtkTubeFilter
from vtkmodules.vtkFiltersCore import vtkTubeBender
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
cornflower_blue_rgb = (0.392, 0.584, 0.929)
slate_gray_rgb = (0.439, 0.502, 0.565)

# Build a polyline with sharp bends
points = vtkPoints()
points.InsertNextPoint(0, 0, 0)
points.InsertNextPoint(1, 0, 0)
points.InsertNextPoint(1, 1, 0)
points.InsertNextPoint(2, 1, 0)
points.InsertNextPoint(2, 2, 0)
points.InsertNextPoint(3, 2, 0)

lines = vtkCellArray()
lines.InsertNextCell(6)
for i in range(6):
    lines.InsertCellPoint(i)

polyline = vtkPolyData()
polyline.SetPoints(points)
polyline.SetLines(lines)

# Filter: smooth the bends in the polyline
tube_bender = vtkTubeBender()
tube_bender.SetInputData(polyline)
tube_bender.SetRadius(0.15)

# Filter: generate tube geometry from the smoothed polyline
tube_filter = vtkTubeFilter()
tube_filter.SetInputConnection(tube_bender.GetOutputPort())
tube_filter.SetRadius(0.15)
tube_filter.SetNumberOfSides(20)

# Mapper: map the tube to graphics primitives
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(tube_filter.GetOutputPort())

# Actor: assign the mapped geometry
actor = vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetColor(cornflower_blue_rgb)

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(slate_gray_rgb)

# Render window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("tube bender")
render_window.SetMultiSamples(0)
render_window.SetSize(640, 480)

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Scene: configure the camera
renderer.ResetCamera()

# Start: launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
