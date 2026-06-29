#!/usr/bin/env python

# Demonstrate vtkModifiedBSPTree ray-polygon intersection on a cloud
# of small spheres, highlighting intersected cells and intersection points.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import (
    vtkIdList,
    vtkMath,
    vtkPoints,
)
from vtkmodules.vtkCommonDataModel import (
    vtkCellArray,
    vtkPolyData,
    vtkSelectionNode,
)
from vtkmodules.vtkFiltersCore import vtkGlyph3D
from vtkmodules.vtkFiltersExtraction import vtkExtractSelection
from vtkmodules.vtkFiltersSources import (
    vtkLineSource,
    vtkPointSource,
    vtkSelectionSource,
    vtkSphereSource,
)
from vtkmodules.vtkFiltersFlowPaths import vtkModifiedBSPTree
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkDataSetMapper,
    vtkPolyDataMapper,
    vtkProperty,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Random seed for reproducibility
vtkMath.RandomSeed(931)

# Random point cloud
points = vtkPointSource()
points.SetRadius(0.05)
points.SetNumberOfPoints(30)

# Small sphere for glyphing
sphere = vtkSphereSource()
sphere.SetRadius(0.0125)
sphere.SetCenter(0.0, 0.0, 0.0)
sphere.SetThetaResolution(16)
sphere.SetPhiResolution(16)

# Glyph spheres over point cloud
glyph = vtkGlyph3D()
glyph.SetInputConnection(0, points.GetOutputPort())
glyph.SetSourceConnection(sphere.GetOutputPort())
glyph.SetScaling(0)
glyph.Update()

bounds = glyph.GetOutput().GetBounds()
diag = ((bounds[1] - bounds[0]) ** 2 + (bounds[3] - bounds[2]) ** 2 + (bounds[5] - bounds[4]) ** 2) ** 0.5
tol = diag / 1e6

# Build BSP tree
bsp_tree = vtkModifiedBSPTree()
bsp_tree.SetDataSet(glyph.GetOutput())
bsp_tree.SetMaxLevel(12)
bsp_tree.SetNumberOfCellsPerNode(16)
bsp_tree.BuildLocator()

# Intersect ray with BSP tree
verts = vtkPoints()
cell_ids = vtkIdList()
p1 = [-0.1, -0.1, -0.1]
p2 = [0.1, 0.1, 0.1]
bsp_tree.IntersectWithLine(p1, p2, tol, verts, cell_ids)

# Create polydata for intersection points
intersections = vtkPolyData()
vertices = vtkCellArray()
n = verts.GetNumberOfPoints()
for i in range(n):
    vertices.InsertNextCell(1, [i])
intersections.SetPoints(verts)
intersections.SetVerts(vertices)

# Extract intersected cells
selection = vtkSelectionSource()
selection.SetContentType(vtkSelectionNode.INDICES)
selection.SetFieldType(vtkSelectionNode.CELL)
for i in range(cell_ids.GetNumberOfIds()):
    selection.AddID(-1, cell_ids.GetId(i))

extract = vtkExtractSelection()
extract.SetInputConnection(glyph.GetOutputPort())
extract.SetSelectionConnection(selection.GetOutputPort())
extract.Update()

# Render cloud of target spheres
sphere_cloud_mapper = vtkPolyDataMapper()
sphere_cloud_mapper.SetInputConnection(glyph.GetOutputPort())

sphere_cloud_property = vtkProperty()
sphere_cloud_property.SetColor(1.0, 1.0, 1.0)
sphere_cloud_property.SetAmbient(0.0)
sphere_cloud_property.SetBackfaceCulling(1)
sphere_cloud_property.SetFrontfaceCulling(0)
sphere_cloud_property.SetRepresentationToPoints()
sphere_cloud_property.SetInterpolationToFlat()

sphere_cloud_actor = vtkActor()
sphere_cloud_actor.SetMapper(sphere_cloud_mapper)
sphere_cloud_actor.SetProperty(sphere_cloud_property)

# Render intersection points as small glyphs
intersection_glyph = vtkGlyph3D()
intersection_glyph.SetInputData(intersections)
intersection_glyph.SetSourceConnection(sphere.GetOutputPort())
intersection_glyph.SetScaling(1)
intersection_glyph.SetScaleFactor(0.05)
intersection_glyph.Update()

intersection_mapper = vtkPolyDataMapper()
intersection_mapper.SetInputConnection(intersection_glyph.GetOutputPort())

intersection_property = vtkProperty()
intersection_property.SetOpacity(1.0)
intersection_property.SetColor(0.0, 0.0, 1.0)
intersection_property.SetBackfaceCulling(1)
intersection_property.SetFrontfaceCulling(0)

intersection_actor = vtkActor()
intersection_actor.SetMapper(intersection_mapper)
intersection_actor.SetProperty(intersection_property)

# Render ray
ray = vtkLineSource()
ray.SetPoint1(p1)
ray.SetPoint2(p2)

ray_mapper = vtkPolyDataMapper()
ray_mapper.SetInputConnection(ray.GetOutputPort())

ray_actor = vtkActor()
ray_actor.SetMapper(ray_mapper)

# Render intersected cells (extracted using selection)
cell_mapper = vtkDataSetMapper()
cell_mapper.SetInputConnection(extract.GetOutputPort())

cell_property = vtkProperty()
cell_property.SetColor(0.0, 1.0, 1.0)
cell_property.SetBackfaceCulling(0)
cell_property.SetFrontfaceCulling(0)
cell_property.SetAmbient(1.0)
cell_property.SetLineWidth(3.0)
cell_property.SetRepresentationToWireframe()
cell_property.SetInterpolationToFlat()

cell_actor = vtkActor()
cell_actor.SetMapper(cell_mapper)
cell_actor.SetProperty(cell_property)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(sphere_cloud_actor)
renderer.AddActor(intersection_actor)
renderer.AddActor(ray_actor)
renderer.AddActor(cell_actor)
renderer.SetBackground(0.0, 0.0, 0.0)

# Window
render_window = vtkRenderWindow()
render_window.SetSize(300, 300)
render_window.SetMultiSamples(0)
render_window.AddRenderer(renderer)
render_window.SetWindowName("bsp tree")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.GetActiveCamera().SetPosition(0.0, 0.15, 0.0)
renderer.GetActiveCamera().SetFocalPoint(0.0, 0.0, 0.0)
renderer.GetActiveCamera().SetViewUp(0.0, 0.0, 1.0)
renderer.ResetCameraClippingRange()

interactor.Initialize()
interactor.Start()
