#!/usr/bin/env python

# Demonstrate vtkButterflySubdivisionFilter on a Schwarz minimal surface
# patch built from hand-crafted triangles, replicated via rotations and
# reflections, with feature edge tubes overlay.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import vtkMath, vtkPoints, vtkUnsignedCharArray
from vtkmodules.vtkCommonDataModel import vtkCellArray, vtkPolyData
from vtkmodules.vtkCommonTransforms import vtkTransform
from vtkmodules.vtkFiltersCore import (
    vtkAppendPolyData,
    vtkCleanPolyData,
    vtkFeatureEdges,
    vtkStripper,
    vtkTubeFilter,
)
from vtkmodules.vtkFiltersGeneral import vtkTransformPolyDataFilter
from vtkmodules.vtkFiltersModeling import vtkButterflySubdivisionFilter
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkDataSetMapper,
    vtkPolyDataMapper,
    vtkProperty,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Build base Schwarz surface patch
points = vtkPoints()
points.InsertNextPoint(2, 4, 0)
points.InsertNextPoint(2.6, 2.6, 0)
points.InsertNextPoint(4, 2, 0)
points.InsertNextPoint(1.4, 4, 1.4)
points.InsertNextPoint(2, 3, 1)
points.InsertNextPoint(3, 2, 1)
points.InsertNextPoint(4, 1.4, 1.4)
points.InsertNextPoint(0, 4, 2)
points.InsertNextPoint(1, 3, 2)
points.InsertNextPoint(2, 2, 2)
points.InsertNextPoint(3, 1, 2)
points.InsertNextPoint(4, 0, 2)
points.InsertNextPoint(0, 2.6, 2.6)
points.InsertNextPoint(1, 2, 3)
points.InsertNextPoint(2, 1, 3)
points.InsertNextPoint(2.6, 0, 2.6)
points.InsertNextPoint(0, 2, 4)
points.InsertNextPoint(1.4, 1.4, 4)
points.InsertNextPoint(2, 0, 4)

faces = vtkCellArray()
tri_indices = [
    (0, 3, 4), (0, 4, 1), (1, 4, 5), (1, 5, 2), (2, 5, 6),
    (3, 7, 8), (3, 8, 4), (4, 8, 9), (4, 9, 5), (5, 9, 10),
    (5, 10, 6), (6, 10, 11), (7, 12, 8), (8, 12, 13), (8, 13, 9),
    (9, 13, 14), (9, 14, 10), (10, 14, 15), (10, 15, 11),
    (12, 16, 13), (13, 16, 17), (13, 17, 14), (14, 17, 18), (14, 18, 15),
]
for tri in tri_indices:
    faces.InsertNextCell(3)
    for pt_id in tri:
        faces.InsertCellPoint(pt_id)

model = vtkPolyData()
model.SetPolys(faces)
model.SetPoints(points)

# Random cell colors
vtk_math = vtkMath()
cell_colors = vtkUnsignedCharArray()
cell_colors.SetNumberOfComponents(3)
cell_colors.SetNumberOfTuples(model.GetNumberOfCells())
for i in range(model.GetNumberOfCells()):
    cell_colors.InsertComponent(i, 0, vtk_math.Random(100, 255))
    cell_colors.InsertComponent(i, 1, vtk_math.Random(100, 255))
    cell_colors.InsertComponent(i, 2, vtk_math.Random(100, 255))
model.GetCellData().SetScalars(cell_colors)

# Replicate via 4 rotations around Z
transform_0 = vtkTransform()
transform_0.Identity()
transform_filter_0 = vtkTransformPolyDataFilter()
transform_filter_0.SetTransform(transform_0)
transform_filter_0.SetInputData(model)

transform_1 = vtkTransform()
transform_1.Identity()
transform_1.RotateZ(90)
transform_filter_1 = vtkTransformPolyDataFilter()
transform_filter_1.SetTransform(transform_1)
transform_filter_1.SetInputData(model)

transform_2 = vtkTransform()
transform_2.Identity()
transform_2.RotateZ(180)
transform_filter_2 = vtkTransformPolyDataFilter()
transform_filter_2.SetTransform(transform_2)
transform_filter_2.SetInputData(model)

transform_3 = vtkTransform()
transform_3.Identity()
transform_3.RotateZ(270)
transform_filter_3 = vtkTransformPolyDataFilter()
transform_filter_3.SetTransform(transform_3)
transform_filter_3.SetInputData(model)

append_rotations = vtkAppendPolyData()
append_rotations.AddInputConnection(transform_filter_0.GetOutputPort())
append_rotations.AddInputConnection(transform_filter_1.GetOutputPort())
append_rotations.AddInputConnection(transform_filter_2.GetOutputPort())
append_rotations.AddInputConnection(transform_filter_3.GetOutputPort())

# Reflect across X
transform_4 = vtkTransform()
transform_4.Identity()
transform_4.RotateX(180)
transform_filter_4 = vtkTransformPolyDataFilter()
transform_filter_4.SetTransform(transform_4)
transform_filter_4.SetInputConnection(append_rotations.GetOutputPort())

append_reflected = vtkAppendPolyData()
append_reflected.AddInputConnection(append_rotations.GetOutputPort())
append_reflected.AddInputConnection(transform_filter_4.GetOutputPort())

# Translate along Z
transform_5 = vtkTransform()
transform_5.Identity()
transform_5.Translate(0, 0, -8)
transform_filter_5 = vtkTransformPolyDataFilter()
transform_filter_5.SetTransform(transform_5)
transform_filter_5.SetInputConnection(append_reflected.GetOutputPort())

append_z_translated = vtkAppendPolyData()
append_z_translated.AddInputConnection(append_reflected.GetOutputPort())
append_z_translated.AddInputConnection(transform_filter_5.GetOutputPort())

# Translate along Y
transform_6 = vtkTransform()
transform_6.Identity()
transform_6.Translate(0, -8, 0)
transform_filter_6 = vtkTransformPolyDataFilter()
transform_filter_6.SetTransform(transform_6)
transform_filter_6.SetInputConnection(append_z_translated.GetOutputPort())

append_y_translated = vtkAppendPolyData()
append_y_translated.AddInputConnection(append_z_translated.GetOutputPort())
append_y_translated.AddInputConnection(transform_filter_6.GetOutputPort())

# Clean and subdivide
clean = vtkCleanPolyData()
clean.SetTolerance(0.001)
clean.SetInputConnection(append_y_translated.GetOutputPort())

subdivide = vtkButterflySubdivisionFilter()
subdivide.SetInputConnection(clean.GetOutputPort())
subdivide.SetNumberOfSubdivisions(3)

# Surface mapper
mapper = vtkDataSetMapper()
mapper.SetInputConnection(subdivide.GetOutputPort())

surface = vtkActor()
surface.SetMapper(mapper)
surface.GetProperty().SetDiffuseColor(1, 0.4, 0.3)
surface.GetProperty().SetSpecular(0.4)
surface.GetProperty().SetDiffuse(0.8)
surface.GetProperty().SetSpecularPower(40)

back_property = vtkProperty()
back_property.SetDiffuseColor(1, 1, 0.3)
surface.SetBackfaceProperty(back_property)

# Feature edges as tubes
feature_edges = vtkFeatureEdges()
feature_edges.SetInputConnection(subdivide.GetOutputPort())
feature_edges.SetFeatureAngle(100)

feature_edges_stripper = vtkStripper()
feature_edges_stripper.SetInputConnection(feature_edges.GetOutputPort())

feature_edges_tubes = vtkTubeFilter()
feature_edges_tubes.SetInputConnection(feature_edges_stripper.GetOutputPort())
feature_edges_tubes.SetRadius(0.1)

feature_edges_mapper = vtkPolyDataMapper()
feature_edges_mapper.SetInputConnection(feature_edges_tubes.GetOutputPort())

edges = vtkActor()
edges.SetMapper(feature_edges_mapper)
edges.GetProperty().SetDiffuseColor(0.2, 0.2, 0.2)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(surface)
renderer.AddActor(edges)
renderer.SetBackground(0.1, 0.2, 0.4)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(300, 300)
render_window.SetWindowName("schwarz")

# Scene
renderer.ResetCamera()
camera = renderer.GetActiveCamera()
camera.Azimuth(90)
renderer.ResetCamera()
camera.Zoom(1.5)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
