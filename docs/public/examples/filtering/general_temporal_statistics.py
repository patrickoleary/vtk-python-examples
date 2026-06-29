#!/usr/bin/env python

# Visualize temporal statistics by generating scalar data over multiple
# time steps and displaying the average, minimum, and maximum as colored
# bars side by side.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersSources import vtkPlaneSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
    vtkTextActor,
)

# Simulate temporal statistics results:
# For a scalar that goes 0..19 over 20 time steps:
# average = 9.5, minimum = 0, maximum = 19
ts = list(range(20))
avg_val = sum(ts) / len(ts)
min_val = float(min(ts))
max_val = float(max(ts))

# Average bar
bar_avg = vtkPlaneSource()
bar_avg.SetOrigin(0.0, 0, 0)
bar_avg.SetPoint1(1.5, 0, 0)
bar_avg.SetPoint2(0.0, avg_val, 0)

bar_avg_mapper = vtkPolyDataMapper()
bar_avg_mapper.SetInputConnection(bar_avg.GetOutputPort())

bar_avg_actor = vtkActor()
bar_avg_actor.SetMapper(bar_avg_mapper)
bar_avg_actor.GetProperty().SetColor(0.3, 0.8, 0.3)

# Minimum bar
bar_min = vtkPlaneSource()
bar_min.SetOrigin(2.0, 0, 0)
bar_min.SetPoint1(3.5, 0, 0)
bar_min.SetPoint2(2.0, min_val, 0)

bar_min_mapper = vtkPolyDataMapper()
bar_min_mapper.SetInputConnection(bar_min.GetOutputPort())

bar_min_actor = vtkActor()
bar_min_actor.SetMapper(bar_min_mapper)
bar_min_actor.GetProperty().SetColor(0.3, 0.3, 1.0)

# Maximum bar
bar_max = vtkPlaneSource()
bar_max.SetOrigin(4.0, 0, 0)
bar_max.SetPoint1(5.5, 0, 0)
bar_max.SetPoint2(4.0, max_val, 0)

bar_max_mapper = vtkPolyDataMapper()
bar_max_mapper.SetInputConnection(bar_max.GetOutputPort())

bar_max_actor = vtkActor()
bar_max_actor.SetMapper(bar_max_mapper)
bar_max_actor.GetProperty().SetColor(1.0, 0.3, 0.3)

# Labels
label = vtkTextActor()
label.SetInput("Temporal Statistics: Avg=%.1f  Min=%.0f  Max=%.0f" % (avg_val, min_val, max_val))
label.GetTextProperty().SetFontSize(14)
label.GetTextProperty().SetColor(1, 1, 1)
label.SetPosition(10, 10)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(bar_avg_actor)
renderer.AddActor(bar_min_actor)
renderer.AddActor(bar_max_actor)
renderer.AddViewProp(label)
renderer.SetBackground(0.1, 0.2, 0.4)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(400, 300)
render_window.SetWindowName("general temporal statistics")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.ResetCamera()

interactor.Initialize()
interactor.Start()
