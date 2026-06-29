#!/usr/bin/env python

# Demonstrate vtkImageDataToPointSet by converting a wavelet image dataset
# with a non-identity direction matrix into a structured grid and rendering
# the result colored by the RTData scalar field.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersGeneral import vtkImageDataToPointSet
from vtkmodules.vtkFiltersGeometry import vtkDataSetSurfaceFilter
from vtkmodules.vtkImagingCore import vtkRTAnalyticSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Create wavelet source
wavelet = vtkRTAnalyticSource()
wavelet.SetWholeExtent(-2, 2, -2, 2, -2, 2)
wavelet.SetCenter(0, 0, 0)
wavelet.SetMaximum(255)
wavelet.SetStandardDeviation(0.5)
wavelet.SetXFreq(60)
wavelet.SetYFreq(30)
wavelet.SetZFreq(40)
wavelet.SetXMag(10)
wavelet.SetYMag(18)
wavelet.SetZMag(5)
wavelet.SetSubsampleRate(1)
wavelet.Update()

# Modify the image with a non-identity direction, spacing, origin
image = wavelet.GetOutput()
image.SetDirectionMatrix(1, 0, 0, 0, -1, 0, 0, 0, -1)
image.SetSpacing(0.5, 1.0, 1.2)
image.SetOrigin(100, -3.3, 0)

# Convert to structured grid (point set)
image_to_points = vtkImageDataToPointSet()
image_to_points.SetInputData(image)
image_to_points.Update()

# Extract surface for rendering
surface = vtkDataSetSurfaceFilter()
surface.SetInputConnection(image_to_points.GetOutputPort())

# Mapper and actor
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(surface.GetOutputPort())

actor = vtkActor()
actor.SetMapper(mapper)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(0.1, 0.2, 0.4)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(400, 400)
render_window.SetWindowName("imagedata to pointset")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.ResetCamera()

interactor.Initialize()
interactor.Start()
