#!/usr/bin/env python

# Demonstrate vtkUnsignedDistance by generating random points, computing
# an unsigned distance field, and extracting an isosurface with
# vtkFlyingEdges3D.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import (
    vtkMath,
    vtkPoints,
)
from vtkmodules.vtkCommonDataModel import vtkPolyData
from vtkmodules.vtkCommonSystem import vtkTimerLog
from vtkmodules.vtkFiltersCore import vtkFlyingEdges3D
from vtkmodules.vtkFiltersModeling import vtkOutlineFilter
from vtkmodules.vtkFiltersPoints import vtkUnsignedDistance
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Parameters
n_pts = 100
math = vtkMath()
math.RandomSeed(31415)
res = 50

# Create random points
poly_data = vtkPolyData()
point_positions = vtkPoints()
point_positions.SetDataTypeToFloat()
point_positions.SetNumberOfPoints(n_pts)
for i in range(0, n_pts):
    point_positions.SetPoint(i, math.Random(-1, 1), math.Random(-1, 1), math.Random(-1, 1))
poly_data.SetPoints(point_positions)

# Generate unsigned distance field
unsigned_distance = vtkUnsignedDistance()
unsigned_distance.SetInputData(poly_data)
unsigned_distance.SetRadius(0.25)
unsigned_distance.SetDimensions(res, res, res)
unsigned_distance.CappingOn()
unsigned_distance.AdjustBoundsOn()
unsigned_distance.SetAdjustDistance(0.01)

# Extract isosurface
flying_edges = vtkFlyingEdges3D()
flying_edges.SetInputConnection(unsigned_distance.GetOutputPort())
flying_edges.SetValue(0, 0.075)
flying_edges.ComputeNormalsOff()

timer = vtkTimerLog()
timer.StartTimer()
flying_edges.Update()
timer.StopTimer()
print("Points processed: {0}".format(n_pts))
print("   Time to generate and extract distance function: {0}".format(timer.GetElapsedTime()))
print(unsigned_distance)

surface_mapper = vtkPolyDataMapper()
surface_mapper.SetInputConnection(flying_edges.GetOutputPort())

surface_actor = vtkActor()
surface_actor.SetMapper(surface_mapper)

# Outline
outline = vtkOutlineFilter()
outline.SetInputConnection(flying_edges.GetOutputPort())

outline_mapper = vtkPolyDataMapper()
outline_mapper.SetInputConnection(outline.GetOutputPort())

outline_actor = vtkActor()
outline_actor.SetMapper(outline_mapper)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(surface_actor)
renderer.AddActor(outline_actor)
renderer.SetBackground(0.1, 0.2, 0.4)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(250, 250)
render_window.SetWindowName("unsigned distance filter")

# Scene
camera = renderer.GetActiveCamera()
camera.SetFocalPoint(1, -1, -1)
camera.SetPosition(0, 0, 0)
renderer.ResetCamera()

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
