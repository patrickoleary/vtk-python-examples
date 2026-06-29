#!/usr/bin/env python

# Test texturing a sphere with a JPEG image.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

import os

from vtkmodules.vtkFiltersCore import vtkStripper
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkFiltersTexture import vtkTextureMapToSphere
from vtkmodules.vtkIOImage import vtkJPEGReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkProperty,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
    vtkTexture,
)

# Read texture image
reader = vtkJPEGReader()
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

reader.SetFileName(os.path.join(data_dir, "beach.jpg"))

# Surface rendering
sphere_source = vtkSphereSource()
sphere_source.SetRadius(100)

texture_sphere = vtkTextureMapToSphere()
texture_sphere.SetInputConnection(sphere_source.GetOutputPort())

sphere_stripper = vtkStripper()
sphere_stripper.SetInputConnection(texture_sphere.GetOutputPort())
sphere_stripper.SetMaximumLength(5)

sphere_mapper = vtkPolyDataMapper()
sphere_mapper.SetInputConnection(sphere_stripper.GetOutputPort())
sphere_mapper.ScalarVisibilityOff()

sphere_texture = vtkTexture()
sphere_texture.SetInputConnection(reader.GetOutputPort())

sphere_property = vtkProperty()

sphere_actor = vtkActor()
sphere_actor.SetMapper(sphere_mapper)
sphere_actor.SetTexture(sphere_texture)
sphere_actor.SetProperty(sphere_property)

# Renderer
renderer = vtkRenderer()
renderer.AddViewProp(sphere_actor)

render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("textured sphere basic")
render_window.SetMultiSamples(0)
render_window.SetSize(300, 300)

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
camera = renderer.GetActiveCamera()
camera.SetFocalPoint(0, 0, 0)
camera.SetPosition(100, 400, -100)
camera.SetViewUp(0, 0, -1)
renderer.ResetCameraClippingRange()

interactor.Initialize()
interactor.Start()
