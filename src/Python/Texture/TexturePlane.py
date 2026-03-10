#!/usr/bin/env python

# Map a texture image onto a plane.

import os
from pathlib import Path

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkFiltersSources import vtkPlaneSource
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
dark_slate_gray_rgb = (0.184, 0.310, 0.310)

# Data: locate the texture image
data_dir = Path(os.environ.get("VPE_DATA_DIR", Path(__file__).parent))
file_name = str(data_dir / "masonry.bmp")

# Texture: load the image file. A texture is any unsigned char image.
# vtkImageReader2Factory automatically selects the correct reader.
reader_factory = vtkImageReader2Factory()
image_reader = reader_factory.CreateImageReader2(file_name)
image_reader.SetFileName(file_name)
image_reader.Update()

texture = vtkTexture()
texture.SetInputConnection(image_reader.GetOutputPort())
texture.InterpolateOn()

# Source: create a plane. vtkPlaneSource generates texture coordinates
# automatically so the texture maps directly onto the surface.
plane = vtkPlaneSource()

# Mapper: map polygon data to graphics primitives
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(plane.GetOutputPort())

# Actor: assign the mapped geometry and apply the texture
actor = vtkActor()
actor.SetMapper(mapper)
actor.SetTexture(texture)

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(dark_slate_gray_rgb)
renderer.ResetCamera()
renderer.GetActiveCamera().Elevation(-30)
renderer.GetActiveCamera().Roll(-20)
renderer.ResetCameraClippingRange()

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(640, 480)
render_window.SetWindowName("TexturePlane")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
