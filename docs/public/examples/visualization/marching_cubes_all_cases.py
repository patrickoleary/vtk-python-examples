#!/usr/bin/env python

# Display all 15 marching cubes cases (0-14) in a viewport grid.

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

# Viewport grid: 4 columns x 4 rows = 16 slots for 15 cases
x_grid = 4
y_grid = 4
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
renderer_6 = vtkRenderer()
renderer_6.SetBackground(slate_grey)
renderer_7 = vtkRenderer()
renderer_7.SetBackground(slate_grey)
renderer_8 = vtkRenderer()
renderer_8.SetBackground(slate_grey)
renderer_9 = vtkRenderer()
renderer_9.SetBackground(slate_grey)
renderer_10 = vtkRenderer()
renderer_10.SetBackground(slate_grey)
renderer_11 = vtkRenderer()
renderer_11.SetBackground(slate_grey)
renderer_12 = vtkRenderer()
renderer_12.SetBackground(slate_grey)
renderer_13 = vtkRenderer()
renderer_13.SetBackground(slate_grey)
renderer_14 = vtkRenderer()
renderer_14.SetBackground(slate_grey)
renderer_15 = vtkRenderer()
renderer_15.SetBackground(slate_grey)

# --- Case 0: 00000000 ---

case_0_scalars = vtkFloatArray()
case_0_scalars.InsertNextValue(0.0)
case_0_scalars.InsertNextValue(0.0)
case_0_scalars.InsertNextValue(0.0)
case_0_scalars.InsertNextValue(0.0)
case_0_scalars.InsertNextValue(0.0)
case_0_scalars.InsertNextValue(0.0)
case_0_scalars.InsertNextValue(0.0)
case_0_scalars.InsertNextValue(0.0)

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
case_0_case_label.SetText("Case 0 - 00000000")

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

# --- Case 1: 00000001 ---

case_1_scalars = vtkFloatArray()
case_1_scalars.InsertNextValue(1.0)
case_1_scalars.InsertNextValue(0.0)
case_1_scalars.InsertNextValue(0.0)
case_1_scalars.InsertNextValue(0.0)
case_1_scalars.InsertNextValue(0.0)
case_1_scalars.InsertNextValue(0.0)
case_1_scalars.InsertNextValue(0.0)
case_1_scalars.InsertNextValue(0.0)

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
case_1_case_label.SetText("Case 1 - 00000001")

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

# --- Case 2: 00000011 ---

case_2_scalars = vtkFloatArray()
case_2_scalars.InsertNextValue(1.0)
case_2_scalars.InsertNextValue(1.0)
case_2_scalars.InsertNextValue(0.0)
case_2_scalars.InsertNextValue(0.0)
case_2_scalars.InsertNextValue(0.0)
case_2_scalars.InsertNextValue(0.0)
case_2_scalars.InsertNextValue(0.0)
case_2_scalars.InsertNextValue(0.0)

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
case_2_case_label.SetText("Case 2 - 00000011")

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

# --- Case 3: 00000101 ---

case_3_scalars = vtkFloatArray()
case_3_scalars.InsertNextValue(1.0)
case_3_scalars.InsertNextValue(0.0)
case_3_scalars.InsertNextValue(1.0)
case_3_scalars.InsertNextValue(0.0)
case_3_scalars.InsertNextValue(0.0)
case_3_scalars.InsertNextValue(0.0)
case_3_scalars.InsertNextValue(0.0)
case_3_scalars.InsertNextValue(0.0)

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
case_3_case_label.SetText("Case 3 - 00000101")

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

# --- Case 4: 01000001 ---

case_4_scalars = vtkFloatArray()
case_4_scalars.InsertNextValue(1.0)
case_4_scalars.InsertNextValue(0.0)
case_4_scalars.InsertNextValue(0.0)
case_4_scalars.InsertNextValue(0.0)
case_4_scalars.InsertNextValue(0.0)
case_4_scalars.InsertNextValue(0.0)
case_4_scalars.InsertNextValue(1.0)
case_4_scalars.InsertNextValue(0.0)

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
case_4_case_label.SetText("Case 4 - 01000001")

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

# --- Case 5: 00110010 ---

case_5_scalars = vtkFloatArray()
case_5_scalars.InsertNextValue(0.0)
case_5_scalars.InsertNextValue(1.0)
case_5_scalars.InsertNextValue(0.0)
case_5_scalars.InsertNextValue(0.0)
case_5_scalars.InsertNextValue(1.0)
case_5_scalars.InsertNextValue(1.0)
case_5_scalars.InsertNextValue(0.0)
case_5_scalars.InsertNextValue(0.0)

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
case_5_case_label.SetText("Case 5 - 00110010")

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

# --- Case 6: 00011010 ---

case_6_scalars = vtkFloatArray()
case_6_scalars.InsertNextValue(0.0)
case_6_scalars.InsertNextValue(1.0)
case_6_scalars.InsertNextValue(0.0)
case_6_scalars.InsertNextValue(1.0)
case_6_scalars.InsertNextValue(1.0)
case_6_scalars.InsertNextValue(0.0)
case_6_scalars.InsertNextValue(0.0)
case_6_scalars.InsertNextValue(0.0)

case_6_points = vtkPoints()
case_6_points.InsertNextPoint(0, 0, 0)
case_6_points.InsertNextPoint(1, 0, 0)
case_6_points.InsertNextPoint(1, 1, 0)
case_6_points.InsertNextPoint(0, 1, 0)
case_6_points.InsertNextPoint(0, 0, 1)
case_6_points.InsertNextPoint(1, 0, 1)
case_6_points.InsertNextPoint(1, 1, 1)
case_6_points.InsertNextPoint(0, 1, 1)

case_6_ids = vtkIdList()
case_6_ids.InsertNextId(0)
case_6_ids.InsertNextId(1)
case_6_ids.InsertNextId(2)
case_6_ids.InsertNextId(3)
case_6_ids.InsertNextId(4)
case_6_ids.InsertNextId(5)
case_6_ids.InsertNextId(6)
case_6_ids.InsertNextId(7)

case_6_grid = vtkUnstructuredGrid()
case_6_grid.Allocate(10, 10)
case_6_grid.InsertNextCell(12, case_6_ids)
case_6_grid.SetPoints(case_6_points)
case_6_grid.GetPointData().SetScalars(case_6_scalars)

case_6_marching = vtkContourFilter()
case_6_marching.SetInputData(case_6_grid)
case_6_marching.SetValue(0, 0.5)
case_6_marching.Update()

case_6_triangle_edges = vtkExtractEdges()
case_6_triangle_edges.SetInputConnection(case_6_marching.GetOutputPort())

case_6_triangle_edge_tubes = vtkTubeFilter()
case_6_triangle_edge_tubes.SetInputConnection(case_6_triangle_edges.GetOutputPort())
case_6_triangle_edge_tubes.SetRadius(0.005)
case_6_triangle_edge_tubes.SetNumberOfSides(6)
case_6_triangle_edge_tubes.UseDefaultNormalOn()
case_6_triangle_edge_tubes.SetDefaultNormal(0.577, 0.577, 0.577)

case_6_triangle_edge_mapper = vtkPolyDataMapper()
case_6_triangle_edge_mapper.SetInputConnection(case_6_triangle_edge_tubes.GetOutputPort())
case_6_triangle_edge_mapper.ScalarVisibilityOff()

case_6_triangle_edge_actor = vtkActor()
case_6_triangle_edge_actor.SetMapper(case_6_triangle_edge_mapper)
case_6_triangle_edge_actor.GetProperty().SetDiffuseColor(lamp_black)
case_6_triangle_edge_actor.GetProperty().SetSpecular(0.4)
case_6_triangle_edge_actor.GetProperty().SetSpecularPower(10)

case_6_shrinker = vtkShrinkPolyData()
case_6_shrinker.SetShrinkFactor(1)
case_6_shrinker.SetInputConnection(case_6_marching.GetOutputPort())

case_6_triangle_mapper = vtkPolyDataMapper()
case_6_triangle_mapper.ScalarVisibilityOff()
case_6_triangle_mapper.SetInputConnection(case_6_shrinker.GetOutputPort())

case_6_triangle_actor = vtkActor()
case_6_triangle_actor.SetMapper(case_6_triangle_mapper)
case_6_triangle_actor.GetProperty().SetDiffuseColor(banana)
case_6_triangle_actor.GetProperty().SetOpacity(0.6)

case_6_cube_model = vtkCubeSource()
case_6_cube_model.SetCenter(0.5, 0.5, 0.5)

case_6_cube_edges_filter = vtkExtractEdges()
case_6_cube_edges_filter.SetInputConnection(case_6_cube_model.GetOutputPort())

case_6_cube_tubes = vtkTubeFilter()
case_6_cube_tubes.SetInputConnection(case_6_cube_edges_filter.GetOutputPort())
case_6_cube_tubes.SetRadius(0.01)
case_6_cube_tubes.SetNumberOfSides(6)
case_6_cube_tubes.UseDefaultNormalOn()
case_6_cube_tubes.SetDefaultNormal(0.577, 0.577, 0.577)

case_6_cube_tube_mapper = vtkPolyDataMapper()
case_6_cube_tube_mapper.SetInputConnection(case_6_cube_tubes.GetOutputPort())

case_6_cube_edges_actor = vtkActor()
case_6_cube_edges_actor.SetMapper(case_6_cube_tube_mapper)
case_6_cube_edges_actor.GetProperty().SetDiffuseColor(khaki)
case_6_cube_edges_actor.GetProperty().SetSpecular(0.4)
case_6_cube_edges_actor.GetProperty().SetSpecularPower(10)

case_6_sphere_source = vtkSphereSource()
case_6_sphere_source.SetRadius(0.04)
case_6_sphere_source.SetPhiResolution(20)
case_6_sphere_source.SetThetaResolution(20)

case_6_threshold_in = vtkThresholdPoints()
case_6_threshold_in.SetInputData(case_6_grid)
case_6_threshold_in.SetUpperThreshold(0.5)
case_6_threshold_in.SetThresholdFunction(case_6_threshold_in.THRESHOLD_UPPER)

case_6_vertices_glyph = vtkGlyph3D()
case_6_vertices_glyph.SetInputConnection(case_6_threshold_in.GetOutputPort())
case_6_vertices_glyph.SetSourceConnection(case_6_sphere_source.GetOutputPort())

case_6_sphere_mapper = vtkPolyDataMapper()
case_6_sphere_mapper.SetInputConnection(case_6_vertices_glyph.GetOutputPort())
case_6_sphere_mapper.ScalarVisibilityOff()

case_6_cube_vertices_actor = vtkActor()
case_6_cube_vertices_actor.SetMapper(case_6_sphere_mapper)
case_6_cube_vertices_actor.GetProperty().SetDiffuseColor(tomato)

case_6_case_label = vtkVectorText()
case_6_case_label.SetText("Case 6 - 00011010")

case_6_label_xform = vtkTransform()
case_6_label_xform.Identity()
case_6_label_xform.Translate(-0.2, 0, 1.25)
case_6_label_xform.Scale(0.05, 0.05, 0.05)

case_6_label_transform_filter = vtkTransformPolyDataFilter()
case_6_label_transform_filter.SetTransform(case_6_label_xform)
case_6_label_transform_filter.SetInputConnection(case_6_case_label.GetOutputPort())

case_6_label_mapper = vtkPolyDataMapper()
case_6_label_mapper.SetInputConnection(case_6_label_transform_filter.GetOutputPort())

case_6_label_actor = vtkActor()
case_6_label_actor.SetMapper(case_6_label_mapper)

case_6_base_model = vtkCubeSource()
case_6_base_model.SetXLength(1.5)
case_6_base_model.SetYLength(0.01)
case_6_base_model.SetZLength(1.5)

case_6_base_mapper = vtkPolyDataMapper()
case_6_base_mapper.SetInputConnection(case_6_base_model.GetOutputPort())

case_6_base_actor = vtkActor()
case_6_base_actor.SetMapper(case_6_base_mapper)
case_6_base_actor.SetPosition(0.5, -0.09, 0.5)

renderer_6.AddActor(case_6_triangle_edge_actor)
renderer_6.AddActor(case_6_base_actor)
renderer_6.AddActor(case_6_label_actor)
renderer_6.AddActor(case_6_cube_edges_actor)
renderer_6.AddActor(case_6_cube_vertices_actor)
renderer_6.AddActor(case_6_triangle_actor)

# --- Case 7: 01000011 ---

case_7_scalars = vtkFloatArray()
case_7_scalars.InsertNextValue(1.0)
case_7_scalars.InsertNextValue(1.0)
case_7_scalars.InsertNextValue(0.0)
case_7_scalars.InsertNextValue(0.0)
case_7_scalars.InsertNextValue(0.0)
case_7_scalars.InsertNextValue(0.0)
case_7_scalars.InsertNextValue(1.0)
case_7_scalars.InsertNextValue(0.0)

case_7_points = vtkPoints()
case_7_points.InsertNextPoint(0, 0, 0)
case_7_points.InsertNextPoint(1, 0, 0)
case_7_points.InsertNextPoint(1, 1, 0)
case_7_points.InsertNextPoint(0, 1, 0)
case_7_points.InsertNextPoint(0, 0, 1)
case_7_points.InsertNextPoint(1, 0, 1)
case_7_points.InsertNextPoint(1, 1, 1)
case_7_points.InsertNextPoint(0, 1, 1)

case_7_ids = vtkIdList()
case_7_ids.InsertNextId(0)
case_7_ids.InsertNextId(1)
case_7_ids.InsertNextId(2)
case_7_ids.InsertNextId(3)
case_7_ids.InsertNextId(4)
case_7_ids.InsertNextId(5)
case_7_ids.InsertNextId(6)
case_7_ids.InsertNextId(7)

case_7_grid = vtkUnstructuredGrid()
case_7_grid.Allocate(10, 10)
case_7_grid.InsertNextCell(12, case_7_ids)
case_7_grid.SetPoints(case_7_points)
case_7_grid.GetPointData().SetScalars(case_7_scalars)

case_7_marching = vtkContourFilter()
case_7_marching.SetInputData(case_7_grid)
case_7_marching.SetValue(0, 0.5)
case_7_marching.Update()

case_7_triangle_edges = vtkExtractEdges()
case_7_triangle_edges.SetInputConnection(case_7_marching.GetOutputPort())

case_7_triangle_edge_tubes = vtkTubeFilter()
case_7_triangle_edge_tubes.SetInputConnection(case_7_triangle_edges.GetOutputPort())
case_7_triangle_edge_tubes.SetRadius(0.005)
case_7_triangle_edge_tubes.SetNumberOfSides(6)
case_7_triangle_edge_tubes.UseDefaultNormalOn()
case_7_triangle_edge_tubes.SetDefaultNormal(0.577, 0.577, 0.577)

case_7_triangle_edge_mapper = vtkPolyDataMapper()
case_7_triangle_edge_mapper.SetInputConnection(case_7_triangle_edge_tubes.GetOutputPort())
case_7_triangle_edge_mapper.ScalarVisibilityOff()

case_7_triangle_edge_actor = vtkActor()
case_7_triangle_edge_actor.SetMapper(case_7_triangle_edge_mapper)
case_7_triangle_edge_actor.GetProperty().SetDiffuseColor(lamp_black)
case_7_triangle_edge_actor.GetProperty().SetSpecular(0.4)
case_7_triangle_edge_actor.GetProperty().SetSpecularPower(10)

case_7_shrinker = vtkShrinkPolyData()
case_7_shrinker.SetShrinkFactor(1)
case_7_shrinker.SetInputConnection(case_7_marching.GetOutputPort())

case_7_triangle_mapper = vtkPolyDataMapper()
case_7_triangle_mapper.ScalarVisibilityOff()
case_7_triangle_mapper.SetInputConnection(case_7_shrinker.GetOutputPort())

case_7_triangle_actor = vtkActor()
case_7_triangle_actor.SetMapper(case_7_triangle_mapper)
case_7_triangle_actor.GetProperty().SetDiffuseColor(banana)
case_7_triangle_actor.GetProperty().SetOpacity(0.6)

case_7_cube_model = vtkCubeSource()
case_7_cube_model.SetCenter(0.5, 0.5, 0.5)

case_7_cube_edges_filter = vtkExtractEdges()
case_7_cube_edges_filter.SetInputConnection(case_7_cube_model.GetOutputPort())

case_7_cube_tubes = vtkTubeFilter()
case_7_cube_tubes.SetInputConnection(case_7_cube_edges_filter.GetOutputPort())
case_7_cube_tubes.SetRadius(0.01)
case_7_cube_tubes.SetNumberOfSides(6)
case_7_cube_tubes.UseDefaultNormalOn()
case_7_cube_tubes.SetDefaultNormal(0.577, 0.577, 0.577)

case_7_cube_tube_mapper = vtkPolyDataMapper()
case_7_cube_tube_mapper.SetInputConnection(case_7_cube_tubes.GetOutputPort())

case_7_cube_edges_actor = vtkActor()
case_7_cube_edges_actor.SetMapper(case_7_cube_tube_mapper)
case_7_cube_edges_actor.GetProperty().SetDiffuseColor(khaki)
case_7_cube_edges_actor.GetProperty().SetSpecular(0.4)
case_7_cube_edges_actor.GetProperty().SetSpecularPower(10)

case_7_sphere_source = vtkSphereSource()
case_7_sphere_source.SetRadius(0.04)
case_7_sphere_source.SetPhiResolution(20)
case_7_sphere_source.SetThetaResolution(20)

case_7_threshold_in = vtkThresholdPoints()
case_7_threshold_in.SetInputData(case_7_grid)
case_7_threshold_in.SetUpperThreshold(0.5)
case_7_threshold_in.SetThresholdFunction(case_7_threshold_in.THRESHOLD_UPPER)

case_7_vertices_glyph = vtkGlyph3D()
case_7_vertices_glyph.SetInputConnection(case_7_threshold_in.GetOutputPort())
case_7_vertices_glyph.SetSourceConnection(case_7_sphere_source.GetOutputPort())

case_7_sphere_mapper = vtkPolyDataMapper()
case_7_sphere_mapper.SetInputConnection(case_7_vertices_glyph.GetOutputPort())
case_7_sphere_mapper.ScalarVisibilityOff()

case_7_cube_vertices_actor = vtkActor()
case_7_cube_vertices_actor.SetMapper(case_7_sphere_mapper)
case_7_cube_vertices_actor.GetProperty().SetDiffuseColor(tomato)

case_7_case_label = vtkVectorText()
case_7_case_label.SetText("Case 7 - 01000011")

case_7_label_xform = vtkTransform()
case_7_label_xform.Identity()
case_7_label_xform.Translate(-0.2, 0, 1.25)
case_7_label_xform.Scale(0.05, 0.05, 0.05)

case_7_label_transform_filter = vtkTransformPolyDataFilter()
case_7_label_transform_filter.SetTransform(case_7_label_xform)
case_7_label_transform_filter.SetInputConnection(case_7_case_label.GetOutputPort())

case_7_label_mapper = vtkPolyDataMapper()
case_7_label_mapper.SetInputConnection(case_7_label_transform_filter.GetOutputPort())

case_7_label_actor = vtkActor()
case_7_label_actor.SetMapper(case_7_label_mapper)

case_7_base_model = vtkCubeSource()
case_7_base_model.SetXLength(1.5)
case_7_base_model.SetYLength(0.01)
case_7_base_model.SetZLength(1.5)

case_7_base_mapper = vtkPolyDataMapper()
case_7_base_mapper.SetInputConnection(case_7_base_model.GetOutputPort())

case_7_base_actor = vtkActor()
case_7_base_actor.SetMapper(case_7_base_mapper)
case_7_base_actor.SetPosition(0.5, -0.09, 0.5)

renderer_7.AddActor(case_7_triangle_edge_actor)
renderer_7.AddActor(case_7_base_actor)
renderer_7.AddActor(case_7_label_actor)
renderer_7.AddActor(case_7_cube_edges_actor)
renderer_7.AddActor(case_7_cube_vertices_actor)
renderer_7.AddActor(case_7_triangle_actor)

# --- Case 8: 00110011 ---

case_8_scalars = vtkFloatArray()
case_8_scalars.InsertNextValue(1.0)
case_8_scalars.InsertNextValue(1.0)
case_8_scalars.InsertNextValue(0.0)
case_8_scalars.InsertNextValue(0.0)
case_8_scalars.InsertNextValue(1.0)
case_8_scalars.InsertNextValue(1.0)
case_8_scalars.InsertNextValue(0.0)
case_8_scalars.InsertNextValue(0.0)

case_8_points = vtkPoints()
case_8_points.InsertNextPoint(0, 0, 0)
case_8_points.InsertNextPoint(1, 0, 0)
case_8_points.InsertNextPoint(1, 1, 0)
case_8_points.InsertNextPoint(0, 1, 0)
case_8_points.InsertNextPoint(0, 0, 1)
case_8_points.InsertNextPoint(1, 0, 1)
case_8_points.InsertNextPoint(1, 1, 1)
case_8_points.InsertNextPoint(0, 1, 1)

case_8_ids = vtkIdList()
case_8_ids.InsertNextId(0)
case_8_ids.InsertNextId(1)
case_8_ids.InsertNextId(2)
case_8_ids.InsertNextId(3)
case_8_ids.InsertNextId(4)
case_8_ids.InsertNextId(5)
case_8_ids.InsertNextId(6)
case_8_ids.InsertNextId(7)

case_8_grid = vtkUnstructuredGrid()
case_8_grid.Allocate(10, 10)
case_8_grid.InsertNextCell(12, case_8_ids)
case_8_grid.SetPoints(case_8_points)
case_8_grid.GetPointData().SetScalars(case_8_scalars)

case_8_marching = vtkContourFilter()
case_8_marching.SetInputData(case_8_grid)
case_8_marching.SetValue(0, 0.5)
case_8_marching.Update()

case_8_triangle_edges = vtkExtractEdges()
case_8_triangle_edges.SetInputConnection(case_8_marching.GetOutputPort())

case_8_triangle_edge_tubes = vtkTubeFilter()
case_8_triangle_edge_tubes.SetInputConnection(case_8_triangle_edges.GetOutputPort())
case_8_triangle_edge_tubes.SetRadius(0.005)
case_8_triangle_edge_tubes.SetNumberOfSides(6)
case_8_triangle_edge_tubes.UseDefaultNormalOn()
case_8_triangle_edge_tubes.SetDefaultNormal(0.577, 0.577, 0.577)

case_8_triangle_edge_mapper = vtkPolyDataMapper()
case_8_triangle_edge_mapper.SetInputConnection(case_8_triangle_edge_tubes.GetOutputPort())
case_8_triangle_edge_mapper.ScalarVisibilityOff()

case_8_triangle_edge_actor = vtkActor()
case_8_triangle_edge_actor.SetMapper(case_8_triangle_edge_mapper)
case_8_triangle_edge_actor.GetProperty().SetDiffuseColor(lamp_black)
case_8_triangle_edge_actor.GetProperty().SetSpecular(0.4)
case_8_triangle_edge_actor.GetProperty().SetSpecularPower(10)

case_8_shrinker = vtkShrinkPolyData()
case_8_shrinker.SetShrinkFactor(1)
case_8_shrinker.SetInputConnection(case_8_marching.GetOutputPort())

case_8_triangle_mapper = vtkPolyDataMapper()
case_8_triangle_mapper.ScalarVisibilityOff()
case_8_triangle_mapper.SetInputConnection(case_8_shrinker.GetOutputPort())

case_8_triangle_actor = vtkActor()
case_8_triangle_actor.SetMapper(case_8_triangle_mapper)
case_8_triangle_actor.GetProperty().SetDiffuseColor(banana)
case_8_triangle_actor.GetProperty().SetOpacity(0.6)

case_8_cube_model = vtkCubeSource()
case_8_cube_model.SetCenter(0.5, 0.5, 0.5)

case_8_cube_edges_filter = vtkExtractEdges()
case_8_cube_edges_filter.SetInputConnection(case_8_cube_model.GetOutputPort())

case_8_cube_tubes = vtkTubeFilter()
case_8_cube_tubes.SetInputConnection(case_8_cube_edges_filter.GetOutputPort())
case_8_cube_tubes.SetRadius(0.01)
case_8_cube_tubes.SetNumberOfSides(6)
case_8_cube_tubes.UseDefaultNormalOn()
case_8_cube_tubes.SetDefaultNormal(0.577, 0.577, 0.577)

case_8_cube_tube_mapper = vtkPolyDataMapper()
case_8_cube_tube_mapper.SetInputConnection(case_8_cube_tubes.GetOutputPort())

case_8_cube_edges_actor = vtkActor()
case_8_cube_edges_actor.SetMapper(case_8_cube_tube_mapper)
case_8_cube_edges_actor.GetProperty().SetDiffuseColor(khaki)
case_8_cube_edges_actor.GetProperty().SetSpecular(0.4)
case_8_cube_edges_actor.GetProperty().SetSpecularPower(10)

case_8_sphere_source = vtkSphereSource()
case_8_sphere_source.SetRadius(0.04)
case_8_sphere_source.SetPhiResolution(20)
case_8_sphere_source.SetThetaResolution(20)

case_8_threshold_in = vtkThresholdPoints()
case_8_threshold_in.SetInputData(case_8_grid)
case_8_threshold_in.SetUpperThreshold(0.5)
case_8_threshold_in.SetThresholdFunction(case_8_threshold_in.THRESHOLD_UPPER)

case_8_vertices_glyph = vtkGlyph3D()
case_8_vertices_glyph.SetInputConnection(case_8_threshold_in.GetOutputPort())
case_8_vertices_glyph.SetSourceConnection(case_8_sphere_source.GetOutputPort())

case_8_sphere_mapper = vtkPolyDataMapper()
case_8_sphere_mapper.SetInputConnection(case_8_vertices_glyph.GetOutputPort())
case_8_sphere_mapper.ScalarVisibilityOff()

case_8_cube_vertices_actor = vtkActor()
case_8_cube_vertices_actor.SetMapper(case_8_sphere_mapper)
case_8_cube_vertices_actor.GetProperty().SetDiffuseColor(tomato)

case_8_case_label = vtkVectorText()
case_8_case_label.SetText("Case 8 - 00110011")

case_8_label_xform = vtkTransform()
case_8_label_xform.Identity()
case_8_label_xform.Translate(-0.2, 0, 1.25)
case_8_label_xform.Scale(0.05, 0.05, 0.05)

case_8_label_transform_filter = vtkTransformPolyDataFilter()
case_8_label_transform_filter.SetTransform(case_8_label_xform)
case_8_label_transform_filter.SetInputConnection(case_8_case_label.GetOutputPort())

case_8_label_mapper = vtkPolyDataMapper()
case_8_label_mapper.SetInputConnection(case_8_label_transform_filter.GetOutputPort())

case_8_label_actor = vtkActor()
case_8_label_actor.SetMapper(case_8_label_mapper)

case_8_base_model = vtkCubeSource()
case_8_base_model.SetXLength(1.5)
case_8_base_model.SetYLength(0.01)
case_8_base_model.SetZLength(1.5)

case_8_base_mapper = vtkPolyDataMapper()
case_8_base_mapper.SetInputConnection(case_8_base_model.GetOutputPort())

case_8_base_actor = vtkActor()
case_8_base_actor.SetMapper(case_8_base_mapper)
case_8_base_actor.SetPosition(0.5, -0.09, 0.5)

renderer_8.AddActor(case_8_triangle_edge_actor)
renderer_8.AddActor(case_8_base_actor)
renderer_8.AddActor(case_8_label_actor)
renderer_8.AddActor(case_8_cube_edges_actor)
renderer_8.AddActor(case_8_cube_vertices_actor)
renderer_8.AddActor(case_8_triangle_actor)

# --- Case 9: 01001110 ---

case_9_scalars = vtkFloatArray()
case_9_scalars.InsertNextValue(0.0)
case_9_scalars.InsertNextValue(1.0)
case_9_scalars.InsertNextValue(1.0)
case_9_scalars.InsertNextValue(1.0)
case_9_scalars.InsertNextValue(0.0)
case_9_scalars.InsertNextValue(0.0)
case_9_scalars.InsertNextValue(1.0)
case_9_scalars.InsertNextValue(0.0)

case_9_points = vtkPoints()
case_9_points.InsertNextPoint(0, 0, 0)
case_9_points.InsertNextPoint(1, 0, 0)
case_9_points.InsertNextPoint(1, 1, 0)
case_9_points.InsertNextPoint(0, 1, 0)
case_9_points.InsertNextPoint(0, 0, 1)
case_9_points.InsertNextPoint(1, 0, 1)
case_9_points.InsertNextPoint(1, 1, 1)
case_9_points.InsertNextPoint(0, 1, 1)

case_9_ids = vtkIdList()
case_9_ids.InsertNextId(0)
case_9_ids.InsertNextId(1)
case_9_ids.InsertNextId(2)
case_9_ids.InsertNextId(3)
case_9_ids.InsertNextId(4)
case_9_ids.InsertNextId(5)
case_9_ids.InsertNextId(6)
case_9_ids.InsertNextId(7)

case_9_grid = vtkUnstructuredGrid()
case_9_grid.Allocate(10, 10)
case_9_grid.InsertNextCell(12, case_9_ids)
case_9_grid.SetPoints(case_9_points)
case_9_grid.GetPointData().SetScalars(case_9_scalars)

case_9_marching = vtkContourFilter()
case_9_marching.SetInputData(case_9_grid)
case_9_marching.SetValue(0, 0.5)
case_9_marching.Update()

case_9_triangle_edges = vtkExtractEdges()
case_9_triangle_edges.SetInputConnection(case_9_marching.GetOutputPort())

case_9_triangle_edge_tubes = vtkTubeFilter()
case_9_triangle_edge_tubes.SetInputConnection(case_9_triangle_edges.GetOutputPort())
case_9_triangle_edge_tubes.SetRadius(0.005)
case_9_triangle_edge_tubes.SetNumberOfSides(6)
case_9_triangle_edge_tubes.UseDefaultNormalOn()
case_9_triangle_edge_tubes.SetDefaultNormal(0.577, 0.577, 0.577)

case_9_triangle_edge_mapper = vtkPolyDataMapper()
case_9_triangle_edge_mapper.SetInputConnection(case_9_triangle_edge_tubes.GetOutputPort())
case_9_triangle_edge_mapper.ScalarVisibilityOff()

case_9_triangle_edge_actor = vtkActor()
case_9_triangle_edge_actor.SetMapper(case_9_triangle_edge_mapper)
case_9_triangle_edge_actor.GetProperty().SetDiffuseColor(lamp_black)
case_9_triangle_edge_actor.GetProperty().SetSpecular(0.4)
case_9_triangle_edge_actor.GetProperty().SetSpecularPower(10)

case_9_shrinker = vtkShrinkPolyData()
case_9_shrinker.SetShrinkFactor(1)
case_9_shrinker.SetInputConnection(case_9_marching.GetOutputPort())

case_9_triangle_mapper = vtkPolyDataMapper()
case_9_triangle_mapper.ScalarVisibilityOff()
case_9_triangle_mapper.SetInputConnection(case_9_shrinker.GetOutputPort())

case_9_triangle_actor = vtkActor()
case_9_triangle_actor.SetMapper(case_9_triangle_mapper)
case_9_triangle_actor.GetProperty().SetDiffuseColor(banana)
case_9_triangle_actor.GetProperty().SetOpacity(0.6)

case_9_cube_model = vtkCubeSource()
case_9_cube_model.SetCenter(0.5, 0.5, 0.5)

case_9_cube_edges_filter = vtkExtractEdges()
case_9_cube_edges_filter.SetInputConnection(case_9_cube_model.GetOutputPort())

case_9_cube_tubes = vtkTubeFilter()
case_9_cube_tubes.SetInputConnection(case_9_cube_edges_filter.GetOutputPort())
case_9_cube_tubes.SetRadius(0.01)
case_9_cube_tubes.SetNumberOfSides(6)
case_9_cube_tubes.UseDefaultNormalOn()
case_9_cube_tubes.SetDefaultNormal(0.577, 0.577, 0.577)

case_9_cube_tube_mapper = vtkPolyDataMapper()
case_9_cube_tube_mapper.SetInputConnection(case_9_cube_tubes.GetOutputPort())

case_9_cube_edges_actor = vtkActor()
case_9_cube_edges_actor.SetMapper(case_9_cube_tube_mapper)
case_9_cube_edges_actor.GetProperty().SetDiffuseColor(khaki)
case_9_cube_edges_actor.GetProperty().SetSpecular(0.4)
case_9_cube_edges_actor.GetProperty().SetSpecularPower(10)

case_9_sphere_source = vtkSphereSource()
case_9_sphere_source.SetRadius(0.04)
case_9_sphere_source.SetPhiResolution(20)
case_9_sphere_source.SetThetaResolution(20)

case_9_threshold_in = vtkThresholdPoints()
case_9_threshold_in.SetInputData(case_9_grid)
case_9_threshold_in.SetUpperThreshold(0.5)
case_9_threshold_in.SetThresholdFunction(case_9_threshold_in.THRESHOLD_UPPER)

case_9_vertices_glyph = vtkGlyph3D()
case_9_vertices_glyph.SetInputConnection(case_9_threshold_in.GetOutputPort())
case_9_vertices_glyph.SetSourceConnection(case_9_sphere_source.GetOutputPort())

case_9_sphere_mapper = vtkPolyDataMapper()
case_9_sphere_mapper.SetInputConnection(case_9_vertices_glyph.GetOutputPort())
case_9_sphere_mapper.ScalarVisibilityOff()

case_9_cube_vertices_actor = vtkActor()
case_9_cube_vertices_actor.SetMapper(case_9_sphere_mapper)
case_9_cube_vertices_actor.GetProperty().SetDiffuseColor(tomato)

case_9_case_label = vtkVectorText()
case_9_case_label.SetText("Case 9 - 01001110")

case_9_label_xform = vtkTransform()
case_9_label_xform.Identity()
case_9_label_xform.Translate(-0.2, 0, 1.25)
case_9_label_xform.Scale(0.05, 0.05, 0.05)

case_9_label_transform_filter = vtkTransformPolyDataFilter()
case_9_label_transform_filter.SetTransform(case_9_label_xform)
case_9_label_transform_filter.SetInputConnection(case_9_case_label.GetOutputPort())

case_9_label_mapper = vtkPolyDataMapper()
case_9_label_mapper.SetInputConnection(case_9_label_transform_filter.GetOutputPort())

case_9_label_actor = vtkActor()
case_9_label_actor.SetMapper(case_9_label_mapper)

case_9_base_model = vtkCubeSource()
case_9_base_model.SetXLength(1.5)
case_9_base_model.SetYLength(0.01)
case_9_base_model.SetZLength(1.5)

case_9_base_mapper = vtkPolyDataMapper()
case_9_base_mapper.SetInputConnection(case_9_base_model.GetOutputPort())

case_9_base_actor = vtkActor()
case_9_base_actor.SetMapper(case_9_base_mapper)
case_9_base_actor.SetPosition(0.5, -0.09, 0.5)

renderer_9.AddActor(case_9_triangle_edge_actor)
renderer_9.AddActor(case_9_base_actor)
renderer_9.AddActor(case_9_label_actor)
renderer_9.AddActor(case_9_cube_edges_actor)
renderer_9.AddActor(case_9_cube_vertices_actor)
renderer_9.AddActor(case_9_triangle_actor)

# --- Case 10: 01101001 ---

case_10_scalars = vtkFloatArray()
case_10_scalars.InsertNextValue(1.0)
case_10_scalars.InsertNextValue(0.0)
case_10_scalars.InsertNextValue(0.0)
case_10_scalars.InsertNextValue(1.0)
case_10_scalars.InsertNextValue(0.0)
case_10_scalars.InsertNextValue(1.0)
case_10_scalars.InsertNextValue(1.0)
case_10_scalars.InsertNextValue(0.0)

case_10_points = vtkPoints()
case_10_points.InsertNextPoint(0, 0, 0)
case_10_points.InsertNextPoint(1, 0, 0)
case_10_points.InsertNextPoint(1, 1, 0)
case_10_points.InsertNextPoint(0, 1, 0)
case_10_points.InsertNextPoint(0, 0, 1)
case_10_points.InsertNextPoint(1, 0, 1)
case_10_points.InsertNextPoint(1, 1, 1)
case_10_points.InsertNextPoint(0, 1, 1)

case_10_ids = vtkIdList()
case_10_ids.InsertNextId(0)
case_10_ids.InsertNextId(1)
case_10_ids.InsertNextId(2)
case_10_ids.InsertNextId(3)
case_10_ids.InsertNextId(4)
case_10_ids.InsertNextId(5)
case_10_ids.InsertNextId(6)
case_10_ids.InsertNextId(7)

case_10_grid = vtkUnstructuredGrid()
case_10_grid.Allocate(10, 10)
case_10_grid.InsertNextCell(12, case_10_ids)
case_10_grid.SetPoints(case_10_points)
case_10_grid.GetPointData().SetScalars(case_10_scalars)

case_10_marching = vtkContourFilter()
case_10_marching.SetInputData(case_10_grid)
case_10_marching.SetValue(0, 0.5)
case_10_marching.Update()

case_10_triangle_edges = vtkExtractEdges()
case_10_triangle_edges.SetInputConnection(case_10_marching.GetOutputPort())

case_10_triangle_edge_tubes = vtkTubeFilter()
case_10_triangle_edge_tubes.SetInputConnection(case_10_triangle_edges.GetOutputPort())
case_10_triangle_edge_tubes.SetRadius(0.005)
case_10_triangle_edge_tubes.SetNumberOfSides(6)
case_10_triangle_edge_tubes.UseDefaultNormalOn()
case_10_triangle_edge_tubes.SetDefaultNormal(0.577, 0.577, 0.577)

case_10_triangle_edge_mapper = vtkPolyDataMapper()
case_10_triangle_edge_mapper.SetInputConnection(case_10_triangle_edge_tubes.GetOutputPort())
case_10_triangle_edge_mapper.ScalarVisibilityOff()

case_10_triangle_edge_actor = vtkActor()
case_10_triangle_edge_actor.SetMapper(case_10_triangle_edge_mapper)
case_10_triangle_edge_actor.GetProperty().SetDiffuseColor(lamp_black)
case_10_triangle_edge_actor.GetProperty().SetSpecular(0.4)
case_10_triangle_edge_actor.GetProperty().SetSpecularPower(10)

case_10_shrinker = vtkShrinkPolyData()
case_10_shrinker.SetShrinkFactor(1)
case_10_shrinker.SetInputConnection(case_10_marching.GetOutputPort())

case_10_triangle_mapper = vtkPolyDataMapper()
case_10_triangle_mapper.ScalarVisibilityOff()
case_10_triangle_mapper.SetInputConnection(case_10_shrinker.GetOutputPort())

case_10_triangle_actor = vtkActor()
case_10_triangle_actor.SetMapper(case_10_triangle_mapper)
case_10_triangle_actor.GetProperty().SetDiffuseColor(banana)
case_10_triangle_actor.GetProperty().SetOpacity(0.6)

case_10_cube_model = vtkCubeSource()
case_10_cube_model.SetCenter(0.5, 0.5, 0.5)

case_10_cube_edges_filter = vtkExtractEdges()
case_10_cube_edges_filter.SetInputConnection(case_10_cube_model.GetOutputPort())

case_10_cube_tubes = vtkTubeFilter()
case_10_cube_tubes.SetInputConnection(case_10_cube_edges_filter.GetOutputPort())
case_10_cube_tubes.SetRadius(0.01)
case_10_cube_tubes.SetNumberOfSides(6)
case_10_cube_tubes.UseDefaultNormalOn()
case_10_cube_tubes.SetDefaultNormal(0.577, 0.577, 0.577)

case_10_cube_tube_mapper = vtkPolyDataMapper()
case_10_cube_tube_mapper.SetInputConnection(case_10_cube_tubes.GetOutputPort())

case_10_cube_edges_actor = vtkActor()
case_10_cube_edges_actor.SetMapper(case_10_cube_tube_mapper)
case_10_cube_edges_actor.GetProperty().SetDiffuseColor(khaki)
case_10_cube_edges_actor.GetProperty().SetSpecular(0.4)
case_10_cube_edges_actor.GetProperty().SetSpecularPower(10)

case_10_sphere_source = vtkSphereSource()
case_10_sphere_source.SetRadius(0.04)
case_10_sphere_source.SetPhiResolution(20)
case_10_sphere_source.SetThetaResolution(20)

case_10_threshold_in = vtkThresholdPoints()
case_10_threshold_in.SetInputData(case_10_grid)
case_10_threshold_in.SetUpperThreshold(0.5)
case_10_threshold_in.SetThresholdFunction(case_10_threshold_in.THRESHOLD_UPPER)

case_10_vertices_glyph = vtkGlyph3D()
case_10_vertices_glyph.SetInputConnection(case_10_threshold_in.GetOutputPort())
case_10_vertices_glyph.SetSourceConnection(case_10_sphere_source.GetOutputPort())

case_10_sphere_mapper = vtkPolyDataMapper()
case_10_sphere_mapper.SetInputConnection(case_10_vertices_glyph.GetOutputPort())
case_10_sphere_mapper.ScalarVisibilityOff()

case_10_cube_vertices_actor = vtkActor()
case_10_cube_vertices_actor.SetMapper(case_10_sphere_mapper)
case_10_cube_vertices_actor.GetProperty().SetDiffuseColor(tomato)

case_10_case_label = vtkVectorText()
case_10_case_label.SetText("Case 10 - 01101001")

case_10_label_xform = vtkTransform()
case_10_label_xform.Identity()
case_10_label_xform.Translate(-0.2, 0, 1.25)
case_10_label_xform.Scale(0.05, 0.05, 0.05)

case_10_label_transform_filter = vtkTransformPolyDataFilter()
case_10_label_transform_filter.SetTransform(case_10_label_xform)
case_10_label_transform_filter.SetInputConnection(case_10_case_label.GetOutputPort())

case_10_label_mapper = vtkPolyDataMapper()
case_10_label_mapper.SetInputConnection(case_10_label_transform_filter.GetOutputPort())

case_10_label_actor = vtkActor()
case_10_label_actor.SetMapper(case_10_label_mapper)

case_10_base_model = vtkCubeSource()
case_10_base_model.SetXLength(1.5)
case_10_base_model.SetYLength(0.01)
case_10_base_model.SetZLength(1.5)

case_10_base_mapper = vtkPolyDataMapper()
case_10_base_mapper.SetInputConnection(case_10_base_model.GetOutputPort())

case_10_base_actor = vtkActor()
case_10_base_actor.SetMapper(case_10_base_mapper)
case_10_base_actor.SetPosition(0.5, -0.09, 0.5)

renderer_10.AddActor(case_10_triangle_edge_actor)
renderer_10.AddActor(case_10_base_actor)
renderer_10.AddActor(case_10_label_actor)
renderer_10.AddActor(case_10_cube_edges_actor)
renderer_10.AddActor(case_10_cube_vertices_actor)
renderer_10.AddActor(case_10_triangle_actor)

# --- Case 11: 01110001 ---

case_11_scalars = vtkFloatArray()
case_11_scalars.InsertNextValue(1.0)
case_11_scalars.InsertNextValue(0.0)
case_11_scalars.InsertNextValue(0.0)
case_11_scalars.InsertNextValue(0.0)
case_11_scalars.InsertNextValue(1.0)
case_11_scalars.InsertNextValue(1.0)
case_11_scalars.InsertNextValue(1.0)
case_11_scalars.InsertNextValue(0.0)

case_11_points = vtkPoints()
case_11_points.InsertNextPoint(0, 0, 0)
case_11_points.InsertNextPoint(1, 0, 0)
case_11_points.InsertNextPoint(1, 1, 0)
case_11_points.InsertNextPoint(0, 1, 0)
case_11_points.InsertNextPoint(0, 0, 1)
case_11_points.InsertNextPoint(1, 0, 1)
case_11_points.InsertNextPoint(1, 1, 1)
case_11_points.InsertNextPoint(0, 1, 1)

case_11_ids = vtkIdList()
case_11_ids.InsertNextId(0)
case_11_ids.InsertNextId(1)
case_11_ids.InsertNextId(2)
case_11_ids.InsertNextId(3)
case_11_ids.InsertNextId(4)
case_11_ids.InsertNextId(5)
case_11_ids.InsertNextId(6)
case_11_ids.InsertNextId(7)

case_11_grid = vtkUnstructuredGrid()
case_11_grid.Allocate(10, 10)
case_11_grid.InsertNextCell(12, case_11_ids)
case_11_grid.SetPoints(case_11_points)
case_11_grid.GetPointData().SetScalars(case_11_scalars)

case_11_marching = vtkContourFilter()
case_11_marching.SetInputData(case_11_grid)
case_11_marching.SetValue(0, 0.5)
case_11_marching.Update()

case_11_triangle_edges = vtkExtractEdges()
case_11_triangle_edges.SetInputConnection(case_11_marching.GetOutputPort())

case_11_triangle_edge_tubes = vtkTubeFilter()
case_11_triangle_edge_tubes.SetInputConnection(case_11_triangle_edges.GetOutputPort())
case_11_triangle_edge_tubes.SetRadius(0.005)
case_11_triangle_edge_tubes.SetNumberOfSides(6)
case_11_triangle_edge_tubes.UseDefaultNormalOn()
case_11_triangle_edge_tubes.SetDefaultNormal(0.577, 0.577, 0.577)

case_11_triangle_edge_mapper = vtkPolyDataMapper()
case_11_triangle_edge_mapper.SetInputConnection(case_11_triangle_edge_tubes.GetOutputPort())
case_11_triangle_edge_mapper.ScalarVisibilityOff()

case_11_triangle_edge_actor = vtkActor()
case_11_triangle_edge_actor.SetMapper(case_11_triangle_edge_mapper)
case_11_triangle_edge_actor.GetProperty().SetDiffuseColor(lamp_black)
case_11_triangle_edge_actor.GetProperty().SetSpecular(0.4)
case_11_triangle_edge_actor.GetProperty().SetSpecularPower(10)

case_11_shrinker = vtkShrinkPolyData()
case_11_shrinker.SetShrinkFactor(1)
case_11_shrinker.SetInputConnection(case_11_marching.GetOutputPort())

case_11_triangle_mapper = vtkPolyDataMapper()
case_11_triangle_mapper.ScalarVisibilityOff()
case_11_triangle_mapper.SetInputConnection(case_11_shrinker.GetOutputPort())

case_11_triangle_actor = vtkActor()
case_11_triangle_actor.SetMapper(case_11_triangle_mapper)
case_11_triangle_actor.GetProperty().SetDiffuseColor(banana)
case_11_triangle_actor.GetProperty().SetOpacity(0.6)

case_11_cube_model = vtkCubeSource()
case_11_cube_model.SetCenter(0.5, 0.5, 0.5)

case_11_cube_edges_filter = vtkExtractEdges()
case_11_cube_edges_filter.SetInputConnection(case_11_cube_model.GetOutputPort())

case_11_cube_tubes = vtkTubeFilter()
case_11_cube_tubes.SetInputConnection(case_11_cube_edges_filter.GetOutputPort())
case_11_cube_tubes.SetRadius(0.01)
case_11_cube_tubes.SetNumberOfSides(6)
case_11_cube_tubes.UseDefaultNormalOn()
case_11_cube_tubes.SetDefaultNormal(0.577, 0.577, 0.577)

case_11_cube_tube_mapper = vtkPolyDataMapper()
case_11_cube_tube_mapper.SetInputConnection(case_11_cube_tubes.GetOutputPort())

case_11_cube_edges_actor = vtkActor()
case_11_cube_edges_actor.SetMapper(case_11_cube_tube_mapper)
case_11_cube_edges_actor.GetProperty().SetDiffuseColor(khaki)
case_11_cube_edges_actor.GetProperty().SetSpecular(0.4)
case_11_cube_edges_actor.GetProperty().SetSpecularPower(10)

case_11_sphere_source = vtkSphereSource()
case_11_sphere_source.SetRadius(0.04)
case_11_sphere_source.SetPhiResolution(20)
case_11_sphere_source.SetThetaResolution(20)

case_11_threshold_in = vtkThresholdPoints()
case_11_threshold_in.SetInputData(case_11_grid)
case_11_threshold_in.SetUpperThreshold(0.5)
case_11_threshold_in.SetThresholdFunction(case_11_threshold_in.THRESHOLD_UPPER)

case_11_vertices_glyph = vtkGlyph3D()
case_11_vertices_glyph.SetInputConnection(case_11_threshold_in.GetOutputPort())
case_11_vertices_glyph.SetSourceConnection(case_11_sphere_source.GetOutputPort())

case_11_sphere_mapper = vtkPolyDataMapper()
case_11_sphere_mapper.SetInputConnection(case_11_vertices_glyph.GetOutputPort())
case_11_sphere_mapper.ScalarVisibilityOff()

case_11_cube_vertices_actor = vtkActor()
case_11_cube_vertices_actor.SetMapper(case_11_sphere_mapper)
case_11_cube_vertices_actor.GetProperty().SetDiffuseColor(tomato)

case_11_case_label = vtkVectorText()
case_11_case_label.SetText("Case 11 - 01110001")

case_11_label_xform = vtkTransform()
case_11_label_xform.Identity()
case_11_label_xform.Translate(-0.2, 0, 1.25)
case_11_label_xform.Scale(0.05, 0.05, 0.05)

case_11_label_transform_filter = vtkTransformPolyDataFilter()
case_11_label_transform_filter.SetTransform(case_11_label_xform)
case_11_label_transform_filter.SetInputConnection(case_11_case_label.GetOutputPort())

case_11_label_mapper = vtkPolyDataMapper()
case_11_label_mapper.SetInputConnection(case_11_label_transform_filter.GetOutputPort())

case_11_label_actor = vtkActor()
case_11_label_actor.SetMapper(case_11_label_mapper)

case_11_base_model = vtkCubeSource()
case_11_base_model.SetXLength(1.5)
case_11_base_model.SetYLength(0.01)
case_11_base_model.SetZLength(1.5)

case_11_base_mapper = vtkPolyDataMapper()
case_11_base_mapper.SetInputConnection(case_11_base_model.GetOutputPort())

case_11_base_actor = vtkActor()
case_11_base_actor.SetMapper(case_11_base_mapper)
case_11_base_actor.SetPosition(0.5, -0.09, 0.5)

renderer_11.AddActor(case_11_triangle_edge_actor)
renderer_11.AddActor(case_11_base_actor)
renderer_11.AddActor(case_11_label_actor)
renderer_11.AddActor(case_11_cube_edges_actor)
renderer_11.AddActor(case_11_cube_vertices_actor)
renderer_11.AddActor(case_11_triangle_actor)

# --- Case 12: 00111010 ---

case_12_scalars = vtkFloatArray()
case_12_scalars.InsertNextValue(0.0)
case_12_scalars.InsertNextValue(1.0)
case_12_scalars.InsertNextValue(0.0)
case_12_scalars.InsertNextValue(1.0)
case_12_scalars.InsertNextValue(1.0)
case_12_scalars.InsertNextValue(1.0)
case_12_scalars.InsertNextValue(0.0)
case_12_scalars.InsertNextValue(0.0)

case_12_points = vtkPoints()
case_12_points.InsertNextPoint(0, 0, 0)
case_12_points.InsertNextPoint(1, 0, 0)
case_12_points.InsertNextPoint(1, 1, 0)
case_12_points.InsertNextPoint(0, 1, 0)
case_12_points.InsertNextPoint(0, 0, 1)
case_12_points.InsertNextPoint(1, 0, 1)
case_12_points.InsertNextPoint(1, 1, 1)
case_12_points.InsertNextPoint(0, 1, 1)

case_12_ids = vtkIdList()
case_12_ids.InsertNextId(0)
case_12_ids.InsertNextId(1)
case_12_ids.InsertNextId(2)
case_12_ids.InsertNextId(3)
case_12_ids.InsertNextId(4)
case_12_ids.InsertNextId(5)
case_12_ids.InsertNextId(6)
case_12_ids.InsertNextId(7)

case_12_grid = vtkUnstructuredGrid()
case_12_grid.Allocate(10, 10)
case_12_grid.InsertNextCell(12, case_12_ids)
case_12_grid.SetPoints(case_12_points)
case_12_grid.GetPointData().SetScalars(case_12_scalars)

case_12_marching = vtkContourFilter()
case_12_marching.SetInputData(case_12_grid)
case_12_marching.SetValue(0, 0.5)
case_12_marching.Update()

case_12_triangle_edges = vtkExtractEdges()
case_12_triangle_edges.SetInputConnection(case_12_marching.GetOutputPort())

case_12_triangle_edge_tubes = vtkTubeFilter()
case_12_triangle_edge_tubes.SetInputConnection(case_12_triangle_edges.GetOutputPort())
case_12_triangle_edge_tubes.SetRadius(0.005)
case_12_triangle_edge_tubes.SetNumberOfSides(6)
case_12_triangle_edge_tubes.UseDefaultNormalOn()
case_12_triangle_edge_tubes.SetDefaultNormal(0.577, 0.577, 0.577)

case_12_triangle_edge_mapper = vtkPolyDataMapper()
case_12_triangle_edge_mapper.SetInputConnection(case_12_triangle_edge_tubes.GetOutputPort())
case_12_triangle_edge_mapper.ScalarVisibilityOff()

case_12_triangle_edge_actor = vtkActor()
case_12_triangle_edge_actor.SetMapper(case_12_triangle_edge_mapper)
case_12_triangle_edge_actor.GetProperty().SetDiffuseColor(lamp_black)
case_12_triangle_edge_actor.GetProperty().SetSpecular(0.4)
case_12_triangle_edge_actor.GetProperty().SetSpecularPower(10)

case_12_shrinker = vtkShrinkPolyData()
case_12_shrinker.SetShrinkFactor(1)
case_12_shrinker.SetInputConnection(case_12_marching.GetOutputPort())

case_12_triangle_mapper = vtkPolyDataMapper()
case_12_triangle_mapper.ScalarVisibilityOff()
case_12_triangle_mapper.SetInputConnection(case_12_shrinker.GetOutputPort())

case_12_triangle_actor = vtkActor()
case_12_triangle_actor.SetMapper(case_12_triangle_mapper)
case_12_triangle_actor.GetProperty().SetDiffuseColor(banana)
case_12_triangle_actor.GetProperty().SetOpacity(0.6)

case_12_cube_model = vtkCubeSource()
case_12_cube_model.SetCenter(0.5, 0.5, 0.5)

case_12_cube_edges_filter = vtkExtractEdges()
case_12_cube_edges_filter.SetInputConnection(case_12_cube_model.GetOutputPort())

case_12_cube_tubes = vtkTubeFilter()
case_12_cube_tubes.SetInputConnection(case_12_cube_edges_filter.GetOutputPort())
case_12_cube_tubes.SetRadius(0.01)
case_12_cube_tubes.SetNumberOfSides(6)
case_12_cube_tubes.UseDefaultNormalOn()
case_12_cube_tubes.SetDefaultNormal(0.577, 0.577, 0.577)

case_12_cube_tube_mapper = vtkPolyDataMapper()
case_12_cube_tube_mapper.SetInputConnection(case_12_cube_tubes.GetOutputPort())

case_12_cube_edges_actor = vtkActor()
case_12_cube_edges_actor.SetMapper(case_12_cube_tube_mapper)
case_12_cube_edges_actor.GetProperty().SetDiffuseColor(khaki)
case_12_cube_edges_actor.GetProperty().SetSpecular(0.4)
case_12_cube_edges_actor.GetProperty().SetSpecularPower(10)

case_12_sphere_source = vtkSphereSource()
case_12_sphere_source.SetRadius(0.04)
case_12_sphere_source.SetPhiResolution(20)
case_12_sphere_source.SetThetaResolution(20)

case_12_threshold_in = vtkThresholdPoints()
case_12_threshold_in.SetInputData(case_12_grid)
case_12_threshold_in.SetUpperThreshold(0.5)
case_12_threshold_in.SetThresholdFunction(case_12_threshold_in.THRESHOLD_UPPER)

case_12_vertices_glyph = vtkGlyph3D()
case_12_vertices_glyph.SetInputConnection(case_12_threshold_in.GetOutputPort())
case_12_vertices_glyph.SetSourceConnection(case_12_sphere_source.GetOutputPort())

case_12_sphere_mapper = vtkPolyDataMapper()
case_12_sphere_mapper.SetInputConnection(case_12_vertices_glyph.GetOutputPort())
case_12_sphere_mapper.ScalarVisibilityOff()

case_12_cube_vertices_actor = vtkActor()
case_12_cube_vertices_actor.SetMapper(case_12_sphere_mapper)
case_12_cube_vertices_actor.GetProperty().SetDiffuseColor(tomato)

case_12_case_label = vtkVectorText()
case_12_case_label.SetText("Case 12 - 00111010")

case_12_label_xform = vtkTransform()
case_12_label_xform.Identity()
case_12_label_xform.Translate(-0.2, 0, 1.25)
case_12_label_xform.Scale(0.05, 0.05, 0.05)

case_12_label_transform_filter = vtkTransformPolyDataFilter()
case_12_label_transform_filter.SetTransform(case_12_label_xform)
case_12_label_transform_filter.SetInputConnection(case_12_case_label.GetOutputPort())

case_12_label_mapper = vtkPolyDataMapper()
case_12_label_mapper.SetInputConnection(case_12_label_transform_filter.GetOutputPort())

case_12_label_actor = vtkActor()
case_12_label_actor.SetMapper(case_12_label_mapper)

case_12_base_model = vtkCubeSource()
case_12_base_model.SetXLength(1.5)
case_12_base_model.SetYLength(0.01)
case_12_base_model.SetZLength(1.5)

case_12_base_mapper = vtkPolyDataMapper()
case_12_base_mapper.SetInputConnection(case_12_base_model.GetOutputPort())

case_12_base_actor = vtkActor()
case_12_base_actor.SetMapper(case_12_base_mapper)
case_12_base_actor.SetPosition(0.5, -0.09, 0.5)

renderer_12.AddActor(case_12_triangle_edge_actor)
renderer_12.AddActor(case_12_base_actor)
renderer_12.AddActor(case_12_label_actor)
renderer_12.AddActor(case_12_cube_edges_actor)
renderer_12.AddActor(case_12_cube_vertices_actor)
renderer_12.AddActor(case_12_triangle_actor)

# --- Case 13: 01011010 ---

case_13_scalars = vtkFloatArray()
case_13_scalars.InsertNextValue(0.0)
case_13_scalars.InsertNextValue(1.0)
case_13_scalars.InsertNextValue(0.0)
case_13_scalars.InsertNextValue(1.0)
case_13_scalars.InsertNextValue(1.0)
case_13_scalars.InsertNextValue(0.0)
case_13_scalars.InsertNextValue(1.0)
case_13_scalars.InsertNextValue(0.0)

case_13_points = vtkPoints()
case_13_points.InsertNextPoint(0, 0, 0)
case_13_points.InsertNextPoint(1, 0, 0)
case_13_points.InsertNextPoint(1, 1, 0)
case_13_points.InsertNextPoint(0, 1, 0)
case_13_points.InsertNextPoint(0, 0, 1)
case_13_points.InsertNextPoint(1, 0, 1)
case_13_points.InsertNextPoint(1, 1, 1)
case_13_points.InsertNextPoint(0, 1, 1)

case_13_ids = vtkIdList()
case_13_ids.InsertNextId(0)
case_13_ids.InsertNextId(1)
case_13_ids.InsertNextId(2)
case_13_ids.InsertNextId(3)
case_13_ids.InsertNextId(4)
case_13_ids.InsertNextId(5)
case_13_ids.InsertNextId(6)
case_13_ids.InsertNextId(7)

case_13_grid = vtkUnstructuredGrid()
case_13_grid.Allocate(10, 10)
case_13_grid.InsertNextCell(12, case_13_ids)
case_13_grid.SetPoints(case_13_points)
case_13_grid.GetPointData().SetScalars(case_13_scalars)

case_13_marching = vtkContourFilter()
case_13_marching.SetInputData(case_13_grid)
case_13_marching.SetValue(0, 0.5)
case_13_marching.Update()

case_13_triangle_edges = vtkExtractEdges()
case_13_triangle_edges.SetInputConnection(case_13_marching.GetOutputPort())

case_13_triangle_edge_tubes = vtkTubeFilter()
case_13_triangle_edge_tubes.SetInputConnection(case_13_triangle_edges.GetOutputPort())
case_13_triangle_edge_tubes.SetRadius(0.005)
case_13_triangle_edge_tubes.SetNumberOfSides(6)
case_13_triangle_edge_tubes.UseDefaultNormalOn()
case_13_triangle_edge_tubes.SetDefaultNormal(0.577, 0.577, 0.577)

case_13_triangle_edge_mapper = vtkPolyDataMapper()
case_13_triangle_edge_mapper.SetInputConnection(case_13_triangle_edge_tubes.GetOutputPort())
case_13_triangle_edge_mapper.ScalarVisibilityOff()

case_13_triangle_edge_actor = vtkActor()
case_13_triangle_edge_actor.SetMapper(case_13_triangle_edge_mapper)
case_13_triangle_edge_actor.GetProperty().SetDiffuseColor(lamp_black)
case_13_triangle_edge_actor.GetProperty().SetSpecular(0.4)
case_13_triangle_edge_actor.GetProperty().SetSpecularPower(10)

case_13_shrinker = vtkShrinkPolyData()
case_13_shrinker.SetShrinkFactor(1)
case_13_shrinker.SetInputConnection(case_13_marching.GetOutputPort())

case_13_triangle_mapper = vtkPolyDataMapper()
case_13_triangle_mapper.ScalarVisibilityOff()
case_13_triangle_mapper.SetInputConnection(case_13_shrinker.GetOutputPort())

case_13_triangle_actor = vtkActor()
case_13_triangle_actor.SetMapper(case_13_triangle_mapper)
case_13_triangle_actor.GetProperty().SetDiffuseColor(banana)
case_13_triangle_actor.GetProperty().SetOpacity(0.6)

case_13_cube_model = vtkCubeSource()
case_13_cube_model.SetCenter(0.5, 0.5, 0.5)

case_13_cube_edges_filter = vtkExtractEdges()
case_13_cube_edges_filter.SetInputConnection(case_13_cube_model.GetOutputPort())

case_13_cube_tubes = vtkTubeFilter()
case_13_cube_tubes.SetInputConnection(case_13_cube_edges_filter.GetOutputPort())
case_13_cube_tubes.SetRadius(0.01)
case_13_cube_tubes.SetNumberOfSides(6)
case_13_cube_tubes.UseDefaultNormalOn()
case_13_cube_tubes.SetDefaultNormal(0.577, 0.577, 0.577)

case_13_cube_tube_mapper = vtkPolyDataMapper()
case_13_cube_tube_mapper.SetInputConnection(case_13_cube_tubes.GetOutputPort())

case_13_cube_edges_actor = vtkActor()
case_13_cube_edges_actor.SetMapper(case_13_cube_tube_mapper)
case_13_cube_edges_actor.GetProperty().SetDiffuseColor(khaki)
case_13_cube_edges_actor.GetProperty().SetSpecular(0.4)
case_13_cube_edges_actor.GetProperty().SetSpecularPower(10)

case_13_sphere_source = vtkSphereSource()
case_13_sphere_source.SetRadius(0.04)
case_13_sphere_source.SetPhiResolution(20)
case_13_sphere_source.SetThetaResolution(20)

case_13_threshold_in = vtkThresholdPoints()
case_13_threshold_in.SetInputData(case_13_grid)
case_13_threshold_in.SetUpperThreshold(0.5)
case_13_threshold_in.SetThresholdFunction(case_13_threshold_in.THRESHOLD_UPPER)

case_13_vertices_glyph = vtkGlyph3D()
case_13_vertices_glyph.SetInputConnection(case_13_threshold_in.GetOutputPort())
case_13_vertices_glyph.SetSourceConnection(case_13_sphere_source.GetOutputPort())

case_13_sphere_mapper = vtkPolyDataMapper()
case_13_sphere_mapper.SetInputConnection(case_13_vertices_glyph.GetOutputPort())
case_13_sphere_mapper.ScalarVisibilityOff()

case_13_cube_vertices_actor = vtkActor()
case_13_cube_vertices_actor.SetMapper(case_13_sphere_mapper)
case_13_cube_vertices_actor.GetProperty().SetDiffuseColor(tomato)

case_13_case_label = vtkVectorText()
case_13_case_label.SetText("Case 13 - 01011010")

case_13_label_xform = vtkTransform()
case_13_label_xform.Identity()
case_13_label_xform.Translate(-0.2, 0, 1.25)
case_13_label_xform.Scale(0.05, 0.05, 0.05)

case_13_label_transform_filter = vtkTransformPolyDataFilter()
case_13_label_transform_filter.SetTransform(case_13_label_xform)
case_13_label_transform_filter.SetInputConnection(case_13_case_label.GetOutputPort())

case_13_label_mapper = vtkPolyDataMapper()
case_13_label_mapper.SetInputConnection(case_13_label_transform_filter.GetOutputPort())

case_13_label_actor = vtkActor()
case_13_label_actor.SetMapper(case_13_label_mapper)

case_13_base_model = vtkCubeSource()
case_13_base_model.SetXLength(1.5)
case_13_base_model.SetYLength(0.01)
case_13_base_model.SetZLength(1.5)

case_13_base_mapper = vtkPolyDataMapper()
case_13_base_mapper.SetInputConnection(case_13_base_model.GetOutputPort())

case_13_base_actor = vtkActor()
case_13_base_actor.SetMapper(case_13_base_mapper)
case_13_base_actor.SetPosition(0.5, -0.09, 0.5)

renderer_13.AddActor(case_13_triangle_edge_actor)
renderer_13.AddActor(case_13_base_actor)
renderer_13.AddActor(case_13_label_actor)
renderer_13.AddActor(case_13_cube_edges_actor)
renderer_13.AddActor(case_13_cube_vertices_actor)
renderer_13.AddActor(case_13_triangle_actor)

# --- Case 14: 11101101 ---

case_14_scalars = vtkFloatArray()
case_14_scalars.InsertNextValue(1.0)
case_14_scalars.InsertNextValue(0.0)
case_14_scalars.InsertNextValue(1.0)
case_14_scalars.InsertNextValue(1.0)
case_14_scalars.InsertNextValue(0.0)
case_14_scalars.InsertNextValue(1.0)
case_14_scalars.InsertNextValue(1.0)
case_14_scalars.InsertNextValue(1.0)

case_14_points = vtkPoints()
case_14_points.InsertNextPoint(0, 0, 0)
case_14_points.InsertNextPoint(1, 0, 0)
case_14_points.InsertNextPoint(1, 1, 0)
case_14_points.InsertNextPoint(0, 1, 0)
case_14_points.InsertNextPoint(0, 0, 1)
case_14_points.InsertNextPoint(1, 0, 1)
case_14_points.InsertNextPoint(1, 1, 1)
case_14_points.InsertNextPoint(0, 1, 1)

case_14_ids = vtkIdList()
case_14_ids.InsertNextId(0)
case_14_ids.InsertNextId(1)
case_14_ids.InsertNextId(2)
case_14_ids.InsertNextId(3)
case_14_ids.InsertNextId(4)
case_14_ids.InsertNextId(5)
case_14_ids.InsertNextId(6)
case_14_ids.InsertNextId(7)

case_14_grid = vtkUnstructuredGrid()
case_14_grid.Allocate(10, 10)
case_14_grid.InsertNextCell(12, case_14_ids)
case_14_grid.SetPoints(case_14_points)
case_14_grid.GetPointData().SetScalars(case_14_scalars)

case_14_marching = vtkContourFilter()
case_14_marching.SetInputData(case_14_grid)
case_14_marching.SetValue(0, 0.5)
case_14_marching.Update()

case_14_triangle_edges = vtkExtractEdges()
case_14_triangle_edges.SetInputConnection(case_14_marching.GetOutputPort())

case_14_triangle_edge_tubes = vtkTubeFilter()
case_14_triangle_edge_tubes.SetInputConnection(case_14_triangle_edges.GetOutputPort())
case_14_triangle_edge_tubes.SetRadius(0.005)
case_14_triangle_edge_tubes.SetNumberOfSides(6)
case_14_triangle_edge_tubes.UseDefaultNormalOn()
case_14_triangle_edge_tubes.SetDefaultNormal(0.577, 0.577, 0.577)

case_14_triangle_edge_mapper = vtkPolyDataMapper()
case_14_triangle_edge_mapper.SetInputConnection(case_14_triangle_edge_tubes.GetOutputPort())
case_14_triangle_edge_mapper.ScalarVisibilityOff()

case_14_triangle_edge_actor = vtkActor()
case_14_triangle_edge_actor.SetMapper(case_14_triangle_edge_mapper)
case_14_triangle_edge_actor.GetProperty().SetDiffuseColor(lamp_black)
case_14_triangle_edge_actor.GetProperty().SetSpecular(0.4)
case_14_triangle_edge_actor.GetProperty().SetSpecularPower(10)

case_14_shrinker = vtkShrinkPolyData()
case_14_shrinker.SetShrinkFactor(1)
case_14_shrinker.SetInputConnection(case_14_marching.GetOutputPort())

case_14_triangle_mapper = vtkPolyDataMapper()
case_14_triangle_mapper.ScalarVisibilityOff()
case_14_triangle_mapper.SetInputConnection(case_14_shrinker.GetOutputPort())

case_14_triangle_actor = vtkActor()
case_14_triangle_actor.SetMapper(case_14_triangle_mapper)
case_14_triangle_actor.GetProperty().SetDiffuseColor(banana)
case_14_triangle_actor.GetProperty().SetOpacity(0.6)

case_14_cube_model = vtkCubeSource()
case_14_cube_model.SetCenter(0.5, 0.5, 0.5)

case_14_cube_edges_filter = vtkExtractEdges()
case_14_cube_edges_filter.SetInputConnection(case_14_cube_model.GetOutputPort())

case_14_cube_tubes = vtkTubeFilter()
case_14_cube_tubes.SetInputConnection(case_14_cube_edges_filter.GetOutputPort())
case_14_cube_tubes.SetRadius(0.01)
case_14_cube_tubes.SetNumberOfSides(6)
case_14_cube_tubes.UseDefaultNormalOn()
case_14_cube_tubes.SetDefaultNormal(0.577, 0.577, 0.577)

case_14_cube_tube_mapper = vtkPolyDataMapper()
case_14_cube_tube_mapper.SetInputConnection(case_14_cube_tubes.GetOutputPort())

case_14_cube_edges_actor = vtkActor()
case_14_cube_edges_actor.SetMapper(case_14_cube_tube_mapper)
case_14_cube_edges_actor.GetProperty().SetDiffuseColor(khaki)
case_14_cube_edges_actor.GetProperty().SetSpecular(0.4)
case_14_cube_edges_actor.GetProperty().SetSpecularPower(10)

case_14_sphere_source = vtkSphereSource()
case_14_sphere_source.SetRadius(0.04)
case_14_sphere_source.SetPhiResolution(20)
case_14_sphere_source.SetThetaResolution(20)

case_14_threshold_in = vtkThresholdPoints()
case_14_threshold_in.SetInputData(case_14_grid)
case_14_threshold_in.SetUpperThreshold(0.5)
case_14_threshold_in.SetThresholdFunction(case_14_threshold_in.THRESHOLD_UPPER)

case_14_vertices_glyph = vtkGlyph3D()
case_14_vertices_glyph.SetInputConnection(case_14_threshold_in.GetOutputPort())
case_14_vertices_glyph.SetSourceConnection(case_14_sphere_source.GetOutputPort())

case_14_sphere_mapper = vtkPolyDataMapper()
case_14_sphere_mapper.SetInputConnection(case_14_vertices_glyph.GetOutputPort())
case_14_sphere_mapper.ScalarVisibilityOff()

case_14_cube_vertices_actor = vtkActor()
case_14_cube_vertices_actor.SetMapper(case_14_sphere_mapper)
case_14_cube_vertices_actor.GetProperty().SetDiffuseColor(tomato)

case_14_case_label = vtkVectorText()
case_14_case_label.SetText("Case 14 - 11101101")

case_14_label_xform = vtkTransform()
case_14_label_xform.Identity()
case_14_label_xform.Translate(-0.2, 0, 1.25)
case_14_label_xform.Scale(0.05, 0.05, 0.05)

case_14_label_transform_filter = vtkTransformPolyDataFilter()
case_14_label_transform_filter.SetTransform(case_14_label_xform)
case_14_label_transform_filter.SetInputConnection(case_14_case_label.GetOutputPort())

case_14_label_mapper = vtkPolyDataMapper()
case_14_label_mapper.SetInputConnection(case_14_label_transform_filter.GetOutputPort())

case_14_label_actor = vtkActor()
case_14_label_actor.SetMapper(case_14_label_mapper)

case_14_base_model = vtkCubeSource()
case_14_base_model.SetXLength(1.5)
case_14_base_model.SetYLength(0.01)
case_14_base_model.SetZLength(1.5)

case_14_base_mapper = vtkPolyDataMapper()
case_14_base_mapper.SetInputConnection(case_14_base_model.GetOutputPort())

case_14_base_actor = vtkActor()
case_14_base_actor.SetMapper(case_14_base_mapper)
case_14_base_actor.SetPosition(0.5, -0.09, 0.5)

renderer_14.AddActor(case_14_triangle_edge_actor)
renderer_14.AddActor(case_14_base_actor)
renderer_14.AddActor(case_14_label_actor)
renderer_14.AddActor(case_14_cube_edges_actor)
renderer_14.AddActor(case_14_cube_vertices_actor)
renderer_14.AddActor(case_14_triangle_actor)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer_0)
render_window.AddRenderer(renderer_1)
render_window.AddRenderer(renderer_2)
render_window.AddRenderer(renderer_3)
render_window.AddRenderer(renderer_4)
render_window.AddRenderer(renderer_5)
render_window.AddRenderer(renderer_6)
render_window.AddRenderer(renderer_7)
render_window.AddRenderer(renderer_8)
render_window.AddRenderer(renderer_9)
render_window.AddRenderer(renderer_10)
render_window.AddRenderer(renderer_11)
render_window.AddRenderer(renderer_12)
render_window.AddRenderer(renderer_13)
render_window.AddRenderer(renderer_14)
render_window.AddRenderer(renderer_15)
render_window.SetWindowName("marching cubes all cases")
render_window.SetMultiSamples(0)
render_window.SetSize(renderer_size * x_grid, renderer_size * y_grid)

# Viewport layout: 4 columns x 4 rows
renderer_0.SetViewport(0.0, 0.75, 0.25, 1.0)
renderer_1.SetViewport(0.25, 0.75, 0.5, 1.0)
renderer_2.SetViewport(0.5, 0.75, 0.75, 1.0)
renderer_3.SetViewport(0.75, 0.75, 1.0, 1.0)
renderer_4.SetViewport(0.0, 0.5, 0.25, 0.75)
renderer_5.SetViewport(0.25, 0.5, 0.5, 0.75)
renderer_6.SetViewport(0.5, 0.5, 0.75, 0.75)
renderer_7.SetViewport(0.75, 0.5, 1.0, 0.75)
renderer_8.SetViewport(0.0, 0.25, 0.25, 0.5)
renderer_9.SetViewport(0.25, 0.25, 0.5, 0.5)
renderer_10.SetViewport(0.5, 0.25, 0.75, 0.5)
renderer_11.SetViewport(0.75, 0.25, 1.0, 0.5)
renderer_12.SetViewport(0.0, 0.0, 0.25, 0.25)
renderer_13.SetViewport(0.25, 0.0, 0.5, 0.25)
renderer_14.SetViewport(0.5, 0.0, 0.75, 0.25)
renderer_15.SetViewport(0.75, 0.0, 1.0, 0.25)

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
renderer_6.SetActiveCamera(renderer_0.GetActiveCamera())
renderer_7.SetActiveCamera(renderer_0.GetActiveCamera())
renderer_8.SetActiveCamera(renderer_0.GetActiveCamera())
renderer_9.SetActiveCamera(renderer_0.GetActiveCamera())
renderer_10.SetActiveCamera(renderer_0.GetActiveCamera())
renderer_11.SetActiveCamera(renderer_0.GetActiveCamera())
renderer_12.SetActiveCamera(renderer_0.GetActiveCamera())
renderer_13.SetActiveCamera(renderer_0.GetActiveCamera())
renderer_14.SetActiveCamera(renderer_0.GetActiveCamera())

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
