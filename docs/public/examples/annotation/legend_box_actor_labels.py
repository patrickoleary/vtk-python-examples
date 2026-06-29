#!/usr/bin/env python

# Test vtkLegendBoxActor with line source entries and colored text.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersSources import vtkLineSource
from vtkmodules.vtkRenderingAnnotation import vtkLegendBoxActor
from vtkmodules.vtkRenderingCore import (
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors
text_colors = [
    [1.0, 0.0, 0.0],
    [0.0, 1.0, 0.0],
    [0.0, 0.0, 1.0],
    [1.0, 0.5, 0.5],
    [0.5, 1.0, 0.5],
]
labels = ["Text1", "Text2", "Text3", "Text4", "Text5"]

# Legend box actor
legend_actor = vtkLegendBoxActor()
legend_actor.SetNumberOfEntries(5)
legend_actor.SetUseBackground(1)
legend_actor.SetBackgroundColor(0.8, 0.5, 0.0)
legend_actor.SetBackgroundOpacity(1.0)

legend_actor.GetPositionCoordinate().SetCoordinateSystemToView()
legend_actor.GetPositionCoordinate().SetValue(-0.7, -0.8)

legend_actor.GetPosition2Coordinate().SetCoordinateSystemToView()
legend_actor.GetPosition2Coordinate().SetValue(0.7, 0.8)

# Entries with line source geometry.
ls_0 = vtkLineSource()
ls_0.Update()
legend_actor.SetEntry(0, ls_0.GetOutput(), labels[0], text_colors[0])

ls_1 = vtkLineSource()
ls_1.Update()
legend_actor.SetEntry(1, ls_1.GetOutput(), labels[1], text_colors[1])

ls_2 = vtkLineSource()
ls_2.Update()
legend_actor.SetEntry(2, ls_2.GetOutput(), labels[2], text_colors[2])

ls_3 = vtkLineSource()
ls_3.Update()
legend_actor.SetEntry(3, ls_3.GetOutput(), labels[3], text_colors[3])

ls_4 = vtkLineSource()
ls_4.Update()
legend_actor.SetEntry(4, ls_4.GetOutput(), labels[4], text_colors[4])

# Renderer
renderer = vtkRenderer()
renderer.AddViewProp(legend_actor)
renderer.SetBackground(0.0, 0.0, 0.0)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("legend box actor labels")
render_window.SetMultiSamples(0)
render_window.SetSize(350, 350)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.GetActiveCamera().ParallelProjectionOn()

interactor.Initialize()
interactor.Start()
