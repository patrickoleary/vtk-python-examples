#!/usr/bin/env python
# Demonstrate coloring points with scalar arrays using glyphs.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import vtkPoints, vtkUnsignedCharArray
from vtkmodules.vtkCommonDataModel import vtkPolyVertex, vtkUnstructuredGrid
from vtkmodules.vtkFiltersCore import vtkGlyph3D
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkDataSetMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Create color array.
color_array = vtkUnsignedCharArray()
color_array.SetName("Colors")
color_array.SetNumberOfComponents(3)
color_array.SetNumberOfTuples(3)
color_array.InsertComponent(0, 0, 255)
color_array.InsertComponent(0, 1, 99)
color_array.InsertComponent(0, 2, 71)
color_array.InsertComponent(1, 0, 125)
color_array.InsertComponent(1, 1, 255)
color_array.InsertComponent(1, 2, 0)
color_array.InsertComponent(2, 0, 226)
color_array.InsertComponent(2, 1, 207)
color_array.InsertComponent(2, 2, 87)

# Create size array.
sizes = vtkUnsignedCharArray()
sizes.SetName("Sizes")
sizes.SetNumberOfComponents(1)
sizes.SetNumberOfTuples(3)
sizes.SetValue(0, 1)
sizes.SetValue(1, 2)
sizes.SetValue(2, 3)

# Create points.
poly_vertex_points = vtkPoints()
poly_vertex_points.SetNumberOfPoints(3)
poly_vertex_points.InsertPoint(0, 0.0, 0.0, 0.0)
poly_vertex_points.InsertPoint(1, 2.5, 0.0, 0.0)
poly_vertex_points.InsertPoint(2, 5.0, 0.0, 0.0)

# Create a poly vertex cell.
poly_vertex = vtkPolyVertex()
poly_vertex.GetPointIds().SetNumberOfIds(3)
poly_vertex.GetPointIds().SetId(0, 0)
poly_vertex.GetPointIds().SetId(1, 1)
poly_vertex.GetPointIds().SetId(2, 2)

# Create unstructured grid.
poly_vertex_grid = vtkUnstructuredGrid()
poly_vertex_grid.Allocate(1, 1)
poly_vertex_grid.InsertNextCell(poly_vertex.GetCellType(), poly_vertex.GetPointIds())
poly_vertex_grid.SetPoints(poly_vertex_points)
poly_vertex_grid.GetPointData().SetScalars(sizes)
poly_vertex_grid.GetPointData().AddArray(color_array)

# Create sphere source for glyphs.
sphere = vtkSphereSource()
sphere.SetRadius(1.0)
sphere.Update()

# Create glyphs.
glyphs = vtkGlyph3D()
glyphs.ScalingOn()
glyphs.SetColorModeToColorByScalar()
glyphs.SetScaleModeToScaleByScalar()
glyphs.SetScaleFactor(1)
glyphs.SetInputData(poly_vertex_grid)
glyphs.SetSourceConnection(sphere.GetOutputPort())
glyphs.SetInputArrayToProcess(0, 0, 0, 0, "Sizes")
glyphs.SetInputArrayToProcess(3, 0, 0, 0, "Colors")

# Mapper and actor.
glyphs_mapper = vtkDataSetMapper()
glyphs_mapper.SetInputConnection(glyphs.GetOutputPort())

glyphs_actor = vtkActor()
glyphs_actor.SetMapper(glyphs_mapper)
glyphs_actor.GetProperty().BackfaceCullingOn()
glyphs_actor.GetProperty().SetDiffuseColor(1, 1, 1)

renderer = vtkRenderer()
renderer.SetBackground(0.1, 0.2, 0.4)
renderer.AddActor(glyphs_actor)

render_window = vtkRenderWindow()
render_window.SetSize(300, 300)
render_window.AddRenderer(renderer)
render_window.SetWindowName("scalar colors")

renderer.ResetCamera()
renderer.GetActiveCamera().Azimuth(30)
renderer.GetActiveCamera().Elevation(20)
renderer.GetActiveCamera().Dolly(1.25)
renderer.ResetCameraClippingRange()

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
