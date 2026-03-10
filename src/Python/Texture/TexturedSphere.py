#!/usr/bin/env python

# Map an earth texture onto a sphere using vtkTexturedSphereSource.

import os
from pathlib import Path

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkFiltersSources import vtkTexturedSphereSource
from vtkmodules.vtkFiltersTexture import vtkTransformTextureCoords
from vtkmodules.vtkIOImage import vtkImageReader2Factory
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
    vtkTexture,
)

# Colors (normalized RGB)
black_rgb = (0.0, 0.0, 0.0)

# Data: locate the earth texture image
data_dir = Path(os.environ.get("VPE_DATA_DIR", Path(__file__).parent))
file_name = str(data_dir / "earth.ppm")

# Source: create a sphere with built-in texture coordinates.
# vtkTexturedSphereSource generates a sphere with proper spherical
# texture coordinates for mapping equirectangular images.
sphere = vtkTexturedSphereSource()
sphere.SetThetaResolution(100)
sphere.SetPhiResolution(100)

# TransformTextureCoords: shift the texture coordinates so the prime
# meridian is centered in the view (Null Island at 0°N 0°E).
transform_texture = vtkTransformTextureCoords()
transform_texture.SetInputConnection(sphere.GetOutputPort())
transform_texture.SetPosition(0.25, 0.0, 0.0)

# Texture: load the earth image
reader_factory = vtkImageReader2Factory()
image_reader = reader_factory.CreateImageReader2(file_name)
image_reader.SetFileName(file_name)
image_reader.Update()

texture = vtkTexture()
texture.SetInputConnection(image_reader.GetOutputPort())

# Mapper: map polygon data to graphics primitives
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(transform_texture.GetOutputPort())

# Actor: assign the mapped geometry and apply the earth texture
actor = vtkActor()
actor.SetMapper(mapper)
actor.SetTexture(texture)

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(black_rgb)
renderer.ResetCamera()
renderer.GetActiveCamera().Elevation(-90)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(640, 480)
render_window.SetWindowName("TexturedSphere")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
