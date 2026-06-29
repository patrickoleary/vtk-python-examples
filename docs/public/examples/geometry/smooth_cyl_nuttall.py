#!/usr/bin/env python

# Demonstrate vtkWindowedSincPolyDataFilter comparing Hamming vs Nuttall
# window functions side-by-side on a semi-cylinder created via
# vtkRotationalExtrusionFilter, warped with Brownian points.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonColor import vtkNamedColors
from vtkmodules.vtkFiltersCore import vtkPolyDataNormals, vtkWindowedSincPolyDataFilter
from vtkmodules.vtkFiltersGeneral import vtkBrownianPoints, vtkWarpVector
from vtkmodules.vtkFiltersModeling import vtkRotationalExtrusionFilter
from vtkmodules.vtkFiltersSources import vtkLineSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkCamera,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

named_colors = vtkNamedColors()
tomato_rgb = [0.0, 0.0, 0.0]
named_colors.GetColorRGB("tomato", tomato_rgb)
beige_rgb = [0.0, 0.0, 0.0]
named_colors.GetColorRGB("beige", beige_rgb)

# Hamming window pipeline
line_0 = vtkLineSource()
line_0.SetPoint1(0, 1, 0)
line_0.SetPoint2(0, 1, 2)
line_0.SetResolution(50)

line_sweeper_0 = vtkRotationalExtrusionFilter()
line_sweeper_0.SetResolution(100)
line_sweeper_0.SetInputConnection(line_0.GetOutputPort())
line_sweeper_0.SetAngle(270)

bump_0 = vtkBrownianPoints()
bump_0.SetInputConnection(line_sweeper_0.GetOutputPort())

warp_0 = vtkWarpVector()
warp_0.SetInputConnection(bump_0.GetOutputPort())
warp_0.SetScaleFactor(0.005)

smooth_0 = vtkWindowedSincPolyDataFilter()
smooth_0.SetInputConnection(warp_0.GetOutputPort())
smooth_0.SetNumberOfIterations(20)
smooth_0.BoundarySmoothingOn()
smooth_0.SetFeatureAngle(120)
smooth_0.SetEdgeAngle(90)
smooth_0.SetPassBand(0.1)
smooth_0.SetWindowFunction(vtkWindowedSincPolyDataFilter.HAMMING)

normals_0 = vtkPolyDataNormals()
normals_0.SetInputConnection(smooth_0.GetOutputPort())

# Nuttall window pipeline
line_1 = vtkLineSource()
line_1.SetPoint1(0, 1, 0)
line_1.SetPoint2(0, 1, 2)
line_1.SetResolution(50)

line_sweeper_1 = vtkRotationalExtrusionFilter()
line_sweeper_1.SetResolution(100)
line_sweeper_1.SetInputConnection(line_1.GetOutputPort())
line_sweeper_1.SetAngle(270)

bump_1 = vtkBrownianPoints()
bump_1.SetInputConnection(line_sweeper_1.GetOutputPort())

warp_1 = vtkWarpVector()
warp_1.SetInputConnection(bump_1.GetOutputPort())
warp_1.SetScaleFactor(0.005)

smooth_1 = vtkWindowedSincPolyDataFilter()
smooth_1.SetInputConnection(warp_1.GetOutputPort())
smooth_1.SetNumberOfIterations(20)
smooth_1.BoundarySmoothingOn()
smooth_1.SetFeatureAngle(120)
smooth_1.SetEdgeAngle(90)
smooth_1.SetPassBand(0.1)
smooth_1.SetWindowFunction(vtkWindowedSincPolyDataFilter.NUTTALL)

normals_1 = vtkPolyDataNormals()
normals_1.SetInputConnection(smooth_1.GetOutputPort())

# Mapper and actor pairs
smoothing_output_mapper_0 = vtkPolyDataMapper()
smoothing_output_mapper_0.SetInputConnection(normals_0.GetOutputPort())
smoothing_output_actor_0 = vtkActor()
smoothing_output_actor_0.SetMapper(smoothing_output_mapper_0)
smoothing_output_actor_0.GetProperty().SetInterpolationToGouraud()
smoothing_output_actor_0.GetProperty().SetInterpolationToFlat()
smoothing_output_actor_0.GetProperty().SetColor(tomato_rgb)

smoothing_input_mapper_0 = vtkPolyDataMapper()
smoothing_input_mapper_0.SetInputConnection(warp_0.GetOutputPort())
smoothing_input_actor_0 = vtkActor()
smoothing_input_actor_0.SetMapper(smoothing_input_mapper_0)
smoothing_input_actor_0.GetProperty().SetInterpolationToFlat()

smoothing_output_mapper_1 = vtkPolyDataMapper()
smoothing_output_mapper_1.SetInputConnection(normals_1.GetOutputPort())
smoothing_output_actor_1 = vtkActor()
smoothing_output_actor_1.SetMapper(smoothing_output_mapper_1)
smoothing_output_actor_1.GetProperty().SetInterpolationToGouraud()
smoothing_output_actor_1.GetProperty().SetInterpolationToFlat()
smoothing_output_actor_1.GetProperty().SetColor(tomato_rgb)

smoothing_input_mapper_1 = vtkPolyDataMapper()
smoothing_input_mapper_1.SetInputConnection(warp_1.GetOutputPort())
smoothing_input_actor_1 = vtkActor()
smoothing_input_actor_1.SetMapper(smoothing_input_mapper_1)
smoothing_input_actor_1.GetProperty().SetInterpolationToFlat()

# Renderers
renderer_0 = vtkRenderer()
renderer_0.SetViewport(0, 0, 0.5, 1.0)
renderer_0.AddActor(smoothing_output_actor_0)
renderer_0.AddActor(smoothing_input_actor_0)
renderer_0.SetBackground(1, 1, 1)

renderer_1 = vtkRenderer()
renderer_1.SetViewport(0.5, 0, 1.0, 1.0)
renderer_1.AddActor(smoothing_output_actor_1)
renderer_1.AddActor(smoothing_input_actor_1)
renderer_1.SetBackground(1, 1, 1)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer_0)
render_window.AddRenderer(renderer_1)
render_window.SetSize(300, 150)
render_window.SetWindowName("smooth cyl nuttall")

# Scene
camera_0 = vtkCamera()
camera_0.SetClippingRange(0.576398, 28.8199)
camera_0.SetFocalPoint(0.0463079, -0.0356571, 1.01993)
camera_0.SetPosition(-2.47044, 2.39516, -3.56066)
camera_0.SetViewUp(0.607296, -0.513537, -0.606195)
renderer_0.SetActiveCamera(camera_0)

camera_1 = vtkCamera()
camera_1.SetClippingRange(0.576398, 28.8199)
camera_1.SetFocalPoint(0.0463079, -0.0356571, 1.01993)
camera_1.SetPosition(-2.47044, 2.39516, -3.56066)
camera_1.SetViewUp(0.607296, -0.513537, -0.606195)
renderer_1.SetActiveCamera(camera_1)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
