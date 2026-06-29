#!/usr/bin/env python

# Test vtkLegendScaleActor in default configuration with a sphere.

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

# Mapper
sphere_mapper = vtkPolyDataMapper()
sphere_mapper.SetInputConnection(sphere_source.GetOutputPort())

# Actor
sphere_actor = vtkActor()
sphere_actor.SetMapper(sphere_mapper)

# Legend scale actor (default config)
legend_actor = vtkLegendScaleActor()

# Bigger text for robustness
text_prop = vtkTextProperty()
text_prop.SetFontSize(14)
text_prop.BoldOn()
legend_actor.SetUseFontSizeFromProperty(True)
legend_actor.SetAxesTextProperty(text_prop)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(sphere_actor)
renderer.AddViewProp(legend_actor)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("legend scale actor default")
render_window.SetMultiSamples(0)
render_window.SetSize(300, 300)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
