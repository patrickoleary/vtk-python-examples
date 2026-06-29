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
box_a_points = vtkPoints()
box_a_points.SetNumberOfPoints(8)
box_a_points.SetPoint(0, box_a_bounds[1], box_a_bounds[2], box_a_bounds[5])
box_a_points.SetPoint(1, box_a_bounds[1], box_a_bounds[2], box_a_bounds[4])
box_a_points.SetPoint(2, box_a_bounds[1], box_a_bounds[3], box_a_bounds[4])
box_a_points.SetPoint(3, box_a_bounds[1], box_a_bounds[3], box_a_bounds[5])
box_a_points.SetPoint(4, box_a_bounds[0], box_a_bounds[2], box_a_bounds[5])
box_a_points.SetPoint(5, box_a_bounds[0], box_a_bounds[2], box_a_bounds[4])
box_a_points.SetPoint(6, box_a_bounds[0], box_a_bounds[3], box_a_bounds[4])
box_a_points.SetPoint(7, box_a_bounds[0], box_a_bounds[3], box_a_bounds[5])
hit_a = planes_intersection.IntersectsRegion(box_a_points)
print("Box A (overlapping) intersects? ", "Yes" if hit_a == 1 else "No")

# ---- Box B: displaced well outside the sphere ----
offset = 3.0
box_b_bounds = [b + offset for b in sphere_bounds]
box_b_points = vtkPoints()
box_b_points.SetNumberOfPoints(8)
box_b_points.SetPoint(0, box_b_bounds[1], box_b_bounds[2], box_b_bounds[5])
box_b_points.SetPoint(1, box_b_bounds[1], box_b_bounds[2], box_b_bounds[4])
box_b_points.SetPoint(2, box_b_bounds[1], box_b_bounds[3], box_b_bounds[4])
box_b_points.SetPoint(3, box_b_bounds[1], box_b_bounds[3], box_b_bounds[5])
box_b_points.SetPoint(4, box_b_bounds[0], box_b_bounds[2], box_b_bounds[5])
box_b_points.SetPoint(5, box_b_bounds[0], box_b_bounds[2], box_b_bounds[4])
box_b_points.SetPoint(6, box_b_bounds[0], box_b_bounds[3], box_b_bounds[4])
box_b_points.SetPoint(7, box_b_bounds[0], box_b_bounds[3], box_b_bounds[5])
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

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("planes intersection")
render_window.SetMultiSamples(0)
render_window.SetSize(640, 480)

# Interactor
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Scene: configure the camera
renderer.ResetCamera()
renderer.GetActiveCamera().Azimuth(30)
renderer.GetActiveCamera().Elevation(20)
renderer.ResetCameraClippingRange()

render_window_interactor.Initialize()
render_window_interactor.Start()
