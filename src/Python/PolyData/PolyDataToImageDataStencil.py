#!/usr/bin/env python

# Mask a PNG image with a sphere stencil and a contour stencil, then display
# the two results side-by-side using vtkPolyDataToImageStencil.

import os
from pathlib import Path

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkCommonDataModel import vtkPlane
from vtkmodules.vtkFiltersCore import (
    vtkCutter,
    vtkImageAppend,
    vtkStripper,
    vtkTriangleFilter,
)
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkIOImage import vtkPNGReader
from vtkmodules.vtkImagingStencil import (
    vtkImageStencil,
    vtkPolyDataToImageStencil,
)
from vtkmodules.vtkRenderingCore import (
    vtkImageActor,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Data file
data_dir = Path(os.environ.get("VPE_DATA_DIR", Path(__file__).parent))
image_file = str(data_dir / "VTKLogo.png")

# Reader: load the PNG image
reader = vtkPNGReader()
reader.SetDataSpacing(0.8, 0.8, 1.5)
reader.SetDataOrigin(0.0, 0.0, 0.0)
reader.SetFileName(image_file)

# Source: sphere used as the stencil shape
sphere = vtkSphereSource()
sphere.SetPhiResolution(12)
sphere.SetThetaResolution(12)
sphere.SetCenter(102, 102, 0)
sphere.SetRadius(60)

# Stencil 1: triangulated sphere surface → image stencil
triangle = vtkTriangleFilter()
triangle.SetInputConnection(sphere.GetOutputPort())

stripper = vtkStripper()
stripper.SetInputConnection(triangle.GetOutputPort())

data_to_stencil = vtkPolyDataToImageStencil()
data_to_stencil.SetInputConnection(stripper.GetOutputPort())
data_to_stencil.SetOutputSpacing(0.8, 0.8, 1.5)
data_to_stencil.SetOutputOrigin(0.0, 0.0, 0.0)

stencil = vtkImageStencil()
stencil.SetInputConnection(reader.GetOutputPort())
stencil.SetStencilConnection(data_to_stencil.GetOutputPort())
stencil.ReverseStencilOn()
stencil.SetBackgroundValue(500)

# Stencil 2: contour (cut sphere with z-plane) → image stencil
reader2 = vtkPNGReader()
reader2.SetDataSpacing(0.8, 0.8, 1.5)
reader2.SetDataOrigin(0.0, 0.0, 0.0)
reader2.SetFileName(image_file)

plane = vtkPlane()
plane.SetOrigin(0, 0, 0)
plane.SetNormal(0, 0, 1)

cutter = vtkCutter()
cutter.SetInputConnection(sphere.GetOutputPort())
cutter.SetCutFunction(plane)

stripper2 = vtkStripper()
stripper2.SetInputConnection(cutter.GetOutputPort())

data_to_stencil2 = vtkPolyDataToImageStencil()
data_to_stencil2.SetInputConnection(stripper2.GetOutputPort())
data_to_stencil2.SetOutputSpacing(0.8, 0.8, 1.5)
data_to_stencil2.SetOutputOrigin(0.0, 0.0, 0.0)

stencil2 = vtkImageStencil()
stencil2.SetInputConnection(reader2.GetOutputPort())
stencil2.SetStencilConnection(data_to_stencil2.GetOutputPort())
stencil2.SetBackgroundValue(500)

# Append the two stencil results side-by-side
image_append = vtkImageAppend()
image_append.SetInputConnection(stencil.GetOutputPort())
image_append.AddInputConnection(stencil2.GetOutputPort())

# Actor: display the side-by-side stencil results as a 2-D slice
image_actor = vtkImageActor()
image_actor.GetMapper().SetInputConnection(image_append.GetOutputPort())

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.AddActor(image_actor)
renderer.ResetCamera()

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(640, 480)
render_window.SetWindowName("PolyDataToImageDataStencil")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window.Render()
render_window_interactor.Start()
