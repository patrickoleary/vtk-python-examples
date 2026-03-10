#!/usr/bin/env python

# Create a bottle by rotationally extruding a hand-built profile polyline.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkCommonCore import vtkPoints
from vtkmodules.vtkCommonDataModel import (
    vtkCellArray,
    vtkPolyData,
)
from vtkmodules.vtkFiltersCore import (
    vtkStripper,
    vtkTubeFilter,
)
from vtkmodules.vtkFiltersModeling import vtkRotationalExtrusionFilter
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
burlywood_background_rgb = (0.871, 0.722, 0.529)
mint_rgb = (0.741, 0.988, 0.788)
tomato_rgb = (1.000, 0.388, 0.278)

# Source: define the bottle profile as a polyline
points = vtkPoints()
points.InsertPoint(0, 0.01, 0.0, 0.0)
points.InsertPoint(1, 1.5, 0.0, 0.0)
points.InsertPoint(2, 1.5, 0.0, 3.5)
points.InsertPoint(3, 1.25, 0.0, 3.75)
points.InsertPoint(4, 0.75, 0.0, 4.00)
points.InsertPoint(5, 0.6, 0.0, 4.35)
points.InsertPoint(6, 0.7, 0.0, 4.65)
points.InsertPoint(7, 1.0, 0.0, 4.75)
points.InsertPoint(8, 1.0, 0.0, 5.0)
points.InsertPoint(9, 0.2, 0.0, 5.0)

lines = vtkCellArray()
lines.InsertNextCell(10)
lines.InsertCellPoint(0)
lines.InsertCellPoint(1)
lines.InsertCellPoint(2)
lines.InsertCellPoint(3)
lines.InsertCellPoint(4)
lines.InsertCellPoint(5)
lines.InsertCellPoint(6)
lines.InsertCellPoint(7)
lines.InsertCellPoint(8)
lines.InsertCellPoint(9)

profile = vtkPolyData()
profile.SetPoints(points)
profile.SetLines(lines)

# Filter: rotationally extrude the profile to form the bottle surface
extrude = vtkRotationalExtrusionFilter()
extrude.SetInputData(profile)
extrude.SetResolution(60)

# Mapper: map the extruded bottle surface
bottle_mapper = vtkPolyDataMapper()
bottle_mapper.SetInputConnection(extrude.GetOutputPort())

# Actor: the bottle surface
bottle_actor = vtkActor()
bottle_actor.SetMapper(bottle_mapper)
bottle_actor.GetProperty().SetColor(mint_rgb)

# Filter: display the original profile as a tube
stripper = vtkStripper()
stripper.SetInputData(profile)

tubes = vtkTubeFilter()
tubes.SetInputConnection(stripper.GetOutputPort())
tubes.SetNumberOfSides(11)
tubes.SetRadius(0.05)

# Mapper: map the profile tube
profile_mapper = vtkPolyDataMapper()
profile_mapper.SetInputConnection(tubes.GetOutputPort())

# Actor: the profile tube
profile_actor = vtkActor()
profile_actor.SetMapper(profile_mapper)
profile_actor.GetProperty().SetColor(tomato_rgb)

# Renderer: assemble the scene and configure the camera
renderer = vtkRenderer()
renderer.AddActor(bottle_actor)
renderer.AddActor(profile_actor)
renderer.SetBackground(burlywood_background_rgb)
renderer.GetActiveCamera().SetPosition(1, 0, 0)
renderer.GetActiveCamera().SetFocalPoint(0, 0, 0)
renderer.GetActiveCamera().SetViewUp(0, 0, 1)
renderer.ResetCamera()
renderer.GetActiveCamera().Azimuth(30)
renderer.GetActiveCamera().Elevation(30)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(640, 480)
render_window.SetWindowName("Bottle")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
