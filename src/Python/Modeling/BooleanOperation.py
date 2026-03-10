#!/usr/bin/env python

# Demonstrate boolean operations (union, intersection, difference) on
# two overlapping spheres using vtkBooleanOperationPolyDataFilter.
# Three viewports show one operation each.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkFiltersGeneral import vtkBooleanOperationPolyDataFilter
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
slate_gray_background_rgb = (0.439, 0.502, 0.565)
cornflower_blue_background_rgb = (0.392, 0.584, 0.929)
light_coral_background_rgb = (0.941, 0.502, 0.502)
banana_rgb = (0.890, 0.812, 0.341)

# Source: two overlapping spheres
sphere1 = vtkSphereSource()
sphere1.SetCenter(-0.3, 0.0, 0.0)
sphere1.SetRadius(1.0)
sphere1.SetThetaResolution(40)
sphere1.SetPhiResolution(40)

sphere2 = vtkSphereSource()
sphere2.SetCenter(0.3, 0.0, 0.0)
sphere2.SetRadius(1.0)
sphere2.SetThetaResolution(40)
sphere2.SetPhiResolution(40)

# Filter: boolean union
boolean_union = vtkBooleanOperationPolyDataFilter()
boolean_union.SetOperation(vtkBooleanOperationPolyDataFilter.VTK_UNION)
boolean_union.SetInputConnection(0, sphere1.GetOutputPort())
boolean_union.SetInputConnection(1, sphere2.GetOutputPort())

union_mapper = vtkPolyDataMapper()
union_mapper.SetInputConnection(boolean_union.GetOutputPort())
union_mapper.ScalarVisibilityOff()

union_actor = vtkActor()
union_actor.SetMapper(union_mapper)
union_actor.GetProperty().SetColor(banana_rgb)

# Filter: boolean intersection
boolean_intersection = vtkBooleanOperationPolyDataFilter()
boolean_intersection.SetOperation(vtkBooleanOperationPolyDataFilter.VTK_INTERSECTION)
boolean_intersection.SetInputConnection(0, sphere1.GetOutputPort())
boolean_intersection.SetInputConnection(1, sphere2.GetOutputPort())

intersection_mapper = vtkPolyDataMapper()
intersection_mapper.SetInputConnection(boolean_intersection.GetOutputPort())
intersection_mapper.ScalarVisibilityOff()

intersection_actor = vtkActor()
intersection_actor.SetMapper(intersection_mapper)
intersection_actor.GetProperty().SetColor(banana_rgb)

# Filter: boolean difference
boolean_difference = vtkBooleanOperationPolyDataFilter()
boolean_difference.SetOperation(vtkBooleanOperationPolyDataFilter.VTK_DIFFERENCE)
boolean_difference.SetInputConnection(0, sphere1.GetOutputPort())
boolean_difference.SetInputConnection(1, sphere2.GetOutputPort())

difference_mapper = vtkPolyDataMapper()
difference_mapper.SetInputConnection(boolean_difference.GetOutputPort())
difference_mapper.ScalarVisibilityOff()

difference_actor = vtkActor()
difference_actor.SetMapper(difference_mapper)
difference_actor.GetProperty().SetColor(banana_rgb)

# Renderer: left viewport — union
left_renderer = vtkRenderer()
left_renderer.AddActor(union_actor)
left_renderer.SetBackground(slate_gray_background_rgb)
left_renderer.SetViewport(0.0, 0.0, 1.0 / 3.0, 1.0)

# Renderer: center viewport — intersection
center_renderer = vtkRenderer()
center_renderer.AddActor(intersection_actor)
center_renderer.SetBackground(cornflower_blue_background_rgb)
center_renderer.SetViewport(1.0 / 3.0, 0.0, 2.0 / 3.0, 1.0)

# Renderer: right viewport — difference
right_renderer = vtkRenderer()
right_renderer.AddActor(difference_actor)
right_renderer.SetBackground(light_coral_background_rgb)
right_renderer.SetViewport(2.0 / 3.0, 0.0, 1.0, 1.0)

# Share camera across all viewports
left_renderer.ResetCamera()
left_renderer.GetActiveCamera().Azimuth(30)
left_renderer.GetActiveCamera().Elevation(30)
left_renderer.ResetCamera()
center_renderer.SetActiveCamera(left_renderer.GetActiveCamera())
right_renderer.SetActiveCamera(left_renderer.GetActiveCamera())

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(left_renderer)
render_window.AddRenderer(center_renderer)
render_window.AddRenderer(right_renderer)
render_window.SetSize(960, 320)
render_window.SetWindowName("BooleanOperation")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
