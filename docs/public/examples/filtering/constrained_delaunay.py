#!/usr/bin/env python

# Create a constrained Delaunay triangulation from defined polygon
# boundaries and visualize with tube edges.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonColor import vtkNamedColors
from vtkmodules.vtkCommonCore import vtkPoints
from vtkmodules.vtkCommonDataModel import (
    vtkCellArray,
    vtkPolyData,
)
from vtkmodules.vtkFiltersCore import (
    vtkDelaunay2D,
    vtkExtractEdges,
    vtkTubeFilter,
)
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

colors = vtkNamedColors()
peacock = [0.0, 0.0, 0.0]
colors.GetColorRGB("peacock", peacock)

# Generate the input points and constrained polygons
points = vtkPoints()
points.InsertPoint(0, 1, 4, 0)
points.InsertPoint(1, 3, 4, 0)
points.InsertPoint(2, 7, 4, 0)
points.InsertPoint(3, 11, 4, 0)
points.InsertPoint(4, 13, 4, 0)
points.InsertPoint(5, 13, 8, 0)
points.InsertPoint(6, 13, 12, 0)
points.InsertPoint(7, 10, 12, 0)
points.InsertPoint(8, 7, 12, 0)
points.InsertPoint(9, 4, 12, 0)
points.InsertPoint(10, 1, 12, 0)
points.InsertPoint(11, 1, 8, 0)
points.InsertPoint(12, 3.5, 5, 0)
points.InsertPoint(13, 4.5, 5, 0)
points.InsertPoint(14, 5.5, 8, 0)
points.InsertPoint(15, 6.5, 8, 0)
points.InsertPoint(16, 6.5, 5, 0)
points.InsertPoint(17, 7.5, 5, 0)
points.InsertPoint(18, 7.5, 8, 0)
points.InsertPoint(19, 9, 8, 0)
points.InsertPoint(20, 9, 5, 0)
points.InsertPoint(21, 10, 5, 0)
points.InsertPoint(22, 10, 7, 0)
points.InsertPoint(23, 11, 5, 0)
points.InsertPoint(24, 12, 5, 0)
points.InsertPoint(25, 10.5, 8, 0)
points.InsertPoint(26, 12, 11, 0)
points.InsertPoint(27, 11, 11, 0)
points.InsertPoint(28, 10, 9, 0)
points.InsertPoint(29, 10, 11, 0)
points.InsertPoint(30, 9, 11, 0)
points.InsertPoint(31, 9, 9, 0)
points.InsertPoint(32, 7.5, 9, 0)
points.InsertPoint(33, 7.5, 11, 0)
points.InsertPoint(34, 6.5, 11, 0)
points.InsertPoint(35, 6.5, 9, 0)
points.InsertPoint(36, 5, 9, 0)
points.InsertPoint(37, 4, 6, 0)
points.InsertPoint(38, 3, 9, 0)
points.InsertPoint(39, 2, 9, 0)

# Outer boundary polygon
polys = vtkCellArray()
polys.InsertNextCell(12)
for i in range(12):
    polys.InsertCellPoint(i)

# Inner constraint polygon
polys.InsertNextCell(28)
for i in range(39, 11, -1):
    polys.InsertCellPoint(i)

poly_data = vtkPolyData()
poly_data.SetPoints(points)
poly_data.SetPolys(polys)

# Constrained Delaunay triangulation
del2d = vtkDelaunay2D()
del2d.SetInputData(poly_data)
del2d.SetSourceData(poly_data)

mesh_mapper = vtkPolyDataMapper()
mesh_mapper.SetInputConnection(del2d.GetOutputPort())

mesh_actor = vtkActor()
mesh_actor.SetMapper(mesh_mapper)

# Tubes around mesh edges
extract = vtkExtractEdges()
extract.SetInputConnection(del2d.GetOutputPort())

tubes = vtkTubeFilter()
tubes.SetInputConnection(extract.GetOutputPort())
tubes.SetRadius(0.1)
tubes.SetNumberOfSides(6)

edge_mapper = vtkPolyDataMapper()
edge_mapper.SetInputConnection(tubes.GetOutputPort())

edge_actor = vtkActor()
edge_actor.SetMapper(edge_mapper)
edge_actor.GetProperty().SetColor(peacock)
edge_actor.GetProperty().SetSpecularColor(1, 1, 1)
edge_actor.GetProperty().SetSpecular(0.3)
edge_actor.GetProperty().SetSpecularPower(20)
edge_actor.GetProperty().SetAmbient(0.2)
edge_actor.GetProperty().SetDiffuse(0.8)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(mesh_actor)
renderer.AddActor(edge_actor)
renderer.SetBackground(0, 0, 0)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(450, 300)
render_window.SetWindowName("constrained delaunay")

# Scene
renderer.ResetCamera()
renderer.GetActiveCamera().Zoom(2)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
