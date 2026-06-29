#!/usr/bin/env python

# Test vtkAxisActor2D with custom text and line properties.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkRenderingAnnotation import vtkAxisActor2D
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Axis actor 2D along a diagonal
axis = vtkAxisActor2D()
axis.SetPoint1(0.1, 0.1)
axis.SetPoint2(0.9, 0.9)

# Custom text property
axis.SetUseFontSizeFromProperty(True)
label_text_prop = axis.GetLabelTextProperty()
label_text_prop.SetColor(1.0, 0.5, 0.0)
label_text_prop.SetFontSize(18)
label_text_prop.BoldOn()
axis.SetLabelTextProperty(label_text_prop)

# Custom line property
axis.GetProperty().SetColor(1.0, 0.0, 0.0)
axis.GetProperty().SetLineWidth(4)

# Source
sphere_source = vtkSphereSource()

sphere_mapper = vtkPolyDataMapper()
sphere_mapper.SetInputConnection(sphere_source.GetOutputPort())

sphere_actor = vtkActor()
sphere_actor.SetMapper(sphere_mapper)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(axis)
renderer.AddActor(sphere_actor)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("axis actor2d")
render_window.SetMultiSamples(0)
render_window.SetSize(300, 300)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.GetActiveCamera().ParallelProjectionOn()

interactor.Initialize()
interactor.Start()
