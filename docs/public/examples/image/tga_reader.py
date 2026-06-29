#!/usr/bin/env python

# Read a TGA file and display with vtkImageActor.

import os

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkIOImage import vtkTGAReader
from vtkmodules.vtkRenderingCore import (
    vtkImageActor,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Source
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Read TGA file
tga_reader = vtkTGAReader()
tga_reader.SetFileName(os.path.join(data_dir, "vtk.tga"))
tga_reader.Update()

# Display with vtkImageActor
image_actor = vtkImageActor()
image_actor.GetMapper().SetInputConnection(tga_reader.GetOutputPort())

# Renderer
renderer = vtkRenderer()
renderer.AddActor(image_actor)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("tga reader")
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
