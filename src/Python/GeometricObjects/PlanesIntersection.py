#!/usr/bin/env python

# Visualize a planes-intersection test with two boxes.  A sphere is rendered
# with an overlapping box (green, intersects) and a displaced box (red, does
# not intersect).  Each box is tested with vtkPlanesIntersection.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkCommonCore import vtkPoints
from vtkmodules.vtkCommonDataModel import vtkPlanesIntersection
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

# Colors (normalized RGB)
green_rgb = (0.0, 1.0, 0.0)
red_rgb = (1.0, 0.0, 0.0)
cornsilk_rgb = (1.0, 0.973, 0.863)
slate_gray_background_rgb = (0.439, 0.502, 0.565)


def make_box_points(bounds):
    """Return a vtkPoints with the eight corners of the given bounds."""
    x_min, x_max, y_min, y_max, z_min, z_max = bounds
    pts = vtkPoints()
    pts.SetNumberOfPoints(8)
    pts.SetPoint(0, x_max, y_min, z_max)
    pts.SetPoint(1, x_max, y_min, z_min)
    pts.SetPoint(2, x_max, y_max, z_min)
    pts.SetPoint(3, x_max, y_max, z_max)
    pts.SetPoint(4, x_min, y_min, z_max)
    pts.SetPoint(5, x_min, y_min, z_min)
    pts.SetPoint(6, x_min, y_max, z_min)
    pts.SetPoint(7, x_min, y_max, z_max)
    return pts


# Source: generate a unit sphere and extract its bounding box
sphere_source = vtkSphereSource()
sphere_source.SetPhiResolution(32)
sphere_source.SetThetaResolution(32)
sphere_source.Update()

sphere_bounds = [0.0] * 6
sphere_source.GetOutput().GetBounds(sphere_bounds)

# Build planes from the sphere's bounding box
planes_intersection = vtkPlanesIntersection()
planes_intersection.SetBounds(sphere_bounds)

# ---- Box A: overlapping (same bounds as the sphere) ----
box_a_bounds = list(sphere_bounds)
box_a_points = make_box_points(box_a_bounds)
hit_a = planes_intersection.IntersectsRegion(box_a_points)
print("Box A (overlapping) intersects? ", "Yes" if hit_a == 1 else "No")

# ---- Box B: displaced well outside the sphere ----
offset = 3.0
box_b_bounds = [b + offset for b in sphere_bounds]
box_b_points = make_box_points(box_b_bounds)
hit_b = planes_intersection.IntersectsRegion(box_b_points)
print("Box B (displaced)   intersects? ", "Yes" if hit_b == 1 else "No")

# Mapper / Actor: sphere (cornsilk, semi-transparent)
sphere_mapper = vtkPolyDataMapper()
sphere_mapper.SetInputConnection(sphere_source.GetOutputPort())

sphere_actor = vtkActor()
sphere_actor.SetMapper(sphere_mapper)
sphere_actor.GetProperty().SetColor(cornsilk_rgb)
sphere_actor.GetProperty().SetOpacity(0.5)

# Source / Mapper / Actor: Box A wireframe (green — intersects)
cube_a_source = vtkCubeSource()
cube_a_source.SetBounds(box_a_bounds)

cube_a_mapper = vtkPolyDataMapper()
cube_a_mapper.SetInputConnection(cube_a_source.GetOutputPort())

cube_a_actor = vtkActor()
cube_a_actor.SetMapper(cube_a_mapper)
cube_a_actor.GetProperty().SetRepresentationToWireframe()
cube_a_actor.GetProperty().SetLineWidth(3)
cube_a_actor.GetProperty().SetColor(green_rgb if hit_a == 1 else red_rgb)

# Source / Mapper / Actor: Box B wireframe (red — does not intersect)
cube_b_source = vtkCubeSource()
cube_b_source.SetBounds(box_b_bounds)

cube_b_mapper = vtkPolyDataMapper()
cube_b_mapper.SetInputConnection(cube_b_source.GetOutputPort())

cube_b_actor = vtkActor()
cube_b_actor.SetMapper(cube_b_mapper)
cube_b_actor.GetProperty().SetRepresentationToWireframe()
cube_b_actor.GetProperty().SetLineWidth(3)
cube_b_actor.GetProperty().SetColor(green_rgb if hit_b == 1 else red_rgb)

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.AddActor(sphere_actor)
renderer.AddActor(cube_a_actor)
renderer.AddActor(cube_b_actor)
renderer.SetBackground(slate_gray_background_rgb)
renderer.ResetCamera()
renderer.GetActiveCamera().Azimuth(30)
renderer.GetActiveCamera().Elevation(20)
renderer.ResetCameraClippingRange()

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(640, 480)
render_window.SetWindowName("PlanesIntersection")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
