#!/usr/bin/env python
# Demonstrate vtkKdTree representation with point glyphs and wireframe bounding boxes.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import vtkPoints
from vtkmodules.vtkCommonDataModel import vtkKdTree, vtkPolyData, vtkCellArray
from vtkmodules.vtkFiltersCore import vtkGlyph3D
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Random points (pre-generated).
glyph_size = 0.05
point_coords = [
    [0.840188, 0.394383, 0.783099],
    [0.79844, 0.911647, 0.197551],
    [0.335223, 0.76823, 0.277775],
    [0.55397, 0.477397, 0.628871],
    [0.364784, 0.513401, 0.95223],
    [0.916195, 0.635712, 0.717297],
    [0.141603, 0.606969, 0.0163006],
    [0.242887, 0.137232, 0.804177],
    [0.156679, 0.400944, 0.12979],
    [0.108809, 0.998925, 0.218257],
]

# Generate point data.
point_data = vtkPolyData()
points = vtkPoints()
points.SetDataTypeToDouble()
points.SetNumberOfPoints(len(point_coords))
point_data.AllocateEstimate(len(point_coords), 1)
cells = vtkCellArray()
for i, pt in enumerate(point_coords):
    points.SetPoint(i, pt)
    cells.InsertNextCell(1, [i])
point_data.SetPoints(points)
point_data.SetVerts(cells)

# Create a kd-tree.
kd_tree = vtkKdTree()
kd_tree.SetMinCells(1)
kd_tree.BuildLocatorFromPoints(points)

# Generate a kd-tree representation.
kd_tree_repr = vtkPolyData()
kd_tree.GenerateRepresentation(2, kd_tree_repr)
kd_tree_repr_mapper = vtkPolyDataMapper()
kd_tree_repr_mapper.SetInputData(kd_tree_repr)

kd_tree_repr_actor = vtkActor()
kd_tree_repr_actor.SetMapper(kd_tree_repr_mapper)
kd_tree_repr_actor.GetProperty().SetColor(1.0, 1.0, 1.0)
kd_tree_repr_actor.GetProperty().SetRepresentationToWireframe()
kd_tree_repr_actor.GetProperty().SetLineWidth(4)
kd_tree_repr_actor.GetProperty().LightingOff()

# Create vertex glyphs.
sphere = vtkSphereSource()
sphere.SetRadius(glyph_size)

glyph = vtkGlyph3D()
glyph.SetInputData(0, point_data)
glyph.SetInputConnection(1, sphere.GetOutputPort())

glyph_mapper = vtkPolyDataMapper()
glyph_mapper.SetInputConnection(glyph.GetOutputPort())

glyph_actor = vtkActor()
glyph_actor.SetMapper(glyph_mapper)

# Standard rendering pipeline.
renderer = vtkRenderer()
renderer.AddActor(glyph_actor)
renderer.AddActor(kd_tree_repr_actor)

render_window = vtkRenderWindow()
render_window.SetSize(400, 400)
render_window.AddRenderer(renderer)
render_window.SetWindowName("kd tree representation")

renderer.GetActiveCamera().SetPosition(-10, 10, 20)
renderer.GetActiveCamera().SetFocalPoint(0, 0, 0)
renderer.ResetCamera()

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
