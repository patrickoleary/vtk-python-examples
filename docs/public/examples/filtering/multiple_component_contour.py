#!/usr/bin/env python

# Demonstrate contouring on multi-component image data using
# vtkContourFilter with SetArrayComponent to select components.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersCore import vtkContourFilter
from vtkmodules.vtkImagingCore import vtkImageAppendComponents
from vtkmodules.vtkImagingSources import vtkImageGaussianSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Two Gaussian sources at different centers
gaussian_source_1 = vtkImageGaussianSource()
gaussian_source_1.SetWholeExtent(0, 31, 0, 31, 0, 31)
gaussian_source_1.SetCenter(10, 16, 16)
gaussian_source_1.SetMaximum(1000)
gaussian_source_1.SetStandardDeviation(7)

gaussian_source_2 = vtkImageGaussianSource()
gaussian_source_2.SetWholeExtent(0, 31, 0, 31, 0, 31)
gaussian_source_2.SetCenter(22, 16, 16)
gaussian_source_2.SetMaximum(1000)
gaussian_source_2.SetStandardDeviation(7)

# Combine into a two-component image
append_components = vtkImageAppendComponents()
append_components.AddInputConnection(gaussian_source_1.GetOutputPort())
append_components.AddInputConnection(gaussian_source_2.GetOutputPort())

# Contour component 0
contour_filter_1 = vtkContourFilter()
contour_filter_1.SetInputConnection(append_components.GetOutputPort())
contour_filter_1.SetValue(0, 500)
contour_filter_1.SetArrayComponent(0)

# Contour component 1
contour_filter_2 = vtkContourFilter()
contour_filter_2.SetInputConnection(append_components.GetOutputPort())
contour_filter_2.SetValue(0, 500)
contour_filter_2.SetArrayComponent(1)

# Mapper/actor for component 0 (white)
mapper_1 = vtkPolyDataMapper()
mapper_1.SetInputConnection(contour_filter_1.GetOutputPort())
mapper_1.SetScalarRange(0, 1)
mapper_1.SetScalarVisibility(0)
mapper_1.Update()

actor_1 = vtkActor()
actor_1.SetMapper(mapper_1)
actor_1.GetProperty().SetColor(1, 1, 1)

# Mapper/actor for component 1 (red)
mapper_2 = vtkPolyDataMapper()
mapper_2.SetInputConnection(contour_filter_2.GetOutputPort())
mapper_2.SetScalarRange(0, 1)
mapper_2.SetScalarVisibility(0)

actor_2 = vtkActor()
actor_2.SetMapper(mapper_2)
actor_2.GetProperty().SetColor(1, 0, 0)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(actor_1)
renderer.AddActor(actor_2)
renderer.SetBackground(0.3, 0.3, 0.3)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(400, 400)
render_window.SetWindowName("multiple component contour")

# Scene
renderer.ResetCamera()

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
