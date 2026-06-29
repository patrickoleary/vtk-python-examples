#!/usr/bin/env python
# Demonstrate displaying a PNG image via vtkImageItem in a 2D context scene.

import os

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingContextOpenGL2  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonDataModel import vtkImageData
from vtkmodules.vtkIOImage import vtkPNGReader
from vtkmodules.vtkRenderingContext2D import vtkContextActor, vtkImageItem
from vtkmodules.vtkRenderingCore import (
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Read the PNG image.
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))
logo_path = os.path.join(data_dir, "vtk.png")

reader = vtkPNGReader()
reader.SetFileName(logo_path)
reader.Update()

# Create the image item and set its position.
item = vtkImageItem()
item.SetImage(reader.GetOutput())
item.SetPosition(25, 30)

# Context actor and scene wiring.
context_actor = vtkContextActor()
context_actor.GetScene().AddItem(item)

# Renderer
renderer = vtkRenderer()
renderer.SetBackground(1.0, 1.0, 1.0)
context_actor.GetScene().SetRenderer(renderer)
renderer.AddActor(context_actor)

# Window
render_window = vtkRenderWindow()
render_window.SetSize(320, 181)
render_window.SetMultiSamples(0)
render_window.AddRenderer(renderer)
render_window.SetWindowName("context image")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
