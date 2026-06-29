#!/usr/bin/env python

# Clip a hexahedron cell and visualize the result with edges, vertices,
# and a label using vtkClipDataSet.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonColor import vtkNamedColors
from vtkmodules.vtkCommonCore import (
    vtkFloatArray,
    vtkIdList,
    vtkPoints,
)
from vtkmodules.vtkCommonDataModel import vtkUnstructuredGrid
from vtkmodules.vtkCommonTransforms import vtkTransform
from vtkmodules.vtkFiltersCore import (
    vtkExtractEdges,
    vtkGlyph3D,
    vtkThresholdPoints,
    vtkTubeFilter,
)
from vtkmodules.vtkFiltersGeneral import (
    vtkClipDataSet,
    vtkShrinkFilter,
    vtkTransformPolyDataFilter,
)
from vtkmodules.vtkFiltersSources import (
    vtkCubeSource,
    vtkSphereSource,
)
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkDataSetMapper,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)
from vtkmodules.vtkRenderingFreeType import vtkVectorText

colors = vtkNamedColors()

# Define a single hexahedron
scalars = vtkFloatArray()
scalars.InsertNextValue(1.0)
scalars.InsertNextValue(1.0)
scalars.InsertNextValue(0.0)
scalars.InsertNextValue(0.0)
scalars.InsertNextValue(0.0)
scalars.InsertNextValue(0.0)
scalars.InsertNextValue(0.0)
scalars.InsertNextValue(0.0)

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
for i in range(8):
    ids.InsertNextId(i)

grid = vtkUnstructuredGrid()
grid.Allocate(10, 10)
grid.InsertNextCell(12, ids)
grid.SetPoints(points)
grid.GetPointData().SetScalars(scalars)

# Clip the hex
clipper = vtkClipDataSet()
clipper.SetInputData(grid)
clipper.SetValue(0.5)

# Tube edges for clipped output
tet_edges = vtkExtractEdges()
tet_edges.SetInputConnection(clipper.GetOutputPort())

tet_edge_tubes = vtkTubeFilter()
tet_edge_tubes.SetInputConnection(tet_edges.GetOutputPort())
tet_edge_tubes.SetRadius(0.005)
tet_edge_tubes.SetNumberOfSides(6)
tet_edge_tubes.UseDefaultNormalOn()
tet_edge_tubes.SetDefaultNormal(0.577, 0.577, 0.577)

tet_edge_mapper = vtkPolyDataMapper()
tet_edge_mapper.SetInputConnection(tet_edge_tubes.GetOutputPort())
tet_edge_mapper.ScalarVisibilityOff()

rgb = [0.0, 0.0, 0.0]

tet_edge_actor = vtkActor()
tet_edge_actor.SetMapper(tet_edge_mapper)
colors.GetColorRGB("lamp_black", rgb)
tet_edge_actor.GetProperty().SetDiffuseColor(rgb)
tet_edge_actor.GetProperty().SetSpecular(0.4)
tet_edge_actor.GetProperty().SetSpecularPower(10)

# Shrink the clipped cells
shrinker = vtkShrinkFilter()
shrinker.SetShrinkFactor(1)
shrinker.SetInputConnection(clipper.GetOutputPort())

shrink_mapper = vtkDataSetMapper()
shrink_mapper.ScalarVisibilityOff()
shrink_mapper.SetInputConnection(shrinker.GetOutputPort())

colors.GetColorRGB("banana", rgb)
tets_actor = vtkActor()
tets_actor.SetMapper(shrink_mapper)
tets_actor.GetProperty().SetDiffuseColor(rgb)

# Cube wireframe model
cube_model = vtkCubeSource()
cube_model.SetCenter(0.5, 0.5, 0.5)

edges = vtkExtractEdges()
edges.SetInputConnection(cube_model.GetOutputPort())

tubes = vtkTubeFilter()
tubes.SetInputConnection(edges.GetOutputPort())
tubes.SetRadius(0.01)
tubes.SetNumberOfSides(6)
tubes.UseDefaultNormalOn()
tubes.SetDefaultNormal(0.577, 0.577, 0.577)

tube_mapper = vtkPolyDataMapper()
tube_mapper.SetInputConnection(tubes.GetOutputPort())

colors.GetColorRGB("khaki", rgb)
cube_edges_actor = vtkActor()
cube_edges_actor.SetMapper(tube_mapper)
cube_edges_actor.GetProperty().SetDiffuseColor(rgb)
cube_edges_actor.GetProperty().SetSpecular(0.4)
cube_edges_actor.GetProperty().SetSpecularPower(10)

# Vertex glyphs
sphere = vtkSphereSource()
sphere.SetRadius(0.04)
sphere.SetPhiResolution(20)
sphere.SetThetaResolution(20)

threshold_in = vtkThresholdPoints()
threshold_in.SetInputData(grid)
threshold_in.SetUpperThreshold(0.5)
threshold_in.SetThresholdFunction(vtkThresholdPoints.THRESHOLD_UPPER)

vertices = vtkGlyph3D()
vertices.SetInputConnection(threshold_in.GetOutputPort())
vertices.SetSourceConnection(sphere.GetOutputPort())

sphere_mapper = vtkPolyDataMapper()
sphere_mapper.SetInputConnection(vertices.GetOutputPort())
sphere_mapper.ScalarVisibilityOff()

colors.GetColorRGB("tomato", rgb)
cube_vertices_actor = vtkActor()
cube_vertices_actor.SetMapper(sphere_mapper)
cube_vertices_actor.GetProperty().SetDiffuseColor(rgb)

# Label
case_label = vtkVectorText()
case_label.SetText("Case 2")

label_transform = vtkTransform()
label_transform.Identity()
label_transform.Translate(-0.2, 0, 1.25)
label_transform.Scale(0.05, 0.05, 0.05)

label_tpd = vtkTransformPolyDataFilter()
label_tpd.SetTransform(label_transform)
label_tpd.SetInputConnection(case_label.GetOutputPort())

label_mapper = vtkPolyDataMapper()
label_mapper.SetInputConnection(label_tpd.GetOutputPort())

label_actor = vtkActor()
label_actor.SetMapper(label_mapper)

# Base platform
base_model = vtkCubeSource()
base_model.SetXLength(1.5)
base_model.SetYLength(0.01)
base_model.SetZLength(1.5)

base_mapper = vtkPolyDataMapper()
base_mapper.SetInputConnection(base_model.GetOutputPort())

base_actor = vtkActor()
base_actor.SetMapper(base_mapper)
base_actor.SetPosition(0.5, -0.09, 0.5)

# Renderer
colors.GetColorRGB("slate_grey", rgb)
renderer = vtkRenderer()
renderer.AddActor(tet_edge_actor)
renderer.AddActor(base_actor)
renderer.AddActor(label_actor)
renderer.AddActor(cube_edges_actor)
renderer.AddActor(cube_vertices_actor)
renderer.AddActor(tets_actor)
renderer.SetBackground(rgb)

# Set scalars for case 2
scalars.InsertValue(0, 1)
scalars.InsertValue(1, 1)
scalars.InsertValue(2, 0)
scalars.InsertValue(3, 0)
scalars.InsertValue(4, 0)
scalars.InsertValue(5, 0)
scalars.InsertValue(6, 0)
scalars.InsertValue(7, 0)
case_label.SetText("Case 2 - 00000011")

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(400, 400)
render_window.SetWindowName("clip hex")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.ResetCamera()
renderer.GetActiveCamera().Dolly(1.2)
renderer.GetActiveCamera().Azimuth(30)
renderer.GetActiveCamera().Elevation(20)
renderer.ResetCameraClippingRange()

interactor.Initialize()
interactor.Start()
