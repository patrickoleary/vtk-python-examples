#!/usr/bin/env python

# Test vtkTriangularTexture applied to two triangles.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import (
    vtkFloatArray,
    vtkPoints,
)
from vtkmodules.vtkCommonDataModel import (
    vtkCellArray,
    vtkPolyData,
)
from vtkmodules.vtkImagingHybrid import vtkTriangularTexture
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
    vtkTexture,
)

# Create a triangular texture
triangular_texture = vtkTriangularTexture()
triangular_texture.SetTexturePattern(1)
triangular_texture.SetXSize(32)
triangular_texture.SetYSize(32)

# Build two triangles with texture coordinates
points = vtkPoints()
points.InsertPoint(0, 0.0, 0.0, 0.0)
points.InsertPoint(1, 1.0, 0.0, 0.0)
points.InsertPoint(2, 0.5, 1.0, 0.0)
points.InsertPoint(3, 1.0, 0.0, 0.0)
points.InsertPoint(4, 0.0, 0.0, 0.0)
points.InsertPoint(5, 0.5, -1.0, 0.5)

texture_coords = vtkFloatArray()
texture_coords.SetNumberOfComponents(2)
texture_coords.InsertTuple2(0, 0.0, 0.0)
texture_coords.InsertTuple2(1, 1.0, 0.0)
texture_coords.InsertTuple2(2, 0.5, 0.86602540378443864676)
texture_coords.InsertTuple2(3, 0.0, 0.0)
texture_coords.InsertTuple2(4, 1.0, 0.0)
texture_coords.InsertTuple2(5, 0.5, 0.86602540378443864676)

triangles = vtkCellArray()
triangles.InsertNextCell(3)
triangles.InsertCellPoint(0)
triangles.InsertCellPoint(1)
triangles.InsertCellPoint(2)
triangles.InsertNextCell(3)
triangles.InsertCellPoint(3)
triangles.InsertCellPoint(4)
triangles.InsertCellPoint(5)

triangle = vtkPolyData()
triangle.SetPolys(triangles)
triangle.SetPoints(points)
triangle.GetPointData().SetTCoords(texture_coords)

triangle_mapper = vtkPolyDataMapper()
triangle_mapper.SetInputData(triangle)

texture = vtkTexture()
texture.SetInputConnection(triangular_texture.GetOutputPort())

actor = vtkActor()
actor.SetMapper(triangle_mapper)
actor.SetTexture(texture)

renderer = vtkRenderer()
renderer.SetBackground(0.3, 0.7, 0.2)
renderer.AddActor(actor)

render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(300, 300)
render_window.SetWindowName("triangular texture")

# Scene
renderer.ResetCamera()
renderer.GetActiveCamera().Zoom(1.5)

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
