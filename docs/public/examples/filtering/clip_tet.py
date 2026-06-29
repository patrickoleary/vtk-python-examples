#!/usr/bin/env python

# Clip a tetrahedron cell and visualize the result with edges, vertices,
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
rgb = [0.0, 0.0, 0.0]

# Define a single tetrahedron
scalars = vtkFloatArray()
scalars.InsertNextValue(1.0)
scalars.InsertNextValue(0.0)
scalars.InsertNextValue(0.0)
scalars.InsertNextValue(1.0)

points = vtkPoints()
points.InsertNextPoint(0, 0, 0)
points.InsertNextPoint(1, 0, 0)
points.InsertNextPoint(0, 1, 0)
points.InsertNextPoint(0, 0, 1)

ids = vtkIdList()
for i in range(4):
    ids.InsertNextId(i)

grid = vtkUnstructuredGrid()
grid.Allocate(10, 10)
grid.InsertNextCell(10, ids)
grid.SetPoints(points)
grid.GetPointData().SetScalars(scalars)

# Clip the tetra
clipper = vtkClipDataSet()
clipper.SetInputData(grid)
clipper.SetValue(0.5)
clipper.Update()

# Tube edges for clipped output
tet_edges = vtkExtractEdges()
tet_edges.SetInputConnection(clipper.GetOutputPort())

tet_edge_tubes = vtkTubeFilter()
tet_edge_tubes.SetInputConnection(tet_edges.GetOutputPort())
tet_edge_tubes.SetRadius(0.005)
tet_edge_tubes.SetNumberOfSides(6)

tet_edge_mapper = vtkPolyDataMapper()
tet_edge_mapper.SetInputConnection(tet_edge_tubes.GetOutputPort())
tet_edge_mapper.ScalarVisibilityOff()

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

tets_actor = vtkActor()
tets_actor.SetMapper(shrink_mapper)
colors.GetColorRGB("banana", rgb)
tets_actor.GetProperty().SetDiffuseColor(rgb)

# Tet wireframe model
model_edges = vtkExtractEdges()
model_edges.SetInputData(grid)

model_tubes = vtkTubeFilter()
model_tubes.SetInputConnection(model_edges.GetOutputPort())
model_tubes.SetRadius(0.01)
model_tubes.SetNumberOfSides(6)

model_tube_mapper = vtkPolyDataMapper()
model_tube_mapper.SetInputConnection(model_tubes.GetOutputPort())
model_tube_mapper.ScalarVisibilityOff()

cube_edges_actor = vtkActor()
cube_edges_actor.SetMapper(model_tube_mapper)
colors.GetColorRGB("khaki", rgb)
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

vertex_glyphs = vtkGlyph3D()
vertex_glyphs.SetInputConnection(threshold_in.GetOutputPort())
vertex_glyphs.SetSourceConnection(sphere.GetOutputPort())

sphere_mapper = vtkPolyDataMapper()
sphere_mapper.SetInputConnection(vertex_glyphs.GetOutputPort())
sphere_mapper.ScalarVisibilityOff()

cube_vertices_actor = vtkActor()
cube_vertices_actor.SetMapper(sphere_mapper)
colors.GetColorRGB("tomato", rgb)
cube_vertices_actor.GetProperty().SetDiffuseColor(rgb)

# Label
case_label = vtkVectorText()
case_label.SetText("Case 1")

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

# Update scalars for case 3
mask = [1, 2, 4, 8, 16, 32]
for i in range(4):
    m = mask[i]
    if m & 3 == 0:
        scalars.SetValue(i, 0)
    else:
        scalars.SetValue(i, 1)
case_label.SetText("Case 3")
grid.Modified()

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(400, 400)
render_window.SetWindowName("clip tet")

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
