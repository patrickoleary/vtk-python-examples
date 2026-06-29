#!/usr/bin/env python

# Test vtkLegendScaleActor with custom axis visibility and text properties.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkRenderingAnnotation import vtkLegendScaleActor
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
    vtkTextProperty,
)

# Source
sphere_source = vtkSphereSource()
sphere_source.SetCenter(1, 2, 3)

# Mapper
sphere_mapper = vtkPolyDataMapper()
sphere_mapper.SetInputConnection(sphere_source.GetOutputPort())

# Actor
sphere_actor = vtkActor()
sphere_actor.SetMapper(sphere_mapper)

# Legend scale actor
legend_actor = vtkLegendScaleActor()
legend_actor.TopAxisVisibilityOn()
legend_actor.SetLabelModeToCoordinates()
legend_actor.AllAxesOff()
legend_actor.LeftAxisVisibilityOn()
legend_actor.TopAxisVisibilityOn()
legend_actor.LegendVisibilityOff()
legend_actor.SetLeftBorderOffset(70)
legend_actor.SetTopBorderOffset(50)
legend_actor.GetTopAxis().SetNumberOfLabels(3)
legend_actor.SetCornerOffsetFactor(1)
legend_actor.SetOrigin(1, 1, 1)

text_prop = vtkTextProperty()
text_prop.SetColor(1, 0.5, 0)
text_prop.SetFontSize(18)
text_prop.BoldOn()
legend_actor.SetUseFontSizeFromProperty(True)
legend_actor.SetAxesTextProperty(text_prop)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(sphere_actor)
renderer.AddViewProp(legend_actor)
renderer.SetBackground(0.1, 0.2, 0.4)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("legend scale actor")
render_window.SetMultiSamples(0)
render_window.SetSize(300, 300)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.GetActiveCamera().ParallelProjectionOn()
renderer.ResetCamera()

interactor.Initialize()
interactor.Start()
