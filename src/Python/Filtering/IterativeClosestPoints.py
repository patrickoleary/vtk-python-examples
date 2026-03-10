#!/usr/bin/env python

# Align a source point set to a target point set using
# vtkIterativeClosestPointTransform and visualize source,
# target, and the transformed result as colored sphere glyphs.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkCommonCore import vtkPoints
from vtkmodules.vtkCommonDataModel import (
    vtkCellArray,
    vtkIterativeClosestPointTransform,
    vtkPolyData,
)
from vtkmodules.vtkFiltersGeneral import vtkTransformPolyDataFilter
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkGlyph3DMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
red_rgb = (1.0, 0.0, 0.0)
green_rgb = (0.0, 1.0, 0.0)
blue_rgb = (0.0, 0.0, 1.0)
background_rgb = (0.1, 0.1, 0.1)

# Source points: slightly offset from the target
source_points = vtkPoints()
source_verts = vtkCellArray()
for pt in [(1.0, 0.1, 0.0), (0.1, 1.1, 0.0), (0.0, 0.1, 1.0)]:
    pid = source_points.InsertNextPoint(pt)
    source_verts.InsertNextCell(1)
    source_verts.InsertCellPoint(pid)

source = vtkPolyData()
source.SetPoints(source_points)
source.SetVerts(source_verts)

# Target points: the ideal positions
target_points = vtkPoints()
target_verts = vtkCellArray()
for pt in [(1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, 0.0, 1.0)]:
    pid = target_points.InsertNextPoint(pt)
    target_verts.InsertNextCell(1)
    target_verts.InsertCellPoint(pid)

target = vtkPolyData()
target.SetPoints(target_points)
target.SetVerts(target_verts)

# ICP: align source to target using rigid body transform
icp = vtkIterativeClosestPointTransform()
icp.SetSource(source)
icp.SetTarget(target)
icp.GetLandmarkTransform().SetModeToRigidBody()
icp.SetMaximumNumberOfIterations(20)
icp.StartByMatchingCentroidsOn()
icp.Modified()
icp.Update()

# Transform: apply the ICP result to the source points
transform_filter = vtkTransformPolyDataFilter()
transform_filter.SetInputData(source)
transform_filter.SetTransform(icp)
transform_filter.Update()

# Glyph source: small sphere for point visualization
glyph_sphere = vtkSphereSource()
glyph_sphere.SetRadius(0.05)

# Actor: source points (red)
source_mapper = vtkGlyph3DMapper()
source_mapper.SetInputData(source)
source_mapper.SetSourceConnection(glyph_sphere.GetOutputPort())
source_mapper.ScalarVisibilityOff()
source_actor = vtkActor()
source_actor.SetMapper(source_mapper)
source_actor.GetProperty().SetColor(red_rgb)

# Actor: target points (green)
target_mapper = vtkGlyph3DMapper()
target_mapper.SetInputData(target)
target_mapper.SetSourceConnection(glyph_sphere.GetOutputPort())
target_mapper.ScalarVisibilityOff()
target_actor = vtkActor()
target_actor.SetMapper(target_mapper)
target_actor.GetProperty().SetColor(green_rgb)

# Actor: transformed source points (blue)
transformed_mapper = vtkGlyph3DMapper()
transformed_mapper.SetInputConnection(transform_filter.GetOutputPort())
transformed_mapper.SetSourceConnection(glyph_sphere.GetOutputPort())
transformed_mapper.ScalarVisibilityOff()
transformed_actor = vtkActor()
transformed_actor.SetMapper(transformed_mapper)
transformed_actor.GetProperty().SetColor(blue_rgb)

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.AddActor(source_actor)
renderer.AddActor(target_actor)
renderer.AddActor(transformed_actor)
renderer.SetBackground(background_rgb)
renderer.ResetCamera()

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(640, 480)
render_window.SetWindowName("IterativeClosestPoints")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
