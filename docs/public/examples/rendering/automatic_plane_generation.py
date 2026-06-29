#!/usr/bin/env python

# Demonstrate vtkTextureMapToPlane with automatic plane generation,
# mapping an earth PPM texture onto a plane source.

import os

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersSources import vtkPlaneSource
from vtkmodules.vtkFiltersTexture import vtkTextureMapToPlane
from vtkmodules.vtkIOImage import vtkPNMReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
    vtkTexture,
)

data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Plane source offset from origin
a_plane = vtkPlaneSource()
a_plane.SetCenter(-100, -100, -100)
a_plane.SetOrigin(-100, -100, -100)
a_plane.SetPoint1(-90, -100, -100)
a_plane.SetPoint2(-100, -90, -100)
a_plane.SetNormal(0, -1, 1)

# Read texture image
image_in = vtkPNMReader()
image_in.SetFileName(os.path.join(data_dir, "earth.ppm"))

texture = vtkTexture()
texture.SetInputConnection(image_in.GetOutputPort())

# Automatic texture coordinate generation
texture_plane = vtkTextureMapToPlane()
texture_plane.SetInputConnection(a_plane.GetOutputPort())
texture_plane.AutomaticPlaneGenerationOn()

# Mapper and actor
plane_mapper = vtkPolyDataMapper()
plane_mapper.SetInputConnection(texture_plane.GetOutputPort())

textured_plane = vtkActor()
textured_plane.SetMapper(plane_mapper)
textured_plane.SetTexture(texture)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(textured_plane)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(200, 200)
render_window.SetWindowName("automatic plane generation")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
