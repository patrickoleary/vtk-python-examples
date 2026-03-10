#!/usr/bin/env python

# Cut a sphere with multiple planes and display the resulting polylines
# using vtkCutter and vtkStripper.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkCommonDataModel import vtkPlane
from vtkmodules.vtkFiltersCore import (
    vtkCutter,
    vtkStripper,
)
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
peacock_rgb = (0.200, 0.631, 0.788)
silver_rgb = (0.753, 0.753, 0.753)
wheat_rgb = (0.961, 0.871, 0.702)

# Source: sphere
sphere_source = vtkSphereSource()

# Filter: cut with a plane at 10 evenly spaced positions
plane = vtkPlane()

cutter = vtkCutter()
cutter.SetInputConnection(sphere_source.GetOutputPort())
cutter.SetCutFunction(plane)
cutter.GenerateValues(10, -0.5, 0.5)

# Mapper & Actor: map sphere surface to graphics primitives
model_mapper = vtkPolyDataMapper()
model_mapper.SetInputConnection(sphere_source.GetOutputPort())

model_actor = vtkActor()
model_actor.SetMapper(model_mapper)
model_actor.GetProperty().SetDiffuseColor(silver_rgb)
model_actor.GetProperty().SetInterpolationToFlat()

# Filter: join cut segments into contiguous polylines
stripper = vtkStripper()
stripper.SetInputConnection(cutter.GetOutputPort())
stripper.JoinContiguousSegmentsOn()

# Mapper & Actor: map cut lines to graphics primitives
lines_mapper = vtkPolyDataMapper()
lines_mapper.SetInputConnection(stripper.GetOutputPort())

lines_actor = vtkActor()
lines_actor.SetMapper(lines_mapper)
lines_actor.GetProperty().SetDiffuseColor(peacock_rgb)
lines_actor.GetProperty().SetLineWidth(3.0)

# Renderer: assemble the scene and configure the camera
renderer = vtkRenderer()
renderer.AddActor(model_actor)
renderer.AddActor(lines_actor)
renderer.SetBackground(wheat_rgb)
renderer.GetActiveCamera().Azimuth(-45)
renderer.GetActiveCamera().Elevation(-22.5)
renderer.ResetCamera()

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(640, 480)
render_window.SetWindowName("ExtractPolyLinesFromPolyData")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window.Render()
render_window_interactor.Start()
