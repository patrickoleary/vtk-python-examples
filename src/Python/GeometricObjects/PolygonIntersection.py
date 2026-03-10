#!/usr/bin/env python

# Visualize a line-polygon intersection test.  A unit square lies in the
# x-y plane and a line segment crosses it along z.  The intersection point
# is marked with a sphere glyph colored green (hit) or red (miss).

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkCommonCore import (
    mutable,
    vtkPoints,
)
from vtkmodules.vtkCommonDataModel import (
    vtkCellArray,
    vtkLine,
    vtkPolyData,
    vtkPolygon,
)
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
green_rgb = (0.0, 1.0, 0.0)
red_rgb = (1.0, 0.0, 0.0)
light_blue_rgb = (0.529, 0.808, 0.922)
white_rgb = (1.0, 1.0, 1.0)
dark_green_background_rgb = (0.0, 0.392, 0.0)

# ---- Data: a unit square polygon in the x-y plane ----
square_points = vtkPoints()
square_points.InsertNextPoint(0.0, 0.0, 0.0)
square_points.InsertNextPoint(1.0, 0.0, 0.0)
square_points.InsertNextPoint(1.0, 1.0, 0.0)
square_points.InsertNextPoint(0.0, 1.0, 0.0)

polygon = vtkPolygon()
polygon.GetPoints().DeepCopy(square_points)
polygon.GetPointIds().SetNumberOfIds(4)
polygon.GetPointIds().SetId(0, 0)
polygon.GetPointIds().SetId(1, 1)
polygon.GetPointIds().SetId(2, 2)
polygon.GetPointIds().SetId(3, 3)

square_cells = vtkCellArray()
square_cells.InsertNextCell(polygon)

square_poly_data = vtkPolyData()
square_poly_data.SetPoints(square_points)
square_poly_data.SetPolys(square_cells)

# ---- Intersection test ----
p1 = [0.1, 0.0, -1.0]
p2 = [0.1, 0.0, 1.0]
tolerance = 0.001

t = mutable(0)        # parametric coordinate (0 → p1, 1 → p2)
x = [0.0, 0.0, 0.0]  # intersection point
pcoords = [0.0, 0.0, 0.0]
sub_id = mutable(0)

hit = polygon.IntersectWithLine(p1, p2, tolerance, t, x, pcoords, sub_id)
print("intersected?  ", "Yes" if hit == 1 else "No")
print("intersection: ", x)

# ---- Line segment from p1 to p2 ----
line_points = vtkPoints()
line_points.InsertNextPoint(p1)
line_points.InsertNextPoint(p2)

line_cell = vtkLine()
line_cell.GetPointIds().SetId(0, 0)
line_cell.GetPointIds().SetId(1, 1)

line_cells = vtkCellArray()
line_cells.InsertNextCell(line_cell)

line_poly_data = vtkPolyData()
line_poly_data.SetPoints(line_points)
line_poly_data.SetLines(line_cells)

# ---- Sphere glyph at the intersection point ----
sphere_source = vtkSphereSource()
sphere_source.SetCenter(x)
sphere_source.SetRadius(0.04)
sphere_source.SetPhiResolution(16)
sphere_source.SetThetaResolution(16)

# Mapper / Actor: polygon (light blue, semi-transparent)
square_mapper = vtkPolyDataMapper()
square_mapper.SetInputData(square_poly_data)

square_actor = vtkActor()
square_actor.SetMapper(square_mapper)
square_actor.GetProperty().SetColor(light_blue_rgb)
square_actor.GetProperty().SetOpacity(0.5)

# Mapper / Actor: line segment (white)
line_mapper = vtkPolyDataMapper()
line_mapper.SetInputData(line_poly_data)

line_actor = vtkActor()
line_actor.SetMapper(line_mapper)
line_actor.GetProperty().SetColor(white_rgb)
line_actor.GetProperty().SetLineWidth(3)

# Mapper / Actor: intersection glyph (green if hit, red if miss)
sphere_mapper = vtkPolyDataMapper()
sphere_mapper.SetInputConnection(sphere_source.GetOutputPort())

sphere_actor = vtkActor()
sphere_actor.SetMapper(sphere_mapper)
sphere_actor.GetProperty().SetColor(green_rgb if hit == 1 else red_rgb)

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.AddActor(square_actor)
renderer.AddActor(line_actor)
renderer.AddActor(sphere_actor)
renderer.SetBackground(dark_green_background_rgb)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("PolygonIntersection")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
