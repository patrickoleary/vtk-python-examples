#!/usr/bin/env python

# Demonstrate text with a leader line pointing to a 3D position using
# vtkCaptionActor2D, labeling the tip and base of a cone.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkFiltersSources import vtkConeSource
from vtkmodules.vtkRenderingAnnotation import vtkCaptionActor2D
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
peach_puff_rgb = (1.0, 0.855, 0.725)
tomato_rgb = (1.0, 0.388, 0.278)
steel_blue_rgb = (0.275, 0.510, 0.706)
background_rgb = (0.200, 0.302, 0.400)

# Source: generate a cone
source = vtkConeSource()
source.SetResolution(30)
source.SetHeight(2.0)
source.SetRadius(0.5)
source.SetCenter(0.0, 0.0, 0.0)
source.SetDirection(1.0, 0.0, 0.0)
source.Update()

# Mapper: map polygon data to graphics primitives
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(source.GetOutputPort())

# Actor: assign the mapped geometry
actor = vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetColor(peach_puff_rgb)

# Caption: label the tip of the cone with a leader line
tip_caption = vtkCaptionActor2D()
tip_caption.SetCaption("Tip")
tip_caption.SetAttachmentPoint(1.0, 0.0, 0.0)
tip_caption.BorderOff()
tip_caption.SetPosition(25, 10)
tip_caption.GetTextActor().SetTextScaleModeToNone()
tip_caption.GetCaptionTextProperty().SetFontSize(18)
tip_caption.GetCaptionTextProperty().SetColor(tomato_rgb)
tip_caption.GetCaptionTextProperty().BoldOn()
tip_caption.GetCaptionTextProperty().ItalicOff()
tip_caption.GetCaptionTextProperty().ShadowOff()

# Caption: label the base of the cone with a leader line
base_caption = vtkCaptionActor2D()
base_caption.SetCaption("Base")
base_caption.SetAttachmentPoint(-1.0, 0.0, 0.0)
base_caption.BorderOff()
base_caption.SetPosition(25, 10)
base_caption.GetTextActor().SetTextScaleModeToNone()
base_caption.GetCaptionTextProperty().SetFontSize(18)
base_caption.GetCaptionTextProperty().SetColor(steel_blue_rgb)
base_caption.GetCaptionTextProperty().BoldOn()
base_caption.GetCaptionTextProperty().ItalicOff()
base_caption.GetCaptionTextProperty().ShadowOff()

# Renderer: assemble the scene and configure the camera
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.AddViewProp(tip_caption)
renderer.AddViewProp(base_caption)
renderer.SetBackground(background_rgb)
renderer.ResetCamera()

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(640, 480)
render_window.SetWindowName("CaptionActor2D")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
