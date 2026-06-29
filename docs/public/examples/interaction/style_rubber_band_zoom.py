#!/usr/bin/env python
# Demonstrate vtkInteractorStyleRubberBandZoom on an image actor.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

import os

from vtkmodules.vtkIOImage import vtkTIFFReader
from vtkmodules.vtkRenderingCore import (
    vtkImageActor,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Read the beach image
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))
reader = vtkTIFFReader()
reader.SetFileName(os.path.join(data_dir, "beach.tif"))
reader.SetOrientationType(4)

# Display with an image actor
image_actor = vtkImageActor()
image_actor.GetMapper().SetInputConnection(reader.GetOutputPort())

renderer = vtkRenderer()
renderer.AddActor(image_actor)

render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(400, 400)
render_window.SetWindowName("style rubber band zoom")

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
