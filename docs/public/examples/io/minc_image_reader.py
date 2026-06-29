#!/usr/bin/env python

# Read a MINC image file and display it using the standard rendering pipeline.

import os

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkIOMINC import vtkMINCImageReader
from vtkmodules.vtkRenderingCore import (
    vtkImageActor,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Source
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Read the MINC image
minc_reader = vtkMINCImageReader()
minc_reader.SetFileName(os.path.join(data_dir, "t3_grid_0.mnc"))

# Display with standard rendering pipeline
image_actor = vtkImageActor()
image_actor.GetMapper().SetInputConnection(minc_reader.GetOutputPort())

renderer = vtkRenderer()
renderer.AddActor(image_actor)

render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("minc image reader")
render_window.SetMultiSamples(0)
render_window.SetSize(300, 300)

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.GetActiveCamera().ParallelProjectionOn()
renderer.ResetCamera()

interactor.Initialize()
interactor.Start()
