#!/usr/bin/env python

# Demonstrate vtkPlaneCutter to slice a sphere with a plane, producing a
# colored cross-section.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkCommonDataModel import vtkPlane
from vtkmodules.vtkFiltersCore import vtkPlaneCutter
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
tomato_rgb = (0.980, 0.502, 0.447)
misty_rose_rgb = (1.000, 0.894, 0.882)
slate_gray_rgb = (0.439, 0.502, 0.565)

# Source: high-resolution sphere
sphere = vtkSphereSource()
sphere.SetPhiResolution(64)
sphere.SetThetaResolution(64)

# Plane: cuts through the center
plane = vtkPlane()
plane.SetOrigin(0, 0, 0)
plane.SetNormal(0.3, 0.6, 1)

# Filter: cut the sphere with the plane
cutter = vtkPlaneCutter()
cutter.SetInputConnection(sphere.GetOutputPort())
cutter.SetPlane(plane)

# Mapper: map the cut cross-section to graphics primitives
cut_mapper = vtkPolyDataMapper()
cut_mapper.SetInputConnection(cutter.GetOutputPort())

# Actor: assign the cut geometry
cut_actor = vtkActor()
cut_actor.SetMapper(cut_mapper)
cut_actor.GetProperty().SetColor(tomato_rgb)
cut_actor.GetProperty().SetLineWidth(3)

# Mapper: map the sphere to graphics primitives
sphere_mapper = vtkPolyDataMapper()
sphere_mapper.SetInputConnection(sphere.GetOutputPort())

# Actor: translucent wireframe context
sphere_actor = vtkActor()
sphere_actor.SetMapper(sphere_mapper)
sphere_actor.GetProperty().SetColor(misty_rose_rgb)
sphere_actor.GetProperty().SetOpacity(0.3)

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.AddActor(sphere_actor)
renderer.AddActor(cut_actor)
renderer.SetBackground(slate_gray_rgb)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(640, 480)
render_window.SetWindowName("PlaneCutter")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
