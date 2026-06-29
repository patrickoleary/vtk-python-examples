#!/usr/bin/env python

# Demonstrate vtkRuledSurfaceFilter by cutting a sphere with a plane,
# stripping the cut lines, appending a tip point, and generating a ruled
# surface using point walk mode.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import vtkPoints
from vtkmodules.vtkCommonDataModel import vtkCellArray, vtkPlane, vtkPolyData
from vtkmodules.vtkFiltersCore import (
    vtkAppendPolyData,
    vtkCleanPolyData,
    vtkCutter,
    vtkStripper,
)
from vtkmodules.vtkFiltersModeling import vtkRuledSurfaceFilter
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Sphere source
sphere = vtkSphereSource()
sphere.SetPhiResolution(15)
sphere.SetThetaResolution(30)

# Cut plane
plane = vtkPlane()
plane.SetNormal(1, 0, 0)

cut = vtkCutter()
cut.SetInputConnection(sphere.GetOutputPort())
cut.SetCutFunction(plane)
cut.GenerateCutScalarsOn()

# Strip cut lines
strip = vtkStripper()
strip.SetInputConnection(cut.GetOutputPort())

# Create a tip point
tip_points = vtkPoints()
tip_points.InsertPoint(0, 1, 0, 0)

tip_lines = vtkCellArray()
tip_lines.InsertNextCell(2)
tip_lines.InsertCellPoint(0)
tip_lines.InsertCellPoint(0)

tip = vtkPolyData()
tip.SetPoints(tip_points)
tip.SetLines(tip_lines)

# Append strip and tip
append_filter = vtkAppendPolyData()
append_filter.AddInputConnection(strip.GetOutputPort())
append_filter.AddInputData(tip)

# Generate ruled surface (point walk mode)
extrude = vtkRuledSurfaceFilter()
extrude.SetInputConnection(append_filter.GetOutputPort())
extrude.SetRuledModeToPointWalk()

# Clean up
clean = vtkCleanPolyData()
clean.SetInputConnection(extrude.GetOutputPort())
clean.ConvertPolysToLinesOff()

mapper = vtkPolyDataMapper()
mapper.SetInputConnection(clean.GetOutputPort())
mapper.ScalarVisibilityOff()

actor = vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetOpacity(0.4)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(0.1, 0.2, 0.4)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(200, 200)
render_window.SetWindowName("ruled surface sphere cut")

# Scene
renderer.ResetCamera()

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
