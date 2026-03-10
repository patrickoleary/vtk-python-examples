#!/usr/bin/env python

# Render a regular pentagon with visible edges using vtkRegularPolygonSource
# and vtkShrinkPolyData.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkFiltersGeneral import vtkShrinkPolyData
from vtkmodules.vtkFiltersSources import vtkRegularPolygonSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
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

# Source: generate a regular pentagon
polygon_source = vtkRegularPolygonSource()
polygon_source.SetNumberOfSides(5)
polygon_source.SetRadius(5)
polygon_source.SetCenter(0, 0, 0)

# Filter: shrink polygons slightly to separate faces visually
shrink = vtkShrinkPolyData()
shrink.SetInputConnection(polygon_source.GetOutputPort())
shrink.SetShrinkFactor(0.9)

# Mapper: map the shrunk polygon to graphics primitives
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(shrink.GetOutputPort())

# Backface property: tomato color for backfaces
back = vtkProperty()
back.SetColor(tomato_rgb)

# Actor: set visual properties — banana front, tomato back, visible edges
actor = vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().EdgeVisibilityOn()
actor.GetProperty().SetLineWidth(5)
actor.GetProperty().SetColor(banana_rgb)
actor.SetBackfaceProperty(back)

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(silver_background_rgb)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("RegularPolygonSource")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
