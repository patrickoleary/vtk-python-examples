#!/usr/bin/env python

# Demonstrate volume picking with cropping planes, clipping planes, and cone markers at pick positions.

import os

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingVolumeOpenGL2  # noqa: F401

from vtkmodules.vtkCommonDataModel import (
    vtkPiecewiseFunction,
    vtkPlane,
)
from vtkmodules.vtkCommonTransforms import vtkTransform
from vtkmodules.vtkFiltersSources import vtkConeSource
from vtkmodules.vtkIOImage import vtkVolume16Reader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkColorTransferFunction,
    vtkDataSetMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
    vtkVolume,
    vtkVolumeProperty,
)
from vtkmodules.vtkRenderingVolume import (
    vtkFixedPointVolumeRayCastMapper,
    vtkVolumePicker,
)

data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Renderer and render window
renderer = vtkRenderer()

render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("volume picker crop")

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Read the volume
volume_reader = vtkVolume16Reader()
volume_reader.SetDataDimensions(64, 64)
volume_reader.SetImageRange(1, 93)
volume_reader.SetDataByteOrderToLittleEndian()
volume_reader.SetFilePrefix(os.path.join(data_dir, "headsq", "quarter"))
volume_reader.SetDataSpacing(3.2, 3.2, 1.5)

# Volume rendering with cropping
volume_mapper = vtkFixedPointVolumeRayCastMapper()
volume_mapper.SetInputConnection(volume_reader.GetOutputPort())
volume_mapper.CroppingOn()
volume_mapper.SetCroppingRegionPlanes(0.0, 141.6, 0.0, 201.6, 0.0, 138.0)

volume_color = vtkColorTransferFunction()
volume_color.AddRGBPoint(0, 0.0, 0.0, 0.0)
volume_color.AddRGBPoint(180, 0.3, 0.1, 0.2)
volume_color.AddRGBPoint(1000, 1.0, 0.7, 0.6)
volume_color.AddRGBPoint(2000, 1.0, 1.0, 0.9)

volume_scalar_opacity = vtkPiecewiseFunction()
volume_scalar_opacity.AddPoint(0, 0.0)
volume_scalar_opacity.AddPoint(180, 0.0)
volume_scalar_opacity.AddPoint(1000, 0.2)
volume_scalar_opacity.AddPoint(2000, 0.8)

volume_gradient_opacity = vtkPiecewiseFunction()
volume_gradient_opacity.AddPoint(0, 0.0)
volume_gradient_opacity.AddPoint(90, 0.5)
volume_gradient_opacity.AddPoint(100, 1.0)

volume_property = vtkVolumeProperty()
volume_property.SetColor(volume_color)
volume_property.SetScalarOpacity(volume_scalar_opacity)
volume_property.SetGradientOpacity(volume_gradient_opacity)
volume_property.SetInterpolationTypeToLinear()
volume_property.ShadeOn()
volume_property.SetAmbient(0.6)
volume_property.SetDiffuse(0.6)
volume_property.SetSpecular(0.1)

volume = vtkVolume()
volume.SetMapper(volume_mapper)
volume.SetProperty(volume_property)

# Transform and clipping plane
transform = vtkTransform()
transform.RotateWXYZ(-20, 0.0, -0.7, 0.7)
volume.SetUserTransform(transform)

center = volume.GetCenter()

volume_clip = vtkPlane()
volume_clip.SetNormal(0, 1, 0)
volume_clip.SetOrigin(center[0], center[1], center[2])
volume_mapper.AddClippingPlane(volume_clip)

renderer.AddViewProp(volume)

camera = renderer.GetActiveCamera()
camera.SetFocalPoint(center[0], center[1], center[2])
camera.SetPosition(center[0] + 500, center[1] - 100, center[2] - 100)
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

# Picker
picker = vtkVolumePicker()
picker.SetTolerance(1e-6)
picker.SetVolumeOpacityIsovalue(0.3)

# Pick part of the volume that is clipped away
picker.Pick(192, 103, 0, renderer)
pick_position = picker.GetPickPosition()
pick_normal = picker.GetPickNormal()

cone_actor_0 = vtkActor()
cone_actor_0.PickableOff()
cone_mapper_0 = vtkDataSetMapper()
cone_mapper_0.SetInputConnection(cone_source.GetOutputPort())
cone_actor_0.SetMapper(cone_mapper_0)
cone_actor_0.GetProperty().SetColor(1, 0, 0)
cone_actor_0.GetProperty().BackfaceCullingOn()
cone_actor_0.SetPosition(pick_position[0], pick_position[1], pick_position[2])
if pick_normal[0] < 0.0:
    cone_actor_0.RotateWXYZ(180, 0, 1, 0)
    cone_actor_0.RotateWXYZ(180, (pick_normal[0] - 1.0) * 0.5, pick_normal[1] * 0.5, pick_normal[2] * 0.5)
else:
    cone_actor_0.RotateWXYZ(180, (pick_normal[0] + 1.0) * 0.5, pick_normal[1] * 0.5, pick_normal[2] * 0.5)
renderer.AddViewProp(cone_actor_0)

# Pick through a cropping plane to some bone
picker.UseVolumeGradientOpacityOn()
picker.Pick(90, 180, 0, renderer)
pick_position = picker.GetPickPosition()
pick_normal = picker.GetPickNormal()

cone_actor_1 = vtkActor()
cone_actor_1.PickableOff()
cone_mapper_1 = vtkDataSetMapper()
cone_mapper_1.SetInputConnection(cone_source.GetOutputPort())
cone_actor_1.SetMapper(cone_mapper_1)
cone_actor_1.GetProperty().SetColor(1, 0, 0)
cone_actor_1.GetProperty().BackfaceCullingOn()
cone_actor_1.SetPosition(pick_position[0], pick_position[1], pick_position[2])
if pick_normal[0] < 0.0:
    cone_actor_1.RotateWXYZ(180, 0, 1, 0)
    cone_actor_1.RotateWXYZ(180, (pick_normal[0] - 1.0) * 0.5, pick_normal[1] * 0.5, pick_normal[2] * 0.5)
else:
    cone_actor_1.RotateWXYZ(180, (pick_normal[0] + 1.0) * 0.5, pick_normal[1] * 0.5, pick_normal[2] * 0.5)
renderer.AddViewProp(cone_actor_1)

# Pick through a cropping plane to some transparent tissue
picker.UseVolumeGradientOpacityOff()
picker.Pick(125, 195, 0, renderer)
pick_position = picker.GetPickPosition()
pick_normal = picker.GetPickNormal()

cone_actor_2 = vtkActor()
cone_actor_2.PickableOff()
cone_mapper_2 = vtkDataSetMapper()
cone_mapper_2.SetInputConnection(cone_source.GetOutputPort())
cone_actor_2.SetMapper(cone_mapper_2)
cone_actor_2.GetProperty().SetColor(1, 0, 0)
cone_actor_2.GetProperty().BackfaceCullingOn()
cone_actor_2.SetPosition(pick_position[0], pick_position[1], pick_position[2])
if pick_normal[0] < 0.0:
    cone_actor_2.RotateWXYZ(180, 0, 1, 0)
    cone_actor_2.RotateWXYZ(180, (pick_normal[0] - 1.0) * 0.5, pick_normal[1] * 0.5, pick_normal[2] * 0.5)
else:
    cone_actor_2.RotateWXYZ(180, (pick_normal[0] + 1.0) * 0.5, pick_normal[1] * 0.5, pick_normal[2] * 0.5)
renderer.AddViewProp(cone_actor_2)

# Pick through a clipping plane
picker.Pick(150, 160, 0, renderer)
pick_position = picker.GetPickPosition()
pick_normal = picker.GetPickNormal()

cone_actor_3 = vtkActor()
cone_actor_3.PickableOff()
cone_mapper_3 = vtkDataSetMapper()
cone_mapper_3.SetInputConnection(cone_source.GetOutputPort())
cone_actor_3.SetMapper(cone_mapper_3)
cone_actor_3.GetProperty().SetColor(1, 0, 0)
cone_actor_3.GetProperty().BackfaceCullingOn()
cone_actor_3.SetPosition(pick_position[0], pick_position[1], pick_position[2])
if pick_normal[0] < 0.0:
    cone_actor_3.RotateWXYZ(180, 0, 1, 0)
    cone_actor_3.RotateWXYZ(180, (pick_normal[0] - 1.0) * 0.5, pick_normal[1] * 0.5, pick_normal[2] * 0.5)
else:
    cone_actor_3.RotateWXYZ(180, (pick_normal[0] + 1.0) * 0.5, pick_normal[1] * 0.5, pick_normal[2] * 0.5)
renderer.AddViewProp(cone_actor_3)

# Pick through a cropping plane with PickCroppingPlanesOn
picker.PickCroppingPlanesOn()
picker.Pick(125, 195, 0, renderer)
pick_position = picker.GetPickPosition()
pick_normal = picker.GetPickNormal()

cone_actor_4 = vtkActor()
cone_actor_4.PickableOff()
cone_mapper_4 = vtkDataSetMapper()
cone_mapper_4.SetInputConnection(cone_source.GetOutputPort())
cone_actor_4.SetMapper(cone_mapper_4)
cone_actor_4.GetProperty().SetColor(0, 1, 0)
cone_actor_4.GetProperty().BackfaceCullingOn()
cone_actor_4.SetPosition(pick_position[0], pick_position[1], pick_position[2])
if pick_normal[0] < 0.0:
    cone_actor_4.RotateWXYZ(180, 0, 1, 0)
    cone_actor_4.RotateWXYZ(180, (pick_normal[0] - 1.0) * 0.5, pick_normal[1] * 0.5, pick_normal[2] * 0.5)
else:
    cone_actor_4.RotateWXYZ(180, (pick_normal[0] + 1.0) * 0.5, pick_normal[1] * 0.5, pick_normal[2] * 0.5)
renderer.AddViewProp(cone_actor_4)

# Pick through a clipping plane with PickCroppingPlanesOn
picker.PickCroppingPlanesOn()
picker.Pick(150, 160, 0, renderer)
pick_position = picker.GetPickPosition()
pick_normal = picker.GetPickNormal()

cone_actor_5 = vtkActor()
cone_actor_5.PickableOff()
cone_mapper_5 = vtkDataSetMapper()
cone_mapper_5.SetInputConnection(cone_source.GetOutputPort())
cone_actor_5.SetMapper(cone_mapper_5)
cone_actor_5.GetProperty().SetColor(0, 1, 0)
cone_actor_5.GetProperty().BackfaceCullingOn()
cone_actor_5.SetPosition(pick_position[0], pick_position[1], pick_position[2])
if pick_normal[0] < 0.0:
    cone_actor_5.RotateWXYZ(180, 0, 1, 0)
    cone_actor_5.RotateWXYZ(180, (pick_normal[0] - 1.0) * 0.5, pick_normal[1] * 0.5, pick_normal[2] * 0.5)
else:
    cone_actor_5.RotateWXYZ(180, (pick_normal[0] + 1.0) * 0.5, pick_normal[1] * 0.5, pick_normal[2] * 0.5)
renderer.AddViewProp(cone_actor_5)

renderer.ResetCameraClippingRange()

interactor.Initialize()
interactor.Start()
