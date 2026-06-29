#!/usr/bin/env python

# Clip discrete regions from a synthetic labeled image using
# vtkDiscreteFlyingEdgesClipper2D with a wireframe grid overlay.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonDataModel import vtkImageData
from vtkmodules.vtkFiltersGeneral import vtkDiscreteFlyingEdgesClipper2D
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkDataSetMapper,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Create synthetic image data (6x5 with labeled regions)
VTK_SHORT = 4
img = vtkImageData()
img.SetDimensions(6, 5, 1)
img.AllocateScalars(VTK_SHORT, 1)

scalars = img.GetPointData().GetScalars()
# Row 0
scalars.SetTuple1(0, 0)
scalars.SetTuple1(1, 0)
scalars.SetTuple1(2, 0)
scalars.SetTuple1(3, 0)
scalars.SetTuple1(4, 0)
scalars.SetTuple1(5, 0)
# Row 1
scalars.SetTuple1(6, 0)
scalars.SetTuple1(7, 0)
scalars.SetTuple1(8, 0)
scalars.SetTuple1(9, 0)
scalars.SetTuple1(10, 0)
scalars.SetTuple1(11, 0)
# Row 2
scalars.SetTuple1(12, 0)
scalars.SetTuple1(13, 0)
scalars.SetTuple1(14, 0)
scalars.SetTuple1(15, 2)
scalars.SetTuple1(16, 4)
scalars.SetTuple1(17, 0)
# Row 3
scalars.SetTuple1(18, 0)
scalars.SetTuple1(19, 0)
scalars.SetTuple1(20, 1)
scalars.SetTuple1(21, 1)
scalars.SetTuple1(22, 3)
scalars.SetTuple1(23, 3)
# Row 4
scalars.SetTuple1(24, 0)
scalars.SetTuple1(25, 0)
scalars.SetTuple1(26, 3)
scalars.SetTuple1(27, 0)
scalars.SetTuple1(28, 0)
scalars.SetTuple1(29, 3)

# Clip discrete regions
discrete = vtkDiscreteFlyingEdgesClipper2D()
discrete.SetInputData(img)
discrete.SetValue(0, 1)
discrete.SetValue(1, 2)
discrete.SetValue(2, 3)
discrete.SetValue(3, 4)
discrete.Update()

# Clipped polygons
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(discrete.GetOutputPort())
mapper.SetScalarModeToUseCellData()
mapper.SetScalarRange(1, 4)

actor = vtkActor()
actor.SetMapper(mapper)

# Image gridlines as wireframe
grid_mapper = vtkDataSetMapper()
grid_mapper.SetInputData(img)
grid_mapper.ScalarVisibilityOff()

grid_actor = vtkActor()
grid_actor.SetMapper(grid_mapper)
grid_actor.GetProperty().SetRepresentationToWireframe()
grid_actor.GetProperty().SetColor(0, 0, 1)

# Renderer
renderer = vtkRenderer()
renderer.SetBackground(1, 1, 1)
renderer.AddActor(actor)
renderer.AddActor(grid_actor)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(400, 400)
render_window.SetWindowName("fe discrete clipper2d")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
