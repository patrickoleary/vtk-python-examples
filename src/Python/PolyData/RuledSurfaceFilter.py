#!/usr/bin/env python

# Generate a ruled surface between two line segments using vtkRuledSurfaceFilter.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkCommonCore import vtkPoints
from vtkmodules.vtkCommonDataModel import (
    vtkCellArray,
    vtkLine,
    vtkPolyData,
)
from vtkmodules.vtkFiltersModeling import vtkRuledSurfaceFilter
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
banana_rgb = (0.890, 0.810, 0.340)
steel_blue_rgb = (0.275, 0.510, 0.706)

# Source: two line segments in 3-D
points = vtkPoints()
points.InsertPoint(0, 0, 0, 1)
points.InsertPoint(1, 1, 0, 0)
points.InsertPoint(2, 0, 1, 0)
points.InsertPoint(3, 1, 1, 1)

line1 = vtkLine()
line1.GetPointIds().SetId(0, 0)
line1.GetPointIds().SetId(1, 1)

line2 = vtkLine()
line2.GetPointIds().SetId(0, 2)
line2.GetPointIds().SetId(1, 3)

lines = vtkCellArray()
lines.InsertNextCell(line1)
lines.InsertNextCell(line2)

polydata = vtkPolyData()
polydata.SetPoints(points)
polydata.SetLines(lines)

# Filter: ruled surface between the two lines
ruled_surface = vtkRuledSurfaceFilter()
ruled_surface.SetInputData(polydata)
ruled_surface.SetResolution(21, 21)
ruled_surface.SetRuledModeToResample()

# Mapper & Actor: map ruled surface to graphics primitives
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(ruled_surface.GetOutputPort())

actor = vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetColor(banana_rgb)
actor.GetProperty().SetSpecular(0.6)
actor.GetProperty().SetSpecularPower(30)

# Renderer: assemble the scene and configure the camera
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(steel_blue_rgb)
renderer.GetActiveCamera().Azimuth(60)
renderer.GetActiveCamera().Elevation(60)
renderer.ResetCamera()

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(640, 480)
render_window.SetWindowName("RuledSurfaceFilter")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window.Render()
render_window_interactor.Start()
