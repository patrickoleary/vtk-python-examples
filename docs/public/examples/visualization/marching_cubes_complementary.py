#!/usr/bin/env python

# Display marching cubes complementary cases 3c, 6c, 7c, 10c, 12c, and 13c.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkCommonCore import (
    vtkFloatArray,
    vtkIdList,
    vtkPoints,
)
from vtkmodules.vtkCommonDataModel import vtkUnstructuredGrid
from vtkmodules.vtkCommonTransforms import vtkTransform
from vtkmodules.vtkFiltersCore import (
    vtkContourFilter,
    vtkExtractEdges,
    vtkGlyph3D,
    vtkThresholdPoints,
    vtkTubeFilter,
)
from vtkmodules.vtkFiltersGeneral import (
    vtkShrinkPolyData,
    vtkTransformPolyDataFilter,
)
from vtkmodules.vtkFiltersSources import (
    vtkCubeSource,
    vtkSphereSource,
)
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)
from vtkmodules.vtkRenderingFreeType import vtkVectorText

# Colors (normalized RGB)
slate_grey = (0.439, 0.502, 0.565)
lamp_black = (0.180, 0.278, 0.231)
banana = (0.890, 0.812, 0.341)
khaki = (0.941, 0.902, 0.549)
tomato = (1.000, 0.388, 0.278)

# Viewport grid: 3 columns x 2 rows = 6 slots
x_grid = 3
y_grid = 2
renderer_size = 300

renderer_0 = vtkRenderer()
renderer_0.SetBackground(slate_grey)
renderer_1 = vtkRenderer()
renderer_1.SetBackground(slate_grey)
renderer_2 = vtkRenderer()
renderer_2.SetBackground(slate_grey)
renderer_3 = vtkRenderer()
renderer_3.SetBackground(slate_grey)
renderer_4 = vtkRenderer()
renderer_4.SetBackground(slate_grey)
renderer_5 = vtkRenderer()
renderer_5.SetBackground(slate_grey)

# --- Case 3c: base [1,0,1,0,0,0,0,0] inverted to [0,1,0,1,1,1,1,1] ---

case_0_scalars = vtkFloatArray()
case_0_scalars.InsertNextValue(0.0)
case_0_scalars.InsertNextValue(1.0)
case_0_scalars.InsertNextValue(0.0)
case_0_scalars.InsertNextValue(1.0)
case_0_scalars.InsertNextValue(1.0)
case_0_scalars.InsertNextValue(1.0)
case_0_scalars.InsertNextValue(1.0)
case_0_scalars.InsertNextValue(1.0)

case_0_points = vtkPoints()
case_0_points.InsertNextPoint(0, 0, 0)
case_0_points.InsertNextPoint(1, 0, 0)
case_0_points.InsertNextPoint(1, 1, 0)
case_0_points.InsertNextPoint(0, 1, 0)
case_0_points.InsertNextPoint(0, 0, 1)
case_0_points.InsertNextPoint(1, 0, 1)
case_0_points.InsertNextPoint(1, 1, 1)
case_0_points.InsertNextPoint(0, 1, 1)

case_0_ids = vtkIdList()
case_0_ids.InsertNextId(0)
case_0_ids.InsertNextId(1)
case_0_ids.InsertNextId(2)
case_0_ids.InsertNextId(3)
case_0_ids.InsertNextId(4)
case_0_ids.InsertNextId(5)
case_0_ids.InsertNextId(6)
case_0_ids.InsertNextId(7)

case_0_grid = vtkUnstructuredGrid()
case_0_grid.Allocate(10, 10)
case_0_grid.InsertNextCell(12, case_0_ids)
case_0_grid.SetPoints(case_0_points)
case_0_grid.GetPointData().SetScalars(case_0_scalars)

case_0_marching = vtkContourFilter()
case_0_marching.SetInputData(case_0_grid)
case_0_marching.SetValue(0, 0.5)
case_0_marching.Update()

case_0_triangle_edges = vtkExtractEdges()
case_0_triangle_edges.SetInputConnection(case_0_marching.GetOutputPort())

case_0_triangle_edge_tubes = vtkTubeFilter()
case_0_triangle_edge_tubes.SetInputConnection(case_0_triangle_edges.GetOutputPort())
case_0_triangle_edge_tubes.SetRadius(0.005)
case_0_triangle_edge_tubes.SetNumberOfSides(6)
case_0_triangle_edge_tubes.UseDefaultNormalOn()
case_0_triangle_edge_tubes.SetDefaultNormal(0.577, 0.577, 0.577)

case_0_triangle_edge_mapper = vtkPolyDataMapper()
case_0_triangle_edge_mapper.SetInputConnection(case_0_triangle_edge_tubes.GetOutputPort())
case_0_triangle_edge_mapper.ScalarVisibilityOff()

case_0_triangle_edge_actor = vtkActor()
case_0_triangle_edge_actor.SetMapper(case_0_triangle_edge_mapper)
case_0_triangle_edge_actor.GetProperty().SetDiffuseColor(lamp_black)
case_0_triangle_edge_actor.GetProperty().SetSpecular(0.4)
case_0_triangle_edge_actor.GetProperty().SetSpecularPower(10)

case_0_shrinker = vtkShrinkPolyData()
case_0_shrinker.SetShrinkFactor(1)
case_0_shrinker.SetInputConnection(case_0_marching.GetOutputPort())

case_0_triangle_mapper = vtkPolyDataMapper()
case_0_triangle_mapper.ScalarVisibilityOff()
case_0_triangle_mapper.SetInputConnection(case_0_shrinker.GetOutputPort())

case_0_triangle_actor = vtkActor()
case_0_triangle_actor.SetMapper(case_0_triangle_mapper)
case_0_triangle_actor.GetProperty().SetDiffuseColor(banana)
case_0_triangle_actor.GetProperty().SetOpacity(0.6)

case_0_cube_model = vtkCubeSource()
case_0_cube_model.SetCenter(0.5, 0.5, 0.5)

case_0_cube_edges_filter = vtkExtractEdges()
case_0_cube_edges_filter.SetInputConnection(case_0_cube_model.GetOutputPort())

case_0_cube_tubes = vtkTubeFilter()
case_0_cube_tubes.SetInputConnection(case_0_cube_edges_filter.GetOutputPort())
case_0_cube_tubes.SetRadius(0.01)
case_0_cube_tubes.SetNumberOfSides(6)
case_0_cube_tubes.UseDefaultNormalOn()
case_0_cube_tubes.SetDefaultNormal(0.577, 0.577, 0.577)

case_0_cube_tube_mapper = vtkPolyDataMapper()
case_0_cube_tube_mapper.SetInputConnection(case_0_cube_tubes.GetOutputPort())

case_0_cube_edges_actor = vtkActor()
case_0_cube_edges_actor.SetMapper(case_0_cube_tube_mapper)
case_0_cube_edges_actor.GetProperty().SetDiffuseColor(khaki)
case_0_cube_edges_actor.GetProperty().SetSpecular(0.4)
case_0_cube_edges_actor.GetProperty().SetSpecularPower(10)

case_0_sphere_source = vtkSphereSource()
case_0_sphere_source.SetRadius(0.04)
case_0_sphere_source.SetPhiResolution(20)
case_0_sphere_source.SetThetaResolution(20)

case_0_threshold_in = vtkThresholdPoints()
case_0_threshold_in.SetInputData(case_0_grid)
case_0_threshold_in.SetUpperThreshold(0.5)
case_0_threshold_in.SetThresholdFunction(case_0_threshold_in.THRESHOLD_UPPER)

case_0_vertices_glyph = vtkGlyph3D()
case_0_vertices_glyph.SetInputConnection(case_0_threshold_in.GetOutputPort())
case_0_vertices_glyph.SetSourceConnection(case_0_sphere_source.GetOutputPort())

case_0_sphere_mapper = vtkPolyDataMapper()
case_0_sphere_mapper.SetInputConnection(case_0_vertices_glyph.GetOutputPort())
case_0_sphere_mapper.ScalarVisibilityOff()

case_0_cube_vertices_actor = vtkActor()
case_0_cube_vertices_actor.SetMapper(case_0_sphere_mapper)
case_0_cube_vertices_actor.GetProperty().SetDiffuseColor(tomato)

case_0_case_label = vtkVectorText()
case_0_case_label.SetText("Case 3c - 11111010")

case_0_label_xform = vtkTransform()
case_0_label_xform.Identity()
case_0_label_xform.Translate(-0.2, 0, 1.25)
case_0_label_xform.Scale(0.05, 0.05, 0.05)

case_0_label_transform_filter = vtkTransformPolyDataFilter()
case_0_label_transform_filter.SetTransform(case_0_label_xform)
case_0_label_transform_filter.SetInputConnection(case_0_case_label.GetOutputPort())

case_0_label_mapper = vtkPolyDataMapper()
case_0_label_mapper.SetInputConnection(case_0_label_transform_filter.GetOutputPort())

case_0_label_actor = vtkActor()
case_0_label_actor.SetMapper(case_0_label_mapper)

case_0_base_model = vtkCubeSource()
case_0_base_model.SetXLength(1.5)
case_0_base_model.SetYLength(0.01)
case_0_base_model.SetZLength(1.5)

case_0_base_mapper = vtkPolyDataMapper()
case_0_base_mapper.SetInputConnection(case_0_base_model.GetOutputPort())

case_0_base_actor = vtkActor()
case_0_base_actor.SetMapper(case_0_base_mapper)
case_0_base_actor.SetPosition(0.5, -0.09, 0.5)

renderer_0.AddActor(case_0_triangle_edge_actor)
renderer_0.AddActor(case_0_base_actor)
renderer_0.AddActor(case_0_label_actor)
renderer_0.AddActor(case_0_cube_edges_actor)
renderer_0.AddActor(case_0_cube_vertices_actor)
renderer_0.AddActor(case_0_triangle_actor)

# --- Case 6c: base [0,1,0,1,1,0,0,0] inverted to [1,0,1,0,0,1,1,1] ---

case_1_scalars = vtkFloatArray()
case_1_scalars.InsertNextValue(1.0)
case_1_scalars.InsertNextValue(0.0)
case_1_scalars.InsertNextValue(1.0)
case_1_scalars.InsertNextValue(0.0)
case_1_scalars.InsertNextValue(0.0)
case_1_scalars.InsertNextValue(1.0)
case_1_scalars.InsertNextValue(1.0)
case_1_scalars.InsertNextValue(1.0)

case_1_points = vtkPoints()
case_1_points.InsertNextPoint(0, 0, 0)
case_1_points.InsertNextPoint(1, 0, 0)
case_1_points.InsertNextPoint(1, 1, 0)
case_1_points.InsertNextPoint(0, 1, 0)
case_1_points.InsertNextPoint(0, 0, 1)
case_1_points.InsertNextPoint(1, 0, 1)
case_1_points.InsertNextPoint(1, 1, 1)
case_1_points.InsertNextPoint(0, 1, 1)

case_1_ids = vtkIdList()
case_1_ids.InsertNextId(0)
case_1_ids.InsertNextId(1)
case_1_ids.InsertNextId(2)
case_1_ids.InsertNextId(3)
case_1_ids.InsertNextId(4)
case_1_ids.InsertNextId(5)
case_1_ids.InsertNextId(6)
case_1_ids.InsertNextId(7)

case_1_grid = vtkUnstructuredGrid()
case_1_grid.Allocate(10, 10)
case_1_grid.InsertNextCell(12, case_1_ids)
case_1_grid.SetPoints(case_1_points)
case_1_grid.GetPointData().SetScalars(case_1_scalars)

case_1_marching = vtkContourFilter()
case_1_marching.SetInputData(case_1_grid)
case_1_marching.SetValue(0, 0.5)
case_1_marching.Update()

case_1_triangle_edges = vtkExtractEdges()
case_1_triangle_edges.SetInputConnection(case_1_marching.GetOutputPort())

case_1_triangle_edge_tubes = vtkTubeFilter()
case_1_triangle_edge_tubes.SetInputConnection(case_1_triangle_edges.GetOutputPort())
case_1_triangle_edge_tubes.SetRadius(0.005)
case_1_triangle_edge_tubes.SetNumberOfSides(6)
case_1_triangle_edge_tubes.UseDefaultNormalOn()
case_1_triangle_edge_tubes.SetDefaultNormal(0.577, 0.577, 0.577)

case_1_triangle_edge_mapper = vtkPolyDataMapper()
case_1_triangle_edge_mapper.SetInputConnection(case_1_triangle_edge_tubes.GetOutputPort())
case_1_triangle_edge_mapper.ScalarVisibilityOff()

case_1_triangle_edge_actor = vtkActor()
case_1_triangle_edge_actor.SetMapper(case_1_triangle_edge_mapper)
case_1_triangle_edge_actor.GetProperty().SetDiffuseColor(lamp_black)
case_1_triangle_edge_actor.GetProperty().SetSpecular(0.4)
case_1_triangle_edge_actor.GetProperty().SetSpecularPower(10)

case_1_shrinker = vtkShrinkPolyData()
case_1_shrinker.SetShrinkFactor(1)
case_1_shrinker.SetInputConnection(case_1_marching.GetOutputPort())

case_1_triangle_mapper = vtkPolyDataMapper()
case_1_triangle_mapper.ScalarVisibilityOff()
case_1_triangle_mapper.SetInputConnection(case_1_shrinker.GetOutputPort())

case_1_triangle_actor = vtkActor()
case_1_triangle_actor.SetMapper(case_1_triangle_mapper)
case_1_triangle_actor.GetProperty().SetDiffuseColor(banana)
case_1_triangle_actor.GetProperty().SetOpacity(0.6)

case_1_cube_model = vtkCubeSource()
case_1_cube_model.SetCenter(0.5, 0.5, 0.5)

case_1_cube_edges_filter = vtkExtractEdges()
case_1_cube_edges_filter.SetInputConnection(case_1_cube_model.GetOutputPort())

case_1_cube_tubes = vtkTubeFilter()
case_1_cube_tubes.SetInputConnection(case_1_cube_edges_filter.GetOutputPort())
case_1_cube_tubes.SetRadius(0.01)
case_1_cube_tubes.SetNumberOfSides(6)
case_1_cube_tubes.UseDefaultNormalOn()
case_1_cube_tubes.SetDefaultNormal(0.577, 0.577, 0.577)

case_1_cube_tube_mapper = vtkPolyDataMapper()
case_1_cube_tube_mapper.SetInputConnection(case_1_cube_tubes.GetOutputPort())

case_1_cube_edges_actor = vtkActor()
case_1_cube_edges_actor.SetMapper(case_1_cube_tube_mapper)
case_1_cube_edges_actor.GetProperty().SetDiffuseColor(khaki)
case_1_cube_edges_actor.GetProperty().SetSpecular(0.4)
case_1_cube_edges_actor.GetProperty().SetSpecularPower(10)

case_1_sphere_source = vtkSphereSource()
case_1_sphere_source.SetRadius(0.04)
case_1_sphere_source.SetPhiResolution(20)
case_1_sphere_source.SetThetaResolution(20)

case_1_threshold_in = vtkThresholdPoints()
case_1_threshold_in.SetInputData(case_1_grid)
case_1_threshold_in.SetUpperThreshold(0.5)
case_1_threshold_in.SetThresholdFunction(case_1_threshold_in.THRESHOLD_UPPER)

case_1_vertices_glyph = vtkGlyph3D()
case_1_vertices_glyph.SetInputConnection(case_1_threshold_in.GetOutputPort())
case_1_vertices_glyph.SetSourceConnection(case_1_sphere_source.GetOutputPort())

case_1_sphere_mapper = vtkPolyDataMapper()
case_1_sphere_mapper.SetInputConnection(case_1_vertices_glyph.GetOutputPort())
case_1_sphere_mapper.ScalarVisibilityOff()

case_1_cube_vertices_actor = vtkActor()
case_1_cube_vertices_actor.SetMapper(case_1_sphere_mapper)
case_1_cube_vertices_actor.GetProperty().SetDiffuseColor(tomato)

case_1_case_label = vtkVectorText()
case_1_case_label.SetText("Case 6c - 11100101")

case_1_label_xform = vtkTransform()
case_1_label_xform.Identity()
case_1_label_xform.Translate(-0.2, 0, 1.25)
case_1_label_xform.Scale(0.05, 0.05, 0.05)

case_1_label_transform_filter = vtkTransformPolyDataFilter()
case_1_label_transform_filter.SetTransform(case_1_label_xform)
case_1_label_transform_filter.SetInputConnection(case_1_case_label.GetOutputPort())

case_1_label_mapper = vtkPolyDataMapper()
case_1_label_mapper.SetInputConnection(case_1_label_transform_filter.GetOutputPort())

case_1_label_actor = vtkActor()
case_1_label_actor.SetMapper(case_1_label_mapper)

case_1_base_model = vtkCubeSource()
case_1_base_model.SetXLength(1.5)
case_1_base_model.SetYLength(0.01)
case_1_base_model.SetZLength(1.5)

case_1_base_mapper = vtkPolyDataMapper()
case_1_base_mapper.SetInputConnection(case_1_base_model.GetOutputPort())

case_1_base_actor = vtkActor()
case_1_base_actor.SetMapper(case_1_base_mapper)
case_1_base_actor.SetPosition(0.5, -0.09, 0.5)

renderer_1.AddActor(case_1_triangle_edge_actor)
renderer_1.AddActor(case_1_base_actor)
renderer_1.AddActor(case_1_label_actor)
renderer_1.AddActor(case_1_cube_edges_actor)
renderer_1.AddActor(case_1_cube_vertices_actor)
renderer_1.AddActor(case_1_triangle_actor)

# --- Case 7c: base [1,1,0,0,0,0,1,0] inverted to [0,0,1,1,1,1,0,1] ---

case_2_scalars = vtkFloatArray()
case_2_scalars.InsertNextValue(0.0)
case_2_scalars.InsertNextValue(0.0)
case_2_scalars.InsertNextValue(1.0)
case_2_scalars.InsertNextValue(1.0)
case_2_scalars.InsertNextValue(1.0)
case_2_scalars.InsertNextValue(1.0)
case_2_scalars.InsertNextValue(0.0)
case_2_scalars.InsertNextValue(1.0)

case_2_points = vtkPoints()
case_2_points.InsertNextPoint(0, 0, 0)
case_2_points.InsertNextPoint(1, 0, 0)
case_2_points.InsertNextPoint(1, 1, 0)
case_2_points.InsertNextPoint(0, 1, 0)
case_2_points.InsertNextPoint(0, 0, 1)
case_2_points.InsertNextPoint(1, 0, 1)
case_2_points.InsertNextPoint(1, 1, 1)
case_2_points.InsertNextPoint(0, 1, 1)

case_2_ids = vtkIdList()
case_2_ids.InsertNextId(0)
case_2_ids.InsertNextId(1)
case_2_ids.InsertNextId(2)
case_2_ids.InsertNextId(3)
case_2_ids.InsertNextId(4)
case_2_ids.InsertNextId(5)
case_2_ids.InsertNextId(6)
case_2_ids.InsertNextId(7)

case_2_grid = vtkUnstructuredGrid()
case_2_grid.Allocate(10, 10)
case_2_grid.InsertNextCell(12, case_2_ids)
case_2_grid.SetPoints(case_2_points)
case_2_grid.GetPointData().SetScalars(case_2_scalars)

case_2_marching = vtkContourFilter()
case_2_marching.SetInputData(case_2_grid)
case_2_marching.SetValue(0, 0.5)
case_2_marching.Update()

case_2_triangle_edges = vtkExtractEdges()
case_2_triangle_edges.SetInputConnection(case_2_marching.GetOutputPort())

case_2_triangle_edge_tubes = vtkTubeFilter()
case_2_triangle_edge_tubes.SetInputConnection(case_2_triangle_edges.GetOutputPort())
case_2_triangle_edge_tubes.SetRadius(0.005)
case_2_triangle_edge_tubes.SetNumberOfSides(6)
case_2_triangle_edge_tubes.UseDefaultNormalOn()
case_2_triangle_edge_tubes.SetDefaultNormal(0.577, 0.577, 0.577)

case_2_triangle_edge_mapper = vtkPolyDataMapper()
case_2_triangle_edge_mapper.SetInputConnection(case_2_triangle_edge_tubes.GetOutputPort())
case_2_triangle_edge_mapper.ScalarVisibilityOff()

case_2_triangle_edge_actor = vtkActor()
case_2_triangle_edge_actor.SetMapper(case_2_triangle_edge_mapper)
case_2_triangle_edge_actor.GetProperty().SetDiffuseColor(lamp_black)
case_2_triangle_edge_actor.GetProperty().SetSpecular(0.4)
case_2_triangle_edge_actor.GetProperty().SetSpecularPower(10)

case_2_shrinker = vtkShrinkPolyData()
case_2_shrinker.SetShrinkFactor(1)
case_2_shrinker.SetInputConnection(case_2_marching.GetOutputPort())

case_2_triangle_mapper = vtkPolyDataMapper()
case_2_triangle_mapper.ScalarVisibilityOff()
case_2_triangle_mapper.SetInputConnection(case_2_shrinker.GetOutputPort())

case_2_triangle_actor = vtkActor()
case_2_triangle_actor.SetMapper(case_2_triangle_mapper)
case_2_triangle_actor.GetProperty().SetDiffuseColor(banana)
case_2_triangle_actor.GetProperty().SetOpacity(0.6)

case_2_cube_model = vtkCubeSource()
case_2_cube_model.SetCenter(0.5, 0.5, 0.5)

case_2_cube_edges_filter = vtkExtractEdges()
case_2_cube_edges_filter.SetInputConnection(case_2_cube_model.GetOutputPort())

case_2_cube_tubes = vtkTubeFilter()
case_2_cube_tubes.SetInputConnection(case_2_cube_edges_filter.GetOutputPort())
case_2_cube_tubes.SetRadius(0.01)
case_2_cube_tubes.SetNumberOfSides(6)
case_2_cube_tubes.UseDefaultNormalOn()
case_2_cube_tubes.SetDefaultNormal(0.577, 0.577, 0.577)

case_2_cube_tube_mapper = vtkPolyDataMapper()
case_2_cube_tube_mapper.SetInputConnection(case_2_cube_tubes.GetOutputPort())

case_2_cube_edges_actor = vtkActor()
case_2_cube_edges_actor.SetMapper(case_2_cube_tube_mapper)
case_2_cube_edges_actor.GetProperty().SetDiffuseColor(khaki)
case_2_cube_edges_actor.GetProperty().SetSpecular(0.4)
case_2_cube_edges_actor.GetProperty().SetSpecularPower(10)

case_2_sphere_source = vtkSphereSource()
case_2_sphere_source.SetRadius(0.04)
case_2_sphere_source.SetPhiResolution(20)
case_2_sphere_source.SetThetaResolution(20)

case_2_threshold_in = vtkThresholdPoints()
case_2_threshold_in.SetInputData(case_2_grid)
case_2_threshold_in.SetUpperThreshold(0.5)
case_2_threshold_in.SetThresholdFunction(case_2_threshold_in.THRESHOLD_UPPER)

case_2_vertices_glyph = vtkGlyph3D()
case_2_vertices_glyph.SetInputConnection(case_2_threshold_in.GetOutputPort())
case_2_vertices_glyph.SetSourceConnection(case_2_sphere_source.GetOutputPort())

case_2_sphere_mapper = vtkPolyDataMapper()
case_2_sphere_mapper.SetInputConnection(case_2_vertices_glyph.GetOutputPort())
case_2_sphere_mapper.ScalarVisibilityOff()

case_2_cube_vertices_actor = vtkActor()
case_2_cube_vertices_actor.SetMapper(case_2_sphere_mapper)
case_2_cube_vertices_actor.GetProperty().SetDiffuseColor(tomato)

case_2_case_label = vtkVectorText()
case_2_case_label.SetText("Case 7c - 10111100")

case_2_label_xform = vtkTransform()
case_2_label_xform.Identity()
case_2_label_xform.Translate(-0.2, 0, 1.25)
case_2_label_xform.Scale(0.05, 0.05, 0.05)

case_2_label_transform_filter = vtkTransformPolyDataFilter()
case_2_label_transform_filter.SetTransform(case_2_label_xform)
case_2_label_transform_filter.SetInputConnection(case_2_case_label.GetOutputPort())

case_2_label_mapper = vtkPolyDataMapper()
case_2_label_mapper.SetInputConnection(case_2_label_transform_filter.GetOutputPort())

case_2_label_actor = vtkActor()
case_2_label_actor.SetMapper(case_2_label_mapper)

case_2_base_model = vtkCubeSource()
case_2_base_model.SetXLength(1.5)
case_2_base_model.SetYLength(0.01)
case_2_base_model.SetZLength(1.5)

case_2_base_mapper = vtkPolyDataMapper()
case_2_base_mapper.SetInputConnection(case_2_base_model.GetOutputPort())

case_2_base_actor = vtkActor()
case_2_base_actor.SetMapper(case_2_base_mapper)
case_2_base_actor.SetPosition(0.5, -0.09, 0.5)

renderer_2.AddActor(case_2_triangle_edge_actor)
renderer_2.AddActor(case_2_base_actor)
renderer_2.AddActor(case_2_label_actor)
renderer_2.AddActor(case_2_cube_edges_actor)
renderer_2.AddActor(case_2_cube_vertices_actor)
renderer_2.AddActor(case_2_triangle_actor)

# --- Case 10c: base [1,0,0,1,0,1,1,0] inverted to [0,1,1,0,1,0,0,1] ---

case_3_scalars = vtkFloatArray()
case_3_scalars.InsertNextValue(0.0)
case_3_scalars.InsertNextValue(1.0)
case_3_scalars.InsertNextValue(1.0)
case_3_scalars.InsertNextValue(0.0)
case_3_scalars.InsertNextValue(1.0)
case_3_scalars.InsertNextValue(0.0)
case_3_scalars.InsertNextValue(0.0)
case_3_scalars.InsertNextValue(1.0)

case_3_points = vtkPoints()
case_3_points.InsertNextPoint(0, 0, 0)
case_3_points.InsertNextPoint(1, 0, 0)
case_3_points.InsertNextPoint(1, 1, 0)
case_3_points.InsertNextPoint(0, 1, 0)
case_3_points.InsertNextPoint(0, 0, 1)
case_3_points.InsertNextPoint(1, 0, 1)
case_3_points.InsertNextPoint(1, 1, 1)
case_3_points.InsertNextPoint(0, 1, 1)

case_3_ids = vtkIdList()
case_3_ids.InsertNextId(0)
case_3_ids.InsertNextId(1)
case_3_ids.InsertNextId(2)
case_3_ids.InsertNextId(3)
case_3_ids.InsertNextId(4)
case_3_ids.InsertNextId(5)
case_3_ids.InsertNextId(6)
case_3_ids.InsertNextId(7)

case_3_grid = vtkUnstructuredGrid()
case_3_grid.Allocate(10, 10)
case_3_grid.InsertNextCell(12, case_3_ids)
case_3_grid.SetPoints(case_3_points)
case_3_grid.GetPointData().SetScalars(case_3_scalars)

case_3_marching = vtkContourFilter()
case_3_marching.SetInputData(case_3_grid)
case_3_marching.SetValue(0, 0.5)
case_3_marching.Update()

case_3_triangle_edges = vtkExtractEdges()
case_3_triangle_edges.SetInputConnection(case_3_marching.GetOutputPort())

case_3_triangle_edge_tubes = vtkTubeFilter()
case_3_triangle_edge_tubes.SetInputConnection(case_3_triangle_edges.GetOutputPort())
case_3_triangle_edge_tubes.SetRadius(0.005)
case_3_triangle_edge_tubes.SetNumberOfSides(6)
case_3_triangle_edge_tubes.UseDefaultNormalOn()
case_3_triangle_edge_tubes.SetDefaultNormal(0.577, 0.577, 0.577)

case_3_triangle_edge_mapper = vtkPolyDataMapper()
case_3_triangle_edge_mapper.SetInputConnection(case_3_triangle_edge_tubes.GetOutputPort())
case_3_triangle_edge_mapper.ScalarVisibilityOff()

case_3_triangle_edge_actor = vtkActor()
case_3_triangle_edge_actor.SetMapper(case_3_triangle_edge_mapper)
case_3_triangle_edge_actor.GetProperty().SetDiffuseColor(lamp_black)
case_3_triangle_edge_actor.GetProperty().SetSpecular(0.4)
case_3_triangle_edge_actor.GetProperty().SetSpecularPower(10)

case_3_shrinker = vtkShrinkPolyData()
case_3_shrinker.SetShrinkFactor(1)
case_3_shrinker.SetInputConnection(case_3_marching.GetOutputPort())

case_3_triangle_mapper = vtkPolyDataMapper()
case_3_triangle_mapper.ScalarVisibilityOff()
case_3_triangle_mapper.SetInputConnection(case_3_shrinker.GetOutputPort())

case_3_triangle_actor = vtkActor()
case_3_triangle_actor.SetMapper(case_3_triangle_mapper)
case_3_triangle_actor.GetProperty().SetDiffuseColor(banana)
case_3_triangle_actor.GetProperty().SetOpacity(0.6)

case_3_cube_model = vtkCubeSource()
case_3_cube_model.SetCenter(0.5, 0.5, 0.5)

case_3_cube_edges_filter = vtkExtractEdges()
case_3_cube_edges_filter.SetInputConnection(case_3_cube_model.GetOutputPort())

case_3_cube_tubes = vtkTubeFilter()
case_3_cube_tubes.SetInputConnection(case_3_cube_edges_filter.GetOutputPort())
case_3_cube_tubes.SetRadius(0.01)
case_3_cube_tubes.SetNumberOfSides(6)
case_3_cube_tubes.UseDefaultNormalOn()
case_3_cube_tubes.SetDefaultNormal(0.577, 0.577, 0.577)

case_3_cube_tube_mapper = vtkPolyDataMapper()
case_3_cube_tube_mapper.SetInputConnection(case_3_cube_tubes.GetOutputPort())

case_3_cube_edges_actor = vtkActor()
case_3_cube_edges_actor.SetMapper(case_3_cube_tube_mapper)
case_3_cube_edges_actor.GetProperty().SetDiffuseColor(khaki)
case_3_cube_edges_actor.GetProperty().SetSpecular(0.4)
case_3_cube_edges_actor.GetProperty().SetSpecularPower(10)

case_3_sphere_source = vtkSphereSource()
case_3_sphere_source.SetRadius(0.04)
case_3_sphere_source.SetPhiResolution(20)
case_3_sphere_source.SetThetaResolution(20)

case_3_threshold_in = vtkThresholdPoints()
case_3_threshold_in.SetInputData(case_3_grid)
case_3_threshold_in.SetUpperThreshold(0.5)
case_3_threshold_in.SetThresholdFunction(case_3_threshold_in.THRESHOLD_UPPER)

case_3_vertices_glyph = vtkGlyph3D()
case_3_vertices_glyph.SetInputConnection(case_3_threshold_in.GetOutputPort())
case_3_vertices_glyph.SetSourceConnection(case_3_sphere_source.GetOutputPort())

case_3_sphere_mapper = vtkPolyDataMapper()
case_3_sphere_mapper.SetInputConnection(case_3_vertices_glyph.GetOutputPort())
case_3_sphere_mapper.ScalarVisibilityOff()

case_3_cube_vertices_actor = vtkActor()
case_3_cube_vertices_actor.SetMapper(case_3_sphere_mapper)
case_3_cube_vertices_actor.GetProperty().SetDiffuseColor(tomato)

case_3_case_label = vtkVectorText()
case_3_case_label.SetText("Case 10c - 10010110")

case_3_label_xform = vtkTransform()
case_3_label_xform.Identity()
case_3_label_xform.Translate(-0.2, 0, 1.25)
case_3_label_xform.Scale(0.05, 0.05, 0.05)

case_3_label_transform_filter = vtkTransformPolyDataFilter()
case_3_label_transform_filter.SetTransform(case_3_label_xform)
case_3_label_transform_filter.SetInputConnection(case_3_case_label.GetOutputPort())

case_3_label_mapper = vtkPolyDataMapper()
case_3_label_mapper.SetInputConnection(case_3_label_transform_filter.GetOutputPort())

case_3_label_actor = vtkActor()
case_3_label_actor.SetMapper(case_3_label_mapper)

case_3_base_model = vtkCubeSource()
case_3_base_model.SetXLength(1.5)
case_3_base_model.SetYLength(0.01)
case_3_base_model.SetZLength(1.5)

case_3_base_mapper = vtkPolyDataMapper()
case_3_base_mapper.SetInputConnection(case_3_base_model.GetOutputPort())

case_3_base_actor = vtkActor()
case_3_base_actor.SetMapper(case_3_base_mapper)
case_3_base_actor.SetPosition(0.5, -0.09, 0.5)

renderer_3.AddActor(case_3_triangle_edge_actor)
renderer_3.AddActor(case_3_base_actor)
renderer_3.AddActor(case_3_label_actor)
renderer_3.AddActor(case_3_cube_edges_actor)
renderer_3.AddActor(case_3_cube_vertices_actor)
renderer_3.AddActor(case_3_triangle_actor)

# --- Case 12c: base [0,1,0,1,1,1,0,0] inverted to [1,0,1,0,0,0,1,1] ---

case_4_scalars = vtkFloatArray()
case_4_scalars.InsertNextValue(1.0)
case_4_scalars.InsertNextValue(0.0)
case_4_scalars.InsertNextValue(1.0)
case_4_scalars.InsertNextValue(0.0)
case_4_scalars.InsertNextValue(0.0)
case_4_scalars.InsertNextValue(0.0)
case_4_scalars.InsertNextValue(1.0)
case_4_scalars.InsertNextValue(1.0)

case_4_points = vtkPoints()
case_4_points.InsertNextPoint(0, 0, 0)
case_4_points.InsertNextPoint(1, 0, 0)
case_4_points.InsertNextPoint(1, 1, 0)
case_4_points.InsertNextPoint(0, 1, 0)
case_4_points.InsertNextPoint(0, 0, 1)
case_4_points.InsertNextPoint(1, 0, 1)
case_4_points.InsertNextPoint(1, 1, 1)
case_4_points.InsertNextPoint(0, 1, 1)

case_4_ids = vtkIdList()
case_4_ids.InsertNextId(0)
case_4_ids.InsertNextId(1)
case_4_ids.InsertNextId(2)
case_4_ids.InsertNextId(3)
case_4_ids.InsertNextId(4)
case_4_ids.InsertNextId(5)
case_4_ids.InsertNextId(6)
case_4_ids.InsertNextId(7)

case_4_grid = vtkUnstructuredGrid()
case_4_grid.Allocate(10, 10)
case_4_grid.InsertNextCell(12, case_4_ids)
case_4_grid.SetPoints(case_4_points)
case_4_grid.GetPointData().SetScalars(case_4_scalars)

case_4_marching = vtkContourFilter()
case_4_marching.SetInputData(case_4_grid)
case_4_marching.SetValue(0, 0.5)
case_4_marching.Update()

case_4_triangle_edges = vtkExtractEdges()
case_4_triangle_edges.SetInputConnection(case_4_marching.GetOutputPort())

case_4_triangle_edge_tubes = vtkTubeFilter()
case_4_triangle_edge_tubes.SetInputConnection(case_4_triangle_edges.GetOutputPort())
case_4_triangle_edge_tubes.SetRadius(0.005)
case_4_triangle_edge_tubes.SetNumberOfSides(6)
case_4_triangle_edge_tubes.UseDefaultNormalOn()
case_4_triangle_edge_tubes.SetDefaultNormal(0.577, 0.577, 0.577)

case_4_triangle_edge_mapper = vtkPolyDataMapper()
case_4_triangle_edge_mapper.SetInputConnection(case_4_triangle_edge_tubes.GetOutputPort())
case_4_triangle_edge_mapper.ScalarVisibilityOff()

case_4_triangle_edge_actor = vtkActor()
case_4_triangle_edge_actor.SetMapper(case_4_triangle_edge_mapper)
case_4_triangle_edge_actor.GetProperty().SetDiffuseColor(lamp_black)
case_4_triangle_edge_actor.GetProperty().SetSpecular(0.4)
case_4_triangle_edge_actor.GetProperty().SetSpecularPower(10)

case_4_shrinker = vtkShrinkPolyData()
case_4_shrinker.SetShrinkFactor(1)
case_4_shrinker.SetInputConnection(case_4_marching.GetOutputPort())

case_4_triangle_mapper = vtkPolyDataMapper()
case_4_triangle_mapper.ScalarVisibilityOff()
case_4_triangle_mapper.SetInputConnection(case_4_shrinker.GetOutputPort())

case_4_triangle_actor = vtkActor()
case_4_triangle_actor.SetMapper(case_4_triangle_mapper)
case_4_triangle_actor.GetProperty().SetDiffuseColor(banana)
case_4_triangle_actor.GetProperty().SetOpacity(0.6)

case_4_cube_model = vtkCubeSource()
case_4_cube_model.SetCenter(0.5, 0.5, 0.5)

case_4_cube_edges_filter = vtkExtractEdges()
case_4_cube_edges_filter.SetInputConnection(case_4_cube_model.GetOutputPort())

case_4_cube_tubes = vtkTubeFilter()
case_4_cube_tubes.SetInputConnection(case_4_cube_edges_filter.GetOutputPort())
case_4_cube_tubes.SetRadius(0.01)
case_4_cube_tubes.SetNumberOfSides(6)
case_4_cube_tubes.UseDefaultNormalOn()
case_4_cube_tubes.SetDefaultNormal(0.577, 0.577, 0.577)

case_4_cube_tube_mapper = vtkPolyDataMapper()
case_4_cube_tube_mapper.SetInputConnection(case_4_cube_tubes.GetOutputPort())

case_4_cube_edges_actor = vtkActor()
case_4_cube_edges_actor.SetMapper(case_4_cube_tube_mapper)
case_4_cube_edges_actor.GetProperty().SetDiffuseColor(khaki)
case_4_cube_edges_actor.GetProperty().SetSpecular(0.4)
case_4_cube_edges_actor.GetProperty().SetSpecularPower(10)

case_4_sphere_source = vtkSphereSource()
case_4_sphere_source.SetRadius(0.04)
case_4_sphere_source.SetPhiResolution(20)
case_4_sphere_source.SetThetaResolution(20)

case_4_threshold_in = vtkThresholdPoints()
case_4_threshold_in.SetInputData(case_4_grid)
case_4_threshold_in.SetUpperThreshold(0.5)
case_4_threshold_in.SetThresholdFunction(case_4_threshold_in.THRESHOLD_UPPER)

case_4_vertices_glyph = vtkGlyph3D()
case_4_vertices_glyph.SetInputConnection(case_4_threshold_in.GetOutputPort())
case_4_vertices_glyph.SetSourceConnection(case_4_sphere_source.GetOutputPort())

case_4_sphere_mapper = vtkPolyDataMapper()
case_4_sphere_mapper.SetInputConnection(case_4_vertices_glyph.GetOutputPort())
case_4_sphere_mapper.ScalarVisibilityOff()

case_4_cube_vertices_actor = vtkActor()
case_4_cube_vertices_actor.SetMapper(case_4_sphere_mapper)
case_4_cube_vertices_actor.GetProperty().SetDiffuseColor(tomato)

case_4_case_label = vtkVectorText()
case_4_case_label.SetText("Case 12c - 11000101")

case_4_label_xform = vtkTransform()
case_4_label_xform.Identity()
case_4_label_xform.Translate(-0.2, 0, 1.25)
case_4_label_xform.Scale(0.05, 0.05, 0.05)

case_4_label_transform_filter = vtkTransformPolyDataFilter()
case_4_label_transform_filter.SetTransform(case_4_label_xform)
case_4_label_transform_filter.SetInputConnection(case_4_case_label.GetOutputPort())

case_4_label_mapper = vtkPolyDataMapper()
case_4_label_mapper.SetInputConnection(case_4_label_transform_filter.GetOutputPort())

case_4_label_actor = vtkActor()
case_4_label_actor.SetMapper(case_4_label_mapper)

case_4_base_model = vtkCubeSource()
case_4_base_model.SetXLength(1.5)
case_4_base_model.SetYLength(0.01)
case_4_base_model.SetZLength(1.5)

case_4_base_mapper = vtkPolyDataMapper()
case_4_base_mapper.SetInputConnection(case_4_base_model.GetOutputPort())

case_4_base_actor = vtkActor()
case_4_base_actor.SetMapper(case_4_base_mapper)
case_4_base_actor.SetPosition(0.5, -0.09, 0.5)

renderer_4.AddActor(case_4_triangle_edge_actor)
renderer_4.AddActor(case_4_base_actor)
renderer_4.AddActor(case_4_label_actor)
renderer_4.AddActor(case_4_cube_edges_actor)
renderer_4.AddActor(case_4_cube_vertices_actor)
renderer_4.AddActor(case_4_triangle_actor)

# --- Case 13c: base [0,1,0,1,1,0,1,0] inverted to [1,0,1,0,0,1,0,1] ---

case_5_scalars = vtkFloatArray()
case_5_scalars.InsertNextValue(1.0)
case_5_scalars.InsertNextValue(0.0)
case_5_scalars.InsertNextValue(1.0)
case_5_scalars.InsertNextValue(0.0)
case_5_scalars.InsertNextValue(0.0)
case_5_scalars.InsertNextValue(1.0)
case_5_scalars.InsertNextValue(0.0)
case_5_scalars.InsertNextValue(1.0)

case_5_points = vtkPoints()
case_5_points.InsertNextPoint(0, 0, 0)
case_5_points.InsertNextPoint(1, 0, 0)
case_5_points.InsertNextPoint(1, 1, 0)
case_5_points.InsertNextPoint(0, 1, 0)
case_5_points.InsertNextPoint(0, 0, 1)
case_5_points.InsertNextPoint(1, 0, 1)
case_5_points.InsertNextPoint(1, 1, 1)
case_5_points.InsertNextPoint(0, 1, 1)

case_5_ids = vtkIdList()
case_5_ids.InsertNextId(0)
case_5_ids.InsertNextId(1)
case_5_ids.InsertNextId(2)
case_5_ids.InsertNextId(3)
case_5_ids.InsertNextId(4)
case_5_ids.InsertNextId(5)
case_5_ids.InsertNextId(6)
case_5_ids.InsertNextId(7)

case_5_grid = vtkUnstructuredGrid()
case_5_grid.Allocate(10, 10)
case_5_grid.InsertNextCell(12, case_5_ids)
case_5_grid.SetPoints(case_5_points)
case_5_grid.GetPointData().SetScalars(case_5_scalars)

case_5_marching = vtkContourFilter()
case_5_marching.SetInputData(case_5_grid)
case_5_marching.SetValue(0, 0.5)
case_5_marching.Update()

case_5_triangle_edges = vtkExtractEdges()
case_5_triangle_edges.SetInputConnection(case_5_marching.GetOutputPort())

case_5_triangle_edge_tubes = vtkTubeFilter()
case_5_triangle_edge_tubes.SetInputConnection(case_5_triangle_edges.GetOutputPort())
case_5_triangle_edge_tubes.SetRadius(0.005)
case_5_triangle_edge_tubes.SetNumberOfSides(6)
case_5_triangle_edge_tubes.UseDefaultNormalOn()
case_5_triangle_edge_tubes.SetDefaultNormal(0.577, 0.577, 0.577)

case_5_triangle_edge_mapper = vtkPolyDataMapper()
case_5_triangle_edge_mapper.SetInputConnection(case_5_triangle_edge_tubes.GetOutputPort())
case_5_triangle_edge_mapper.ScalarVisibilityOff()

case_5_triangle_edge_actor = vtkActor()
case_5_triangle_edge_actor.SetMapper(case_5_triangle_edge_mapper)
case_5_triangle_edge_actor.GetProperty().SetDiffuseColor(lamp_black)
case_5_triangle_edge_actor.GetProperty().SetSpecular(0.4)
case_5_triangle_edge_actor.GetProperty().SetSpecularPower(10)

case_5_shrinker = vtkShrinkPolyData()
case_5_shrinker.SetShrinkFactor(1)
case_5_shrinker.SetInputConnection(case_5_marching.GetOutputPort())

case_5_triangle_mapper = vtkPolyDataMapper()
case_5_triangle_mapper.ScalarVisibilityOff()
case_5_triangle_mapper.SetInputConnection(case_5_shrinker.GetOutputPort())

case_5_triangle_actor = vtkActor()
case_5_triangle_actor.SetMapper(case_5_triangle_mapper)
case_5_triangle_actor.GetProperty().SetDiffuseColor(banana)
case_5_triangle_actor.GetProperty().SetOpacity(0.6)

case_5_cube_model = vtkCubeSource()
case_5_cube_model.SetCenter(0.5, 0.5, 0.5)

case_5_cube_edges_filter = vtkExtractEdges()
case_5_cube_edges_filter.SetInputConnection(case_5_cube_model.GetOutputPort())

case_5_cube_tubes = vtkTubeFilter()
case_5_cube_tubes.SetInputConnection(case_5_cube_edges_filter.GetOutputPort())
case_5_cube_tubes.SetRadius(0.01)
case_5_cube_tubes.SetNumberOfSides(6)
case_5_cube_tubes.UseDefaultNormalOn()
case_5_cube_tubes.SetDefaultNormal(0.577, 0.577, 0.577)

case_5_cube_tube_mapper = vtkPolyDataMapper()
case_5_cube_tube_mapper.SetInputConnection(case_5_cube_tubes.GetOutputPort())

case_5_cube_edges_actor = vtkActor()
case_5_cube_edges_actor.SetMapper(case_5_cube_tube_mapper)
case_5_cube_edges_actor.GetProperty().SetDiffuseColor(khaki)
case_5_cube_edges_actor.GetProperty().SetSpecular(0.4)
case_5_cube_edges_actor.GetProperty().SetSpecularPower(10)

case_5_sphere_source = vtkSphereSource()
case_5_sphere_source.SetRadius(0.04)
case_5_sphere_source.SetPhiResolution(20)
case_5_sphere_source.SetThetaResolution(20)

case_5_threshold_in = vtkThresholdPoints()
case_5_threshold_in.SetInputData(case_5_grid)
case_5_threshold_in.SetUpperThreshold(0.5)
case_5_threshold_in.SetThresholdFunction(case_5_threshold_in.THRESHOLD_UPPER)

case_5_vertices_glyph = vtkGlyph3D()
case_5_vertices_glyph.SetInputConnection(case_5_threshold_in.GetOutputPort())
case_5_vertices_glyph.SetSourceConnection(case_5_sphere_source.GetOutputPort())

case_5_sphere_mapper = vtkPolyDataMapper()
case_5_sphere_mapper.SetInputConnection(case_5_vertices_glyph.GetOutputPort())
case_5_sphere_mapper.ScalarVisibilityOff()

case_5_cube_vertices_actor = vtkActor()
case_5_cube_vertices_actor.SetMapper(case_5_sphere_mapper)
case_5_cube_vertices_actor.GetProperty().SetDiffuseColor(tomato)

case_5_case_label = vtkVectorText()
case_5_case_label.SetText("Case 13c - 10100101")

case_5_label_xform = vtkTransform()
case_5_label_xform.Identity()
case_5_label_xform.Translate(-0.2, 0, 1.25)
case_5_label_xform.Scale(0.05, 0.05, 0.05)

case_5_label_transform_filter = vtkTransformPolyDataFilter()
case_5_label_transform_filter.SetTransform(case_5_label_xform)
case_5_label_transform_filter.SetInputConnection(case_5_case_label.GetOutputPort())

case_5_label_mapper = vtkPolyDataMapper()
case_5_label_mapper.SetInputConnection(case_5_label_transform_filter.GetOutputPort())

case_5_label_actor = vtkActor()
case_5_label_actor.SetMapper(case_5_label_mapper)

case_5_base_model = vtkCubeSource()
case_5_base_model.SetXLength(1.5)
case_5_base_model.SetYLength(0.01)
case_5_base_model.SetZLength(1.5)

case_5_base_mapper = vtkPolyDataMapper()
case_5_base_mapper.SetInputConnection(case_5_base_model.GetOutputPort())

case_5_base_actor = vtkActor()
case_5_base_actor.SetMapper(case_5_base_mapper)
case_5_base_actor.SetPosition(0.5, -0.09, 0.5)

renderer_5.AddActor(case_5_triangle_edge_actor)
renderer_5.AddActor(case_5_base_actor)
renderer_5.AddActor(case_5_label_actor)
renderer_5.AddActor(case_5_cube_edges_actor)
renderer_5.AddActor(case_5_cube_vertices_actor)
renderer_5.AddActor(case_5_triangle_actor)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer_0)
render_window.AddRenderer(renderer_1)
render_window.AddRenderer(renderer_2)
render_window.AddRenderer(renderer_3)
render_window.AddRenderer(renderer_4)
render_window.AddRenderer(renderer_5)
render_window.SetWindowName("marching cubes complementary")
render_window.SetMultiSamples(0)
render_window.SetSize(renderer_size * x_grid, renderer_size * y_grid)

# Viewport layout: 3 columns x 2 rows
renderer_0.SetViewport(0.0, 0.5, 1.0 / 3.0, 1.0)
renderer_1.SetViewport(1.0 / 3.0, 0.5, 2.0 / 3.0, 1.0)
renderer_2.SetViewport(2.0 / 3.0, 0.5, 1.0, 1.0)
renderer_3.SetViewport(0.0, 0.0, 1.0 / 3.0, 0.5)
renderer_4.SetViewport(1.0 / 3.0, 0.0, 2.0 / 3.0, 0.5)
renderer_5.SetViewport(2.0 / 3.0, 0.0, 1.0, 0.5)

# Scene: configure cameras
renderer_0.GetActiveCamera().Dolly(1.2)
renderer_0.GetActiveCamera().Azimuth(30)
renderer_0.GetActiveCamera().Elevation(20)
renderer_0.ResetCamera()
renderer_0.ResetCameraClippingRange()
renderer_1.SetActiveCamera(renderer_0.GetActiveCamera())
renderer_2.SetActiveCamera(renderer_0.GetActiveCamera())
renderer_3.SetActiveCamera(renderer_0.GetActiveCamera())
renderer_4.SetActiveCamera(renderer_0.GetActiveCamera())
renderer_5.SetActiveCamera(renderer_0.GetActiveCamera())

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
