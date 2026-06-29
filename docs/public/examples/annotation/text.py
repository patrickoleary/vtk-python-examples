#!/usr/bin/env python

# Demonstrate vtkTextSource and vtkVectorText for 3D text rendering.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersSources import vtkTextSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)
from vtkmodules.vtkRenderingFreeType import vtkVectorText

# Text source with default scalars
text_0_source = vtkTextSource()
text_0_source.SetText("Text Source with Scalars (default)")

text_0_mapper = vtkPolyDataMapper()
text_0_mapper.SetInputConnection(text_0_source.GetOutputPort())

text_0_actor = vtkActor()
text_0_actor.SetMapper(text_0_mapper)
text_0_actor.SetScale(0.1, 0.1, 0.1)
text_0_actor.AddPosition(0, 2, 0)

# Text source with foreground/background colors
text_1_source = vtkTextSource()
text_1_source.SetText("Text Source with Scalars")
text_1_source.SetForegroundColor(1, 0, 0)
text_1_source.SetBackgroundColor(1, 1, 1)

text_1_mapper = vtkPolyDataMapper()
text_1_mapper.SetInputConnection(text_1_source.GetOutputPort())

text_1_actor = vtkActor()
text_1_actor.SetMapper(text_1_mapper)
text_1_actor.SetScale(0.1, 0.1, 0.1)

# Text source without scalars
text_2_source = vtkTextSource()
text_2_source.SetText("Text Source without Scalars")
text_2_source.BackingOff()

text_2_mapper = vtkPolyDataMapper()
text_2_mapper.SetInputConnection(text_2_source.GetOutputPort())
text_2_mapper.ScalarVisibilityOff()

text_2_actor = vtkActor()
text_2_actor.SetMapper(text_2_mapper)
text_2_actor.GetProperty().SetColor(1, 1, 0)
text_2_actor.SetScale(0.1, 0.1, 0.1)
text_2_actor.AddPosition(0, -2, 0)

# Vector text
text_3_source = vtkVectorText()
text_3_source.SetText("Vector Text")

text_3_mapper = vtkPolyDataMapper()
text_3_mapper.SetInputConnection(text_3_source.GetOutputPort())
text_3_mapper.ScalarVisibilityOff()

text_3_actor = vtkActor()
text_3_actor.SetMapper(text_3_mapper)
text_3_actor.GetProperty().SetColor(0.1, 1, 0)
text_3_actor.AddPosition(0, -4, 0)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(text_0_actor)
renderer.AddActor(text_1_actor)
renderer.AddActor(text_2_actor)
renderer.AddActor(text_3_actor)
renderer.SetBackground(0.1, 0.2, 0.4)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("text")
render_window.SetMultiSamples(0)
render_window.SetSize(350, 100)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.ResetCamera()
renderer.GetActiveCamera().Zoom(3)

interactor.Initialize()
interactor.Start()
