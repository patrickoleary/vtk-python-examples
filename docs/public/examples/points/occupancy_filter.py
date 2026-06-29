#!/usr/bin/env python

# Demonstrate vtkPointOccupancyFilter and vtkMaskPointsFilter by creating
# nine extreme points, generating an occupancy mask volume, thresholding
# occupied voxels, and rendering the surface.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import (
    vtkMath,
    vtkPoints,
)
from vtkmodules.vtkCommonDataModel import vtkPolyData
from vtkmodules.vtkFiltersCore import vtkThreshold
from vtkmodules.vtkFiltersModeling import vtkOutlineFilter
from vtkmodules.vtkFiltersPoints import (
    vtkMaskPointsFilter,
    vtkPointOccupancyFilter,
)
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkDataSetMapper,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Parameters
res = 15
math = vtkMath()
math.RandomSeed(31415)

# Nine extreme points
point_positions = vtkPoints()
point_positions.SetNumberOfPoints(9)
point_positions.SetPoint(0, 0, 0, 0)
point_positions.SetPoint(1, -1, -1, -1)
point_positions.SetPoint(2, 1, -1, -1)
point_positions.SetPoint(3, -1, 1, -1)
point_positions.SetPoint(4, 1, 1, -1)
point_positions.SetPoint(5, -1, -1, 1)
point_positions.SetPoint(6, 1, -1, 1)
point_positions.SetPoint(7, -1, 1, 1)
point_positions.SetPoint(8, 1, 1, 1)

point_data = vtkPolyData()
point_data.SetPoints(point_positions)

# Generate occupancy mask
occupancy_filter = vtkPointOccupancyFilter()
occupancy_filter.SetInputData(point_data)
occupancy_filter.SetSampleDimensions(res, res + 2, res + 4)
occupancy_filter.SetOccupiedValue(255)

# Outline
outline = vtkOutlineFilter()
outline.SetInputConnection(occupancy_filter.GetOutputPort())

outline_mapper = vtkPolyDataMapper()
outline_mapper.SetInputConnection(outline.GetOutputPort())

outline_actor = vtkActor()
outline_actor.SetMapper(outline_mapper)

# Threshold to show occupied voxels
surface = vtkThreshold()
surface.SetInputConnection(occupancy_filter.GetOutputPort())
surface.SetThresholdFunction(vtkThreshold.THRESHOLD_UPPER)
surface.SetUpperThreshold(1.0)
surface.AllScalarsOff()

surface_mapper = vtkDataSetMapper()
surface_mapper.SetInputConnection(surface.GetOutputPort())
surface_mapper.ScalarVisibilityOff()

surface_actor = vtkActor()
surface_actor.SetMapper(surface_mapper)

# Mask points filter
mask_points = vtkMaskPointsFilter()
mask_points.SetInputData(point_data)
mask_points.SetMaskConnection(occupancy_filter.GetOutputPort())
mask_points.GenerateVerticesOn()

points_mapper = vtkPolyDataMapper()
points_mapper.SetInputConnection(mask_points.GetOutputPort())

points_actor = vtkActor()
points_actor.SetMapper(points_mapper)
points_actor.GetProperty().SetPointSize(3)
points_actor.GetProperty().SetColor(0, 1, 0)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(surface_actor)
renderer.SetBackground(0, 0, 0)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(300, 300)
render_window.SetWindowName("occupancy filter")

# Scene
camera = renderer.GetActiveCamera()
camera.SetFocalPoint(0, 0, 0)
camera.SetPosition(1, 1, 1)
renderer.ResetCamera()

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
