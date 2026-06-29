#!/usr/bin/env python

# Generate a 2D iso-contour on a minimal single-pixel image using
# vtkFlyingEdges2D to stress boundary conditions.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonDataModel import vtkImageData
from vtkmodules.vtkFiltersCore import vtkFlyingEdges2D
from vtkmodules.vtkFiltersModeling import vtkOutlineFilter
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Create a 2x2x1 image (single pixel) with scalar values
image = vtkImageData()
image.SetDimensions(2, 2, 1)
image.AllocateScalars(10, 1)

scalars = image.GetPointData().GetScalars()
scalars.InsertTuple1(0, -1.0)
scalars.InsertTuple1(1, -1.0)
scalars.InsertTuple1(2, 1.0)
scalars.InsertTuple1(3, 1.0)

# Flying edges 2D contour at zero crossing
iso = vtkFlyingEdges2D()
iso.SetInputData(image)
iso.SetValue(0, 0.0)
iso.Update()

iso_mapper = vtkPolyDataMapper()
iso_mapper.SetInputConnection(iso.GetOutputPort())
iso_mapper.ScalarVisibilityOff()

iso_actor = vtkActor()
iso_actor.SetMapper(iso_mapper)
iso_actor.GetProperty().SetColor(1, 0, 0)
iso_actor.GetProperty().SetOpacity(1)

# Outline
outline = vtkOutlineFilter()
outline.SetInputData(image)

outline_mapper = vtkPolyDataMapper()
outline_mapper.SetInputConnection(outline.GetOutputPort())

outline_actor = vtkActor()
outline_actor.SetMapper(outline_mapper)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(outline_actor)
renderer.AddActor(iso_actor)
renderer.SetBackground(0, 0, 0)

# Window
render_window = vtkRenderWindow()
render_window.SetMultiSamples(0)
render_window.AddRenderer(renderer)
render_window.SetSize(300, 300)
render_window.SetWindowName("flying edges2d thin pixel")

# Scene
renderer.ResetCamera()

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
