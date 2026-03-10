#!/usr/bin/env python

# Transform texture coordinates on a textured sphere using
# vtkTransformTextureCoords to scale, translate, and flip the mapping.
# The left viewport shows the original texture mapping and the right
# viewport shows the transformed result.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkFiltersTexture import (
    vtkTextureMapToSphere,
    vtkTransformTextureCoords,
)
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

# Source: create a sphere
sphere = vtkSphereSource()
sphere.SetRadius(1.0)
sphere.SetPhiResolution(40)
sphere.SetThetaResolution(40)

# Texture image: procedural checkerboard pattern
canvas = vtkImageCanvasSource2D()
canvas.SetScalarTypeToUnsignedChar()
canvas.SetNumberOfScalarComponents(3)
canvas.SetExtent(0, 127, 0, 127, 0, 0)
canvas.SetDrawColor(255, 255, 255)
canvas.FillBox(0, 127, 0, 127)
canvas.SetDrawColor(180, 60, 60)
for row in range(4):
    for col in range(4):
        if (row + col) % 2 == 0:
            canvas.FillBox(col * 32, col * 32 + 31, row * 32, row * 32 + 31)
canvas.Update()

texture = vtkTexture()
texture.SetInputConnection(canvas.GetOutputPort())
texture.InterpolateOn()
texture.RepeatOn()

# TextureMapToSphere: generate spherical texture coordinates
sphere_map = vtkTextureMapToSphere()
sphere_map.SetInputConnection(sphere.GetOutputPort())
sphere_map.PreventSeamOff()

# ---- Left viewport: original texture coordinates ----
original_mapper = vtkPolyDataMapper()
original_mapper.SetInputConnection(sphere_map.GetOutputPort())
original_mapper.ScalarVisibilityOff()

original_actor = vtkActor()
original_actor.SetMapper(original_mapper)
original_actor.SetTexture(texture)

left_renderer = vtkRenderer()
left_renderer.SetViewport(0.0, 0.0, 0.5, 1.0)
left_renderer.AddActor(original_actor)
left_renderer.SetBackground(slate_gray_background_rgb)
left_renderer.ResetCamera()

# ---- Right viewport: transformed texture coordinates ----
transform_tc = vtkTransformTextureCoords()
transform_tc.SetInputConnection(sphere_map.GetOutputPort())
transform_tc.SetScale(2.0, 2.0, 1.0)
transform_tc.SetPosition(0.25, 0.25, 0.0)
transform_tc.SetFlipR(True)

transformed_mapper = vtkPolyDataMapper()
transformed_mapper.SetInputConnection(transform_tc.GetOutputPort())
transformed_mapper.ScalarVisibilityOff()

# Create a second texture instance for the right viewport
texture2 = vtkTexture()
texture2.SetInputConnection(canvas.GetOutputPort())
texture2.InterpolateOn()
texture2.RepeatOn()

transformed_actor = vtkActor()
transformed_actor.SetMapper(transformed_mapper)
transformed_actor.SetTexture(texture2)

right_renderer = vtkRenderer()
right_renderer.SetViewport(0.5, 0.0, 1.0, 1.0)
right_renderer.AddActor(transformed_actor)
right_renderer.SetBackground(slate_gray_background_rgb)
right_renderer.SetActiveCamera(left_renderer.GetActiveCamera())

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(left_renderer)
render_window.AddRenderer(right_renderer)
render_window.SetSize(800, 400)
render_window.SetWindowName("TransformTextureCoords")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
