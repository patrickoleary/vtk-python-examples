#!/usr/bin/env python

# Test vtkCellPicker with texture data on a textured sphere.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

import os

from vtkmodules.vtkFiltersCore import vtkStripper
from vtkmodules.vtkFiltersSources import (
    vtkConeSource,
    vtkSphereSource,
)
from vtkmodules.vtkFiltersTexture import vtkTextureMapToSphere
from vtkmodules.vtkIOImage import vtkJPEGReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkCellPicker,
    vtkDataSetMapper,
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

# Textured sphere
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
sphere_property.BackfaceCullingOn()

sphere_actor = vtkActor()
sphere_actor.SetMapper(sphere_mapper)
sphere_actor.SetTexture(sphere_texture)
sphere_actor.SetProperty(sphere_property)

# Renderer
renderer = vtkRenderer()
renderer.AddViewProp(sphere_actor)

render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("surface picker with texture")
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

render_window.Render()

# Cone source for pick markers
cone_source = vtkConeSource()
cone_source.CappingOn()
cone_source.SetHeight(12)
cone_source.SetRadius(5)
cone_source.SetResolution(31)
cone_source.SetCenter(6, 0, 0)
cone_source.SetDirection(-1, 0, 0)

# Picker with texture data picking
picker = vtkCellPicker()
picker.SetTolerance(1e-6)
picker.PickTextureDataOn()

# Pick the actor
picker.Pick(104, 154, 0, renderer)
p = picker.GetPickPosition()
n = picker.GetPickNormal()
ijk = picker.GetPointIJK()
data = picker.GetDataSet()

i = ijk[0]
j = ijk[1]
k = ijk[2]

if data.IsA("vtkImageData"):
    r = data.GetScalarComponentAsDouble(i, j, k, 0)
    g = data.GetScalarComponentAsDouble(i, j, k, 1)
    b = data.GetScalarComponentAsDouble(i, j, k, 2)
else:
    r = 255.0
    g = 0.0
    b = 0.0

r = r / 255.0
g = g / 255.0
b = b / 255.0

cone_mapper_1 = vtkDataSetMapper()
cone_mapper_1.SetInputConnection(cone_source.GetOutputPort())
cone_actor_1 = vtkActor()
cone_actor_1.PickableOff()
cone_actor_1.SetMapper(cone_mapper_1)
cone_actor_1.GetProperty().SetColor(r, g, b)
cone_actor_1.GetProperty().BackfaceCullingOn()
cone_actor_1.SetPosition(p)
if n[0] < 0.0:
    cone_actor_1.RotateWXYZ(180, 0, 1, 0)
    cone_actor_1.RotateWXYZ(180, (n[0] - 1.0) * 0.5, n[1] * 0.5, n[2] * 0.5)
else:
    cone_actor_1.RotateWXYZ(180, (n[0] + 1.0) * 0.5, n[1] * 0.5, n[2] * 0.5)
renderer.AddViewProp(cone_actor_1)

renderer.ResetCameraClippingRange()

interactor.Initialize()
interactor.Start()
