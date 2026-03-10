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
sphere = vtkSphereSource()
sphere.SetPhiResolution(100)
sphere.SetThetaResolution(100)

# Filter: simplify the mesh
decimator = vtkQuadricClustering()
decimator.SetInputConnection(sphere.GetOutputPort())
decimator.SetNumberOfXDivisions(12)
decimator.SetNumberOfYDivisions(12)
decimator.SetNumberOfZDivisions(12)

# Mapper: map the original sphere to graphics primitives
orig_mapper = vtkPolyDataMapper()
orig_mapper.SetInputConnection(sphere.GetOutputPort())

# Actor: original sphere with visible edges
orig_actor = vtkActor()
orig_actor.SetMapper(orig_mapper)
orig_actor.GetProperty().SetColor(cornflower_blue_rgb)
orig_actor.GetProperty().EdgeVisibilityOn()
orig_actor.GetProperty().SetEdgeColor(black_rgb)

# Mapper: map the decimated mesh to graphics primitives
dec_mapper = vtkPolyDataMapper()
dec_mapper.SetInputConnection(decimator.GetOutputPort())

# Actor: decimated sphere with visible edges
dec_actor = vtkActor()
dec_actor.SetMapper(dec_mapper)
dec_actor.GetProperty().SetColor(tomato_rgb)
dec_actor.GetProperty().EdgeVisibilityOn()
dec_actor.GetProperty().SetEdgeColor(black_rgb)

# Renderer: left viewport — original mesh
left_renderer = vtkRenderer()
left_renderer.AddActor(orig_actor)
left_renderer.SetBackground(slate_gray_rgb)
left_renderer.SetViewport(0, 0, 0.5, 1)

# Renderer: right viewport — decimated mesh
right_renderer = vtkRenderer()
right_renderer.AddActor(dec_actor)
right_renderer.SetBackground(dark_slate_gray_rgb)
right_renderer.SetViewport(0.5, 0, 1, 1)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(left_renderer)
render_window.AddRenderer(right_renderer)
render_window.SetSize(960, 480)
render_window.SetWindowName("QuadricClustering")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
