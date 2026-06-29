#!/usr/bin/env python

# Test vtkImageStencil with a polydata stencil, combining a sphere stencil
# and a contour-based stencil side by side using vtkImageAppend.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

import os

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
from vtkmodules.vtkInteractionStyle import vtkInteractorStyleImage
from vtkmodules.vtkRenderingCore import (
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)
from vtkmodules.vtkRenderingCore import vtkImageSlice, vtkImageSliceMapper

data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Read image
reader = vtkPNGReader()
reader.SetDataSpacing(0.8, 0.8, 1.5)
reader.SetDataOrigin(0.0, 0.0, 0.0)
reader.SetFileName(os.path.join(data_dir, "fullhead15.png"))

# Create sphere stencil
sphere = vtkSphereSource()
sphere.SetPhiResolution(12)
sphere.SetThetaResolution(12)
sphere.SetCenter(102, 102, 0)
sphere.SetRadius(60)

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

# Create contour-based stencil
reader2 = vtkPNGReader()
reader2.SetDataSpacing(0.8, 0.8, 1.5)
reader2.SetDataOrigin(0.0, 0.0, 0.0)
reader2.SetFileName(os.path.join(data_dir, "fullhead15.png"))

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

# Append both stencil results side by side
image_append = vtkImageAppend()
image_append.SetInputConnection(stencil.GetOutputPort())
image_append.AddInputConnection(stencil2.GetOutputPort())

# Display using vtkImageSliceMapper + vtkImageSlice
image_mapper = vtkImageSliceMapper()
image_mapper.SetInputConnection(image_append.GetOutputPort())

image_slice = vtkImageSlice()
image_slice.SetMapper(image_mapper)
image_slice.GetProperty().SetColorWindow(2000)
image_slice.GetProperty().SetColorLevel(1000)

# Renderer
renderer = vtkRenderer()
renderer.AddViewProp(image_slice)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(400, 256)
render_window.SetWindowName("image stencil with polydata")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)
interactor_style_image = vtkInteractorStyleImage()
interactor.SetInteractorStyle(interactor_style_image)

# Scene
renderer.GetActiveCamera().ParallelProjectionOn()
renderer.ResetCamera()

interactor.Initialize()
interactor.Start()
