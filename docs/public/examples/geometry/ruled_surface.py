#!/usr/bin/env python

# Demonstrate vtkRuledSurfaceFilter by creating a room profile polyline,
# transforming it, appending both profiles, and generating a ruled surface
# between them using resample mode.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import vtkPoints
from vtkmodules.vtkCommonDataModel import vtkCellArray, vtkPolyData
from vtkmodules.vtkCommonTransforms import vtkTransform
from vtkmodules.vtkFiltersCore import vtkAppendPolyData
from vtkmodules.vtkFiltersGeneral import vtkTransformPolyDataFilter
from vtkmodules.vtkFiltersModeling import vtkRuledSurfaceFilter
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Create room profile polyline
points = vtkPoints()
points.InsertPoint(0, 0, 0, 0)
points.InsertPoint(1, 1, 0, 0)
points.InsertPoint(2, 1, 1, 0)
points.InsertPoint(3, 2, 1, 0)

lines = vtkCellArray()
lines.InsertNextCell(4)
lines.InsertCellPoint(0)
lines.InsertCellPoint(1)
lines.InsertCellPoint(2)
lines.InsertCellPoint(3)

profile = vtkPolyData()
profile.SetPoints(points)
profile.SetLines(lines)

# Transform the profile
transform = vtkTransform()
transform.Translate(0, 0, 8)
transform.RotateZ(90)

transform_filter = vtkTransformPolyDataFilter()
transform_filter.SetInputData(profile)
transform_filter.SetTransform(transform)

# Append original and transformed profiles
append_filter = vtkAppendPolyData()
append_filter.AddInputData(profile)
append_filter.AddInputConnection(transform_filter.GetOutputPort())

# Generate ruled surface between the two profiles
extrude = vtkRuledSurfaceFilter()
extrude.SetInputConnection(append_filter.GetOutputPort())
extrude.SetResolution(51, 51)
extrude.SetRuledModeToResample()

mapper = vtkPolyDataMapper()
mapper.SetInputConnection(extrude.GetOutputPort())

wall = vtkActor()
wall.SetMapper(mapper)
wall.GetProperty().SetColor(0.3800, 0.7000, 0.1600)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(wall)
renderer.SetBackground(1, 1, 1)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(200, 200)
render_window.SetWindowName("ruled surface")

# Scene
renderer.GetActiveCamera().SetPosition(12.9841, -1.81551, 8.82706)
renderer.GetActiveCamera().SetFocalPoint(0.5, 1, 4)
renderer.GetActiveCamera().SetViewAngle(30)
renderer.GetActiveCamera().SetViewUp(0.128644, -0.675064, -0.726456)
renderer.GetActiveCamera().SetClippingRange(7.59758, 21.3643)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
