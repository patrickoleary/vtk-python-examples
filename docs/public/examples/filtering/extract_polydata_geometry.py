#!/usr/bin/env python

# Demonstrate vtkExtractPolyDataGeometry to extract cells of a sphere
# that lie inside (or outside) a plane implicit function, effectively
# clipping it in half.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkCommonDataModel import vtkPlane
from vtkmodules.vtkFiltersExtraction import vtkExtractPolyDataGeometry
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
slate_gray_rgb = (0.439, 0.502, 0.565)

# Source: high-resolution sphere
sphere_source = vtkSphereSource()
sphere_source.SetPhiResolution(64)
sphere_source.SetThetaResolution(64)

# Implicit function: plane through the origin
clip_plane = vtkPlane()
clip_plane.SetOrigin(0, 0, 0)
clip_plane.SetNormal(1, 0, 0)

# Filter: extract cells inside the plane
extract_geometry = vtkExtractPolyDataGeometry()
extract_geometry.SetInputConnection(sphere_source.GetOutputPort())
extract_geometry.SetImplicitFunction(clip_plane)
extract_geometry.ExtractInsideOn()

# Mapper: map the extracted geometry to graphics primitives
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(extract_geometry.GetOutputPort())

# Actor: assign the mapped geometry
actor = vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetColor(cornflower_blue_rgb)
actor.GetProperty().EdgeVisibilityOn()
actor.GetProperty().SetEdgeColor(0.0, 0.0, 0.0)

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(slate_gray_rgb)

# Render window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("extract polydata geometry")
render_window.SetMultiSamples(0)
render_window.SetSize(640, 480)

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Scene: configure the camera
renderer.ResetCamera()

# Start: launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
