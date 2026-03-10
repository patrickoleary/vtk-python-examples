#!/usr/bin/env python

# Visualize the projection of a point onto a plane.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkCommonCore import vtkPoints
from vtkmodules.vtkCommonDataModel import (
    vtkCellArray,
    vtkPlane,
    vtkPolyData,
)
from vtkmodules.vtkFiltersSources import (
    vtkArrowSource,
    vtkPlaneSource,
    vtkSphereSource,
)
from vtkmodules.vtkCommonTransforms import vtkTransform
from vtkmodules.vtkFiltersGeneral import vtkTransformPolyDataFilter
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)
from vtkmodules.vtkRenderingFreeType import vtkVectorText

# Colors (normalized RGB)
tomato_rgb = (1.0, 0.388, 0.278)
lime_green_rgb = (0.196, 0.804, 0.196)
light_blue_rgb = (0.678, 0.847, 0.902)
yellow_rgb = (1.0, 1.0, 0.0)
cyan_rgb = (0.0, 1.0, 1.0)
dark_slate_gray_rgb = (0.184, 0.310, 0.310)

# Define the point and the plane
point = (2.0, 3.0, 4.0)
plane_origin = (0.0, 0.0, 0.0)
plane_normal = (0.0, 0.0, 1.0)

# Project: compute the projected point using vtkPlane.ProjectPoint
projected = [0.0, 0.0, 0.0]
vtkPlane.ProjectPoint(point, plane_origin, plane_normal, projected)

# Source: plane geometry
plane_source = vtkPlaneSource()
plane_source.SetOrigin(-3, -3, 0)
plane_source.SetPoint1(5, -3, 0)
plane_source.SetPoint2(-3, 5, 0)

plane_mapper = vtkPolyDataMapper()
plane_mapper.SetInputConnection(plane_source.GetOutputPort())

plane_actor = vtkActor()
plane_actor.SetMapper(plane_mapper)
plane_actor.GetProperty().SetColor(light_blue_rgb)
plane_actor.GetProperty().SetOpacity(0.5)

# Source: sphere at the original point
sphere_orig = vtkSphereSource()
sphere_orig.SetCenter(point)
sphere_orig.SetRadius(0.15)
sphere_orig.SetPhiResolution(16)
sphere_orig.SetThetaResolution(16)

sphere_orig_mapper = vtkPolyDataMapper()
sphere_orig_mapper.SetInputConnection(sphere_orig.GetOutputPort())

sphere_orig_actor = vtkActor()
sphere_orig_actor.SetMapper(sphere_orig_mapper)
sphere_orig_actor.GetProperty().SetColor(tomato_rgb)

# Source: sphere at the projected point
sphere_proj = vtkSphereSource()
sphere_proj.SetCenter(projected)
sphere_proj.SetRadius(0.15)
sphere_proj.SetPhiResolution(16)
sphere_proj.SetThetaResolution(16)

sphere_proj_mapper = vtkPolyDataMapper()
sphere_proj_mapper.SetInputConnection(sphere_proj.GetOutputPort())

sphere_proj_actor = vtkActor()
sphere_proj_actor.SetMapper(sphere_proj_mapper)
sphere_proj_actor.GetProperty().SetColor(lime_green_rgb)

# Line: dashed projection line from original point to projected point
line_points = vtkPoints()
line_points.InsertNextPoint(point)
line_points.InsertNextPoint(projected)

line_cells = vtkCellArray()
line_cells.InsertNextCell(2)
line_cells.InsertCellPoint(0)
line_cells.InsertCellPoint(1)

line_poly = vtkPolyData()
line_poly.SetPoints(line_points)
line_poly.SetLines(line_cells)

line_mapper = vtkPolyDataMapper()
line_mapper.SetInputData(line_poly)

line_actor = vtkActor()
line_actor.SetMapper(line_mapper)
line_actor.GetProperty().SetColor(yellow_rgb)
line_actor.GetProperty().SetLineWidth(2.0)

# Arrow: plane normal arrow at the plane origin
arrow_source = vtkArrowSource()
arrow_source.SetTipLength(0.3)
arrow_source.SetTipRadius(0.1)
arrow_source.SetShaftRadius(0.03)

arrow_transform = vtkTransform()
arrow_transform.Translate(plane_origin)
arrow_transform.Scale(2.0, 2.0, 2.0)
arrow_transform.RotateY(-90.0)

arrow_filter = vtkTransformPolyDataFilter()
arrow_filter.SetTransform(arrow_transform)
arrow_filter.SetInputConnection(arrow_source.GetOutputPort())

arrow_mapper = vtkPolyDataMapper()
arrow_mapper.SetInputConnection(arrow_filter.GetOutputPort())

arrow_actor = vtkActor()
arrow_actor.SetMapper(arrow_mapper)
arrow_actor.GetProperty().SetColor(cyan_rgb)

# Label: original point
orig_label = vtkVectorText()
orig_label.SetText(f"P ({point[0]:.0f},{point[1]:.0f},{point[2]:.0f})")

orig_label_mapper = vtkPolyDataMapper()
orig_label_mapper.SetInputConnection(orig_label.GetOutputPort())

orig_label_actor = vtkActor()
orig_label_actor.SetMapper(orig_label_mapper)
orig_label_actor.SetScale(0.25, 0.25, 0.25)
orig_label_actor.SetPosition(point[0] + 0.2, point[1] + 0.2, point[2])
orig_label_actor.GetProperty().SetColor(tomato_rgb)

# Label: projected point
proj_label = vtkVectorText()
proj_label.SetText(f"P' ({projected[0]:.0f},{projected[1]:.0f},{projected[2]:.0f})")

proj_label_mapper = vtkPolyDataMapper()
proj_label_mapper.SetInputConnection(proj_label.GetOutputPort())

proj_label_actor = vtkActor()
proj_label_actor.SetMapper(proj_label_mapper)
proj_label_actor.SetScale(0.25, 0.25, 0.25)
proj_label_actor.SetPosition(projected[0] + 0.2, projected[1] + 0.2, projected[2])
proj_label_actor.GetProperty().SetColor(lime_green_rgb)

# Label: normal
normal_label = vtkVectorText()
normal_label.SetText("n")

normal_label_mapper = vtkPolyDataMapper()
normal_label_mapper.SetInputConnection(normal_label.GetOutputPort())

normal_label_actor = vtkActor()
normal_label_actor.SetMapper(normal_label_mapper)
normal_label_actor.SetScale(0.25, 0.25, 0.25)
normal_label_actor.SetPosition(0.2, 0.0, 2.1)
normal_label_actor.GetProperty().SetColor(cyan_rgb)

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.AddActor(plane_actor)
renderer.AddActor(sphere_orig_actor)
renderer.AddActor(sphere_proj_actor)
renderer.AddActor(line_actor)
renderer.AddActor(arrow_actor)
renderer.AddActor(orig_label_actor)
renderer.AddActor(proj_label_actor)
renderer.AddActor(normal_label_actor)
renderer.SetBackground(dark_slate_gray_rgb)
renderer.ResetCamera()
renderer.GetActiveCamera().Elevation(20)
renderer.GetActiveCamera().Azimuth(-30)
renderer.GetActiveCamera().Dolly(1.1)
renderer.ResetCameraClippingRange()

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(640, 480)
render_window.SetWindowName("ProjectPointToPlane")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
