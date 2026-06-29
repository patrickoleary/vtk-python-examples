#!/usr/bin/env python

# Demonstrate equirectangular to cube map texture conversion with a skybox.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

import os

from vtkmodules.vtkIOImage import vtkJPEGReader
from vtkmodules.vtkRenderingCore import (
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
    vtkSkybox,
    vtkTexture,
)
from vtkmodules.vtkRenderingOpenGL2 import vtkEquirectangularToCubeMapTexture

# Read equirectangular image
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))
reader = vtkJPEGReader()
reader.SetFileName(os.path.join(data_dir, "autoshop.jpg"))

texture = vtkTexture()
texture.SetInputConnection(reader.GetOutputPort())

# Convert to cube map
cubemap = vtkEquirectangularToCubeMapTexture()
cubemap.SetInputTexture(texture)

# Skybox
world = vtkSkybox()
world.SetTexture(cubemap)

# Rendering pipeline
renderer = vtkRenderer()
renderer.AddActor(world)

render_window = vtkRenderWindow()
render_window.SetSize(400, 400)
render_window.AddRenderer(renderer)
render_window.SetWindowName("equirectangular to cube map")

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
