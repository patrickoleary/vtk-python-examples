#!/usr/bin/env python

# Demonstrate vtkModifiedBSPTree ray intersection on a sphere with
# ghost cell arrays, visualizing the BSP tree representation,
# intersection points, and extracted cells.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import (
    vtkIdList,
    vtkPoints,
)
from vtkmodules.vtkCommonDataModel import (
    vtkCellArray,
    vtkDataSetAttributes,
    vtkPolyData,
    vtkSelectionNode,
)
from vtkmodules.vtkFiltersExtraction import vtkExtractSelection
from vtkmodules.vtkFiltersFlowPaths import vtkModifiedBSPTree
from vtkmodules.vtkFiltersSources import (
    vtkLineSource,
    vtkSelectionSource,
    vtkSphereSource,
)
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkDataSetMapper,
    vtkGlyph3DMapper,
    vtkPolyDataMapper,
    vtkProperty,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Create a sphere with ghost cells
sphere_source = vtkSphereSource()
sphere_source.SetRadius(0.05)
sphere_source.Update()
sphere = sphere_source.GetOutput()
sphere.AllocateCellGhostArray()
ghost_cells = sphere.GetCellGhostArray()
ghost_cells.SetTuple1(72, vtkDataSetAttributes.HIDDENCELL)
ghost_cells.SetTuple1(19, vtkDataSetAttributes.HIDDENCELL)

bounds = sphere.GetBounds()
diag = ((bounds[1] - bounds[0]) ** 2 + (bounds[3] - bounds[2]) ** 2 + (bounds[5] - bounds[4]) ** 2) ** 0.5
tol = diag / 1e6

# Build BSP tree
bsp_tree = vtkModifiedBSPTree()
bsp_tree.SetDataSet(sphere)
bsp_tree.SetMaxLevel(12)
bsp_tree.SetNumberOfCellsPerNode(16)
bsp_tree.BuildLocator()

# Render BSP tree representation
bsp_pd = vtkPolyData()
bsp_tree.GenerateRepresentation(2, bsp_pd)

bsp_mapper = vtkPolyDataMapper()
bsp_mapper.SetInputData(bsp_pd)

bsp_actor = vtkActor()
bsp_actor.SetMapper(bsp_mapper)
bsp_actor.GetProperty().SetInterpolationToFlat()
bsp_actor.GetProperty().SetOpacity(0.3)
bsp_actor.GetProperty().EdgeVisibilityOn()
bsp_actor.GetProperty().SetColor(0.45, 0.25, 0.6)

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
extract.SetInputData(sphere)
extract.SetSelectionConnection(selection.GetOutputPort())
extract.Update()

# Render sphere as point cloud
sphere_mapper = vtkPolyDataMapper()
sphere_mapper.SetInputData(sphere)

sphere_property = vtkProperty()
sphere_property.SetColor(1.0, 1.0, 1.0)
sphere_property.SetAmbient(0.0)
sphere_property.SetBackfaceCulling(1)
sphere_property.SetFrontfaceCulling(0)
sphere_property.SetRepresentationToPoints()

sphere_actor = vtkActor()
sphere_actor.SetMapper(sphere_mapper)
sphere_actor.SetProperty(sphere_property)

# Render intersection points as glyphs
intersection_mapper = vtkGlyph3DMapper()
intersection_mapper.SetInputData(intersections)
intersection_mapper.SetSourceConnection(sphere_source.GetOutputPort())
intersection_mapper.SetScaleFactor(0.05)

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

# Render intersected cells
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
renderer.AddActor(bsp_actor)
renderer.AddActor(sphere_actor)
renderer.AddActor(intersection_actor)
renderer.AddActor(ray_actor)
renderer.AddActor(cell_actor)
renderer.SetBackground(0.0, 0.0, 0.0)

# Window
render_window = vtkRenderWindow()
render_window.SetSize(300, 300)
render_window.SetMultiSamples(0)
render_window.AddRenderer(renderer)
render_window.SetWindowName("bsp tree with ghost arrays")

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
