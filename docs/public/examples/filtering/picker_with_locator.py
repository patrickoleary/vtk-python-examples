#!/usr/bin/env python

# Test vtkCellPicker with vtkCellLocator on head CT data with clipping planes.

import os

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import vtkLookupTable
from vtkmodules.vtkCommonDataModel import (
    vtkCellLocator,
    vtkPlane,
)
from vtkmodules.vtkFiltersCore import (
    vtkMarchingCubes,
    vtkPolyDataNormals,
    vtkStripper,
)
from vtkmodules.vtkFiltersSources import vtkConeSource
from vtkmodules.vtkIOImage import vtkVolume16Reader
from vtkmodules.vtkImagingCore import vtkImageMapToColors
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkCellPicker,
    vtkDataSetMapper,
    vtkImageActor,
    vtkPolyDataMapper,
    vtkProperty,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Read volume data
v16 = vtkVolume16Reader()
v16.SetDataDimensions(64, 64)
v16.SetImageRange(1, 93)
v16.SetDataByteOrderToLittleEndian()
v16.SetFilePrefix(os.path.join(data_dir, "headsq", "quarter"))
v16.SetDataSpacing(3.2, 3.2, 1.5)

# Surface rendering - bone extraction
bone_extractor = vtkMarchingCubes()
bone_extractor.SetInputConnection(v16.GetOutputPort())
bone_extractor.SetValue(0, 1150)

bone_normals = vtkPolyDataNormals()
bone_normals.SetInputConnection(bone_extractor.GetOutputPort())
bone_normals.SetFeatureAngle(60.0)

bone_stripper = vtkStripper()
bone_stripper.SetInputConnection(bone_normals.GetOutputPort())
bone_stripper.SetMaximumLength(5)

bone_locator = vtkCellLocator()
bone_locator.SetDataSet(bone_stripper.GetOutput())

bone_mapper = vtkPolyDataMapper()
bone_mapper.SetInputConnection(bone_stripper.GetOutputPort())
bone_mapper.ScalarVisibilityOff()

bone_property = vtkProperty()
bone_property.SetColor(1.0, 1.0, 0.9)

bone = vtkActor()
bone.SetMapper(bone_mapper)
bone.SetProperty(bone_property)

# Image actor
table = vtkLookupTable()
table.SetRange(0, 2000)
table.SetRampToLinear()
table.SetValueRange(0, 1)
table.SetHueRange(0, 0)
table.SetSaturationRange(0, 0)

map_to_colors = vtkImageMapToColors()
map_to_colors.SetInputConnection(v16.GetOutputPort())
map_to_colors.SetLookupTable(table)

image_actor = vtkImageActor()
image_actor.GetMapper().SetInputConnection(map_to_colors.GetOutputPort())
image_actor.SetDisplayExtent(32, 32, 0, 63, 0, 92)

# Clipping planes
cx = 100.8
cy = 100.8
cz = 69.0

bone_clip = vtkPlane()
bone_clip.SetNormal(0, 1, 0)
bone_clip.SetOrigin(cx, cy, cz)

bone_clip_2 = vtkPlane()
bone_clip_2.SetNormal(-1, 0, 0)
bone_clip_2.SetOrigin(cx + 100, cy, cz)

bone_mapper.AddClippingPlane(bone_clip)
bone_mapper.AddClippingPlane(bone_clip_2)

# Renderer
renderer = vtkRenderer()
renderer.AddViewProp(bone)
renderer.AddViewProp(image_actor)

render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("picker with locator")
render_window.SetMultiSamples(0)
render_window.SetSize(300, 300)

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
camera = renderer.GetActiveCamera()
camera.SetFocalPoint(cx, cy, cz)
camera.SetPosition(cx + 400, cy + 100, cz - 100)
camera.SetViewUp(0, 0, -1)
renderer.ResetCameraClippingRange()

# Render before picks — picker needs initialized scene
render_window.Render()

# Cone source for pick markers
cone_source = vtkConeSource()
cone_source.CappingOn()
cone_source.SetHeight(12)
cone_source.SetRadius(5)
cone_source.SetResolution(31)
cone_source.SetCenter(6, 0, 0)
cone_source.SetDirection(-1, 0, 0)

# Picker with locator
picker = vtkCellPicker()
picker.SetTolerance(1e-6)
picker.AddLocator(bone_locator)

# Helper to orient cone along normal
def point_cone(actor, n):
    if n[0] < 0.0:
        actor.RotateWXYZ(180, 0, 1, 0)
        actor.RotateWXYZ(180, (n[0] - 1.0) * 0.5, n[1] * 0.5, n[2] * 0.5)
    else:
        actor.RotateWXYZ(180, (n[0] + 1.0) * 0.5, n[1] * 0.5, n[2] * 0.5)

# Pick the bone actor
picker.Pick(70, 120, 0, renderer)
p = picker.GetPickPosition()
n = picker.GetPickNormal()

cone_actor_1 = vtkActor()
cone_actor_1.PickableOff()
cone_mapper_1 = vtkDataSetMapper()
cone_mapper_1.SetInputConnection(cone_source.GetOutputPort())
cone_actor_1.SetMapper(cone_mapper_1)
cone_actor_1.GetProperty().SetColor(1, 0, 0)
cone_actor_1.SetPosition(p)
point_cone(cone_actor_1, n)
renderer.AddViewProp(cone_actor_1)

# Pick the image
picker.Pick(170, 220, 0, renderer)
p = picker.GetPickPosition()
n = picker.GetPickNormal()

cone_actor_2 = vtkActor()
cone_actor_2.PickableOff()
cone_mapper_2 = vtkDataSetMapper()
cone_mapper_2.SetInputConnection(cone_source.GetOutputPort())
cone_actor_2.SetMapper(cone_mapper_2)
cone_actor_2.GetProperty().SetColor(1, 0, 0)
cone_actor_2.SetPosition(p)
point_cone(cone_actor_2, n)
renderer.AddViewProp(cone_actor_2)

# Pick the actor again with ray clipping
picker.Pick(180, 220, 0, renderer)
p = picker.GetPickPosition()
n = picker.GetPickNormal()

cone_actor_3 = vtkActor()
cone_actor_3.PickableOff()
cone_mapper_3 = vtkDataSetMapper()
cone_mapper_3.SetInputConnection(cone_source.GetOutputPort())
cone_actor_3.SetMapper(cone_mapper_3)
cone_actor_3.GetProperty().SetColor(1, 0, 0)
cone_actor_3.SetPosition(p)
point_cone(cone_actor_3, n)
renderer.AddViewProp(cone_actor_3)

renderer.ResetCameraClippingRange()

interactor.Initialize()
interactor.Start()
