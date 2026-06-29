#!/usr/bin/env python

# Subtract the 2D Laplacian from an image to enhance edges.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

import os

from vtkmodules.vtkIOImage import vtkPNGReader
from vtkmodules.vtkImagingCore import vtkImageCast
from vtkmodules.vtkImagingGeneral import vtkImageLaplacian
from vtkmodules.vtkImagingMath import vtkImageMathematics
from vtkmodules.vtkRenderingCore import (
    vtkImageActor,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Image pipeline
reader = vtkPNGReader()
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

reader.SetFileName(os.path.join(data_dir, "fullhead15.png"))

# Cast to double for Laplacian computation
cast = vtkImageCast()
cast.SetInputConnection(reader.GetOutputPort())
cast.SetOutputScalarTypeToDouble()
cast.Update()

# Compute 2D Laplacian
laplacian = vtkImageLaplacian()
laplacian.SetInputConnection(cast.GetOutputPort())
laplacian.SetDimensionality(2)
laplacian.Update()

# Subtract Laplacian from original
subtract = vtkImageMathematics()
subtract.SetOperationToSubtract()
subtract.SetInput1Data(cast.GetOutput())
subtract.SetInput2Data(laplacian.GetOutput())
subtract.ReleaseDataFlagOff()
subtract.Update()

# Display with vtkImageActor
image_actor = vtkImageActor()
image_actor.GetMapper().SetInputConnection(subtract.GetOutputPort())

# Renderer
renderer = vtkRenderer()
renderer.AddActor(image_actor)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(256, 256)
render_window.SetWindowName("laplacian edge enhance")

# Scene
renderer.ResetCamera()

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
