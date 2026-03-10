#!/usr/bin/env python

# Map a procedural checkerboard texture onto a cylinder using
# vtkTextureMapToCylinder to generate cylindrical texture coordinates.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkFiltersSources import vtkCylinderSource
from vtkmodules.vtkFiltersTexture import vtkTextureMapToCylinder
from vtkmodules.vtkImagingSources import vtkImageCanvasSource2D
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
    vtkTexture,
)

# Colors (normalized RGB)
slate_gray_background_rgb = (0.439, 0.502, 0.565)

# Source: create a cylinder
cylinder = vtkCylinderSource()
cylinder.SetRadius(1.0)
cylinder.SetHeight(2.0)
cylinder.SetResolution(32)
cylinder.CappingOn()

# Texture image: procedural checkerboard pattern
canvas = vtkImageCanvasSource2D()
canvas.SetScalarTypeToUnsignedChar()
canvas.SetNumberOfScalarComponents(3)
canvas.SetExtent(0, 127, 0, 127, 0, 0)
canvas.SetDrawColor(255, 255, 255)
canvas.FillBox(0, 127, 0, 127)
canvas.SetDrawColor(200, 100, 50)
for row in range(8):
    for col in range(8):
        if (row + col) % 2 == 0:
            canvas.FillBox(col * 16, col * 16 + 15, row * 16, row * 16 + 15)
canvas.Update()

texture = vtkTexture()
texture.SetInputConnection(canvas.GetOutputPort())
texture.InterpolateOn()

# TextureMapToCylinder: generate cylindrical texture coordinates
texture_map = vtkTextureMapToCylinder()
texture_map.SetInputConnection(cylinder.GetOutputPort())
texture_map.PreventSeamOn()

# Mapper: map polygon data to graphics primitives
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(texture_map.GetOutputPort())

# Actor: assign the mapped geometry with the texture
actor = vtkActor()
actor.SetMapper(mapper)
actor.SetTexture(texture)

# Renderer: assemble the scene and configure the camera
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(slate_gray_background_rgb)
renderer.ResetCamera()

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(640, 480)
render_window.SetWindowName("TextureMapToCylinder")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
