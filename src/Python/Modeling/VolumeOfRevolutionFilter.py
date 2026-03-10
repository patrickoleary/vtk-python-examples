#!/usr/bin/env python

# Demonstrate vtkVolumeOfRevolutionFilter to revolve a 2D polyline profile
# around the Y axis, creating a vase-like 3D solid.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkCommonCore import vtkPoints
from vtkmodules.vtkCommonDataModel import vtkCellArray, vtkPolyData
from vtkmodules.vtkFiltersGeometry import vtkDataSetSurfaceFilter
from vtkmodules.vtkFiltersModeling import vtkVolumeOfRevolutionFilter
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

# Build a 2D profile (vase cross-section) as a polyline
points = vtkPoints()
points.InsertNextPoint(0.5, 0.0, 0)
points.InsertNextPoint(0.8, 0.5, 0)
points.InsertNextPoint(0.6, 1.0, 0)
points.InsertNextPoint(0.4, 1.5, 0)
points.InsertNextPoint(0.7, 2.0, 0)
points.InsertNextPoint(0.9, 2.5, 0)
points.InsertNextPoint(0.8, 3.0, 0)

lines = vtkCellArray()
lines.InsertNextCell(7)
for i in range(7):
    lines.InsertCellPoint(i)

profile = vtkPolyData()
profile.SetPoints(points)
profile.SetLines(lines)

# Filter: revolve the profile 360 degrees around the Y axis
revolution = vtkVolumeOfRevolutionFilter()
revolution.SetInputData(profile)
revolution.SetResolution(64)
revolution.SetAxisDirection(0, 1, 0)

# Filter: extract surface geometry from the unstructured grid output
surface = vtkDataSetSurfaceFilter()
surface.SetInputConnection(revolution.GetOutputPort())

# Mapper: map the surface to graphics primitives
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(surface.GetOutputPort())

# Actor: assign the mapped geometry
actor = vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetColor(cornflower_blue_rgb)

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(slate_gray_rgb)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(640, 480)
render_window.SetWindowName("VolumeOfRevolutionFilter")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
