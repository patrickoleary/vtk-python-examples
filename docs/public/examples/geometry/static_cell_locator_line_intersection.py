#!/usr/bin/env python

# Demonstrate vtkStaticCellLocator line intersection by shooting rays
# from an outer sphere toward the center of an inner sphere, glyphing
# intersection points and rendering rays.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonColor import vtkNamedColors
from vtkmodules.vtkCommonCore import (
    reference,
    vtkPoints,
)
from vtkmodules.vtkCommonDataModel import (
    vtkCellArray,
    vtkPolyData,
    vtkStaticCellLocator,
)
from vtkmodules.vtkFiltersCore import vtkGlyph3D
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

named_colors = vtkNamedColors()
peacock_rgb = [0.0, 0.0, 0.0]
named_colors.GetColorRGB("peacock", peacock_rgb)
tomato_rgb = [0.0, 0.0, 0.0]
named_colors.GetColorRGB("tomato", tomato_rgb)

# Resolution
resolution = 9

# Inner sphere (target for intersection)
sphere = vtkSphereSource()
sphere.SetThetaResolution(2 * resolution)
sphere.SetPhiResolution(resolution)
sphere.Update()

mapper = vtkPolyDataMapper()
mapper.SetInputConnection(sphere.GetOutputPort())

actor = vtkActor()
actor.SetMapper(mapper)

# Static cell locator
cell_locator = vtkStaticCellLocator()
cell_locator.SetDataSet(sphere.GetOutput())
cell_locator.SetNumberOfCellsPerNode(5)
cell_locator.BuildLocator()

locator_polydata = vtkPolyData()
cell_locator.GenerateRepresentation(4, locator_polydata)

locator_mapper = vtkPolyDataMapper()
locator_mapper.SetInputData(locator_polydata)

locator_actor = vtkActor()
locator_actor.SetMapper(locator_mapper)
locator_actor.GetProperty().SetRepresentationToWireframe()

# Outer sphere (ray origins)
sphere_2 = vtkSphereSource()
sphere_2.SetThetaResolution(resolution)
sphere_2.SetPhiResolution(int(resolution / 2))
sphere_2.SetRadius(3 * sphere.GetRadius())
sphere_2.Update()

# Generate intersection points
center = sphere.GetCenter()
intersection_polydata = vtkPolyData()
intersection_points = vtkPoints()
sphere_pts = sphere_2.GetOutput().GetPoints()
num_rays = sphere_pts.GetNumberOfPoints()
intersection_points.SetNumberOfPoints(num_rays + 1)

ray_polydata = vtkPolyData()
ray_pts = vtkPoints()
ray_pts.SetNumberOfPoints(num_rays + 1)
lines = vtkCellArray()

t = reference(0.0)
sub_id = reference(0)
cell_id = reference(0)
xyz = [0.0, 0.0, 0.0]
x_int = [0.0, 0.0, 0.0]
pc = [0.0, 0.0, 0.0]

intersection_points.SetPoint(0, center)
ray_pts.SetPoint(0, center)
for i in range(0, num_rays):
    sphere_pts.GetPoint(i, xyz)
    ray_pts.SetPoint(i + 1, xyz)
    cell_id = reference(i)
    hit = cell_locator.IntersectWithLine(xyz, center, 0.001, t, x_int, pc, sub_id, cell_id)
    if hit == 0:
        print("Missed: {}".format(i))
        intersection_points.SetPoint(i + 1, center)
    else:
        intersection_points.SetPoint(i + 1, x_int)
    lines.InsertNextCell(2)
    lines.InsertCellPoint(0)
    lines.InsertCellPoint(i + 1)

intersection_polydata.SetPoints(intersection_points)
ray_polydata.SetPoints(ray_pts)
ray_polydata.SetLines(lines)

# Glyph intersection points
glyph_sphere = vtkSphereSource()
glyph_sphere.SetPhiResolution(6)
glyph_sphere.SetThetaResolution(12)

glypher = vtkGlyph3D()
glypher.SetInputData(intersection_polydata)
glypher.SetSourceConnection(glyph_sphere.GetOutputPort())
glypher.SetScaleFactor(0.05)

glyph_mapper = vtkPolyDataMapper()
glyph_mapper.SetInputConnection(glypher.GetOutputPort())

glyph_actor = vtkActor()
glyph_actor.SetMapper(glyph_mapper)
glyph_actor.GetProperty().SetColor(peacock_rgb)

# Ray lines
lines_mapper = vtkPolyDataMapper()
lines_mapper.SetInputData(ray_polydata)

lines_actor = vtkActor()
lines_actor.SetMapper(lines_mapper)
lines_actor.GetProperty().SetColor(tomato_rgb)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.AddActor(glyph_actor)
renderer.AddActor(locator_actor)
renderer.AddActor(lines_actor)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("static cell locator line intersection")

# Scene
renderer.GetActiveCamera().SetPosition(1, 1, 1)
renderer.GetActiveCamera().SetFocalPoint(0, 0, 0)
renderer.ResetCamera()

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
