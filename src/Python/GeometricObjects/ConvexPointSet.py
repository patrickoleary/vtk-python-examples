#!/usr/bin/env python

# Demonstrate a convex point set cell with glyphed vertices.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkCommonCore import vtkPoints
from vtkmodules.vtkCommonDataModel import (
    vtkConvexPointSet,
    vtkPolyData,
    vtkUnstructuredGrid,
)
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkDataSetMapper,
    vtkGlyph3DMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
tomato_rgb = (1.0, 0.388, 0.278)
peacock_rgb = (0.2, 0.631, 0.788)
silver_background_rgb = (0.75, 0.75, 0.75)

# Data: define 13 points — 8 cube corners + 5 face-center points
points = vtkPoints()
points.InsertNextPoint(0, 0, 0)
points.InsertNextPoint(1, 0, 0)
points.InsertNextPoint(1, 1, 0)
points.InsertNextPoint(0, 1, 0)
points.InsertNextPoint(0, 0, 1)
points.InsertNextPoint(1, 0, 1)
points.InsertNextPoint(1, 1, 1)
points.InsertNextPoint(0, 1, 1)
points.InsertNextPoint(0.5, 0, 0)
points.InsertNextPoint(1, 0.5, 0)
points.InsertNextPoint(0.5, 1, 0)
points.InsertNextPoint(0, 0.5, 0)
points.InsertNextPoint(0.5, 0.5, 0)

# Cell: create a convex point set referencing all 13 points
convex_point_set = vtkConvexPointSet()
convex_point_set.GetPointIds().InsertId(0, 0)
convex_point_set.GetPointIds().InsertId(1, 1)
convex_point_set.GetPointIds().InsertId(2, 2)
convex_point_set.GetPointIds().InsertId(3, 3)
convex_point_set.GetPointIds().InsertId(4, 4)
convex_point_set.GetPointIds().InsertId(5, 5)
convex_point_set.GetPointIds().InsertId(6, 6)
convex_point_set.GetPointIds().InsertId(7, 7)
convex_point_set.GetPointIds().InsertId(8, 8)
convex_point_set.GetPointIds().InsertId(9, 9)
convex_point_set.GetPointIds().InsertId(10, 10)
convex_point_set.GetPointIds().InsertId(11, 11)
convex_point_set.GetPointIds().InsertId(12, 12)

# Unstructured grid: store the convex point set cell
unstructured_grid = vtkUnstructuredGrid()
unstructured_grid.Allocate(1, 1)
unstructured_grid.InsertNextCell(
    convex_point_set.GetCellType(), convex_point_set.GetPointIds()
)
unstructured_grid.SetPoints(points)

# Mapper: map the convex hull to graphics primitives
hull_mapper = vtkDataSetMapper()
hull_mapper.SetInputData(unstructured_grid)

# Actor: display the convex hull with edges
hull_actor = vtkActor()
hull_actor.SetMapper(hull_mapper)
hull_actor.GetProperty().SetColor(tomato_rgb)
hull_actor.GetProperty().SetLineWidth(3)
hull_actor.GetProperty().EdgeVisibilityOn()

# Glyph: place small spheres at each point
sphere_source = vtkSphereSource()
sphere_source.SetPhiResolution(21)
sphere_source.SetThetaResolution(21)
sphere_source.SetRadius(0.03)

point_poly_data = vtkPolyData()
point_poly_data.SetPoints(points)

point_mapper = vtkGlyph3DMapper()
point_mapper.SetInputData(point_poly_data)
point_mapper.SetSourceConnection(sphere_source.GetOutputPort())

point_actor = vtkActor()
point_actor.SetMapper(point_mapper)
point_actor.GetProperty().SetColor(peacock_rgb)

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.AddActor(hull_actor)
renderer.AddActor(point_actor)
renderer.SetBackground(silver_background_rgb)
renderer.ResetCamera()
renderer.GetActiveCamera().Azimuth(210)
renderer.GetActiveCamera().Elevation(30)
renderer.ResetCameraClippingRange()

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(640, 480)
render_window.SetWindowName("ConvexPointSet")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
