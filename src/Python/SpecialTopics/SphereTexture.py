#!/usr/bin/env python

# Texture-map a JPEG image onto a sphere using spherical texture coordinates.

import os
from pathlib import Path

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkFiltersTexture import vtkTextureMapToSphere
from vtkmodules.vtkIOImage import vtkJPEGReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
    vtkTexture,
)

# Colors (normalized RGB)
rosy_brown_rgb = (0.737, 0.561, 0.561)

# Data: locate the JPEG texture file
data_dir = Path(os.environ.get("VPE_DATA_DIR", Path(__file__).parent))
jpeg_file = str(data_dir / "masonry-wide.jpg")

# Source: generate sphere polygon data
sphere = vtkSphereSource()
sphere.SetThetaResolution(12)
sphere.SetPhiResolution(12)

# Reader: load the JPEG image
reader = vtkJPEGReader()
reader.SetFileName(jpeg_file)

# Texture: create a texture from the image
texture = vtkTexture()
texture.SetInputConnection(reader.GetOutputPort())

# TextureMapToSphere: generate spherical texture coordinates
map_to_sphere = vtkTextureMapToSphere()
map_to_sphere.SetInputConnection(sphere.GetOutputPort())
map_to_sphere.PreventSeamOn()

# Mapper: map polygon data to graphics primitives
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(map_to_sphere.GetOutputPort())

# Actor: assign the mapped geometry and texture
actor = vtkActor()
actor.SetMapper(mapper)
actor.SetTexture(texture)

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(rosy_brown_rgb)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.SetSize(480, 480)
render_window.SetWindowName("SphereTexture")
render_window.AddRenderer(renderer)

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
