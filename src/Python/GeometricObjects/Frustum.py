#!/usr/bin/env python

# Extract and display a camera frustum using vtkFrustumSource.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkCommonDataModel import vtkPlanes
from vtkmodules.vtkFiltersGeneral import vtkShrinkPolyData
from vtkmodules.vtkFiltersSources import vtkFrustumSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkCamera,
    vtkPolyDataMapper,
    vtkProperty,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
banana_rgb = (0.890, 0.812, 0.341)
tomato_rgb = (1.0, 0.388, 0.278)
silver_background_rgb = (0.75, 0.75, 0.75)

# Data: extract frustum planes from a camera
camera = vtkCamera()
camera.SetClippingRange(0.1, 0.4)
planes_array = [0] * 24
camera.GetFrustumPlanes(1.0, planes_array)

planes = vtkPlanes()
planes.SetFrustumPlanes(planes_array)

# Source: generate the frustum geometry
frustum_source = vtkFrustumSource()
frustum_source.ShowLinesOff()
frustum_source.SetPlanes(planes)

# Filter: shrink the frustum faces slightly
shrink = vtkShrinkPolyData()
shrink.SetInputConnection(frustum_source.GetOutputPort())
shrink.SetShrinkFactor(0.9)

# Mapper: map shrunk frustum to graphics primitives
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(shrink.GetOutputPort())

# Actor: display with edges and backface coloring
back_property = vtkProperty()
back_property.SetColor(tomato_rgb)

actor = vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().EdgeVisibilityOn()
actor.GetProperty().SetColor(banana_rgb)
actor.SetBackfaceProperty(back_property)

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(silver_background_rgb)
renderer.GetActiveCamera().SetPosition(1, 0, 0)
renderer.GetActiveCamera().SetFocalPoint(0, 0, 0)
renderer.GetActiveCamera().SetViewUp(0, 1, 0)
renderer.GetActiveCamera().Azimuth(30)
renderer.GetActiveCamera().Elevation(30)
renderer.ResetCamera()

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("Frustum")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
