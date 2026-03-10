#!/usr/bin/env python

# Displace a polyline by per-point vectors using vtkWarpVector.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkCommonCore import (
    vtkDoubleArray,
    vtkPoints,
)
from vtkmodules.vtkCommonDataModel import (
    vtkCellArray,
    vtkLine,
    vtkPolyData,
)
from vtkmodules.vtkFiltersGeneral import vtkWarpVector
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
cobalt_green_rgb = (0.239, 0.557, 0.251)

# Source: five points along the x-axis connected by line segments
points = vtkPoints()
points.InsertNextPoint(0.0, 0.0, 0.0)
points.InsertNextPoint(1.0, 0.0, 0.0)
points.InsertNextPoint(2.0, 0.0, 0.0)
points.InsertNextPoint(3.0, 0.0, 0.0)
points.InsertNextPoint(4.0, 0.0, 0.0)

lines = vtkCellArray()
line = vtkLine()
line.GetPointIds().SetId(0, 0)
line.GetPointIds().SetId(1, 1)
lines.InsertNextCell(line)
line.GetPointIds().SetId(0, 1)
line.GetPointIds().SetId(1, 2)
lines.InsertNextCell(line)
line.GetPointIds().SetId(0, 2)
line.GetPointIds().SetId(1, 3)
lines.InsertNextCell(line)
line.GetPointIds().SetId(0, 3)
line.GetPointIds().SetId(1, 4)
lines.InsertNextCell(line)

# Per-point displacement vectors (y-component only)
warp_data = vtkDoubleArray()
warp_data.SetNumberOfComponents(3)
warp_data.SetName("warpData")
warp_data.InsertNextTuple3(0.0, 0.0, 0.0)
warp_data.InsertNextTuple3(0.0, 0.1, 0.0)
warp_data.InsertNextTuple3(0.0, 0.3, 0.0)
warp_data.InsertNextTuple3(0.0, 0.0, 0.0)
warp_data.InsertNextTuple3(0.0, 0.1, 0.0)

polydata = vtkPolyData()
polydata.SetPoints(points)
polydata.SetLines(lines)
polydata.GetPointData().AddArray(warp_data)
polydata.GetPointData().SetActiveVectors(warp_data.GetName())

# Filter: displace points by their vector attribute
warp_vector = vtkWarpVector()
warp_vector.SetInputData(polydata)
warp_vector.Update()

# Mapper & Actor: map warped polyline to graphics primitives
mapper = vtkPolyDataMapper()
mapper.SetInputData(warp_vector.GetPolyDataOutput())

actor = vtkActor()
actor.SetMapper(mapper)

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(cobalt_green_rgb)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(640, 480)
render_window.SetWindowName("WarpVector")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window.Render()
render_window_interactor.Start()
