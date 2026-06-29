#!/usr/bin/env python

# Show anatomical planes transecting a human figure with annotated orientation markers.

import os
from pathlib import Path

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkCommonTransforms import vtkTransform
from vtkmodules.vtkFiltersGeneral import vtkTransformPolyDataFilter
from vtkmodules.vtkFiltersSources import vtkPlaneSource
from vtkmodules.vtkIOXML import vtkXMLPolyDataReader
from vtkmodules.vtkInteractionWidgets import vtkOrientationMarkerWidget
from vtkmodules.vtkRenderingAnnotation import (
    vtkAnnotatedCubeActor,
    vtkAxesActor,
)
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkPropAssembly,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)
from vtkmodules.vtkRenderingFreeType import vtkVectorText

# Colors (normalized RGB)
gainsboro = (0.863, 0.863, 0.863)
light_slate_gray = (0.467, 0.533, 0.600)
tomato = (1.000, 0.388, 0.278)
deep_sky_blue = (0.000, 0.749, 1.000)
sea_green = (0.180, 0.545, 0.341)
old_lace = (0.992, 0.961, 0.902)
misty_rose = (1.000, 0.894, 0.882)

# Data file
data_dir = Path(os.environ.get("VPE_DATA_DIR", Path(__file__).parent))
file_path = data_dir / "Human.vtp"

text_scale = [0.04, 0.04, 0.04]

# Reader: load the human figure model
reader = vtkXMLPolyDataReader()
reader.SetFileName(str(file_path))
reader.Update()

human_mapper = vtkPolyDataMapper()
human_mapper.SetInputConnection(reader.GetOutputPort())
human_mapper.SetScalarModeToUsePointFieldData()
human_mapper.SelectColorArray("Color")
human_mapper.SetColorModeToDirectScalars()

human_actor = vtkActor()
human_actor.SetMapper(human_mapper)
bounds = human_actor.GetBounds()
human_actor.SetScale(1.0 / max(bounds))

# Transverse plane (x-y)
transverse_plane = vtkPlaneSource()
transverse_plane.SetResolution(10, 10)
transverse_plane.SetOrigin(0.0, 0.0, 0.0)
transverse_plane.SetPoint1(1, 0, 0)
transverse_plane.SetPoint2(0, 1, 0)

transverse_transform = vtkTransform()
transverse_transform.RotateWXYZ(0, 0, 0, 0)
transverse_transform.Translate(-0.5, -0.5, 0)

transverse_tpd = vtkTransformPolyDataFilter()
transverse_tpd.SetTransform(transverse_transform)
transverse_tpd.SetInputConnection(transverse_plane.GetOutputPort())

transverse_mapper = vtkPolyDataMapper()
transverse_mapper.SetInputConnection(transverse_tpd.GetOutputPort())

transverse_actor = vtkActor()
transverse_actor.SetMapper(transverse_mapper)
transverse_actor.GetProperty().SetColor(sea_green)

# Coronal plane (x-z)
coronal_plane = vtkPlaneSource()
coronal_plane.SetResolution(10, 10)
coronal_plane.SetOrigin(0.0, 0.0, 0.0)
coronal_plane.SetPoint1(1, 0, 0)
coronal_plane.SetPoint2(0, 1, 0)

coronal_transform = vtkTransform()
coronal_transform.RotateWXYZ(-90, 1, 0, 0)
coronal_transform.Translate(-0.5, -0.5, 0.0)

coronal_tpd = vtkTransformPolyDataFilter()
coronal_tpd.SetTransform(coronal_transform)
coronal_tpd.SetInputConnection(coronal_plane.GetOutputPort())

coronal_mapper = vtkPolyDataMapper()
coronal_mapper.SetInputConnection(coronal_tpd.GetOutputPort())

coronal_actor = vtkActor()
coronal_actor.SetMapper(coronal_mapper)
coronal_actor.GetProperty().SetColor(deep_sky_blue)

# Sagittal plane (y-z)
sagittal_plane = vtkPlaneSource()
sagittal_plane.SetResolution(10, 10)
sagittal_plane.SetOrigin(0.0, 0.0, 0.0)
sagittal_plane.SetPoint1(1, 0, 0)
sagittal_plane.SetPoint2(0, 1, 0)

sagittal_transform = vtkTransform()
sagittal_transform.RotateWXYZ(-90, 0, 1, 0)
sagittal_transform.Translate(-0.5, -0.5, 0.0)

sagittal_tpd = vtkTransformPolyDataFilter()
sagittal_tpd.SetTransform(sagittal_transform)
sagittal_tpd.SetInputConnection(sagittal_plane.GetOutputPort())

sagittal_mapper = vtkPolyDataMapper()
sagittal_mapper.SetInputConnection(sagittal_tpd.GetOutputPort())

sagittal_actor = vtkActor()
sagittal_actor.SetMapper(sagittal_mapper)
sagittal_actor.GetProperty().SetColor(tomato)

# Label: Transverse Superior Cranial
label_sup_text = vtkVectorText()
label_sup_text.SetText("Transverse\nPlane\n\nSuperior\nCranial")

label_sup_transform = vtkTransform()
label_sup_transform.RotateZ(-90)

label_sup_tpd = vtkTransformPolyDataFilter()
label_sup_tpd.SetTransform(label_sup_transform)
label_sup_tpd.SetInputConnection(label_sup_text.GetOutputPort())

label_sup_mapper = vtkPolyDataMapper()
label_sup_mapper.SetInputConnection(label_sup_tpd.GetOutputPort())

label_sup_actor = vtkActor()
label_sup_actor.SetMapper(label_sup_mapper)
label_sup_actor.SetScale(text_scale)
label_sup_actor.AddPosition(0.4, 0.49, 0.01)

# Label: Transverse Inferior Caudal
label_inf_text = vtkVectorText()
label_inf_text.SetText("Transverse\nPlane\n\nInferior\n(Caudal)")

label_inf_transform = vtkTransform()
label_inf_transform.RotateZ(270)
label_inf_transform.RotateWXYZ(180, 0, 1, 0)

label_inf_tpd = vtkTransformPolyDataFilter()
label_inf_tpd.SetTransform(label_inf_transform)
label_inf_tpd.SetInputConnection(label_inf_text.GetOutputPort())

label_inf_mapper = vtkPolyDataMapper()
label_inf_mapper.SetInputConnection(label_inf_tpd.GetOutputPort())

label_inf_actor = vtkActor()
label_inf_actor.SetMapper(label_inf_mapper)
label_inf_actor.SetScale(text_scale)
label_inf_actor.AddPosition(0.4, -0.49, -0.01)

# Label: Sagittal Left
label_left_text = vtkVectorText()
label_left_text.SetText("Sagittal\nPlane\n\nLeft")

label_left_transform = vtkTransform()
label_left_transform.RotateX(90)
label_left_transform.RotateWXYZ(-90, 0, 1, 0)

label_left_tpd = vtkTransformPolyDataFilter()
label_left_tpd.SetTransform(label_left_transform)
label_left_tpd.SetInputConnection(label_left_text.GetOutputPort())

label_left_mapper = vtkPolyDataMapper()
label_left_mapper.SetInputConnection(label_left_tpd.GetOutputPort())

label_left_actor = vtkActor()
label_left_actor.SetMapper(label_left_mapper)
label_left_actor.SetScale(text_scale)
label_left_actor.AddPosition(-0.01, 0.49, 0.4)

# Label: Sagittal Right
label_right_text = vtkVectorText()
label_right_text.SetText("Sagittal\nPlane\n\nRight")

label_right_transform = vtkTransform()
label_right_transform.RotateX(90)
label_right_transform.RotateWXYZ(-270, 0, 1, 0)

label_right_tpd = vtkTransformPolyDataFilter()
label_right_tpd.SetTransform(label_right_transform)
label_right_tpd.SetInputConnection(label_right_text.GetOutputPort())

label_right_mapper = vtkPolyDataMapper()
label_right_mapper.SetInputConnection(label_right_tpd.GetOutputPort())

label_right_actor = vtkActor()
label_right_actor.SetMapper(label_right_mapper)
label_right_actor.SetScale(text_scale)
label_right_actor.AddPosition(0.01, -0.49, 0.4)

# Label: Coronal Anterior
label_ant_text = vtkVectorText()
label_ant_text.SetText("Coronal\nPlane\n\nAnterior")

label_ant_transform = vtkTransform()
label_ant_transform.RotateY(-180)
label_ant_transform.RotateWXYZ(-90, 1, 0, 0)

label_ant_tpd = vtkTransformPolyDataFilter()
label_ant_tpd.SetTransform(label_ant_transform)
label_ant_tpd.SetInputConnection(label_ant_text.GetOutputPort())

label_ant_mapper = vtkPolyDataMapper()
label_ant_mapper.SetInputConnection(label_ant_tpd.GetOutputPort())

label_ant_actor = vtkActor()
label_ant_actor.SetMapper(label_ant_mapper)
label_ant_actor.SetScale(text_scale)
label_ant_actor.AddPosition(0.49, 0.01, 0.20)

# Label: Coronal Posterior
label_post_text = vtkVectorText()
label_post_text.SetText("Coronal\nPlane\n\nPosterior")

label_post_transform = vtkTransform()
label_post_transform.RotateWXYZ(90, 1, 0, 0)

label_post_tpd = vtkTransformPolyDataFilter()
label_post_tpd.SetTransform(label_post_transform)
label_post_tpd.SetInputConnection(label_post_text.GetOutputPort())

label_post_mapper = vtkPolyDataMapper()
label_post_mapper.SetInputConnection(label_post_tpd.GetOutputPort())

label_post_actor = vtkActor()
label_post_actor.SetMapper(label_post_mapper)
label_post_actor.SetScale(text_scale)
label_post_actor.AddPosition(-0.49, -0.01, 0.3)

# Annotated cube actor (used by upper-right widget)
cube = vtkAnnotatedCubeActor()
cube.SetXPlusFaceText("R")
cube.SetXMinusFaceText("L")
cube.SetYPlusFaceText("A")
cube.SetYMinusFaceText("P")
cube.SetZPlusFaceText("S")
cube.SetZMinusFaceText("I")
cube.SetFaceTextScale(0.5)
cube.GetCubeProperty().SetColor(gainsboro)
cube.GetTextEdgesProperty().SetColor(light_slate_gray)
cube.GetXPlusFaceProperty().SetColor(tomato)
cube.GetXMinusFaceProperty().SetColor(tomato)
cube.GetYPlusFaceProperty().SetColor(deep_sky_blue)
cube.GetYMinusFaceProperty().SetColor(deep_sky_blue)
cube.GetZPlusFaceProperty().SetColor(sea_green)
cube.GetZMinusFaceProperty().SetColor(sea_green)

# Orientation widget 0: RPS axes+cube assembly (upper left)
axes_0 = vtkAxesActor()
axes_0.SetScale(1.5, -1.5, 1.5)
axes_0.SetShaftTypeToCylinder()
axes_0.SetXAxisLabelText("X")
axes_0.SetYAxisLabelText("Y")
axes_0.SetZAxisLabelText("Z")
axes_0.SetCylinderRadius(0.5 * axes_0.GetCylinderRadius())
axes_0.SetConeRadius(1.025 * axes_0.GetConeRadius())
axes_0.SetSphereRadius(1.5 * axes_0.GetSphereRadius())
tprop_0 = axes_0.GetXAxisCaptionActor2D().GetCaptionTextProperty()
tprop_0.ItalicOn()
tprop_0.ShadowOn()
tprop_0.SetFontFamilyToTimes()
axes_0.GetYAxisCaptionActor2D().GetCaptionTextProperty().ShallowCopy(tprop_0)
axes_0.GetZAxisCaptionActor2D().GetCaptionTextProperty().ShallowCopy(tprop_0)

cube_0 = vtkAnnotatedCubeActor()
cube_0.SetXPlusFaceText("R")
cube_0.SetXMinusFaceText("L")
cube_0.SetYPlusFaceText("A")
cube_0.SetYMinusFaceText("P")
cube_0.SetZPlusFaceText("S")
cube_0.SetZMinusFaceText("I")
cube_0.SetFaceTextScale(0.5)
cube_0.GetCubeProperty().SetColor(gainsboro)
cube_0.GetTextEdgesProperty().SetColor(light_slate_gray)
cube_0.GetXPlusFaceProperty().SetColor(tomato)
cube_0.GetXMinusFaceProperty().SetColor(tomato)
cube_0.GetYPlusFaceProperty().SetColor(deep_sky_blue)
cube_0.GetYMinusFaceProperty().SetColor(deep_sky_blue)
cube_0.GetZPlusFaceProperty().SetColor(sea_green)
cube_0.GetZMinusFaceProperty().SetColor(sea_green)

assembly_0 = vtkPropAssembly()
assembly_0.AddPart(axes_0)
assembly_0.AddPart(cube_0)

# Orientation widget 1: RAS axes+cube assembly (lower left)
axes_1 = vtkAxesActor()
axes_1.SetScale(1.5, 1.5, 1.5)
axes_1.SetShaftTypeToCylinder()
axes_1.SetXAxisLabelText("X")
axes_1.SetYAxisLabelText("Y")
axes_1.SetZAxisLabelText("Z")
axes_1.SetCylinderRadius(0.5 * axes_1.GetCylinderRadius())
axes_1.SetConeRadius(1.025 * axes_1.GetConeRadius())
axes_1.SetSphereRadius(1.5 * axes_1.GetSphereRadius())
tprop_1 = axes_1.GetXAxisCaptionActor2D().GetCaptionTextProperty()
tprop_1.ItalicOn()
tprop_1.ShadowOn()
tprop_1.SetFontFamilyToTimes()
axes_1.GetYAxisCaptionActor2D().GetCaptionTextProperty().ShallowCopy(tprop_1)
axes_1.GetZAxisCaptionActor2D().GetCaptionTextProperty().ShallowCopy(tprop_1)

cube_1 = vtkAnnotatedCubeActor()
cube_1.SetXPlusFaceText("R")
cube_1.SetXMinusFaceText("L")
cube_1.SetYPlusFaceText("A")
cube_1.SetYMinusFaceText("P")
cube_1.SetZPlusFaceText("S")
cube_1.SetZMinusFaceText("I")
cube_1.SetFaceTextScale(0.5)
cube_1.GetCubeProperty().SetColor(gainsboro)
cube_1.GetTextEdgesProperty().SetColor(light_slate_gray)
cube_1.GetXPlusFaceProperty().SetColor(tomato)
cube_1.GetXMinusFaceProperty().SetColor(tomato)
cube_1.GetYPlusFaceProperty().SetColor(deep_sky_blue)
cube_1.GetYMinusFaceProperty().SetColor(deep_sky_blue)
cube_1.GetZPlusFaceProperty().SetColor(sea_green)
cube_1.GetZMinusFaceProperty().SetColor(sea_green)

assembly_1 = vtkPropAssembly()
assembly_1.AddPart(axes_1)
assembly_1.AddPart(cube_1)

# Orientation widget 2: LPS axes+cube assembly (lower right)
axes_2 = vtkAxesActor()
axes_2.SetScale(-1.5, -1.5, 1.5)
axes_2.SetShaftTypeToCylinder()
axes_2.SetXAxisLabelText("X")
axes_2.SetYAxisLabelText("Y")
axes_2.SetZAxisLabelText("Z")
axes_2.SetCylinderRadius(0.5 * axes_2.GetCylinderRadius())
axes_2.SetConeRadius(1.025 * axes_2.GetConeRadius())
axes_2.SetSphereRadius(1.5 * axes_2.GetSphereRadius())
tprop_2 = axes_2.GetXAxisCaptionActor2D().GetCaptionTextProperty()
tprop_2.ItalicOn()
tprop_2.ShadowOn()
tprop_2.SetFontFamilyToTimes()
axes_2.GetYAxisCaptionActor2D().GetCaptionTextProperty().ShallowCopy(tprop_2)
axes_2.GetZAxisCaptionActor2D().GetCaptionTextProperty().ShallowCopy(tprop_2)

cube_2 = vtkAnnotatedCubeActor()
cube_2.SetXPlusFaceText("R")
cube_2.SetXMinusFaceText("L")
cube_2.SetYPlusFaceText("A")
cube_2.SetYMinusFaceText("P")
cube_2.SetZPlusFaceText("S")
cube_2.SetZMinusFaceText("I")
cube_2.SetFaceTextScale(0.5)
cube_2.GetCubeProperty().SetColor(gainsboro)
cube_2.GetTextEdgesProperty().SetColor(light_slate_gray)
cube_2.GetXPlusFaceProperty().SetColor(tomato)
cube_2.GetXMinusFaceProperty().SetColor(tomato)
cube_2.GetYPlusFaceProperty().SetColor(deep_sky_blue)
cube_2.GetYMinusFaceProperty().SetColor(deep_sky_blue)
cube_2.GetZPlusFaceProperty().SetColor(sea_green)
cube_2.GetZMinusFaceProperty().SetColor(sea_green)

assembly_2 = vtkPropAssembly()
assembly_2.AddPart(axes_2)
assembly_2.AddPart(cube_2)

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.AddActor(human_actor)
renderer.AddViewProp(transverse_actor)
renderer.AddViewProp(coronal_actor)
renderer.AddViewProp(sagittal_actor)
renderer.AddViewProp(label_sup_actor)
renderer.AddViewProp(label_inf_actor)
renderer.AddViewProp(label_left_actor)
renderer.AddViewProp(label_right_actor)
renderer.AddViewProp(label_ant_actor)
renderer.AddViewProp(label_post_actor)
renderer.SetBackground(misty_rose)
renderer.SetBackground2(old_lace)
renderer.GradientBackgroundOn()

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("anatomical orientation")
render_window.SetMultiSamples(0)
render_window.SetSize(780, 780)

# Scene: camera configuration
renderer.ResetCamera()
renderer.GetActiveCamera().Zoom(1.6)
renderer.GetActiveCamera().SetPosition(-2.3, 4.1, 4.2)
renderer.GetActiveCamera().SetViewUp(0.0, 0.0, 1.0)
renderer.ResetCameraClippingRange()

# Interactor: handle mouse and keyboard events
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene: orientation marker widgets
om_0 = vtkOrientationMarkerWidget()
om_0.SetOrientationMarker(assembly_0)
om_0.SetViewport(0.0, 0.8, 0.2, 1.0)
om_0.SetInteractor(interactor)
om_0.EnabledOn()
om_0.InteractiveOn()

om_1 = vtkOrientationMarkerWidget()
om_1.SetOrientationMarker(assembly_1)
om_1.SetViewport(0.0, 0.0, 0.2, 0.2)
om_1.SetInteractor(interactor)
om_1.EnabledOn()
om_1.InteractiveOn()

om_2 = vtkOrientationMarkerWidget()
om_2.SetOrientationMarker(assembly_2)
om_2.SetViewport(0.8, 0.0, 1.0, 0.2)
om_2.SetInteractor(interactor)
om_2.EnabledOn()
om_2.InteractiveOn()

om_3 = vtkOrientationMarkerWidget()
om_3.SetOrientationMarker(cube)
om_3.SetViewport(0.8, 0.8, 1.0, 1.0)
om_3.SetInteractor(interactor)
om_3.EnabledOn()
om_3.InteractiveOn()

# Launch the interactive visualization
interactor.Initialize()
interactor.Start()
