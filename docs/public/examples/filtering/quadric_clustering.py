#!/usr/bin/env python

# Demonstrate vtkQuadricClustering for mesh simplification.  A high-resolution
# sphere is decimated and shown side-by-side with the original.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkFiltersCore import vtkQuadricClustering
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
cornflower_blue_rgb = (0.392, 0.584, 0.929)
tomato_rgb = (0.980, 0.502, 0.447)
black_rgb = (0.0, 0.0, 0.0)
slate_gray_rgb = (0.439, 0.502, 0.565)
dark_slate_gray_rgb = (0.184, 0.310, 0.310)

# Source: high-resolution sphere
sphere_source = vtkSphereSource()
sphere_source.SetPhiResolution(100)
sphere_source.SetThetaResolution(100)

# Filter: simplify the mesh
decimator = vtkQuadricClustering()
decimator.SetInputConnection(sphere_source.GetOutputPort())
decimator.SetNumberOfXDivisions(12)
decimator.SetNumberOfYDivisions(12)
decimator.SetNumberOfZDivisions(12)

# Mapper: map the original sphere to graphics primitives
original_mapper = vtkPolyDataMapper()
original_mapper.SetInputConnection(sphere_source.GetOutputPort())

# Actor: original sphere with visible edges
original_actor = vtkActor()
original_actor.SetMapper(original_mapper)
original_actor.GetProperty().SetColor(cornflower_blue_rgb)
original_actor.GetProperty().EdgeVisibilityOn()
original_actor.GetProperty().SetEdgeColor(black_rgb)

# Mapper: map the decimated mesh to graphics primitives
decimated_mapper = vtkPolyDataMapper()
decimated_mapper.SetInputConnection(decimator.GetOutputPort())

# Actor: decimated sphere with visible edges
decimated_actor = vtkActor()
decimated_actor.SetMapper(decimated_mapper)
decimated_actor.GetProperty().SetColor(tomato_rgb)
decimated_actor.GetProperty().EdgeVisibilityOn()
decimated_actor.GetProperty().SetEdgeColor(black_rgb)

# Renderer: left viewport — original mesh
left_renderer = vtkRenderer()
left_renderer.AddActor(original_actor)
left_renderer.SetBackground(slate_gray_rgb)
left_renderer.SetViewport(0, 0, 0.5, 1)

# Renderer: right viewport — decimated mesh
right_renderer = vtkRenderer()
right_renderer.AddActor(decimated_actor)
right_renderer.SetBackground(dark_slate_gray_rgb)
right_renderer.SetViewport(0.5, 0, 1, 1)

# Render window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(left_renderer)
render_window.AddRenderer(right_renderer)
render_window.SetWindowName("quadric clustering")
render_window.SetMultiSamples(0)
render_window.SetSize(960, 480)

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Scene: configure the camera
left_renderer.ResetCamera()
right_renderer.ResetCamera()

# Start: launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
