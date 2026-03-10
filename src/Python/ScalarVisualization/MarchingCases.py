#!/usr/bin/env python

# Visualize marching cubes case 7 for 3D isosurface generation.

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

# Case 7 vertex pattern: 1=IN, 0=OUT
pattern = [1, 1, 0, 0, 0, 0, 1, 0]
label_str = "Case 7 - 01000011"

# Source: define a single hexahedron cell
scalars = vtkFloatArray()
for v in pattern:
    scalars.InsertNextValue(float(v))

points = vtkPoints()
points.InsertNextPoint(0, 0, 0)
points.InsertNextPoint(1, 0, 0)
points.InsertNextPoint(1, 1, 0)
points.InsertNextPoint(0, 1, 0)
points.InsertNextPoint(0, 0, 1)
points.InsertNextPoint(1, 0, 1)
points.InsertNextPoint(1, 1, 1)
points.InsertNextPoint(0, 1, 1)

ids = vtkIdList()
for j in range(8):
    ids.InsertNextId(j)

grid = vtkUnstructuredGrid()
grid.Allocate(10, 10)
grid.InsertNextCell(12, ids)
grid.SetPoints(points)
grid.GetPointData().SetScalars(scalars)

# Filter: contour at 0.5 to find isosurface triangles
marching = vtkContourFilter()
marching.SetInputData(grid)
marching.SetValue(0, 0.5)
marching.Update()

# Filter: extract and tube the triangle edges
triangle_edges = vtkExtractEdges()
triangle_edges.SetInputConnection(marching.GetOutputPort())

triangle_edge_tubes = vtkTubeFilter()
triangle_edge_tubes.SetInputConnection(triangle_edges.GetOutputPort())
triangle_edge_tubes.SetRadius(0.005)
triangle_edge_tubes.SetNumberOfSides(6)
triangle_edge_tubes.UseDefaultNormalOn()
triangle_edge_tubes.SetDefaultNormal(0.577, 0.577, 0.577)

triangle_edge_mapper = vtkPolyDataMapper()
triangle_edge_mapper.SetInputConnection(triangle_edge_tubes.GetOutputPort())
triangle_edge_mapper.ScalarVisibilityOff()

triangle_edge_actor = vtkActor()
triangle_edge_actor.SetMapper(triangle_edge_mapper)
triangle_edge_actor.GetProperty().SetDiffuseColor(lamp_black)
triangle_edge_actor.GetProperty().SetSpecular(0.4)
triangle_edge_actor.GetProperty().SetSpecularPower(10)

# Filter: shrink the contour triangles for clarity
shrinker = vtkShrinkPolyData()
shrinker.SetShrinkFactor(1)
shrinker.SetInputConnection(marching.GetOutputPort())

triangle_mapper = vtkPolyDataMapper()
triangle_mapper.ScalarVisibilityOff()
triangle_mapper.SetInputConnection(shrinker.GetOutputPort())

triangle_actor = vtkActor()
triangle_actor.SetMapper(triangle_mapper)
triangle_actor.GetProperty().SetDiffuseColor(banana)
triangle_actor.GetProperty().SetOpacity(0.6)

# Source: cube outline
cube_model = vtkCubeSource()
cube_model.SetCenter(0.5, 0.5, 0.5)

cube_edges_filter = vtkExtractEdges()
cube_edges_filter.SetInputConnection(cube_model.GetOutputPort())

cube_tubes = vtkTubeFilter()
cube_tubes.SetInputConnection(cube_edges_filter.GetOutputPort())
cube_tubes.SetRadius(0.01)
cube_tubes.SetNumberOfSides(6)
cube_tubes.UseDefaultNormalOn()
cube_tubes.SetDefaultNormal(0.577, 0.577, 0.577)

cube_tube_mapper = vtkPolyDataMapper()
cube_tube_mapper.SetInputConnection(cube_tubes.GetOutputPort())

cube_edges_actor = vtkActor()
cube_edges_actor.SetMapper(cube_tube_mapper)
cube_edges_actor.GetProperty().SetDiffuseColor(khaki)
cube_edges_actor.GetProperty().SetSpecular(0.4)
cube_edges_actor.GetProperty().SetSpecularPower(10)

# Filter: sphere glyphs at active (IN) vertices
sphere_source = vtkSphereSource()
sphere_source.SetRadius(0.04)
sphere_source.SetPhiResolution(20)
sphere_source.SetThetaResolution(20)

threshold_in = vtkThresholdPoints()
threshold_in.SetInputData(grid)
threshold_in.SetUpperThreshold(0.5)
threshold_in.SetThresholdFunction(threshold_in.THRESHOLD_UPPER)

vertices_glyph = vtkGlyph3D()
vertices_glyph.SetInputConnection(threshold_in.GetOutputPort())
vertices_glyph.SetSourceConnection(sphere_source.GetOutputPort())

sphere_mapper = vtkPolyDataMapper()
sphere_mapper.SetInputConnection(vertices_glyph.GetOutputPort())
sphere_mapper.ScalarVisibilityOff()

cube_vertices_actor = vtkActor()
cube_vertices_actor.SetMapper(sphere_mapper)
cube_vertices_actor.GetProperty().SetDiffuseColor(tomato)

# Label: case text positioned above the cube
case_label = vtkVectorText()
case_label.SetText(label_str)

label_xform = vtkTransform()
label_xform.Identity()
label_xform.Translate(-0.2, 0, 1.25)
label_xform.Scale(0.05, 0.05, 0.05)

label_transform_filter = vtkTransformPolyDataFilter()
label_transform_filter.SetTransform(label_xform)
label_transform_filter.SetInputConnection(case_label.GetOutputPort())

label_mapper = vtkPolyDataMapper()
label_mapper.SetInputConnection(label_transform_filter.GetOutputPort())

label_actor = vtkActor()
label_actor.SetMapper(label_mapper)

# Source: base platform
base_model = vtkCubeSource()
base_model.SetXLength(1.5)
base_model.SetYLength(0.01)
base_model.SetZLength(1.5)

base_mapper = vtkPolyDataMapper()
base_mapper.SetInputConnection(base_model.GetOutputPort())

base_actor = vtkActor()
base_actor.SetMapper(base_mapper)
base_actor.SetPosition(0.5, -0.09, 0.5)

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.AddActor(triangle_edge_actor)
renderer.AddActor(base_actor)
renderer.AddActor(label_actor)
renderer.AddActor(cube_edges_actor)
renderer.AddActor(cube_vertices_actor)
renderer.AddActor(triangle_actor)
renderer.SetBackground(slate_grey)
renderer.GetActiveCamera().Dolly(1.2)
renderer.GetActiveCamera().Azimuth(30)
renderer.GetActiveCamera().Elevation(20)
renderer.ResetCamera()
renderer.ResetCameraClippingRange()

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("MarchingCases")
render_window.SetSize(300, 300)

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Start()
