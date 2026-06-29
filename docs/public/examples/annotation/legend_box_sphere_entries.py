#!/usr/bin/env python

# Test vtkLegendBoxActor with sphere source entries and colored text.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersSources import vtkSphereSource
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

# Entries with sphere source geometry.
sphere_0 = vtkSphereSource()
sphere_0.SetRadius(10.0)
sphere_0.Update()
legend_actor.SetEntry(0, sphere_0.GetOutput(), labels[0], text_colors[0])

sphere_1 = vtkSphereSource()
sphere_1.SetRadius(20.0)
sphere_1.Update()
legend_actor.SetEntry(1, sphere_1.GetOutput(), labels[1], text_colors[1])

sphere_2 = vtkSphereSource()
sphere_2.SetRadius(30.0)
sphere_2.Update()
legend_actor.SetEntry(2, sphere_2.GetOutput(), labels[2], text_colors[2])

sphere_3 = vtkSphereSource()
sphere_3.SetRadius(40.0)
sphere_3.Update()
legend_actor.SetEntry(3, sphere_3.GetOutput(), labels[3], text_colors[3])

sphere_4 = vtkSphereSource()
sphere_4.SetRadius(50.0)
sphere_4.Update()
legend_actor.SetEntry(4, sphere_4.GetOutput(), labels[4], text_colors[4])

# Renderer
renderer = vtkRenderer()
renderer.AddViewProp(legend_actor)
renderer.SetBackground(0.0, 0.0, 0.0)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("legend box sphere entries")
render_window.SetMultiSamples(0)
render_window.SetSize(350, 350)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.GetActiveCamera().ParallelProjectionOn()

interactor.Initialize()
interactor.Start()
