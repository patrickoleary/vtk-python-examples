#!/usr/bin/env python

# View preprocessed VTK tissue surfaces of a segmented frog dataset.

import json
import os
from pathlib import Path

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkCommonColor import vtkNamedColors
from vtkmodules.vtkCommonCore import (
    vtkCommand,
    vtkLookupTable,
)
from vtkmodules.vtkCommonMath import vtkMatrix4x4
from vtkmodules.vtkCommonTransforms import vtkTransform
from vtkmodules.vtkFiltersCore import vtkPolyDataNormals
from vtkmodules.vtkFiltersGeneral import vtkTransformPolyDataFilter
from vtkmodules.vtkIOLegacy import vtkPolyDataReader
from vtkmodules.vtkInteractionStyle import vtkInteractorStyleTrackballCamera
from vtkmodules.vtkInteractionWidgets import (
    vtkCameraOrientationWidget,
    vtkSliderRepresentation2D,
    vtkSliderWidget,
)
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
paraview_bkg_rgb = (0.322, 0.341, 0.431)
black_rgb = (0.0, 0.0, 0.0)
indigo_rgb = (0.294, 0.0, 0.510)
burlywood_rgb = (0.871, 0.722, 0.529)
lime_rgb = (0.0, 1.0, 0.0)
dark_slate_gray_rgb = (0.184, 0.310, 0.310)
colors = vtkNamedColors()

# Data: locate the JSON configuration file for VTK tissue files
data_dir = Path(os.environ.get("VPE_DATA_DIR", Path(__file__).parent))
json_file = data_dir / "Frog_vtk.json"

# SliceOrder: orientation transforms keyed by acquisition order name
si_mat = vtkMatrix4x4()
si_mat.Zero()
si_mat.SetElement(0, 0, 1)
si_mat.SetElement(1, 2, 1)
si_mat.SetElement(2, 1, -1)
si_mat.SetElement(3, 3, 1)

is_mat = vtkMatrix4x4()
is_mat.Zero()
is_mat.SetElement(0, 0, 1)
is_mat.SetElement(1, 2, -1)
is_mat.SetElement(2, 1, -1)
is_mat.SetElement(3, 3, 1)

lr_mat = vtkMatrix4x4()
lr_mat.Zero()
lr_mat.SetElement(0, 2, -1)
lr_mat.SetElement(1, 1, -1)
lr_mat.SetElement(2, 0, 1)
lr_mat.SetElement(3, 3, 1)

rl_mat = vtkMatrix4x4()
rl_mat.Zero()
rl_mat.SetElement(0, 2, 1)
rl_mat.SetElement(1, 1, -1)
rl_mat.SetElement(2, 0, 1)
rl_mat.SetElement(3, 3, 1)

hf_mat = vtkMatrix4x4()
hf_mat.Zero()
hf_mat.SetElement(0, 0, -1)
hf_mat.SetElement(1, 1, 1)
hf_mat.SetElement(2, 2, -1)
hf_mat.SetElement(3, 3, 1)

slice_transforms = {}

si_t = vtkTransform()
si_t.SetMatrix(si_mat)
slice_transforms["si"] = si_t

is_t = vtkTransform()
is_t.SetMatrix(is_mat)
slice_transforms["is"] = is_t

ap_t = vtkTransform()
ap_t.Scale(1, -1, 1)
slice_transforms["ap"] = ap_t

pa_t = vtkTransform()
pa_t.Scale(1, -1, -1)
slice_transforms["pa"] = pa_t

lr_t = vtkTransform()
lr_t.SetMatrix(lr_mat)
slice_transforms["lr"] = lr_t

rl_t = vtkTransform()
rl_t.SetMatrix(rl_mat)
slice_transforms["rl"] = rl_t

hf_t = vtkTransform()
hf_t.SetMatrix(hf_mat)
slice_transforms["hf"] = hf_t

hfsi_t = vtkTransform()
hfsi_t.SetMatrix(hf_mat)
hfsi_t.Concatenate(si_mat)
slice_transforms["hfsi"] = hfsi_t

hfis_t = vtkTransform()
hfis_t.SetMatrix(hf_mat)
hfis_t.Concatenate(is_mat)
slice_transforms["hfis"] = hfis_t

hfap_t = vtkTransform()
hfap_t.SetMatrix(hf_mat)
hfap_t.Scale(1, -1, 1)
slice_transforms["hfap"] = hfap_t

hfpa_t = vtkTransform()
hfpa_t.SetMatrix(hf_mat)
hfpa_t.Scale(1, -1, -1)
slice_transforms["hfpa"] = hfpa_t

hflr_t = vtkTransform()
hflr_t.SetMatrix(hf_mat)
hflr_t.Concatenate(lr_mat)
slice_transforms["hflr"] = hflr_t

hfrl_t = vtkTransform()
hfrl_t.SetMatrix(hf_mat)
hfrl_t.Concatenate(rl_mat)
slice_transforms["hfrl"] = hfrl_t

slice_transforms["I"] = vtkTransform()

z_t = vtkTransform()
z_t.Scale(0, 0, 0)
slice_transforms["Z"] = z_t

# Parse the JSON configuration file
with open(json_file) as f:
    json_data = json.load(f)

# Resolve VTK file paths relative to the JSON file location
root = data_dir / json_data["files"]["root"]
vtk_files = {}
for p in json_data["files"]["vtk_files"]:
    fp = root / p
    vtk_files[fp.stem] = str(fp)

# Extract tissue metadata from JSON
tissue_colors = json_data["tissues"]["colors"]
tissue_indices = json_data["tissues"]["indices"]
tissue_names = json_data["tissues"]["names"]
tissue_opacity = json_data["tissues"]["opacity"]
tissue_orientation = json_data["tissues"]["orientation"]

# LookupTable: tissue label to color
color_lut = vtkLookupTable()
color_lut.SetNumberOfColors(len(tissue_colors))
color_lut.SetTableRange(0, len(tissue_colors) - 1)
color_lut.Build()
for name in tissue_names:
    color_lut.SetTableValue(tissue_indices[name], colors.GetColor4d(tissue_colors[name]))

# --- Tissue 0: skin ---
skin_reader = vtkPolyDataReader()
skin_reader.SetFileName(vtk_files["skin"])
skin_reader.Update()

skin_trans = vtkTransform()
skin_trans.DeepCopy(slice_transforms[tissue_orientation["skin"]])
skin_trans.Scale(1, -1, -1)

skin_tf = vtkTransformPolyDataFilter()
skin_tf.SetInputConnection(skin_reader.GetOutputPort())
skin_tf.SetTransform(skin_trans)

skin_normals = vtkPolyDataNormals()
skin_normals.SetInputConnection(skin_tf.GetOutputPort())
skin_normals.SetFeatureAngle(60.0)

skin_mapper = vtkPolyDataMapper()
skin_mapper.SetInputConnection(skin_normals.GetOutputPort())

skin_actor = vtkActor()
skin_actor.SetMapper(skin_mapper)
skin_actor.GetProperty().SetOpacity(tissue_opacity["skin"])
skin_actor.GetProperty().SetDiffuseColor(color_lut.GetTableValue(tissue_indices["skin"])[:3])
skin_actor.GetProperty().SetSpecular(0.2)
skin_actor.GetProperty().SetSpecularPower(10)

skin_slider_rep = vtkSliderRepresentation2D()
skin_slider_rep.SetMinimumValue(0.0)
skin_slider_rep.SetMaximumValue(1.0)
skin_slider_rep.SetValue(tissue_opacity["skin"])
skin_slider_rep.SetTitleText("skin")
skin_slider_rep.SetTubeWidth(0.004)
skin_slider_rep.SetSliderLength(0.015)
skin_slider_rep.SetSliderWidth(0.008)
skin_slider_rep.SetEndCapLength(0.008)
skin_slider_rep.SetEndCapWidth(0.02)
skin_slider_rep.SetTitleHeight(0.02)
skin_slider_rep.SetLabelHeight(0.02)
skin_slider_rep.GetPoint1Coordinate().SetCoordinateSystemToNormalizedDisplay()
skin_slider_rep.GetPoint1Coordinate().SetValue(0.02, 0.275)
skin_slider_rep.GetPoint2Coordinate().SetCoordinateSystemToNormalizedDisplay()
skin_slider_rep.GetPoint2Coordinate().SetValue(0.18, 0.275)
skin_slider_rep.GetTubeProperty().SetColor(black_rgb)
skin_slider_rep.GetCapProperty().SetColor(indigo_rgb)
skin_slider_rep.GetSliderProperty().SetColor(burlywood_rgb)
skin_slider_rep.GetSelectedProperty().SetColor(lime_rgb)
skin_slider_rep.GetLabelProperty().SetColor(dark_slate_gray_rgb)
skin_slider_rep.GetTitleProperty().SetColor(color_lut.GetTableValue(tissue_indices["skin"])[:3])
skin_slider_rep.GetTitleProperty().ShadowOff()

skin_sw = vtkSliderWidget()
skin_sw.SetRepresentation(skin_slider_rep)
skin_sw.SetAnimationModeToAnimate()
skin_sw.AddObserver(vtkCommand.InteractionEvent,
                    lambda caller, ev, prop=skin_actor.GetProperty(): prop.SetOpacity(
                        caller.GetRepresentation().GetValue()))

# --- Tissue 1: blood ---
blood_reader = vtkPolyDataReader()
blood_reader.SetFileName(vtk_files["blood"])
blood_reader.Update()

blood_trans = vtkTransform()
blood_trans.DeepCopy(slice_transforms[tissue_orientation["blood"]])
blood_trans.Scale(1, -1, -1)

blood_tf = vtkTransformPolyDataFilter()
blood_tf.SetInputConnection(blood_reader.GetOutputPort())
blood_tf.SetTransform(blood_trans)

blood_normals = vtkPolyDataNormals()
blood_normals.SetInputConnection(blood_tf.GetOutputPort())
blood_normals.SetFeatureAngle(60.0)

blood_mapper = vtkPolyDataMapper()
blood_mapper.SetInputConnection(blood_normals.GetOutputPort())

blood_actor = vtkActor()
blood_actor.SetMapper(blood_mapper)
blood_actor.GetProperty().SetOpacity(tissue_opacity["blood"])
blood_actor.GetProperty().SetDiffuseColor(color_lut.GetTableValue(tissue_indices["blood"])[:3])
blood_actor.GetProperty().SetSpecular(0.2)
blood_actor.GetProperty().SetSpecularPower(10)

blood_slider_rep = vtkSliderRepresentation2D()
blood_slider_rep.SetMinimumValue(0.0)
blood_slider_rep.SetMaximumValue(1.0)
blood_slider_rep.SetValue(tissue_opacity["blood"])
blood_slider_rep.SetTitleText("blood")
blood_slider_rep.SetTubeWidth(0.004)
blood_slider_rep.SetSliderLength(0.015)
blood_slider_rep.SetSliderWidth(0.008)
blood_slider_rep.SetEndCapLength(0.008)
blood_slider_rep.SetEndCapWidth(0.02)
blood_slider_rep.SetTitleHeight(0.02)
blood_slider_rep.SetLabelHeight(0.02)
blood_slider_rep.GetPoint1Coordinate().SetCoordinateSystemToNormalizedDisplay()
blood_slider_rep.GetPoint1Coordinate().SetValue(0.02, 0.275 + 1.0 / 9)
blood_slider_rep.GetPoint2Coordinate().SetCoordinateSystemToNormalizedDisplay()
blood_slider_rep.GetPoint2Coordinate().SetValue(0.18, 0.275 + 1.0 / 9)
blood_slider_rep.GetTubeProperty().SetColor(black_rgb)
blood_slider_rep.GetCapProperty().SetColor(indigo_rgb)
blood_slider_rep.GetSliderProperty().SetColor(burlywood_rgb)
blood_slider_rep.GetSelectedProperty().SetColor(lime_rgb)
blood_slider_rep.GetLabelProperty().SetColor(dark_slate_gray_rgb)
blood_slider_rep.GetTitleProperty().SetColor(color_lut.GetTableValue(tissue_indices["blood"])[:3])
blood_slider_rep.GetTitleProperty().ShadowOff()

blood_sw = vtkSliderWidget()
blood_sw.SetRepresentation(blood_slider_rep)
blood_sw.SetAnimationModeToAnimate()
blood_sw.AddObserver(vtkCommand.InteractionEvent,
                     lambda caller, ev, prop=blood_actor.GetProperty(): prop.SetOpacity(
                         caller.GetRepresentation().GetValue()))

# --- Tissue 2: brain ---
brain_reader = vtkPolyDataReader()
brain_reader.SetFileName(vtk_files["brain"])
brain_reader.Update()

brain_trans = vtkTransform()
brain_trans.DeepCopy(slice_transforms[tissue_orientation["brain"]])
brain_trans.Scale(1, -1, -1)

brain_tf = vtkTransformPolyDataFilter()
brain_tf.SetInputConnection(brain_reader.GetOutputPort())
brain_tf.SetTransform(brain_trans)

brain_normals = vtkPolyDataNormals()
brain_normals.SetInputConnection(brain_tf.GetOutputPort())
brain_normals.SetFeatureAngle(60.0)

brain_mapper = vtkPolyDataMapper()
brain_mapper.SetInputConnection(brain_normals.GetOutputPort())

brain_actor = vtkActor()
brain_actor.SetMapper(brain_mapper)
brain_actor.GetProperty().SetOpacity(tissue_opacity["brain"])
brain_actor.GetProperty().SetDiffuseColor(color_lut.GetTableValue(tissue_indices["brain"])[:3])
brain_actor.GetProperty().SetSpecular(0.2)
brain_actor.GetProperty().SetSpecularPower(10)

brain_slider_rep = vtkSliderRepresentation2D()
brain_slider_rep.SetMinimumValue(0.0)
brain_slider_rep.SetMaximumValue(1.0)
brain_slider_rep.SetValue(tissue_opacity["brain"])
brain_slider_rep.SetTitleText("brain")
brain_slider_rep.SetTubeWidth(0.004)
brain_slider_rep.SetSliderLength(0.015)
brain_slider_rep.SetSliderWidth(0.008)
brain_slider_rep.SetEndCapLength(0.008)
brain_slider_rep.SetEndCapWidth(0.02)
brain_slider_rep.SetTitleHeight(0.02)
brain_slider_rep.SetLabelHeight(0.02)
brain_slider_rep.GetPoint1Coordinate().SetCoordinateSystemToNormalizedDisplay()
brain_slider_rep.GetPoint1Coordinate().SetValue(0.02, 0.275 + 2.0 / 9)
brain_slider_rep.GetPoint2Coordinate().SetCoordinateSystemToNormalizedDisplay()
brain_slider_rep.GetPoint2Coordinate().SetValue(0.18, 0.275 + 2.0 / 9)
brain_slider_rep.GetTubeProperty().SetColor(black_rgb)
brain_slider_rep.GetCapProperty().SetColor(indigo_rgb)
brain_slider_rep.GetSliderProperty().SetColor(burlywood_rgb)
brain_slider_rep.GetSelectedProperty().SetColor(lime_rgb)
brain_slider_rep.GetLabelProperty().SetColor(dark_slate_gray_rgb)
brain_slider_rep.GetTitleProperty().SetColor(color_lut.GetTableValue(tissue_indices["brain"])[:3])
brain_slider_rep.GetTitleProperty().ShadowOff()

brain_sw = vtkSliderWidget()
brain_sw.SetRepresentation(brain_slider_rep)
brain_sw.SetAnimationModeToAnimate()
brain_sw.AddObserver(vtkCommand.InteractionEvent,
                     lambda caller, ev, prop=brain_actor.GetProperty(): prop.SetOpacity(
                         caller.GetRepresentation().GetValue()))

# --- Tissue 3: duodenum ---
duodenum_reader = vtkPolyDataReader()
duodenum_reader.SetFileName(vtk_files["duodenum"])
duodenum_reader.Update()

duodenum_trans = vtkTransform()
duodenum_trans.DeepCopy(slice_transforms[tissue_orientation["duodenum"]])
duodenum_trans.Scale(1, -1, -1)

duodenum_tf = vtkTransformPolyDataFilter()
duodenum_tf.SetInputConnection(duodenum_reader.GetOutputPort())
duodenum_tf.SetTransform(duodenum_trans)

duodenum_normals = vtkPolyDataNormals()
duodenum_normals.SetInputConnection(duodenum_tf.GetOutputPort())
duodenum_normals.SetFeatureAngle(60.0)

duodenum_mapper = vtkPolyDataMapper()
duodenum_mapper.SetInputConnection(duodenum_normals.GetOutputPort())

duodenum_actor = vtkActor()
duodenum_actor.SetMapper(duodenum_mapper)
duodenum_actor.GetProperty().SetOpacity(tissue_opacity["duodenum"])
duodenum_actor.GetProperty().SetDiffuseColor(color_lut.GetTableValue(tissue_indices["duodenum"])[:3])
duodenum_actor.GetProperty().SetSpecular(0.2)
duodenum_actor.GetProperty().SetSpecularPower(10)

duodenum_slider_rep = vtkSliderRepresentation2D()
duodenum_slider_rep.SetMinimumValue(0.0)
duodenum_slider_rep.SetMaximumValue(1.0)
duodenum_slider_rep.SetValue(tissue_opacity["duodenum"])
duodenum_slider_rep.SetTitleText("duodenum")
duodenum_slider_rep.SetTubeWidth(0.004)
duodenum_slider_rep.SetSliderLength(0.015)
duodenum_slider_rep.SetSliderWidth(0.008)
duodenum_slider_rep.SetEndCapLength(0.008)
duodenum_slider_rep.SetEndCapWidth(0.02)
duodenum_slider_rep.SetTitleHeight(0.02)
duodenum_slider_rep.SetLabelHeight(0.02)
duodenum_slider_rep.GetPoint1Coordinate().SetCoordinateSystemToNormalizedDisplay()
duodenum_slider_rep.GetPoint1Coordinate().SetValue(0.02, 0.275 + 3.0 / 9)
duodenum_slider_rep.GetPoint2Coordinate().SetCoordinateSystemToNormalizedDisplay()
duodenum_slider_rep.GetPoint2Coordinate().SetValue(0.18, 0.275 + 3.0 / 9)
duodenum_slider_rep.GetTubeProperty().SetColor(black_rgb)
duodenum_slider_rep.GetCapProperty().SetColor(indigo_rgb)
duodenum_slider_rep.GetSliderProperty().SetColor(burlywood_rgb)
duodenum_slider_rep.GetSelectedProperty().SetColor(lime_rgb)
duodenum_slider_rep.GetLabelProperty().SetColor(dark_slate_gray_rgb)
duodenum_slider_rep.GetTitleProperty().SetColor(color_lut.GetTableValue(tissue_indices["duodenum"])[:3])
duodenum_slider_rep.GetTitleProperty().ShadowOff()

duodenum_sw = vtkSliderWidget()
duodenum_sw.SetRepresentation(duodenum_slider_rep)
duodenum_sw.SetAnimationModeToAnimate()
duodenum_sw.AddObserver(vtkCommand.InteractionEvent,
                        lambda caller, ev, prop=duodenum_actor.GetProperty(): prop.SetOpacity(
                            caller.GetRepresentation().GetValue()))

# --- Tissue 4: eye_retna ---
eye_retna_reader = vtkPolyDataReader()
eye_retna_reader.SetFileName(vtk_files["eye_retna"])
eye_retna_reader.Update()

eye_retna_trans = vtkTransform()
eye_retna_trans.DeepCopy(slice_transforms[tissue_orientation["eye_retna"]])
eye_retna_trans.Scale(1, -1, -1)

eye_retna_tf = vtkTransformPolyDataFilter()
eye_retna_tf.SetInputConnection(eye_retna_reader.GetOutputPort())
eye_retna_tf.SetTransform(eye_retna_trans)

eye_retna_normals = vtkPolyDataNormals()
eye_retna_normals.SetInputConnection(eye_retna_tf.GetOutputPort())
eye_retna_normals.SetFeatureAngle(60.0)

eye_retna_mapper = vtkPolyDataMapper()
eye_retna_mapper.SetInputConnection(eye_retna_normals.GetOutputPort())

eye_retna_actor = vtkActor()
eye_retna_actor.SetMapper(eye_retna_mapper)
eye_retna_actor.GetProperty().SetOpacity(tissue_opacity["eye_retna"])
eye_retna_actor.GetProperty().SetDiffuseColor(color_lut.GetTableValue(tissue_indices["eye_retna"])[:3])
eye_retna_actor.GetProperty().SetSpecular(0.2)
eye_retna_actor.GetProperty().SetSpecularPower(10)

eye_retna_slider_rep = vtkSliderRepresentation2D()
eye_retna_slider_rep.SetMinimumValue(0.0)
eye_retna_slider_rep.SetMaximumValue(1.0)
eye_retna_slider_rep.SetValue(tissue_opacity["eye_retna"])
eye_retna_slider_rep.SetTitleText("eye_retna")
eye_retna_slider_rep.SetTubeWidth(0.004)
eye_retna_slider_rep.SetSliderLength(0.015)
eye_retna_slider_rep.SetSliderWidth(0.008)
eye_retna_slider_rep.SetEndCapLength(0.008)
eye_retna_slider_rep.SetEndCapWidth(0.02)
eye_retna_slider_rep.SetTitleHeight(0.02)
eye_retna_slider_rep.SetLabelHeight(0.02)
eye_retna_slider_rep.GetPoint1Coordinate().SetCoordinateSystemToNormalizedDisplay()
eye_retna_slider_rep.GetPoint1Coordinate().SetValue(0.02, 0.275 + 4.0 / 9)
eye_retna_slider_rep.GetPoint2Coordinate().SetCoordinateSystemToNormalizedDisplay()
eye_retna_slider_rep.GetPoint2Coordinate().SetValue(0.18, 0.275 + 4.0 / 9)
eye_retna_slider_rep.GetTubeProperty().SetColor(black_rgb)
eye_retna_slider_rep.GetCapProperty().SetColor(indigo_rgb)
eye_retna_slider_rep.GetSliderProperty().SetColor(burlywood_rgb)
eye_retna_slider_rep.GetSelectedProperty().SetColor(lime_rgb)
eye_retna_slider_rep.GetLabelProperty().SetColor(dark_slate_gray_rgb)
eye_retna_slider_rep.GetTitleProperty().SetColor(color_lut.GetTableValue(tissue_indices["eye_retna"])[:3])
eye_retna_slider_rep.GetTitleProperty().ShadowOff()

eye_retna_sw = vtkSliderWidget()
eye_retna_sw.SetRepresentation(eye_retna_slider_rep)
eye_retna_sw.SetAnimationModeToAnimate()
eye_retna_sw.AddObserver(vtkCommand.InteractionEvent,
                         lambda caller, ev, prop=eye_retna_actor.GetProperty(): prop.SetOpacity(
                             caller.GetRepresentation().GetValue()))

# --- Tissue 5: eye_white ---
eye_white_reader = vtkPolyDataReader()
eye_white_reader.SetFileName(vtk_files["eye_white"])
eye_white_reader.Update()

eye_white_trans = vtkTransform()
eye_white_trans.DeepCopy(slice_transforms[tissue_orientation["eye_white"]])
eye_white_trans.Scale(1, -1, -1)

eye_white_tf = vtkTransformPolyDataFilter()
eye_white_tf.SetInputConnection(eye_white_reader.GetOutputPort())
eye_white_tf.SetTransform(eye_white_trans)

eye_white_normals = vtkPolyDataNormals()
eye_white_normals.SetInputConnection(eye_white_tf.GetOutputPort())
eye_white_normals.SetFeatureAngle(60.0)

eye_white_mapper = vtkPolyDataMapper()
eye_white_mapper.SetInputConnection(eye_white_normals.GetOutputPort())

eye_white_actor = vtkActor()
eye_white_actor.SetMapper(eye_white_mapper)
eye_white_actor.GetProperty().SetOpacity(tissue_opacity["eye_white"])
eye_white_actor.GetProperty().SetDiffuseColor(color_lut.GetTableValue(tissue_indices["eye_white"])[:3])
eye_white_actor.GetProperty().SetSpecular(0.2)
eye_white_actor.GetProperty().SetSpecularPower(10)

eye_white_slider_rep = vtkSliderRepresentation2D()
eye_white_slider_rep.SetMinimumValue(0.0)
eye_white_slider_rep.SetMaximumValue(1.0)
eye_white_slider_rep.SetValue(tissue_opacity["eye_white"])
eye_white_slider_rep.SetTitleText("eye_white")
eye_white_slider_rep.SetTubeWidth(0.004)
eye_white_slider_rep.SetSliderLength(0.015)
eye_white_slider_rep.SetSliderWidth(0.008)
eye_white_slider_rep.SetEndCapLength(0.008)
eye_white_slider_rep.SetEndCapWidth(0.02)
eye_white_slider_rep.SetTitleHeight(0.02)
eye_white_slider_rep.SetLabelHeight(0.02)
eye_white_slider_rep.GetPoint1Coordinate().SetCoordinateSystemToNormalizedDisplay()
eye_white_slider_rep.GetPoint1Coordinate().SetValue(0.02, 0.275 + 5.0 / 9)
eye_white_slider_rep.GetPoint2Coordinate().SetCoordinateSystemToNormalizedDisplay()
eye_white_slider_rep.GetPoint2Coordinate().SetValue(0.18, 0.275 + 5.0 / 9)
eye_white_slider_rep.GetTubeProperty().SetColor(black_rgb)
eye_white_slider_rep.GetCapProperty().SetColor(indigo_rgb)
eye_white_slider_rep.GetSliderProperty().SetColor(burlywood_rgb)
eye_white_slider_rep.GetSelectedProperty().SetColor(lime_rgb)
eye_white_slider_rep.GetLabelProperty().SetColor(dark_slate_gray_rgb)
eye_white_slider_rep.GetTitleProperty().SetColor(color_lut.GetTableValue(tissue_indices["eye_white"])[:3])
eye_white_slider_rep.GetTitleProperty().ShadowOff()

eye_white_sw = vtkSliderWidget()
eye_white_sw.SetRepresentation(eye_white_slider_rep)
eye_white_sw.SetAnimationModeToAnimate()
eye_white_sw.AddObserver(vtkCommand.InteractionEvent,
                         lambda caller, ev, prop=eye_white_actor.GetProperty(): prop.SetOpacity(
                             caller.GetRepresentation().GetValue()))

# --- Tissue 6: heart ---
heart_reader = vtkPolyDataReader()
heart_reader.SetFileName(vtk_files["heart"])
heart_reader.Update()

heart_trans = vtkTransform()
heart_trans.DeepCopy(slice_transforms[tissue_orientation["heart"]])
heart_trans.Scale(1, -1, -1)

heart_tf = vtkTransformPolyDataFilter()
heart_tf.SetInputConnection(heart_reader.GetOutputPort())
heart_tf.SetTransform(heart_trans)

heart_normals = vtkPolyDataNormals()
heart_normals.SetInputConnection(heart_tf.GetOutputPort())
heart_normals.SetFeatureAngle(60.0)

heart_mapper = vtkPolyDataMapper()
heart_mapper.SetInputConnection(heart_normals.GetOutputPort())

heart_actor = vtkActor()
heart_actor.SetMapper(heart_mapper)
heart_actor.GetProperty().SetOpacity(tissue_opacity["heart"])
heart_actor.GetProperty().SetDiffuseColor(color_lut.GetTableValue(tissue_indices["heart"])[:3])
heart_actor.GetProperty().SetSpecular(0.2)
heart_actor.GetProperty().SetSpecularPower(10)

heart_slider_rep = vtkSliderRepresentation2D()
heart_slider_rep.SetMinimumValue(0.0)
heart_slider_rep.SetMaximumValue(1.0)
heart_slider_rep.SetValue(tissue_opacity["heart"])
heart_slider_rep.SetTitleText("heart")
heart_slider_rep.SetTubeWidth(0.004)
heart_slider_rep.SetSliderLength(0.015)
heart_slider_rep.SetSliderWidth(0.008)
heart_slider_rep.SetEndCapLength(0.008)
heart_slider_rep.SetEndCapWidth(0.02)
heart_slider_rep.SetTitleHeight(0.02)
heart_slider_rep.SetLabelHeight(0.02)
heart_slider_rep.GetPoint1Coordinate().SetCoordinateSystemToNormalizedDisplay()
heart_slider_rep.GetPoint1Coordinate().SetValue(0.02, 0.275 + 6.0 / 9)
heart_slider_rep.GetPoint2Coordinate().SetCoordinateSystemToNormalizedDisplay()
heart_slider_rep.GetPoint2Coordinate().SetValue(0.18, 0.275 + 6.0 / 9)
heart_slider_rep.GetTubeProperty().SetColor(black_rgb)
heart_slider_rep.GetCapProperty().SetColor(indigo_rgb)
heart_slider_rep.GetSliderProperty().SetColor(burlywood_rgb)
heart_slider_rep.GetSelectedProperty().SetColor(lime_rgb)
heart_slider_rep.GetLabelProperty().SetColor(dark_slate_gray_rgb)
heart_slider_rep.GetTitleProperty().SetColor(color_lut.GetTableValue(tissue_indices["heart"])[:3])
heart_slider_rep.GetTitleProperty().ShadowOff()

heart_sw = vtkSliderWidget()
heart_sw.SetRepresentation(heart_slider_rep)
heart_sw.SetAnimationModeToAnimate()
heart_sw.AddObserver(vtkCommand.InteractionEvent,
                     lambda caller, ev, prop=heart_actor.GetProperty(): prop.SetOpacity(
                         caller.GetRepresentation().GetValue()))

# --- Tissue 7: ileum (right column starts here) ---
ileum_reader = vtkPolyDataReader()
ileum_reader.SetFileName(vtk_files["ileum"])
ileum_reader.Update()

ileum_trans = vtkTransform()
ileum_trans.DeepCopy(slice_transforms[tissue_orientation["ileum"]])
ileum_trans.Scale(1, -1, -1)

ileum_tf = vtkTransformPolyDataFilter()
ileum_tf.SetInputConnection(ileum_reader.GetOutputPort())
ileum_tf.SetTransform(ileum_trans)

ileum_normals = vtkPolyDataNormals()
ileum_normals.SetInputConnection(ileum_tf.GetOutputPort())
ileum_normals.SetFeatureAngle(60.0)

ileum_mapper = vtkPolyDataMapper()
ileum_mapper.SetInputConnection(ileum_normals.GetOutputPort())

ileum_actor = vtkActor()
ileum_actor.SetMapper(ileum_mapper)
ileum_actor.GetProperty().SetOpacity(tissue_opacity["ileum"])
ileum_actor.GetProperty().SetDiffuseColor(color_lut.GetTableValue(tissue_indices["ileum"])[:3])
ileum_actor.GetProperty().SetSpecular(0.2)
ileum_actor.GetProperty().SetSpecularPower(10)

ileum_slider_rep = vtkSliderRepresentation2D()
ileum_slider_rep.SetMinimumValue(0.0)
ileum_slider_rep.SetMaximumValue(1.0)
ileum_slider_rep.SetValue(tissue_opacity["ileum"])
ileum_slider_rep.SetTitleText("ileum")
ileum_slider_rep.SetTubeWidth(0.004)
ileum_slider_rep.SetSliderLength(0.015)
ileum_slider_rep.SetSliderWidth(0.008)
ileum_slider_rep.SetEndCapLength(0.008)
ileum_slider_rep.SetEndCapWidth(0.02)
ileum_slider_rep.SetTitleHeight(0.02)
ileum_slider_rep.SetLabelHeight(0.02)
ileum_slider_rep.GetPoint1Coordinate().SetCoordinateSystemToNormalizedDisplay()
ileum_slider_rep.GetPoint1Coordinate().SetValue(0.82, 0.05)
ileum_slider_rep.GetPoint2Coordinate().SetCoordinateSystemToNormalizedDisplay()
ileum_slider_rep.GetPoint2Coordinate().SetValue(0.98, 0.05)
ileum_slider_rep.GetTubeProperty().SetColor(black_rgb)
ileum_slider_rep.GetCapProperty().SetColor(indigo_rgb)
ileum_slider_rep.GetSliderProperty().SetColor(burlywood_rgb)
ileum_slider_rep.GetSelectedProperty().SetColor(lime_rgb)
ileum_slider_rep.GetLabelProperty().SetColor(dark_slate_gray_rgb)
ileum_slider_rep.GetTitleProperty().SetColor(color_lut.GetTableValue(tissue_indices["ileum"])[:3])
ileum_slider_rep.GetTitleProperty().ShadowOff()

ileum_sw = vtkSliderWidget()
ileum_sw.SetRepresentation(ileum_slider_rep)
ileum_sw.SetAnimationModeToAnimate()
ileum_sw.AddObserver(vtkCommand.InteractionEvent,
                     lambda caller, ev, prop=ileum_actor.GetProperty(): prop.SetOpacity(
                         caller.GetRepresentation().GetValue()))

# --- Tissue 8: kidney ---
kidney_reader = vtkPolyDataReader()
kidney_reader.SetFileName(vtk_files["kidney"])
kidney_reader.Update()

kidney_trans = vtkTransform()
kidney_trans.DeepCopy(slice_transforms[tissue_orientation["kidney"]])
kidney_trans.Scale(1, -1, -1)

kidney_tf = vtkTransformPolyDataFilter()
kidney_tf.SetInputConnection(kidney_reader.GetOutputPort())
kidney_tf.SetTransform(kidney_trans)

kidney_normals = vtkPolyDataNormals()
kidney_normals.SetInputConnection(kidney_tf.GetOutputPort())
kidney_normals.SetFeatureAngle(60.0)

kidney_mapper = vtkPolyDataMapper()
kidney_mapper.SetInputConnection(kidney_normals.GetOutputPort())

kidney_actor = vtkActor()
kidney_actor.SetMapper(kidney_mapper)
kidney_actor.GetProperty().SetOpacity(tissue_opacity["kidney"])
kidney_actor.GetProperty().SetDiffuseColor(color_lut.GetTableValue(tissue_indices["kidney"])[:3])
kidney_actor.GetProperty().SetSpecular(0.2)
kidney_actor.GetProperty().SetSpecularPower(10)

kidney_slider_rep = vtkSliderRepresentation2D()
kidney_slider_rep.SetMinimumValue(0.0)
kidney_slider_rep.SetMaximumValue(1.0)
kidney_slider_rep.SetValue(tissue_opacity["kidney"])
kidney_slider_rep.SetTitleText("kidney")
kidney_slider_rep.SetTubeWidth(0.004)
kidney_slider_rep.SetSliderLength(0.015)
kidney_slider_rep.SetSliderWidth(0.008)
kidney_slider_rep.SetEndCapLength(0.008)
kidney_slider_rep.SetEndCapWidth(0.02)
kidney_slider_rep.SetTitleHeight(0.02)
kidney_slider_rep.SetLabelHeight(0.02)
kidney_slider_rep.GetPoint1Coordinate().SetCoordinateSystemToNormalizedDisplay()
kidney_slider_rep.GetPoint1Coordinate().SetValue(0.82, 0.05 + 1.0 / 9)
kidney_slider_rep.GetPoint2Coordinate().SetCoordinateSystemToNormalizedDisplay()
kidney_slider_rep.GetPoint2Coordinate().SetValue(0.98, 0.05 + 1.0 / 9)
kidney_slider_rep.GetTubeProperty().SetColor(black_rgb)
kidney_slider_rep.GetCapProperty().SetColor(indigo_rgb)
kidney_slider_rep.GetSliderProperty().SetColor(burlywood_rgb)
kidney_slider_rep.GetSelectedProperty().SetColor(lime_rgb)
kidney_slider_rep.GetLabelProperty().SetColor(dark_slate_gray_rgb)
kidney_slider_rep.GetTitleProperty().SetColor(color_lut.GetTableValue(tissue_indices["kidney"])[:3])
kidney_slider_rep.GetTitleProperty().ShadowOff()

kidney_sw = vtkSliderWidget()
kidney_sw.SetRepresentation(kidney_slider_rep)
kidney_sw.SetAnimationModeToAnimate()
kidney_sw.AddObserver(vtkCommand.InteractionEvent,
                      lambda caller, ev, prop=kidney_actor.GetProperty(): prop.SetOpacity(
                          caller.GetRepresentation().GetValue()))

# --- Tissue 9: l_intestine ---
l_intestine_reader = vtkPolyDataReader()
l_intestine_reader.SetFileName(vtk_files["l_intestine"])
l_intestine_reader.Update()

l_intestine_trans = vtkTransform()
l_intestine_trans.DeepCopy(slice_transforms[tissue_orientation["l_intestine"]])
l_intestine_trans.Scale(1, -1, -1)

l_intestine_tf = vtkTransformPolyDataFilter()
l_intestine_tf.SetInputConnection(l_intestine_reader.GetOutputPort())
l_intestine_tf.SetTransform(l_intestine_trans)

l_intestine_normals = vtkPolyDataNormals()
l_intestine_normals.SetInputConnection(l_intestine_tf.GetOutputPort())
l_intestine_normals.SetFeatureAngle(60.0)

l_intestine_mapper = vtkPolyDataMapper()
l_intestine_mapper.SetInputConnection(l_intestine_normals.GetOutputPort())

l_intestine_actor = vtkActor()
l_intestine_actor.SetMapper(l_intestine_mapper)
l_intestine_actor.GetProperty().SetOpacity(tissue_opacity["l_intestine"])
l_intestine_actor.GetProperty().SetDiffuseColor(color_lut.GetTableValue(tissue_indices["l_intestine"])[:3])
l_intestine_actor.GetProperty().SetSpecular(0.2)
l_intestine_actor.GetProperty().SetSpecularPower(10)

l_intestine_slider_rep = vtkSliderRepresentation2D()
l_intestine_slider_rep.SetMinimumValue(0.0)
l_intestine_slider_rep.SetMaximumValue(1.0)
l_intestine_slider_rep.SetValue(tissue_opacity["l_intestine"])
l_intestine_slider_rep.SetTitleText("l_intestine")
l_intestine_slider_rep.SetTubeWidth(0.004)
l_intestine_slider_rep.SetSliderLength(0.015)
l_intestine_slider_rep.SetSliderWidth(0.008)
l_intestine_slider_rep.SetEndCapLength(0.008)
l_intestine_slider_rep.SetEndCapWidth(0.02)
l_intestine_slider_rep.SetTitleHeight(0.02)
l_intestine_slider_rep.SetLabelHeight(0.02)
l_intestine_slider_rep.GetPoint1Coordinate().SetCoordinateSystemToNormalizedDisplay()
l_intestine_slider_rep.GetPoint1Coordinate().SetValue(0.82, 0.05 + 2.0 / 9)
l_intestine_slider_rep.GetPoint2Coordinate().SetCoordinateSystemToNormalizedDisplay()
l_intestine_slider_rep.GetPoint2Coordinate().SetValue(0.98, 0.05 + 2.0 / 9)
l_intestine_slider_rep.GetTubeProperty().SetColor(black_rgb)
l_intestine_slider_rep.GetCapProperty().SetColor(indigo_rgb)
l_intestine_slider_rep.GetSliderProperty().SetColor(burlywood_rgb)
l_intestine_slider_rep.GetSelectedProperty().SetColor(lime_rgb)
l_intestine_slider_rep.GetLabelProperty().SetColor(dark_slate_gray_rgb)
l_intestine_slider_rep.GetTitleProperty().SetColor(color_lut.GetTableValue(tissue_indices["l_intestine"])[:3])
l_intestine_slider_rep.GetTitleProperty().ShadowOff()

l_intestine_sw = vtkSliderWidget()
l_intestine_sw.SetRepresentation(l_intestine_slider_rep)
l_intestine_sw.SetAnimationModeToAnimate()
l_intestine_sw.AddObserver(vtkCommand.InteractionEvent,
                           lambda caller, ev, prop=l_intestine_actor.GetProperty(): prop.SetOpacity(
                               caller.GetRepresentation().GetValue()))

# --- Tissue 10: liver ---
liver_reader = vtkPolyDataReader()
liver_reader.SetFileName(vtk_files["liver"])
liver_reader.Update()

liver_trans = vtkTransform()
liver_trans.DeepCopy(slice_transforms[tissue_orientation["liver"]])
liver_trans.Scale(1, -1, -1)

liver_tf = vtkTransformPolyDataFilter()
liver_tf.SetInputConnection(liver_reader.GetOutputPort())
liver_tf.SetTransform(liver_trans)

liver_normals = vtkPolyDataNormals()
liver_normals.SetInputConnection(liver_tf.GetOutputPort())
liver_normals.SetFeatureAngle(60.0)

liver_mapper = vtkPolyDataMapper()
liver_mapper.SetInputConnection(liver_normals.GetOutputPort())

liver_actor = vtkActor()
liver_actor.SetMapper(liver_mapper)
liver_actor.GetProperty().SetOpacity(tissue_opacity["liver"])
liver_actor.GetProperty().SetDiffuseColor(color_lut.GetTableValue(tissue_indices["liver"])[:3])
liver_actor.GetProperty().SetSpecular(0.2)
liver_actor.GetProperty().SetSpecularPower(10)

liver_slider_rep = vtkSliderRepresentation2D()
liver_slider_rep.SetMinimumValue(0.0)
liver_slider_rep.SetMaximumValue(1.0)
liver_slider_rep.SetValue(tissue_opacity["liver"])
liver_slider_rep.SetTitleText("liver")
liver_slider_rep.SetTubeWidth(0.004)
liver_slider_rep.SetSliderLength(0.015)
liver_slider_rep.SetSliderWidth(0.008)
liver_slider_rep.SetEndCapLength(0.008)
liver_slider_rep.SetEndCapWidth(0.02)
liver_slider_rep.SetTitleHeight(0.02)
liver_slider_rep.SetLabelHeight(0.02)
liver_slider_rep.GetPoint1Coordinate().SetCoordinateSystemToNormalizedDisplay()
liver_slider_rep.GetPoint1Coordinate().SetValue(0.82, 0.05 + 3.0 / 9)
liver_slider_rep.GetPoint2Coordinate().SetCoordinateSystemToNormalizedDisplay()
liver_slider_rep.GetPoint2Coordinate().SetValue(0.98, 0.05 + 3.0 / 9)
liver_slider_rep.GetTubeProperty().SetColor(black_rgb)
liver_slider_rep.GetCapProperty().SetColor(indigo_rgb)
liver_slider_rep.GetSliderProperty().SetColor(burlywood_rgb)
liver_slider_rep.GetSelectedProperty().SetColor(lime_rgb)
liver_slider_rep.GetLabelProperty().SetColor(dark_slate_gray_rgb)
liver_slider_rep.GetTitleProperty().SetColor(color_lut.GetTableValue(tissue_indices["liver"])[:3])
liver_slider_rep.GetTitleProperty().ShadowOff()

liver_sw = vtkSliderWidget()
liver_sw.SetRepresentation(liver_slider_rep)
liver_sw.SetAnimationModeToAnimate()
liver_sw.AddObserver(vtkCommand.InteractionEvent,
                     lambda caller, ev, prop=liver_actor.GetProperty(): prop.SetOpacity(
                         caller.GetRepresentation().GetValue()))

# --- Tissue 11: lung ---
lung_reader = vtkPolyDataReader()
lung_reader.SetFileName(vtk_files["lung"])
lung_reader.Update()

lung_trans = vtkTransform()
lung_trans.DeepCopy(slice_transforms[tissue_orientation["lung"]])
lung_trans.Scale(1, -1, -1)

lung_tf = vtkTransformPolyDataFilter()
lung_tf.SetInputConnection(lung_reader.GetOutputPort())
lung_tf.SetTransform(lung_trans)

lung_normals = vtkPolyDataNormals()
lung_normals.SetInputConnection(lung_tf.GetOutputPort())
lung_normals.SetFeatureAngle(60.0)

lung_mapper = vtkPolyDataMapper()
lung_mapper.SetInputConnection(lung_normals.GetOutputPort())

lung_actor = vtkActor()
lung_actor.SetMapper(lung_mapper)
lung_actor.GetProperty().SetOpacity(tissue_opacity["lung"])
lung_actor.GetProperty().SetDiffuseColor(color_lut.GetTableValue(tissue_indices["lung"])[:3])
lung_actor.GetProperty().SetSpecular(0.2)
lung_actor.GetProperty().SetSpecularPower(10)

lung_slider_rep = vtkSliderRepresentation2D()
lung_slider_rep.SetMinimumValue(0.0)
lung_slider_rep.SetMaximumValue(1.0)
lung_slider_rep.SetValue(tissue_opacity["lung"])
lung_slider_rep.SetTitleText("lung")
lung_slider_rep.SetTubeWidth(0.004)
lung_slider_rep.SetSliderLength(0.015)
lung_slider_rep.SetSliderWidth(0.008)
lung_slider_rep.SetEndCapLength(0.008)
lung_slider_rep.SetEndCapWidth(0.02)
lung_slider_rep.SetTitleHeight(0.02)
lung_slider_rep.SetLabelHeight(0.02)
lung_slider_rep.GetPoint1Coordinate().SetCoordinateSystemToNormalizedDisplay()
lung_slider_rep.GetPoint1Coordinate().SetValue(0.82, 0.05 + 4.0 / 9)
lung_slider_rep.GetPoint2Coordinate().SetCoordinateSystemToNormalizedDisplay()
lung_slider_rep.GetPoint2Coordinate().SetValue(0.98, 0.05 + 4.0 / 9)
lung_slider_rep.GetTubeProperty().SetColor(black_rgb)
lung_slider_rep.GetCapProperty().SetColor(indigo_rgb)
lung_slider_rep.GetSliderProperty().SetColor(burlywood_rgb)
lung_slider_rep.GetSelectedProperty().SetColor(lime_rgb)
lung_slider_rep.GetLabelProperty().SetColor(dark_slate_gray_rgb)
lung_slider_rep.GetTitleProperty().SetColor(color_lut.GetTableValue(tissue_indices["lung"])[:3])
lung_slider_rep.GetTitleProperty().ShadowOff()

lung_sw = vtkSliderWidget()
lung_sw.SetRepresentation(lung_slider_rep)
lung_sw.SetAnimationModeToAnimate()
lung_sw.AddObserver(vtkCommand.InteractionEvent,
                    lambda caller, ev, prop=lung_actor.GetProperty(): prop.SetOpacity(
                        caller.GetRepresentation().GetValue()))

# --- Tissue 12: nerve ---
nerve_reader = vtkPolyDataReader()
nerve_reader.SetFileName(vtk_files["nerve"])
nerve_reader.Update()

nerve_trans = vtkTransform()
nerve_trans.DeepCopy(slice_transforms[tissue_orientation["nerve"]])
nerve_trans.Scale(1, -1, -1)

nerve_tf = vtkTransformPolyDataFilter()
nerve_tf.SetInputConnection(nerve_reader.GetOutputPort())
nerve_tf.SetTransform(nerve_trans)

nerve_normals = vtkPolyDataNormals()
nerve_normals.SetInputConnection(nerve_tf.GetOutputPort())
nerve_normals.SetFeatureAngle(60.0)

nerve_mapper = vtkPolyDataMapper()
nerve_mapper.SetInputConnection(nerve_normals.GetOutputPort())

nerve_actor = vtkActor()
nerve_actor.SetMapper(nerve_mapper)
nerve_actor.GetProperty().SetOpacity(tissue_opacity["nerve"])
nerve_actor.GetProperty().SetDiffuseColor(color_lut.GetTableValue(tissue_indices["nerve"])[:3])
nerve_actor.GetProperty().SetSpecular(0.2)
nerve_actor.GetProperty().SetSpecularPower(10)

nerve_slider_rep = vtkSliderRepresentation2D()
nerve_slider_rep.SetMinimumValue(0.0)
nerve_slider_rep.SetMaximumValue(1.0)
nerve_slider_rep.SetValue(tissue_opacity["nerve"])
nerve_slider_rep.SetTitleText("nerve")
nerve_slider_rep.SetTubeWidth(0.004)
nerve_slider_rep.SetSliderLength(0.015)
nerve_slider_rep.SetSliderWidth(0.008)
nerve_slider_rep.SetEndCapLength(0.008)
nerve_slider_rep.SetEndCapWidth(0.02)
nerve_slider_rep.SetTitleHeight(0.02)
nerve_slider_rep.SetLabelHeight(0.02)
nerve_slider_rep.GetPoint1Coordinate().SetCoordinateSystemToNormalizedDisplay()
nerve_slider_rep.GetPoint1Coordinate().SetValue(0.82, 0.05 + 5.0 / 9)
nerve_slider_rep.GetPoint2Coordinate().SetCoordinateSystemToNormalizedDisplay()
nerve_slider_rep.GetPoint2Coordinate().SetValue(0.98, 0.05 + 5.0 / 9)
nerve_slider_rep.GetTubeProperty().SetColor(black_rgb)
nerve_slider_rep.GetCapProperty().SetColor(indigo_rgb)
nerve_slider_rep.GetSliderProperty().SetColor(burlywood_rgb)
nerve_slider_rep.GetSelectedProperty().SetColor(lime_rgb)
nerve_slider_rep.GetLabelProperty().SetColor(dark_slate_gray_rgb)
nerve_slider_rep.GetTitleProperty().SetColor(color_lut.GetTableValue(tissue_indices["nerve"])[:3])
nerve_slider_rep.GetTitleProperty().ShadowOff()

nerve_sw = vtkSliderWidget()
nerve_sw.SetRepresentation(nerve_slider_rep)
nerve_sw.SetAnimationModeToAnimate()
nerve_sw.AddObserver(vtkCommand.InteractionEvent,
                     lambda caller, ev, prop=nerve_actor.GetProperty(): prop.SetOpacity(
                         caller.GetRepresentation().GetValue()))

# --- Tissue 13: skeleton ---
skeleton_reader = vtkPolyDataReader()
skeleton_reader.SetFileName(vtk_files["skeleton"])
skeleton_reader.Update()

skeleton_trans = vtkTransform()
skeleton_trans.DeepCopy(slice_transforms[tissue_orientation["skeleton"]])
skeleton_trans.Scale(1, -1, -1)

skeleton_tf = vtkTransformPolyDataFilter()
skeleton_tf.SetInputConnection(skeleton_reader.GetOutputPort())
skeleton_tf.SetTransform(skeleton_trans)

skeleton_normals = vtkPolyDataNormals()
skeleton_normals.SetInputConnection(skeleton_tf.GetOutputPort())
skeleton_normals.SetFeatureAngle(60.0)

skeleton_mapper = vtkPolyDataMapper()
skeleton_mapper.SetInputConnection(skeleton_normals.GetOutputPort())

skeleton_actor = vtkActor()
skeleton_actor.SetMapper(skeleton_mapper)
skeleton_actor.GetProperty().SetOpacity(tissue_opacity["skeleton"])
skeleton_actor.GetProperty().SetDiffuseColor(color_lut.GetTableValue(tissue_indices["skeleton"])[:3])
skeleton_actor.GetProperty().SetSpecular(0.2)
skeleton_actor.GetProperty().SetSpecularPower(10)

skeleton_slider_rep = vtkSliderRepresentation2D()
skeleton_slider_rep.SetMinimumValue(0.0)
skeleton_slider_rep.SetMaximumValue(1.0)
skeleton_slider_rep.SetValue(tissue_opacity["skeleton"])
skeleton_slider_rep.SetTitleText("skeleton")
skeleton_slider_rep.SetTubeWidth(0.004)
skeleton_slider_rep.SetSliderLength(0.015)
skeleton_slider_rep.SetSliderWidth(0.008)
skeleton_slider_rep.SetEndCapLength(0.008)
skeleton_slider_rep.SetEndCapWidth(0.02)
skeleton_slider_rep.SetTitleHeight(0.02)
skeleton_slider_rep.SetLabelHeight(0.02)
skeleton_slider_rep.GetPoint1Coordinate().SetCoordinateSystemToNormalizedDisplay()
skeleton_slider_rep.GetPoint1Coordinate().SetValue(0.82, 0.05 + 6.0 / 9)
skeleton_slider_rep.GetPoint2Coordinate().SetCoordinateSystemToNormalizedDisplay()
skeleton_slider_rep.GetPoint2Coordinate().SetValue(0.98, 0.05 + 6.0 / 9)
skeleton_slider_rep.GetTubeProperty().SetColor(black_rgb)
skeleton_slider_rep.GetCapProperty().SetColor(indigo_rgb)
skeleton_slider_rep.GetSliderProperty().SetColor(burlywood_rgb)
skeleton_slider_rep.GetSelectedProperty().SetColor(lime_rgb)
skeleton_slider_rep.GetLabelProperty().SetColor(dark_slate_gray_rgb)
skeleton_slider_rep.GetTitleProperty().SetColor(color_lut.GetTableValue(tissue_indices["skeleton"])[:3])
skeleton_slider_rep.GetTitleProperty().ShadowOff()

skeleton_sw = vtkSliderWidget()
skeleton_sw.SetRepresentation(skeleton_slider_rep)
skeleton_sw.SetAnimationModeToAnimate()
skeleton_sw.AddObserver(vtkCommand.InteractionEvent,
                        lambda caller, ev, prop=skeleton_actor.GetProperty(): prop.SetOpacity(
                            caller.GetRepresentation().GetValue()))

# --- Tissue 14: spleen ---
spleen_reader = vtkPolyDataReader()
spleen_reader.SetFileName(vtk_files["spleen"])
spleen_reader.Update()

spleen_trans = vtkTransform()
spleen_trans.DeepCopy(slice_transforms[tissue_orientation["spleen"]])
spleen_trans.Scale(1, -1, -1)

spleen_tf = vtkTransformPolyDataFilter()
spleen_tf.SetInputConnection(spleen_reader.GetOutputPort())
spleen_tf.SetTransform(spleen_trans)

spleen_normals = vtkPolyDataNormals()
spleen_normals.SetInputConnection(spleen_tf.GetOutputPort())
spleen_normals.SetFeatureAngle(60.0)

spleen_mapper = vtkPolyDataMapper()
spleen_mapper.SetInputConnection(spleen_normals.GetOutputPort())

spleen_actor = vtkActor()
spleen_actor.SetMapper(spleen_mapper)
spleen_actor.GetProperty().SetOpacity(tissue_opacity["spleen"])
spleen_actor.GetProperty().SetDiffuseColor(color_lut.GetTableValue(tissue_indices["spleen"])[:3])
spleen_actor.GetProperty().SetSpecular(0.2)
spleen_actor.GetProperty().SetSpecularPower(10)

spleen_slider_rep = vtkSliderRepresentation2D()
spleen_slider_rep.SetMinimumValue(0.0)
spleen_slider_rep.SetMaximumValue(1.0)
spleen_slider_rep.SetValue(tissue_opacity["spleen"])
spleen_slider_rep.SetTitleText("spleen")
spleen_slider_rep.SetTubeWidth(0.004)
spleen_slider_rep.SetSliderLength(0.015)
spleen_slider_rep.SetSliderWidth(0.008)
spleen_slider_rep.SetEndCapLength(0.008)
spleen_slider_rep.SetEndCapWidth(0.02)
spleen_slider_rep.SetTitleHeight(0.02)
spleen_slider_rep.SetLabelHeight(0.02)
spleen_slider_rep.GetPoint1Coordinate().SetCoordinateSystemToNormalizedDisplay()
spleen_slider_rep.GetPoint1Coordinate().SetValue(0.82, 0.05 + 7.0 / 9)
spleen_slider_rep.GetPoint2Coordinate().SetCoordinateSystemToNormalizedDisplay()
spleen_slider_rep.GetPoint2Coordinate().SetValue(0.98, 0.05 + 7.0 / 9)
spleen_slider_rep.GetTubeProperty().SetColor(black_rgb)
spleen_slider_rep.GetCapProperty().SetColor(indigo_rgb)
spleen_slider_rep.GetSliderProperty().SetColor(burlywood_rgb)
spleen_slider_rep.GetSelectedProperty().SetColor(lime_rgb)
spleen_slider_rep.GetLabelProperty().SetColor(dark_slate_gray_rgb)
spleen_slider_rep.GetTitleProperty().SetColor(color_lut.GetTableValue(tissue_indices["spleen"])[:3])
spleen_slider_rep.GetTitleProperty().ShadowOff()

spleen_sw = vtkSliderWidget()
spleen_sw.SetRepresentation(spleen_slider_rep)
spleen_sw.SetAnimationModeToAnimate()
spleen_sw.AddObserver(vtkCommand.InteractionEvent,
                      lambda caller, ev, prop=spleen_actor.GetProperty(): prop.SetOpacity(
                          caller.GetRepresentation().GetValue()))

# --- Tissue 15: stomach ---
stomach_reader = vtkPolyDataReader()
stomach_reader.SetFileName(vtk_files["stomach"])
stomach_reader.Update()

stomach_trans = vtkTransform()
stomach_trans.DeepCopy(slice_transforms[tissue_orientation["stomach"]])
stomach_trans.Scale(1, -1, -1)

stomach_tf = vtkTransformPolyDataFilter()
stomach_tf.SetInputConnection(stomach_reader.GetOutputPort())
stomach_tf.SetTransform(stomach_trans)

stomach_normals = vtkPolyDataNormals()
stomach_normals.SetInputConnection(stomach_tf.GetOutputPort())
stomach_normals.SetFeatureAngle(60.0)

stomach_mapper = vtkPolyDataMapper()
stomach_mapper.SetInputConnection(stomach_normals.GetOutputPort())

stomach_actor = vtkActor()
stomach_actor.SetMapper(stomach_mapper)
stomach_actor.GetProperty().SetOpacity(tissue_opacity["stomach"])
stomach_actor.GetProperty().SetDiffuseColor(color_lut.GetTableValue(tissue_indices["stomach"])[:3])
stomach_actor.GetProperty().SetSpecular(0.2)
stomach_actor.GetProperty().SetSpecularPower(10)

stomach_slider_rep = vtkSliderRepresentation2D()
stomach_slider_rep.SetMinimumValue(0.0)
stomach_slider_rep.SetMaximumValue(1.0)
stomach_slider_rep.SetValue(tissue_opacity["stomach"])
stomach_slider_rep.SetTitleText("stomach")
stomach_slider_rep.SetTubeWidth(0.004)
stomach_slider_rep.SetSliderLength(0.015)
stomach_slider_rep.SetSliderWidth(0.008)
stomach_slider_rep.SetEndCapLength(0.008)
stomach_slider_rep.SetEndCapWidth(0.02)
stomach_slider_rep.SetTitleHeight(0.02)
stomach_slider_rep.SetLabelHeight(0.02)
stomach_slider_rep.GetPoint1Coordinate().SetCoordinateSystemToNormalizedDisplay()
stomach_slider_rep.GetPoint1Coordinate().SetValue(0.82, 0.05 + 8.0 / 9)
stomach_slider_rep.GetPoint2Coordinate().SetCoordinateSystemToNormalizedDisplay()
stomach_slider_rep.GetPoint2Coordinate().SetValue(0.98, 0.05 + 8.0 / 9)
stomach_slider_rep.GetTubeProperty().SetColor(black_rgb)
stomach_slider_rep.GetCapProperty().SetColor(indigo_rgb)
stomach_slider_rep.GetSliderProperty().SetColor(burlywood_rgb)
stomach_slider_rep.GetSelectedProperty().SetColor(lime_rgb)
stomach_slider_rep.GetLabelProperty().SetColor(dark_slate_gray_rgb)
stomach_slider_rep.GetTitleProperty().SetColor(color_lut.GetTableValue(tissue_indices["stomach"])[:3])
stomach_slider_rep.GetTitleProperty().ShadowOff()

stomach_sw = vtkSliderWidget()
stomach_sw.SetRepresentation(stomach_slider_rep)
stomach_sw.SetAnimationModeToAnimate()
stomach_sw.AddObserver(vtkCommand.InteractionEvent,
                       lambda caller, ev, prop=stomach_actor.GetProperty(): prop.SetOpacity(
                           caller.GetRepresentation().GetValue()))

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.AddActor(skin_actor)
renderer.AddActor(blood_actor)
renderer.AddActor(brain_actor)
renderer.AddActor(duodenum_actor)
renderer.AddActor(eye_retna_actor)
renderer.AddActor(eye_white_actor)
renderer.AddActor(heart_actor)
renderer.AddActor(ileum_actor)
renderer.AddActor(kidney_actor)
renderer.AddActor(l_intestine_actor)
renderer.AddActor(liver_actor)
renderer.AddActor(lung_actor)
renderer.AddActor(nerve_actor)
renderer.AddActor(skeleton_actor)
renderer.AddActor(spleen_actor)
renderer.AddActor(stomach_actor)
renderer.SetBackground(paraview_bkg_rgb)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("froggie view")
render_window.SetMultiSamples(0)
render_window.SetSize(1024 + 400, 1024)

# Scene: configure camera
camera = renderer.GetActiveCamera()
cam_transform = vtkTransform()
cam_transform.SetMatrix(camera.GetModelTransformMatrix())
cam_transform.RotateY(-90)
cam_transform.RotateZ(90)
camera.SetModelTransformMatrix(cam_transform.GetMatrix())
renderer.ResetCamera()

# CameraOrientationWidget: interactive orientation gizmo
cow = vtkCameraOrientationWidget()
cow.SetParentRenderer(renderer)
cow.Off()
cow.EnabledOff()

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)
style = vtkInteractorStyleTrackballCamera()
render_window_interactor.SetInteractorStyle(style)

# Enable slider widgets
skin_sw.SetInteractor(render_window_interactor)
skin_sw.EnabledOn()
blood_sw.SetInteractor(render_window_interactor)
blood_sw.EnabledOn()
brain_sw.SetInteractor(render_window_interactor)
brain_sw.EnabledOn()
duodenum_sw.SetInteractor(render_window_interactor)
duodenum_sw.EnabledOn()
eye_retna_sw.SetInteractor(render_window_interactor)
eye_retna_sw.EnabledOn()
eye_white_sw.SetInteractor(render_window_interactor)
eye_white_sw.EnabledOn()
heart_sw.SetInteractor(render_window_interactor)
heart_sw.EnabledOn()
ileum_sw.SetInteractor(render_window_interactor)
ileum_sw.EnabledOn()
kidney_sw.SetInteractor(render_window_interactor)
kidney_sw.EnabledOn()
l_intestine_sw.SetInteractor(render_window_interactor)
l_intestine_sw.EnabledOn()
liver_sw.SetInteractor(render_window_interactor)
liver_sw.EnabledOn()
lung_sw.SetInteractor(render_window_interactor)
lung_sw.EnabledOn()
nerve_sw.SetInteractor(render_window_interactor)
nerve_sw.EnabledOn()
skeleton_sw.SetInteractor(render_window_interactor)
skeleton_sw.EnabledOn()
spleen_sw.SetInteractor(render_window_interactor)
spleen_sw.EnabledOn()
stomach_sw.SetInteractor(render_window_interactor)
stomach_sw.EnabledOn()

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
