#!/usr/bin/env python

# Test vtkLegendScaleActor with custom label counts, grid, notation, and axis properties.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersSources import vtkConeSource
from vtkmodules.vtkRenderingAnnotation import vtkLegendScaleActor
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkProperty2D,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
    vtkTextProperty,
)

# Source
cone_source = vtkConeSource()

# Mapper
cone_mapper = vtkPolyDataMapper()
cone_mapper.SetInputConnection(cone_source.GetOutputPort())

# Actor
cone_actor = vtkActor()
cone_actor.SetMapper(cone_mapper)

# Legend scale actor
legend_actor = vtkLegendScaleActor()
legend_actor.TopAxisVisibilityOn()
legend_actor.SetLabelModeToCoordinates()
legend_actor.TopAxisVisibilityOff()
legend_actor.SetLegendVisibility(False)
legend_actor.SetGridVisibility(True)
legend_actor.SetNotation(1)
legend_actor.SetPrecision(2)
legend_actor.SetCornerOffsetFactor(1)
legend_actor.SetNumberOfHorizontalLabels(4)
legend_actor.SetNumberOfVerticalLabels(3)

# Text property
text_prop = vtkTextProperty()
text_prop.SetColor(1, 0.5, 0)
text_prop.SetFontSize(10)
text_prop.BoldOn()
legend_actor.SetUseFontSizeFromProperty(True)
legend_actor.SetAxesTextProperty(text_prop)

# Axes property
axes_property = vtkProperty2D()
axes_property.SetColor(0.2, 0.9, 0.2)
legend_actor.SetAxesProperty(axes_property)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(cone_actor)
renderer.AddViewProp(legend_actor)
renderer.SetBackground(0.1, 0.2, 0.4)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("legend scale actor custom labels")
render_window.SetMultiSamples(0)
render_window.SetSize(300, 300)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.GetActiveCamera().ParallelProjectionOn()

interactor.Initialize()
interactor.Start()
