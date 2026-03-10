#!/usr/bin/env python

# Cut a sphere to obtain a circle contour, extrude it, and use the extruded
# surface as a stencil to stamp a binary image, then display the result.

import math

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkCommonCore import VTK_UNSIGNED_CHAR
from vtkmodules.vtkCommonDataModel import (
    vtkImageData,
    vtkPlane,
)
from vtkmodules.vtkFiltersCore import (
    vtkCutter,
    vtkStripper,
)
from vtkmodules.vtkFiltersModeling import vtkLinearExtrusionFilter
from vtkmodules.vtkFiltersSources import vtkSphereSource
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

# Source: sphere centered at (40,40,0)
sphere_source = vtkSphereSource()
sphere_source.SetPhiResolution(30)
sphere_source.SetThetaResolution(30)
sphere_source.SetCenter(40, 40, 0)
sphere_source.SetRadius(20)

# Filter: cut the sphere with a z-normal plane through its center → circle
cut_plane = vtkPlane()
cut_plane.SetOrigin(sphere_source.GetCenter())
cut_plane.SetNormal(0, 0, 1)

circle_cutter = vtkCutter()
circle_cutter.SetInputConnection(sphere_source.GetOutputPort())
circle_cutter.SetCutFunction(cut_plane)

stripper = vtkStripper()
stripper.SetInputConnection(circle_cutter.GetOutputPort())
stripper.Update()
circle = stripper.GetOutput()

# Prepare a white voxel image covering the circle bounds
bounds = [0.0] * 6
circle.GetBounds(bounds)
spacing = [0.5, 0.5, 0.5]

dim = [0, 0, 0]
for i in range(3):
    dim[i] = int(math.ceil((bounds[i * 2 + 1] - bounds[i * 2]) / spacing[i])) + 1
    if dim[i] < 1:
        dim[i] = 1

origin = [bounds[0], bounds[2], bounds[4]]

white_image = vtkImageData()
white_image.SetSpacing(spacing)
white_image.SetDimensions(dim)
white_image.SetExtent(0, dim[0] - 1, 0, dim[1] - 1, 0, dim[2] - 1)
white_image.SetOrigin(origin)
white_image.AllocateScalars(VTK_UNSIGNED_CHAR, 1)

for i in range(white_image.GetNumberOfPoints()):
    white_image.GetPointData().GetScalars().SetTuple1(i, 255)

# Filter: extrude the circle contour along z
extruder = vtkLinearExtrusionFilter()
extruder.SetInputData(circle)
extruder.SetScaleFactor(1.0)
extruder.SetExtrusionTypeToVectorExtrusion()
extruder.SetVector(0, 0, 1)

# Filter: convert extruded polydata to an image stencil
poly_to_stencil = vtkPolyDataToImageStencil()
poly_to_stencil.SetTolerance(0)
poly_to_stencil.SetInputConnection(extruder.GetOutputPort())
poly_to_stencil.SetOutputOrigin(origin)
poly_to_stencil.SetOutputSpacing(spacing)
poly_to_stencil.SetOutputWholeExtent(white_image.GetExtent())
poly_to_stencil.Update()

# Filter: apply the stencil — inside keeps white (255), outside → black (0)
image_stencil = vtkImageStencil()
image_stencil.SetInputData(white_image)
image_stencil.SetStencilConnection(poly_to_stencil.GetOutputPort())
image_stencil.ReverseStencilOff()
image_stencil.SetBackgroundValue(0)
image_stencil.Update()

# Actor: display the stamped image as a 2-D slice
image_actor = vtkImageActor()
image_actor.GetMapper().SetInputConnection(image_stencil.GetOutputPort())

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.AddActor(image_actor)
renderer.ResetCamera()

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(640, 480)
render_window.SetWindowName("PolyDataContourToImageData")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window.Render()
render_window_interactor.Start()
