#!/usr/bin/env python

# Demonstrate vtkPointSource with exponential distribution by creating
# nine point sources with varying lambda values, appending them, and
# rendering the combined point cloud.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersCore import vtkAppendPolyData
from vtkmodules.vtkFiltersSources import vtkPointSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

num_pts = 1000
radius = 0.5

point_source_0 = vtkPointSource()
point_source_0.SetDistributionToExponential()
point_source_0.SetCenter(-1, -1, -1)
point_source_0.SetRadius(radius)
point_source_0.SetNumberOfPoints(num_pts)
point_source_0.SetLambda(0.1)

point_source_1 = vtkPointSource()
point_source_1.SetDistributionToExponential()
point_source_1.SetCenter(1, -1, -1)
point_source_1.SetRadius(radius)
point_source_1.SetNumberOfPoints(num_pts)
point_source_1.SetLambda(-10)

point_source_2 = vtkPointSource()
point_source_2.SetDistributionToExponential()
point_source_2.SetCenter(1, 1, -1)
point_source_2.SetRadius(radius)
point_source_2.SetNumberOfPoints(num_pts)
point_source_2.SetLambda(0.6)

point_source_3 = vtkPointSource()
point_source_3.SetDistributionToExponential()
point_source_3.SetCenter(-1, 1, -1)
point_source_3.SetRadius(radius)
point_source_3.SetNumberOfPoints(num_pts)
point_source_3.SetLambda(0.8)

point_source_4 = vtkPointSource()
point_source_4.SetDistributionToExponential()
point_source_4.SetCenter(0, 0, 0)
point_source_4.SetRadius(radius)
point_source_4.SetNumberOfPoints(num_pts)
point_source_4.SetLambda(1.0)

point_source_5 = vtkPointSource()
point_source_5.SetDistributionToExponential()
point_source_5.SetCenter(-1, -1, 1)
point_source_5.SetRadius(radius)
point_source_5.SetNumberOfPoints(num_pts)
point_source_5.SetLambda(2)

point_source_6 = vtkPointSource()
point_source_6.SetDistributionToExponential()
point_source_6.SetCenter(1, -1, 1)
point_source_6.SetRadius(radius)
point_source_6.SetNumberOfPoints(num_pts)
point_source_6.SetLambda(4)

point_source_7 = vtkPointSource()
point_source_7.SetDistributionToExponential()
point_source_7.SetCenter(1, 1, 1)
point_source_7.SetRadius(radius)
point_source_7.SetNumberOfPoints(num_pts)
point_source_7.SetLambda(6)

point_source_8 = vtkPointSource()
point_source_8.SetDistributionToExponential()
point_source_8.SetCenter(-1, 1, 1)
point_source_8.SetRadius(radius)
point_source_8.SetNumberOfPoints(num_pts)
point_source_8.SetLambda(10)

# Append selected point sources (skip point_source_0 and point_source_7 which are along
# the camera view vector and clutter the display)
append_filter = vtkAppendPolyData()
append_filter.AddInputConnection(point_source_1.GetOutputPort())
append_filter.AddInputConnection(point_source_2.GetOutputPort())
append_filter.AddInputConnection(point_source_3.GetOutputPort())
append_filter.AddInputConnection(point_source_4.GetOutputPort())
append_filter.AddInputConnection(point_source_5.GetOutputPort())
append_filter.AddInputConnection(point_source_6.GetOutputPort())
append_filter.AddInputConnection(point_source_8.GetOutputPort())

mapper = vtkPolyDataMapper()
mapper.SetInputConnection(append_filter.GetOutputPort())

actor = vtkActor()
actor.SetMapper(mapper)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(0, 0, 0)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(300, 300)
render_window.SetWindowName("exponential point source")

# Scene
renderer.GetActiveCamera().SetPosition(1, 1, 1)
renderer.ResetCamera()

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
