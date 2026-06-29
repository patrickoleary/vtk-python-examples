#!/usr/bin/env python

# Display text overlaid on an image using vtkTextMapper and vtkImageMapper.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkImagingSources import vtkImageEllipsoidSource
from vtkmodules.vtkRenderingCore import (
    vtkActor2D,
    vtkImageMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
    vtkTextMapper,
)

# Image source
ellipse = vtkImageEllipsoidSource()

image_mapper = vtkImageMapper()
image_mapper.SetInputConnection(ellipse.GetOutputPort())
image_mapper.SetColorWindow(255)
image_mapper.SetColorLevel(127.5)

image_actor = vtkActor2D()
image_actor.SetMapper(image_mapper)

# Text overlay
text_mapper = vtkTextMapper()
text_mapper.SetInput("Text Overlay")
text_mapper.GetTextProperty().SetFontSize(15)
text_mapper.GetTextProperty().SetColor(0, 1, 1)
text_mapper.GetTextProperty().BoldOn()
text_mapper.GetTextProperty().ShadowOn()

text_actor = vtkActor2D()
text_actor.SetMapper(text_mapper)
text_actor.SetPosition(138, 128)

# Renderer
renderer = vtkRenderer()
renderer.AddViewProp(image_actor)
renderer.AddViewProp(text_actor)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("overlay text on image")
render_window.SetMultiSamples(0)
render_window.SetSize(300, 300)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
