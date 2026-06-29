#!/usr/bin/env python

# Render a tessellated box with shrunk faces and visible edges using
# vtkTessellatedBoxSource and vtkShrinkFilter.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkFiltersGeneral import vtkShrinkFilter
from vtkmodules.vtkFiltersSources import vtkTessellatedBoxSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkDataSetMapper,
    vtkProperty,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
banana_rgb = (0.890, 0.812, 0.341)
tomato_rgb = (1.0, 0.388, 0.278)
silver_background_rgb = (0.75, 0.75, 0.75)

# Source: generate a tessellated box with quads at subdivision level 3
box_source = vtkTessellatedBoxSource()
box_source.SetLevel(3)
box_source.QuadsOn()
box_source.SetBounds(-10.0, 10.0, 10.0, 20.0, -5.0, 5.0)
SINGLE_PRECISION = 0  # DOUBLE_PRECISION = 1, DEFAULT_PRECISION = 2
box_source.SetOutputPointsPrecision(SINGLE_PRECISION)

# Filter: shrink each face toward its centroid
shrink = vtkShrinkFilter()
shrink.SetInputConnection(box_source.GetOutputPort())
shrink.SetShrinkFactor(0.8)

# Mapper: map the shrunk box to graphics primitives
mapper = vtkDataSetMapper()
mapper.SetInputConnection(shrink.GetOutputPort())

# Backface property: tomato color for backfaces
back = vtkProperty()
back.SetColor(tomato_rgb)

# Actor: set visual properties — banana front, tomato back, visible edges
actor = vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().EdgeVisibilityOn()
actor.GetProperty().SetColor(banana_rgb)
actor.SetBackfaceProperty(back)

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(silver_background_rgb)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("tessellated box source")
render_window.SetMultiSamples(0)
render_window.SetSize(640, 480)

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Scene: configure the camera
renderer.ResetCamera()
renderer.GetActiveCamera().Azimuth(30)
renderer.GetActiveCamera().Elevation(30)
renderer.ResetCameraClippingRange()

render_window_interactor.Initialize()
render_window_interactor.Start()
