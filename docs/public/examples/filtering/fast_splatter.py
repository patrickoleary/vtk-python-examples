#!/usr/bin/env python

# Test vtkFastSplatter with a custom splat image and five sample points.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import (
    VTK_FLOAT,
    vtkPoints,
)
from vtkmodules.vtkCommonDataModel import (
    vtkImageData,
    vtkPolyData,
)
from vtkmodules.vtkImagingCore import vtkImageShiftScale
from vtkmodules.vtkImagingHybrid import vtkFastSplatter
from vtkmodules.vtkRenderingCore import (
    vtkImageActor,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

SPLAT_IMAGE_SIZE = 100

# Build the splat image by hand
splat_image = vtkImageData()
splat_image.SetDimensions(SPLAT_IMAGE_SIZE, SPLAT_IMAGE_SIZE, 1)
splat_image.AllocateScalars(VTK_FLOAT, 1)

for i in range(SPLAT_IMAGE_SIZE):
    for j in range(SPLAT_IMAGE_SIZE):
        x_coord = 1 - abs((i - SPLAT_IMAGE_SIZE / 2) / (SPLAT_IMAGE_SIZE / 2.0))
        y_coord = 1 - abs((j - SPLAT_IMAGE_SIZE / 2) / (SPLAT_IMAGE_SIZE / 2.0))
        splat_image.SetScalarComponentFromDouble(i, j, 0, 0, x_coord * y_coord)

# Create splat points
splat_points = vtkPolyData()
points = vtkPoints()
points.SetNumberOfPoints(5)
points.SetPoint(0, 0, 0, 0)
points.SetPoint(1, 1, 1, 0)
points.SetPoint(2, -1, 1, 0)
points.SetPoint(3, 1, -1, 0)
points.SetPoint(4, -1, -1, 0)
splat_points.SetPoints(points)

# Splatter
splatter = vtkFastSplatter()
splatter.SetInputData(splat_points)
splatter.SetOutputDimensions(2 * SPLAT_IMAGE_SIZE, 2 * SPLAT_IMAGE_SIZE, 1)
splatter.SetInputData(1, splat_image)

# Convert to unsigned char for display
result_scale = vtkImageShiftScale()
result_scale.SetOutputScalarTypeToUnsignedChar()
result_scale.SetShift(0)
result_scale.SetScale(255)
result_scale.SetInputConnection(splatter.GetOutputPort())
result_scale.Update()

# Display
actor = vtkImageActor()
actor.GetMapper().SetInputConnection(result_scale.GetOutputPort())

renderer = vtkRenderer()
renderer.AddViewProp(actor)

render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(300, 300)
render_window.SetWindowName("fast splatter")

# Scene
renderer.GetActiveCamera().ParallelProjectionOn()
renderer.ResetCamera()

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
