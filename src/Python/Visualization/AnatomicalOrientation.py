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

# Renderer: assemble the scene and configure the camera
renderer = vtkRenderer()
renderer.SetBackground(misty_rose)
renderer.SetBackground2(old_lace)
renderer.GradientBackgroundOn()

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.SetSize(780, 780)
render_window.AddRenderer(renderer)
render_window.SetWindowName("AnatomicalOrientation")

# Interactor: handle mouse and keyboard events
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# --- Annotated cube actor (used by all four orientation widgets) ---
# Inline: build annotated cube with anatomical labels
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

# Inline: build axes actor with given scale and labels
xyz_labels = ["X", "Y", "Z"]
text_scale = [0.04, 0.04, 0.04]

orientation_widgets = []
scales_viewports = [
    ([1.5, -1.5, 1.5], (0.0, 0.8, 0.2, 1.0)),   # RPS — upper left
    ([1.5, 1.5, 1.5], (0.0, 0.0, 0.2, 0.2)),     # RAS — lower left
    ([-1.5, -1.5, 1.5], (0.8, 0.0, 1.0, 0.2)),   # LPS — lower right
]

for scale, viewport in scales_viewports:
    axes = vtkAxesActor()
    axes.SetScale(scale)
    axes.SetShaftTypeToCylinder()
    axes.SetXAxisLabelText(xyz_labels[0])
    axes.SetYAxisLabelText(xyz_labels[1])
    axes.SetZAxisLabelText(xyz_labels[2])
    axes.SetCylinderRadius(0.5 * axes.GetCylinderRadius())
    axes.SetConeRadius(1.025 * axes.GetConeRadius())
    axes.SetSphereRadius(1.5 * axes.GetSphereRadius())
    tprop = axes.GetXAxisCaptionActor2D().GetCaptionTextProperty()
    tprop.ItalicOn()
    tprop.ShadowOn()
    tprop.SetFontFamilyToTimes()
    axes.GetYAxisCaptionActor2D().GetCaptionTextProperty().ShallowCopy(tprop)
    axes.GetZAxisCaptionActor2D().GetCaptionTextProperty().ShallowCopy(tprop)

    cube_copy = vtkAnnotatedCubeActor()
    cube_copy.SetXPlusFaceText("R")
    cube_copy.SetXMinusFaceText("L")
    cube_copy.SetYPlusFaceText("A")
    cube_copy.SetYMinusFaceText("P")
    cube_copy.SetZPlusFaceText("S")
    cube_copy.SetZMinusFaceText("I")
    cube_copy.SetFaceTextScale(0.5)
    cube_copy.GetCubeProperty().SetColor(gainsboro)
    cube_copy.GetTextEdgesProperty().SetColor(light_slate_gray)
    cube_copy.GetXPlusFaceProperty().SetColor(tomato)
    cube_copy.GetXMinusFaceProperty().SetColor(tomato)
    cube_copy.GetYPlusFaceProperty().SetColor(deep_sky_blue)
    cube_copy.GetYMinusFaceProperty().SetColor(deep_sky_blue)
    cube_copy.GetZPlusFaceProperty().SetColor(sea_green)
    cube_copy.GetZMinusFaceProperty().SetColor(sea_green)

    assembly = vtkPropAssembly()
    assembly.AddPart(axes)
    assembly.AddPart(cube_copy)

    om = vtkOrientationMarkerWidget()
    om.SetOrientationMarker(assembly)
    om.SetViewport(viewport)
    om.SetInteractor(interactor)
    om.EnabledOn()
    om.InteractiveOn()
    orientation_widgets.append(om)

# Upper right: annotated cube only (no axes)
om3 = vtkOrientationMarkerWidget()
om3.SetOrientationMarker(cube)
om3.SetViewport(0.8, 0.8, 1.0, 1.0)
om3.SetInteractor(interactor)
om3.EnabledOn()
om3.InteractiveOn()
orientation_widgets.append(om3)

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
renderer.AddActor(human_actor)

# Anatomical planes: transverse (x-y), coronal (x-z), sagittal (y-z)
resolution = [10, 10]
origin = [0.0, 0.0, 0.0]
point1 = [1, 0, 0]
point2 = [0, 1, 0]

plane_params = [
    ([0, 0, 0, 0], [-0.5, -0.5, 0], sea_green),        # Transverse (x-y)
    ([-90, 1, 0, 0], [-0.5, -0.5, 0.0], deep_sky_blue), # Coronal (x-z)
    ([-90, 0, 1, 0], [-0.5, -0.5, 0.0], tomato),        # Sagittal (y-z)
]

for wxyz, translate, color in plane_params:
    plane = vtkPlaneSource()
    plane.SetResolution(*resolution)
    plane.SetOrigin(origin)
    plane.SetPoint1(point1)
    plane.SetPoint2(point2)
    trnf = vtkTransform()
    trnf.RotateWXYZ(*wxyz)
    trnf.Translate(translate)
    tpd = vtkTransformPolyDataFilter()
    tpd.SetTransform(trnf)
    tpd.SetInputConnection(plane.GetOutputPort())
    mapper = vtkPolyDataMapper()
    mapper.SetInputConnection(tpd.GetOutputPort())
    actor = vtkActor()
    actor.SetMapper(mapper)
    actor.GetProperty().SetColor(color)
    renderer.AddViewProp(actor)

# Text labels on the planes
label_defs = [
    ("Transverse\nPlane\n\nSuperior\nCranial", lambda t: t.RotateZ(-90),
     (0.4, 0.49, 0.01)),
    ("Transverse\nPlane\n\nInferior\n(Caudal)", lambda t: (t.RotateZ(270), t.RotateWXYZ(180, 0, 1, 0)),
     (0.4, -0.49, -0.01)),
    ("Sagittal\nPlane\n\nLeft", lambda t: (t.RotateX(90), t.RotateWXYZ(-90, 0, 1, 0)),
     (-0.01, 0.49, 0.4)),
    ("Sagittal\nPlane\n\nRight", lambda t: (t.RotateX(90), t.RotateWXYZ(-270, 0, 1, 0)),
     (0.01, -0.49, 0.4)),
    ("Coronal\nPlane\n\nAnterior", lambda t: (t.RotateY(-180), t.RotateWXYZ(-90, 1, 0, 0)),
     (0.49, 0.01, 0.20)),
    ("Coronal\nPlane\n\nPosterior", lambda t: t.RotateWXYZ(90, 1, 0, 0),
     (-0.49, -0.01, 0.3)),
]

for label_text, transform_fn, position in label_defs:
    vt = vtkVectorText()
    vt.SetText(label_text)
    trnf = vtkTransform()
    transform_fn(trnf)
    tpd = vtkTransformPolyDataFilter()
    tpd.SetTransform(trnf)
    tpd.SetInputConnection(vt.GetOutputPort())
    mapper = vtkPolyDataMapper()
    mapper.SetInputConnection(tpd.GetOutputPort())
    actor = vtkActor()
    actor.SetMapper(mapper)
    actor.SetScale(text_scale)
    actor.AddPosition(position)
    renderer.AddViewProp(actor)

renderer.ResetCamera()
renderer.GetActiveCamera().Zoom(1.6)
renderer.GetActiveCamera().SetPosition(-2.3, 4.1, 4.2)
renderer.GetActiveCamera().SetViewUp(0.0, 0.0, 1.0)
renderer.ResetCameraClippingRange()

# Launch the interactive visualization
interactor.Start()
