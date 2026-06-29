#!/usr/bin/env python

# Test vtkLassoStencilSource with polygon and spline shapes.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

import os

from vtkmodules.vtkCommonCore import vtkPoints
from vtkmodules.vtkIOImage import vtkPNGReader
from vtkmodules.vtkImagingCore import vtkImageShiftScale
from vtkmodules.vtkImagingStencil import (
    vtkImageStencil,
    vtkLassoStencilSource,
)
from vtkmodules.vtkRenderingCore import (
    vtkActor2D,
    vtkImageMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Read image
reader = vtkPNGReader()
reader.SetDataSpacing(0.8, 0.8, 1.5)
reader.SetDataOrigin(0.0, 0.0, 0.0)
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

reader.SetFileName(os.path.join(data_dir, "fullhead15.png"))
reader.Update()

# Dimmed background
shift_scale = vtkImageShiftScale()
shift_scale.SetInputConnection(reader.GetOutputPort())
shift_scale.SetScale(0.2)
shift_scale.Update()

# Polygon points (closed)
points1 = vtkPoints()
points1.InsertNextPoint(80, 50, 0)
points1.InsertNextPoint(100, 90, 0)
points1.InsertNextPoint(200, 50, 0)
points1.InsertNextPoint(230, 100, 0)
points1.InsertNextPoint(150, 170, 0)
points1.InsertNextPoint(110, 170, 0)
points1.InsertNextPoint(80, 50, 0)

# Polygon points (open)
points2 = vtkPoints()
points2.InsertNextPoint(80, 50, 0)
points2.InsertNextPoint(100, 90, 0)
points2.InsertNextPoint(200, 50, 0)
points2.InsertNextPoint(230, 100, 0)
points2.InsertNextPoint(150, 170, 0)
points2.InsertNextPoint(110, 170, 0)

# Polygon with slice points
roi_stencil1 = vtkLassoStencilSource()
roi_stencil1.SetShapeToPolygon()
roi_stencil1.SetSlicePoints(0, points1)
roi_stencil1.SetInformationInput(reader.GetOutput())

# Polygon with points
roi_stencil2 = vtkLassoStencilSource()
roi_stencil2.SetShapeToPolygon()
roi_stencil2.SetPoints(points2)
roi_stencil2.SetInformationInput(reader.GetOutput())

# Spline with points
roi_stencil3 = vtkLassoStencilSource()
roi_stencil3.SetShapeToSpline()
roi_stencil3.SetPoints(points1)
roi_stencil3.SetInformationInput(reader.GetOutput())

# Spline with slice points
roi_stencil4 = vtkLassoStencilSource()
roi_stencil4.SetShapeToSpline()
roi_stencil4.SetSlicePoints(0, points2)
roi_stencil4.SetInformationInput(reader.GetOutput())
roi_stencil4.Update()

# Apply stencils
stencil1 = vtkImageStencil()
stencil1.SetInputConnection(reader.GetOutputPort())
stencil1.SetBackgroundInputData(shift_scale.GetOutput())
stencil1.SetStencilConnection(roi_stencil1.GetOutputPort())

stencil2 = vtkImageStencil()
stencil2.SetInputConnection(reader.GetOutputPort())
stencil2.SetBackgroundInputData(shift_scale.GetOutput())
stencil2.SetStencilConnection(roi_stencil2.GetOutputPort())

stencil3 = vtkImageStencil()
stencil3.SetInputConnection(reader.GetOutputPort())
stencil3.SetBackgroundInputData(shift_scale.GetOutput())
stencil3.SetStencilConnection(roi_stencil3.GetOutputPort())

stencil4 = vtkImageStencil()
stencil4.SetInputConnection(reader.GetOutputPort())
stencil4.SetBackgroundInputData(shift_scale.GetOutput())
stencil4.SetStencilConnection(roi_stencil4.GetOutputPort())

# Mapper + Actor pairs
mapper_0 = vtkImageMapper()
mapper_0.SetInputConnection(stencil1.GetOutputPort())
mapper_0.SetColorWindow(2000)
mapper_0.SetColorLevel(1000)
mapper_0.SetZSlice(0)

actor_0 = vtkActor2D()
actor_0.SetMapper(mapper_0)

mapper_1 = vtkImageMapper()
mapper_1.SetInputConnection(stencil2.GetOutputPort())
mapper_1.SetColorWindow(2000)
mapper_1.SetColorLevel(1000)
mapper_1.SetZSlice(0)

actor_1 = vtkActor2D()
actor_1.SetMapper(mapper_1)

mapper_2 = vtkImageMapper()
mapper_2.SetInputConnection(stencil3.GetOutputPort())
mapper_2.SetColorWindow(2000)
mapper_2.SetColorLevel(1000)
mapper_2.SetZSlice(0)

actor_2 = vtkActor2D()
actor_2.SetMapper(mapper_2)

mapper_3 = vtkImageMapper()
mapper_3.SetInputConnection(stencil4.GetOutputPort())
mapper_3.SetColorWindow(2000)
mapper_3.SetColorLevel(1000)
mapper_3.SetZSlice(0)

actor_3 = vtkActor2D()
actor_3.SetMapper(mapper_3)

# Renderers in four viewports
renderer_0 = vtkRenderer()
renderer_0.AddViewProp(actor_0)
renderer_0.SetViewport(0.5, 0.0, 1.0, 0.5)

renderer_1 = vtkRenderer()
renderer_1.AddViewProp(actor_1)
renderer_1.SetViewport(0.0, 0.0, 0.5, 0.5)

renderer_2 = vtkRenderer()
renderer_2.AddViewProp(actor_2)
renderer_2.SetViewport(0.5, 0.5, 1.0, 1.0)

renderer_3 = vtkRenderer()
renderer_3.AddViewProp(actor_3)
renderer_3.SetViewport(0.0, 0.5, 0.5, 1.0)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer_0)
render_window.AddRenderer(renderer_1)
render_window.AddRenderer(renderer_2)
render_window.AddRenderer(renderer_3)
render_window.SetSize(512, 512)
render_window.SetWindowName("lasso stencil")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
