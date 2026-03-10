#!/usr/bin/env python

# Adaptively subdivide a coarse sphere mesh so that no triangle edge
# exceeds a specified maximum length, using vtkAdaptiveSubdivisionFilter.
# The original coarse mesh is shown on the left and the subdivided mesh
# on the right, both rendered as wireframes.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkFiltersCore import vtkTriangleFilter
from vtkmodules.vtkFiltersModeling import vtkAdaptiveSubdivisionFilter
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
tomato_rgb = (1.0, 0.388, 0.278)
steel_blue_rgb = (0.275, 0.510, 0.706)
slate_gray_background_rgb = (0.439, 0.502, 0.565)

# Source: create a coarse sphere with few subdivisions
sphere = vtkSphereSource()
sphere.SetRadius(1.0)
sphere.SetPhiResolution(6)
sphere.SetThetaResolution(6)

# Triangulate: ensure all cells are triangles (required by the filter)
triangulate = vtkTriangleFilter()
triangulate.SetInputConnection(sphere.GetOutputPort())

# Filter: adaptively subdivide so no edge exceeds 0.2 length units
adaptive = vtkAdaptiveSubdivisionFilter()
adaptive.SetInputConnection(triangulate.GetOutputPort())
adaptive.SetMaximumEdgeLength(0.2)
adaptive.Update()

# ---- Left viewport: original coarse mesh ----
original_mapper = vtkPolyDataMapper()
original_mapper.SetInputConnection(triangulate.GetOutputPort())

original_actor = vtkActor()
original_actor.SetMapper(original_mapper)
original_actor.GetProperty().SetRepresentationToWireframe()
original_actor.GetProperty().SetColor(tomato_rgb)
original_actor.GetProperty().SetLineWidth(2)

left_renderer = vtkRenderer()
left_renderer.SetViewport(0.0, 0.0, 0.5, 1.0)
left_renderer.AddActor(original_actor)
left_renderer.SetBackground(slate_gray_background_rgb)
left_renderer.ResetCamera()

# ---- Right viewport: adaptively subdivided mesh ----
subdivided_mapper = vtkPolyDataMapper()
subdivided_mapper.SetInputConnection(adaptive.GetOutputPort())

subdivided_actor = vtkActor()
subdivided_actor.SetMapper(subdivided_mapper)
subdivided_actor.GetProperty().SetRepresentationToWireframe()
subdivided_actor.GetProperty().SetColor(steel_blue_rgb)
subdivided_actor.GetProperty().SetLineWidth(1)

right_renderer = vtkRenderer()
right_renderer.SetViewport(0.5, 0.0, 1.0, 1.0)
right_renderer.AddActor(subdivided_actor)
right_renderer.SetBackground(slate_gray_background_rgb)
right_renderer.SetActiveCamera(left_renderer.GetActiveCamera())

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(left_renderer)
render_window.AddRenderer(right_renderer)
render_window.SetSize(800, 400)
render_window.SetWindowName("AdaptiveSubdivision")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
