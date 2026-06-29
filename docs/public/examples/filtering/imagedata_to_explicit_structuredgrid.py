#!/usr/bin/env python

# Convert a wavelet image dataset to an explicit structured grid
# using vtkImageDataToExplicitStructuredGrid.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersCore import vtkImageDataToExplicitStructuredGrid
from vtkmodules.vtkImagingCore import vtkRTAnalyticSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkDataSetMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Source: wavelet dataset
wavelet = vtkRTAnalyticSource()
wavelet.SetWholeExtent(-10, 10, -10, 10, -10, 10)
wavelet.SetCenter(0.0, 0.0, 0.0)
wavelet.Update()

# Filter: convert image data to explicit structured grid
esg_converter = vtkImageDataToExplicitStructuredGrid()
esg_converter.SetInputConnection(wavelet.GetOutputPort())

# Mapper
mapper = vtkDataSetMapper()
mapper.SetInputConnection(esg_converter.GetOutputPort())

# Actor
actor = vtkActor()
actor.SetMapper(mapper)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(actor)

# Window
render_window = vtkRenderWindow()
render_window.SetSize(300, 300)
render_window.AddRenderer(renderer)
render_window.SetWindowName("imagedata to explicit structuredgrid")

# Scene
renderer.ResetCamera()

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
