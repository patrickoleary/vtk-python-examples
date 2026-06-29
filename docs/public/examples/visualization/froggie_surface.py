#!/usr/bin/env python

# Construct surfaces from a segmented frog dataset using a JSON configuration.

import copy
import json
import os
from pathlib import Path

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkCommonColor import vtkNamedColors
from vtkmodules.vtkCommonCore import vtkLookupTable
from vtkmodules.vtkCommonMath import vtkMatrix4x4
from vtkmodules.vtkCommonTransforms import vtkTransform
from vtkmodules.vtkFiltersCore import (
    vtkFlyingEdges3D,
    vtkPolyDataNormals,
    vtkStripper,
    vtkWindowedSincPolyDataFilter,
)
from vtkmodules.vtkFiltersGeneral import vtkTransformPolyDataFilter
from vtkmodules.vtkIOImage import vtkMetaImageReader
from vtkmodules.vtkImagingCore import (
    vtkImageShrink3D,
    vtkImageThreshold,
)
from vtkmodules.vtkImagingGeneral import vtkImageGaussianSmooth
from vtkmodules.vtkInteractionStyle import vtkInteractorStyleTrackballCamera
from vtkmodules.vtkInteractionWidgets import vtkCameraOrientationWidget
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
paraview_bkg_rgb = (0.322, 0.341, 0.431)
colors = vtkNamedColors()

# Data: locate the JSON configuration file
data_dir = Path(os.environ.get("VPE_DATA_DIR", Path(__file__).parent))
json_file = data_dir / "Frog_mhd.json"

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

# Parse the JSON configuration file
with open(json_file) as f:
    json_data = json.load(f)

# Resolve MHD file paths relative to the JSON file location
root = data_dir / json_data["files"]["root"]
mhd_files = {}
for p in json_data["files"]["mhd_files"]:
    fp = root / p
    mhd_files[fp.stem] = fp

# Assemble per-tissue parameters from JSON defaults + overrides
base_params = {k.lower(): v for k, v in json_data["tissue_parameters"]["default"].items()}
frog_params = copy.deepcopy(base_params)
for k, v in json_data["tissue_parameters"]["frog"].items():
    frog_params[k.lower()] = v

tissue_colors = json_data["tissues"]["colors"]
tissue_names = []
tissue_params = {}
for name, overrides in json_data["tissue_parameters"].items():
    if name in ("default", "frog", "parameter types", "brainbin"):
        continue
    if name == "skin":
        params = copy.deepcopy(base_params)
    else:
        params = copy.deepcopy(frog_params)
    for k, v in overrides.items():
        params[k.lower()] = v
    tissue_params[name] = params
    tissue_names.append(params["name"])

# LookupTable: tissue label to color
tissue_indices = {name: tissue_params[name]["tissue"] for name in tissue_names}
color_lut = vtkLookupTable()
color_lut.SetNumberOfColors(len(tissue_colors))
color_lut.SetTableRange(0, len(tissue_colors) - 1)
color_lut.Build()
for name, idx in tissue_indices.items():
    color_lut.SetTableValue(idx, colors.GetColor4d(tissue_colors[name]))

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.SetBackground(paraview_bkg_rgb)

# ---- skin (tissue 0) ----
skin_reader = vtkMetaImageReader()
skin_reader.SetFileName(str(mhd_files["frog"]))
skin_reader.SetDataSpacing(1, 1, 1.5)
skin_reader.SetDataOrigin(-250.0, -235.0, 1.5)
skin_reader.SetDataExtent(0, 499, 0, 469, 1, 138)
skin_reader.Update()

skin_shrinker = vtkImageShrink3D()
skin_shrinker.SetInputConnection(skin_reader.GetOutputPort())
skin_shrinker.SetShrinkFactors(2, 2, 1)
skin_shrinker.AveragingOn()

skin_gaussian = vtkImageGaussianSmooth()
skin_gaussian.SetStandardDeviation(2, 2, 2)
skin_gaussian.SetRadiusFactors(2, 2, 2)
skin_gaussian.SetInputConnection(skin_shrinker.GetOutputPort())

skin_iso = vtkFlyingEdges3D()
skin_iso.SetInputConnection(skin_gaussian.GetOutputPort())
skin_iso.ComputeScalarsOff()
skin_iso.ComputeGradientsOff()
skin_iso.ComputeNormalsOff()
skin_iso.SetValue(0, 10.5)
skin_iso.Update()

skin_tf = vtkTransformPolyDataFilter()
skin_tf.SetTransform(slice_transforms["si"])
skin_tf.SetInputConnection(skin_iso.GetOutputPort())

skin_normals = vtkPolyDataNormals()
skin_normals.SetInputConnection(skin_tf.GetOutputPort())
skin_normals.SetFeatureAngle(60)

skin_stripper = vtkStripper()
skin_stripper.SetInputConnection(skin_normals.GetOutputPort())

skin_mapper = vtkPolyDataMapper()
skin_mapper.SetInputConnection(skin_stripper.GetOutputPort())

skin_actor = vtkActor()
skin_actor.SetMapper(skin_mapper)
skin_actor.GetProperty().SetOpacity(0.4)
skin_actor.GetProperty().SetDiffuseColor(color_lut.GetTableValue(0)[:3])
skin_actor.GetProperty().SetSpecular(0.5)
skin_actor.GetProperty().SetSpecularPower(10)
renderer.AddActor(skin_actor)

# ---- blood (tissue 1) ----
blood_reader = vtkMetaImageReader()
blood_reader.SetFileName(str(mhd_files["frogtissue"]))
blood_reader.SetDataSpacing(1, 1, 1.5)
blood_reader.SetDataOrigin(-250.0, -235.0, 21.0)
blood_reader.SetDataExtent(33, 406, 44, 407, 14, 131)
blood_reader.Update()

blood_threshold = vtkImageThreshold()
blood_threshold.ThresholdBetween(1, 1)
blood_threshold.SetInValue(255)
blood_threshold.SetOutValue(0)
blood_threshold.SetInputConnection(blood_reader.GetOutputPort())

blood_shrinker = vtkImageShrink3D()
blood_shrinker.SetInputConnection(blood_threshold.GetOutputPort())
blood_shrinker.SetShrinkFactors(1, 1, 1)
blood_shrinker.AveragingOn()

blood_gaussian = vtkImageGaussianSmooth()
blood_gaussian.SetStandardDeviation(2, 2, 2)
blood_gaussian.SetRadiusFactors(2, 2, 2)
blood_gaussian.SetInputConnection(blood_shrinker.GetOutputPort())

blood_iso = vtkFlyingEdges3D()
blood_iso.SetInputConnection(blood_gaussian.GetOutputPort())
blood_iso.ComputeScalarsOff()
blood_iso.ComputeGradientsOff()
blood_iso.ComputeNormalsOff()
blood_iso.SetValue(0, 127.5)
blood_iso.Update()

blood_tf = vtkTransformPolyDataFilter()
blood_tf.SetTransform(slice_transforms["si"])
blood_tf.SetInputConnection(blood_iso.GetOutputPort())

blood_smoother = vtkWindowedSincPolyDataFilter()
blood_smoother.SetInputConnection(blood_tf.GetOutputPort())
blood_smoother.BoundarySmoothingOff()
blood_smoother.FeatureEdgeSmoothingOff()
blood_smoother.SetFeatureAngle(60)
blood_smoother.SetPassBand(0.1)
blood_smoother.NonManifoldSmoothingOn()
blood_smoother.NormalizeCoordinatesOff()

blood_normals = vtkPolyDataNormals()
blood_normals.SetInputConnection(blood_smoother.GetOutputPort())
blood_normals.SetFeatureAngle(60)

blood_stripper = vtkStripper()
blood_stripper.SetInputConnection(blood_normals.GetOutputPort())

blood_mapper = vtkPolyDataMapper()
blood_mapper.SetInputConnection(blood_stripper.GetOutputPort())

blood_actor = vtkActor()
blood_actor.SetMapper(blood_mapper)
blood_actor.GetProperty().SetOpacity(1.0)
blood_actor.GetProperty().SetDiffuseColor(color_lut.GetTableValue(1)[:3])
blood_actor.GetProperty().SetSpecular(0.5)
blood_actor.GetProperty().SetSpecularPower(10)
renderer.AddActor(blood_actor)

# ---- brain (tissue 2) ----
brain_reader = vtkMetaImageReader()
brain_reader.SetFileName(str(mhd_files["frogtissue"]))
brain_reader.SetDataSpacing(1, 1, 1.5)
brain_reader.SetDataOrigin(-250.0, -235.0, 1.5)
brain_reader.SetDataExtent(349, 436, 217, 258, 1, 33)
brain_reader.Update()

brain_threshold = vtkImageThreshold()
brain_threshold.ThresholdBetween(2, 2)
brain_threshold.SetInValue(255)
brain_threshold.SetOutValue(0)
brain_threshold.SetInputConnection(brain_reader.GetOutputPort())

brain_shrinker = vtkImageShrink3D()
brain_shrinker.SetInputConnection(brain_threshold.GetOutputPort())
brain_shrinker.SetShrinkFactors(1, 1, 1)
brain_shrinker.AveragingOn()

brain_gaussian = vtkImageGaussianSmooth()
brain_gaussian.SetStandardDeviation(2, 2, 2)
brain_gaussian.SetRadiusFactors(2, 2, 2)
brain_gaussian.SetInputConnection(brain_shrinker.GetOutputPort())

brain_iso = vtkFlyingEdges3D()
brain_iso.SetInputConnection(brain_gaussian.GetOutputPort())
brain_iso.ComputeScalarsOff()
brain_iso.ComputeGradientsOff()
brain_iso.ComputeNormalsOff()
brain_iso.SetValue(0, 127.5)
brain_iso.Update()

brain_tf = vtkTransformPolyDataFilter()
brain_tf.SetTransform(slice_transforms["si"])
brain_tf.SetInputConnection(brain_iso.GetOutputPort())

brain_smoother = vtkWindowedSincPolyDataFilter()
brain_smoother.SetInputConnection(brain_tf.GetOutputPort())
brain_smoother.BoundarySmoothingOff()
brain_smoother.FeatureEdgeSmoothingOff()
brain_smoother.SetFeatureAngle(60)
brain_smoother.SetPassBand(0.1)
brain_smoother.NonManifoldSmoothingOn()
brain_smoother.NormalizeCoordinatesOff()

brain_normals = vtkPolyDataNormals()
brain_normals.SetInputConnection(brain_smoother.GetOutputPort())
brain_normals.SetFeatureAngle(60)

brain_stripper = vtkStripper()
brain_stripper.SetInputConnection(brain_normals.GetOutputPort())

brain_mapper = vtkPolyDataMapper()
brain_mapper.SetInputConnection(brain_stripper.GetOutputPort())

brain_actor = vtkActor()
brain_actor.SetMapper(brain_mapper)
brain_actor.GetProperty().SetOpacity(1.0)
brain_actor.GetProperty().SetDiffuseColor(color_lut.GetTableValue(2)[:3])
brain_actor.GetProperty().SetSpecular(0.5)
brain_actor.GetProperty().SetSpecularPower(10)
renderer.AddActor(brain_actor)

# ---- duodenum (tissue 3) ----
duodenum_reader = vtkMetaImageReader()
duodenum_reader.SetFileName(str(mhd_files["frogtissue"]))
duodenum_reader.SetDataSpacing(1, 1, 1.5)
duodenum_reader.SetDataOrigin(-250.0, -235.0, 52.5)
duodenum_reader.SetDataExtent(189, 248, 185, 278, 35, 105)
duodenum_reader.Update()

duodenum_threshold = vtkImageThreshold()
duodenum_threshold.ThresholdBetween(3, 3)
duodenum_threshold.SetInValue(255)
duodenum_threshold.SetOutValue(0)
duodenum_threshold.SetInputConnection(duodenum_reader.GetOutputPort())

duodenum_shrinker = vtkImageShrink3D()
duodenum_shrinker.SetInputConnection(duodenum_threshold.GetOutputPort())
duodenum_shrinker.SetShrinkFactors(1, 1, 1)
duodenum_shrinker.AveragingOn()

duodenum_gaussian = vtkImageGaussianSmooth()
duodenum_gaussian.SetStandardDeviation(2, 2, 2)
duodenum_gaussian.SetRadiusFactors(2, 2, 2)
duodenum_gaussian.SetInputConnection(duodenum_shrinker.GetOutputPort())

duodenum_iso = vtkFlyingEdges3D()
duodenum_iso.SetInputConnection(duodenum_gaussian.GetOutputPort())
duodenum_iso.ComputeScalarsOff()
duodenum_iso.ComputeGradientsOff()
duodenum_iso.ComputeNormalsOff()
duodenum_iso.SetValue(0, 127.5)
duodenum_iso.Update()

duodenum_tf = vtkTransformPolyDataFilter()
duodenum_tf.SetTransform(slice_transforms["si"])
duodenum_tf.SetInputConnection(duodenum_iso.GetOutputPort())

duodenum_smoother = vtkWindowedSincPolyDataFilter()
duodenum_smoother.SetInputConnection(duodenum_tf.GetOutputPort())
duodenum_smoother.BoundarySmoothingOff()
duodenum_smoother.FeatureEdgeSmoothingOff()
duodenum_smoother.SetFeatureAngle(60)
duodenum_smoother.SetPassBand(0.1)
duodenum_smoother.NonManifoldSmoothingOn()
duodenum_smoother.NormalizeCoordinatesOff()

duodenum_normals = vtkPolyDataNormals()
duodenum_normals.SetInputConnection(duodenum_smoother.GetOutputPort())
duodenum_normals.SetFeatureAngle(60)

duodenum_stripper = vtkStripper()
duodenum_stripper.SetInputConnection(duodenum_normals.GetOutputPort())

duodenum_mapper = vtkPolyDataMapper()
duodenum_mapper.SetInputConnection(duodenum_stripper.GetOutputPort())

duodenum_actor = vtkActor()
duodenum_actor.SetMapper(duodenum_mapper)
duodenum_actor.GetProperty().SetOpacity(1.0)
duodenum_actor.GetProperty().SetDiffuseColor(color_lut.GetTableValue(3)[:3])
duodenum_actor.GetProperty().SetSpecular(0.5)
duodenum_actor.GetProperty().SetSpecularPower(10)
renderer.AddActor(duodenum_actor)

# ---- eye_retna (tissue 4) ----
eye_retna_reader = vtkMetaImageReader()
eye_retna_reader.SetFileName(str(mhd_files["frogtissue"]))
eye_retna_reader.SetDataSpacing(1, 1, 1.5)
eye_retna_reader.SetDataOrigin(-250.0, -235.0, 1.5)
eye_retna_reader.SetDataExtent(342, 438, 184, 289, 1, 41)
eye_retna_reader.Update()

eye_retna_threshold = vtkImageThreshold()
eye_retna_threshold.ThresholdBetween(4, 4)
eye_retna_threshold.SetInValue(255)
eye_retna_threshold.SetOutValue(0)
eye_retna_threshold.SetInputConnection(eye_retna_reader.GetOutputPort())

eye_retna_shrinker = vtkImageShrink3D()
eye_retna_shrinker.SetInputConnection(eye_retna_threshold.GetOutputPort())
eye_retna_shrinker.SetShrinkFactors(1, 1, 1)
eye_retna_shrinker.AveragingOn()

eye_retna_gaussian = vtkImageGaussianSmooth()
eye_retna_gaussian.SetStandardDeviation(2, 2, 2)
eye_retna_gaussian.SetRadiusFactors(2, 2, 2)
eye_retna_gaussian.SetInputConnection(eye_retna_shrinker.GetOutputPort())

eye_retna_iso = vtkFlyingEdges3D()
eye_retna_iso.SetInputConnection(eye_retna_gaussian.GetOutputPort())
eye_retna_iso.ComputeScalarsOff()
eye_retna_iso.ComputeGradientsOff()
eye_retna_iso.ComputeNormalsOff()
eye_retna_iso.SetValue(0, 127.5)
eye_retna_iso.Update()

eye_retna_tf = vtkTransformPolyDataFilter()
eye_retna_tf.SetTransform(slice_transforms["si"])
eye_retna_tf.SetInputConnection(eye_retna_iso.GetOutputPort())

eye_retna_smoother = vtkWindowedSincPolyDataFilter()
eye_retna_smoother.SetInputConnection(eye_retna_tf.GetOutputPort())
eye_retna_smoother.BoundarySmoothingOff()
eye_retna_smoother.FeatureEdgeSmoothingOff()
eye_retna_smoother.SetFeatureAngle(60)
eye_retna_smoother.SetPassBand(0.1)
eye_retna_smoother.NonManifoldSmoothingOn()
eye_retna_smoother.NormalizeCoordinatesOff()

eye_retna_normals = vtkPolyDataNormals()
eye_retna_normals.SetInputConnection(eye_retna_smoother.GetOutputPort())
eye_retna_normals.SetFeatureAngle(60)

eye_retna_stripper = vtkStripper()
eye_retna_stripper.SetInputConnection(eye_retna_normals.GetOutputPort())

eye_retna_mapper = vtkPolyDataMapper()
eye_retna_mapper.SetInputConnection(eye_retna_stripper.GetOutputPort())

eye_retna_actor = vtkActor()
eye_retna_actor.SetMapper(eye_retna_mapper)
eye_retna_actor.GetProperty().SetOpacity(1.0)
eye_retna_actor.GetProperty().SetDiffuseColor(color_lut.GetTableValue(4)[:3])
eye_retna_actor.GetProperty().SetSpecular(0.5)
eye_retna_actor.GetProperty().SetSpecularPower(10)
renderer.AddActor(eye_retna_actor)

# ---- eye_white (tissue 5) ----
eye_white_reader = vtkMetaImageReader()
eye_white_reader.SetFileName(str(mhd_files["frogtissue"]))
eye_white_reader.SetDataSpacing(1, 1, 1.5)
eye_white_reader.SetDataOrigin(-250.0, -235.0, 1.5)
eye_white_reader.SetDataExtent(389, 433, 187, 286, 1, 37)
eye_white_reader.Update()

eye_white_threshold = vtkImageThreshold()
eye_white_threshold.ThresholdBetween(5, 5)
eye_white_threshold.SetInValue(255)
eye_white_threshold.SetOutValue(0)
eye_white_threshold.SetInputConnection(eye_white_reader.GetOutputPort())

eye_white_shrinker = vtkImageShrink3D()
eye_white_shrinker.SetInputConnection(eye_white_threshold.GetOutputPort())
eye_white_shrinker.SetShrinkFactors(1, 1, 1)
eye_white_shrinker.AveragingOn()

eye_white_gaussian = vtkImageGaussianSmooth()
eye_white_gaussian.SetStandardDeviation(2, 2, 2)
eye_white_gaussian.SetRadiusFactors(2, 2, 2)
eye_white_gaussian.SetInputConnection(eye_white_shrinker.GetOutputPort())

eye_white_iso = vtkFlyingEdges3D()
eye_white_iso.SetInputConnection(eye_white_gaussian.GetOutputPort())
eye_white_iso.ComputeScalarsOff()
eye_white_iso.ComputeGradientsOff()
eye_white_iso.ComputeNormalsOff()
eye_white_iso.SetValue(0, 127.5)
eye_white_iso.Update()

eye_white_tf = vtkTransformPolyDataFilter()
eye_white_tf.SetTransform(slice_transforms["si"])
eye_white_tf.SetInputConnection(eye_white_iso.GetOutputPort())

eye_white_smoother = vtkWindowedSincPolyDataFilter()
eye_white_smoother.SetInputConnection(eye_white_tf.GetOutputPort())
eye_white_smoother.BoundarySmoothingOff()
eye_white_smoother.FeatureEdgeSmoothingOff()
eye_white_smoother.SetFeatureAngle(60)
eye_white_smoother.SetPassBand(0.1)
eye_white_smoother.NonManifoldSmoothingOn()
eye_white_smoother.NormalizeCoordinatesOff()

eye_white_normals = vtkPolyDataNormals()
eye_white_normals.SetInputConnection(eye_white_smoother.GetOutputPort())
eye_white_normals.SetFeatureAngle(60)

eye_white_stripper = vtkStripper()
eye_white_stripper.SetInputConnection(eye_white_normals.GetOutputPort())

eye_white_mapper = vtkPolyDataMapper()
eye_white_mapper.SetInputConnection(eye_white_stripper.GetOutputPort())

eye_white_actor = vtkActor()
eye_white_actor.SetMapper(eye_white_mapper)
eye_white_actor.GetProperty().SetOpacity(1.0)
eye_white_actor.GetProperty().SetDiffuseColor(color_lut.GetTableValue(5)[:3])
eye_white_actor.GetProperty().SetSpecular(0.5)
eye_white_actor.GetProperty().SetSpecularPower(10)
renderer.AddActor(eye_white_actor)

# ---- heart (tissue 6) ----
heart_reader = vtkMetaImageReader()
heart_reader.SetFileName(str(mhd_files["frogtissue"]))
heart_reader.SetDataSpacing(1, 1, 1.5)
heart_reader.SetDataOrigin(-250.0, -235.0, 73.5)
heart_reader.SetDataExtent(217, 299, 203, 283, 49, 93)
heart_reader.Update()

heart_threshold = vtkImageThreshold()
heart_threshold.ThresholdBetween(6, 6)
heart_threshold.SetInValue(255)
heart_threshold.SetOutValue(0)
heart_threshold.SetInputConnection(heart_reader.GetOutputPort())

heart_shrinker = vtkImageShrink3D()
heart_shrinker.SetInputConnection(heart_threshold.GetOutputPort())
heart_shrinker.SetShrinkFactors(1, 1, 1)
heart_shrinker.AveragingOn()

heart_gaussian = vtkImageGaussianSmooth()
heart_gaussian.SetStandardDeviation(2, 2, 2)
heart_gaussian.SetRadiusFactors(2, 2, 2)
heart_gaussian.SetInputConnection(heart_shrinker.GetOutputPort())

heart_iso = vtkFlyingEdges3D()
heart_iso.SetInputConnection(heart_gaussian.GetOutputPort())
heart_iso.ComputeScalarsOff()
heart_iso.ComputeGradientsOff()
heart_iso.ComputeNormalsOff()
heart_iso.SetValue(0, 127.5)
heart_iso.Update()

heart_tf = vtkTransformPolyDataFilter()
heart_tf.SetTransform(slice_transforms["si"])
heart_tf.SetInputConnection(heart_iso.GetOutputPort())

heart_smoother = vtkWindowedSincPolyDataFilter()
heart_smoother.SetInputConnection(heart_tf.GetOutputPort())
heart_smoother.BoundarySmoothingOff()
heart_smoother.FeatureEdgeSmoothingOff()
heart_smoother.SetFeatureAngle(60)
heart_smoother.SetPassBand(0.1)
heart_smoother.NonManifoldSmoothingOn()
heart_smoother.NormalizeCoordinatesOff()

heart_normals = vtkPolyDataNormals()
heart_normals.SetInputConnection(heart_smoother.GetOutputPort())
heart_normals.SetFeatureAngle(60)

heart_stripper = vtkStripper()
heart_stripper.SetInputConnection(heart_normals.GetOutputPort())

heart_mapper = vtkPolyDataMapper()
heart_mapper.SetInputConnection(heart_stripper.GetOutputPort())

heart_actor = vtkActor()
heart_actor.SetMapper(heart_mapper)
heart_actor.GetProperty().SetOpacity(1.0)
heart_actor.GetProperty().SetDiffuseColor(color_lut.GetTableValue(6)[:3])
heart_actor.GetProperty().SetSpecular(0.5)
heart_actor.GetProperty().SetSpecularPower(10)
renderer.AddActor(heart_actor)

# ---- ileum (tissue 7) ----
ileum_reader = vtkMetaImageReader()
ileum_reader.SetFileName(str(mhd_files["frogtissue"]))
ileum_reader.SetDataSpacing(1, 1, 1.5)
ileum_reader.SetDataOrigin(-250.0, -235.0, 37.5)
ileum_reader.SetDataExtent(172, 243, 179, 268, 25, 93)
ileum_reader.Update()

ileum_threshold = vtkImageThreshold()
ileum_threshold.ThresholdBetween(7, 7)
ileum_threshold.SetInValue(255)
ileum_threshold.SetOutValue(0)
ileum_threshold.SetInputConnection(ileum_reader.GetOutputPort())

ileum_shrinker = vtkImageShrink3D()
ileum_shrinker.SetInputConnection(ileum_threshold.GetOutputPort())
ileum_shrinker.SetShrinkFactors(1, 1, 1)
ileum_shrinker.AveragingOn()

ileum_gaussian = vtkImageGaussianSmooth()
ileum_gaussian.SetStandardDeviation(2, 2, 2)
ileum_gaussian.SetRadiusFactors(2, 2, 2)
ileum_gaussian.SetInputConnection(ileum_shrinker.GetOutputPort())

ileum_iso = vtkFlyingEdges3D()
ileum_iso.SetInputConnection(ileum_gaussian.GetOutputPort())
ileum_iso.ComputeScalarsOff()
ileum_iso.ComputeGradientsOff()
ileum_iso.ComputeNormalsOff()
ileum_iso.SetValue(0, 127.5)
ileum_iso.Update()

ileum_tf = vtkTransformPolyDataFilter()
ileum_tf.SetTransform(slice_transforms["si"])
ileum_tf.SetInputConnection(ileum_iso.GetOutputPort())

ileum_smoother = vtkWindowedSincPolyDataFilter()
ileum_smoother.SetInputConnection(ileum_tf.GetOutputPort())
ileum_smoother.BoundarySmoothingOff()
ileum_smoother.FeatureEdgeSmoothingOff()
ileum_smoother.SetFeatureAngle(60)
ileum_smoother.SetPassBand(0.1)
ileum_smoother.NonManifoldSmoothingOn()
ileum_smoother.NormalizeCoordinatesOff()

ileum_normals = vtkPolyDataNormals()
ileum_normals.SetInputConnection(ileum_smoother.GetOutputPort())
ileum_normals.SetFeatureAngle(60)

ileum_stripper = vtkStripper()
ileum_stripper.SetInputConnection(ileum_normals.GetOutputPort())

ileum_mapper = vtkPolyDataMapper()
ileum_mapper.SetInputConnection(ileum_stripper.GetOutputPort())

ileum_actor = vtkActor()
ileum_actor.SetMapper(ileum_mapper)
ileum_actor.GetProperty().SetOpacity(1.0)
ileum_actor.GetProperty().SetDiffuseColor(color_lut.GetTableValue(7)[:3])
ileum_actor.GetProperty().SetSpecular(0.5)
ileum_actor.GetProperty().SetSpecularPower(10)
renderer.AddActor(ileum_actor)

# ---- kidney (tissue 8) ----
kidney_reader = vtkMetaImageReader()
kidney_reader.SetFileName(str(mhd_files["frogtissue"]))
kidney_reader.SetDataSpacing(1, 1, 1.5)
kidney_reader.SetDataOrigin(-250.0, -235.0, 36.0)
kidney_reader.SetDataExtent(116, 238, 206, 276, 24, 78)
kidney_reader.Update()

kidney_threshold = vtkImageThreshold()
kidney_threshold.ThresholdBetween(8, 8)
kidney_threshold.SetInValue(255)
kidney_threshold.SetOutValue(0)
kidney_threshold.SetInputConnection(kidney_reader.GetOutputPort())

kidney_shrinker = vtkImageShrink3D()
kidney_shrinker.SetInputConnection(kidney_threshold.GetOutputPort())
kidney_shrinker.SetShrinkFactors(1, 1, 1)
kidney_shrinker.AveragingOn()

kidney_gaussian = vtkImageGaussianSmooth()
kidney_gaussian.SetStandardDeviation(2, 2, 2)
kidney_gaussian.SetRadiusFactors(2, 2, 2)
kidney_gaussian.SetInputConnection(kidney_shrinker.GetOutputPort())

kidney_iso = vtkFlyingEdges3D()
kidney_iso.SetInputConnection(kidney_gaussian.GetOutputPort())
kidney_iso.ComputeScalarsOff()
kidney_iso.ComputeGradientsOff()
kidney_iso.ComputeNormalsOff()
kidney_iso.SetValue(0, 127.5)
kidney_iso.Update()

kidney_tf = vtkTransformPolyDataFilter()
kidney_tf.SetTransform(slice_transforms["si"])
kidney_tf.SetInputConnection(kidney_iso.GetOutputPort())

kidney_smoother = vtkWindowedSincPolyDataFilter()
kidney_smoother.SetInputConnection(kidney_tf.GetOutputPort())
kidney_smoother.BoundarySmoothingOff()
kidney_smoother.FeatureEdgeSmoothingOff()
kidney_smoother.SetFeatureAngle(60)
kidney_smoother.SetPassBand(0.1)
kidney_smoother.NonManifoldSmoothingOn()
kidney_smoother.NormalizeCoordinatesOff()

kidney_normals = vtkPolyDataNormals()
kidney_normals.SetInputConnection(kidney_smoother.GetOutputPort())
kidney_normals.SetFeatureAngle(60)

kidney_stripper = vtkStripper()
kidney_stripper.SetInputConnection(kidney_normals.GetOutputPort())

kidney_mapper = vtkPolyDataMapper()
kidney_mapper.SetInputConnection(kidney_stripper.GetOutputPort())

kidney_actor = vtkActor()
kidney_actor.SetMapper(kidney_mapper)
kidney_actor.GetProperty().SetOpacity(1.0)
kidney_actor.GetProperty().SetDiffuseColor(color_lut.GetTableValue(8)[:3])
kidney_actor.GetProperty().SetSpecular(0.5)
kidney_actor.GetProperty().SetSpecularPower(10)
renderer.AddActor(kidney_actor)

# ---- l_intestine (tissue 9) ----
l_intestine_reader = vtkMetaImageReader()
l_intestine_reader.SetFileName(str(mhd_files["frogtissue"]))
l_intestine_reader.SetDataSpacing(1, 1, 1.5)
l_intestine_reader.SetDataOrigin(-250.0, -235.0, 84.0)
l_intestine_reader.SetDataExtent(115, 224, 185, 260, 56, 106)
l_intestine_reader.Update()

l_intestine_threshold = vtkImageThreshold()
l_intestine_threshold.ThresholdBetween(9, 9)
l_intestine_threshold.SetInValue(255)
l_intestine_threshold.SetOutValue(0)
l_intestine_threshold.SetInputConnection(l_intestine_reader.GetOutputPort())

l_intestine_shrinker = vtkImageShrink3D()
l_intestine_shrinker.SetInputConnection(l_intestine_threshold.GetOutputPort())
l_intestine_shrinker.SetShrinkFactors(1, 1, 1)
l_intestine_shrinker.AveragingOn()

l_intestine_gaussian = vtkImageGaussianSmooth()
l_intestine_gaussian.SetStandardDeviation(2, 2, 2)
l_intestine_gaussian.SetRadiusFactors(2, 2, 2)
l_intestine_gaussian.SetInputConnection(l_intestine_shrinker.GetOutputPort())

l_intestine_iso = vtkFlyingEdges3D()
l_intestine_iso.SetInputConnection(l_intestine_gaussian.GetOutputPort())
l_intestine_iso.ComputeScalarsOff()
l_intestine_iso.ComputeGradientsOff()
l_intestine_iso.ComputeNormalsOff()
l_intestine_iso.SetValue(0, 127.5)
l_intestine_iso.Update()

l_intestine_tf = vtkTransformPolyDataFilter()
l_intestine_tf.SetTransform(slice_transforms["si"])
l_intestine_tf.SetInputConnection(l_intestine_iso.GetOutputPort())

l_intestine_smoother = vtkWindowedSincPolyDataFilter()
l_intestine_smoother.SetInputConnection(l_intestine_tf.GetOutputPort())
l_intestine_smoother.BoundarySmoothingOff()
l_intestine_smoother.FeatureEdgeSmoothingOff()
l_intestine_smoother.SetFeatureAngle(60)
l_intestine_smoother.SetPassBand(0.1)
l_intestine_smoother.NonManifoldSmoothingOn()
l_intestine_smoother.NormalizeCoordinatesOff()

l_intestine_normals = vtkPolyDataNormals()
l_intestine_normals.SetInputConnection(l_intestine_smoother.GetOutputPort())
l_intestine_normals.SetFeatureAngle(60)

l_intestine_stripper = vtkStripper()
l_intestine_stripper.SetInputConnection(l_intestine_normals.GetOutputPort())

l_intestine_mapper = vtkPolyDataMapper()
l_intestine_mapper.SetInputConnection(l_intestine_stripper.GetOutputPort())

l_intestine_actor = vtkActor()
l_intestine_actor.SetMapper(l_intestine_mapper)
l_intestine_actor.GetProperty().SetOpacity(1.0)
l_intestine_actor.GetProperty().SetDiffuseColor(color_lut.GetTableValue(9)[:3])
l_intestine_actor.GetProperty().SetSpecular(0.5)
l_intestine_actor.GetProperty().SetSpecularPower(10)
renderer.AddActor(l_intestine_actor)

# ---- liver (tissue 10) ----
liver_reader = vtkMetaImageReader()
liver_reader.SetFileName(str(mhd_files["frogtissue"]))
liver_reader.SetDataSpacing(1, 1, 1.5)
liver_reader.SetDataOrigin(-250.0, -235.0, 37.5)
liver_reader.SetDataExtent(167, 297, 165, 315, 25, 126)
liver_reader.Update()

liver_threshold = vtkImageThreshold()
liver_threshold.ThresholdBetween(10, 10)
liver_threshold.SetInValue(255)
liver_threshold.SetOutValue(0)
liver_threshold.SetInputConnection(liver_reader.GetOutputPort())

liver_shrinker = vtkImageShrink3D()
liver_shrinker.SetInputConnection(liver_threshold.GetOutputPort())
liver_shrinker.SetShrinkFactors(1, 1, 1)
liver_shrinker.AveragingOn()

liver_gaussian = vtkImageGaussianSmooth()
liver_gaussian.SetStandardDeviation(2, 2, 2)
liver_gaussian.SetRadiusFactors(2, 2, 2)
liver_gaussian.SetInputConnection(liver_shrinker.GetOutputPort())

liver_iso = vtkFlyingEdges3D()
liver_iso.SetInputConnection(liver_gaussian.GetOutputPort())
liver_iso.ComputeScalarsOff()
liver_iso.ComputeGradientsOff()
liver_iso.ComputeNormalsOff()
liver_iso.SetValue(0, 127.5)
liver_iso.Update()

liver_tf = vtkTransformPolyDataFilter()
liver_tf.SetTransform(slice_transforms["si"])
liver_tf.SetInputConnection(liver_iso.GetOutputPort())

liver_smoother = vtkWindowedSincPolyDataFilter()
liver_smoother.SetInputConnection(liver_tf.GetOutputPort())
liver_smoother.BoundarySmoothingOff()
liver_smoother.FeatureEdgeSmoothingOff()
liver_smoother.SetFeatureAngle(60)
liver_smoother.SetPassBand(0.1)
liver_smoother.NonManifoldSmoothingOn()
liver_smoother.NormalizeCoordinatesOff()

liver_normals = vtkPolyDataNormals()
liver_normals.SetInputConnection(liver_smoother.GetOutputPort())
liver_normals.SetFeatureAngle(60)

liver_stripper = vtkStripper()
liver_stripper.SetInputConnection(liver_normals.GetOutputPort())

liver_mapper = vtkPolyDataMapper()
liver_mapper.SetInputConnection(liver_stripper.GetOutputPort())

liver_actor = vtkActor()
liver_actor.SetMapper(liver_mapper)
liver_actor.GetProperty().SetOpacity(1.0)
liver_actor.GetProperty().SetDiffuseColor(color_lut.GetTableValue(10)[:3])
liver_actor.GetProperty().SetSpecular(0.5)
liver_actor.GetProperty().SetSpecularPower(10)
renderer.AddActor(liver_actor)

# ---- lung (tissue 11) ----
lung_reader = vtkMetaImageReader()
lung_reader.SetFileName(str(mhd_files["frogtissue"]))
lung_reader.SetDataSpacing(1, 1, 1.5)
lung_reader.SetDataOrigin(-250.0, -235.0, 36.0)
lung_reader.SetDataExtent(222, 324, 178, 312, 24, 59)
lung_reader.Update()

lung_threshold = vtkImageThreshold()
lung_threshold.ThresholdBetween(11, 11)
lung_threshold.SetInValue(255)
lung_threshold.SetOutValue(0)
lung_threshold.SetInputConnection(lung_reader.GetOutputPort())

lung_shrinker = vtkImageShrink3D()
lung_shrinker.SetInputConnection(lung_threshold.GetOutputPort())
lung_shrinker.SetShrinkFactors(1, 1, 1)
lung_shrinker.AveragingOn()

lung_gaussian = vtkImageGaussianSmooth()
lung_gaussian.SetStandardDeviation(2, 2, 2)
lung_gaussian.SetRadiusFactors(2, 2, 2)
lung_gaussian.SetInputConnection(lung_shrinker.GetOutputPort())

lung_iso = vtkFlyingEdges3D()
lung_iso.SetInputConnection(lung_gaussian.GetOutputPort())
lung_iso.ComputeScalarsOff()
lung_iso.ComputeGradientsOff()
lung_iso.ComputeNormalsOff()
lung_iso.SetValue(0, 127.5)
lung_iso.Update()

lung_tf = vtkTransformPolyDataFilter()
lung_tf.SetTransform(slice_transforms["si"])
lung_tf.SetInputConnection(lung_iso.GetOutputPort())

lung_smoother = vtkWindowedSincPolyDataFilter()
lung_smoother.SetInputConnection(lung_tf.GetOutputPort())
lung_smoother.BoundarySmoothingOff()
lung_smoother.FeatureEdgeSmoothingOff()
lung_smoother.SetFeatureAngle(60)
lung_smoother.SetPassBand(0.1)
lung_smoother.NonManifoldSmoothingOn()
lung_smoother.NormalizeCoordinatesOff()

lung_normals = vtkPolyDataNormals()
lung_normals.SetInputConnection(lung_smoother.GetOutputPort())
lung_normals.SetFeatureAngle(60)

lung_stripper = vtkStripper()
lung_stripper.SetInputConnection(lung_normals.GetOutputPort())

lung_mapper = vtkPolyDataMapper()
lung_mapper.SetInputConnection(lung_stripper.GetOutputPort())

lung_actor = vtkActor()
lung_actor.SetMapper(lung_mapper)
lung_actor.GetProperty().SetOpacity(1.0)
lung_actor.GetProperty().SetDiffuseColor(color_lut.GetTableValue(11)[:3])
lung_actor.GetProperty().SetSpecular(0.5)
lung_actor.GetProperty().SetSpecularPower(10)
renderer.AddActor(lung_actor)

# ---- nerve (tissue 12) ----
nerve_reader = vtkMetaImageReader()
nerve_reader.SetFileName(str(mhd_files["frogtissue"]))
nerve_reader.SetDataSpacing(1, 1, 1.5)
nerve_reader.SetDataOrigin(-250.0, -235.0, 10.5)
nerve_reader.SetDataExtent(79, 403, 75, 406, 7, 113)
nerve_reader.Update()

nerve_threshold = vtkImageThreshold()
nerve_threshold.ThresholdBetween(12, 12)
nerve_threshold.SetInValue(255)
nerve_threshold.SetOutValue(0)
nerve_threshold.SetInputConnection(nerve_reader.GetOutputPort())

nerve_shrinker = vtkImageShrink3D()
nerve_shrinker.SetInputConnection(nerve_threshold.GetOutputPort())
nerve_shrinker.SetShrinkFactors(1, 1, 1)
nerve_shrinker.AveragingOn()

nerve_gaussian = vtkImageGaussianSmooth()
nerve_gaussian.SetStandardDeviation(2, 2, 2)
nerve_gaussian.SetRadiusFactors(2, 2, 2)
nerve_gaussian.SetInputConnection(nerve_shrinker.GetOutputPort())

nerve_iso = vtkFlyingEdges3D()
nerve_iso.SetInputConnection(nerve_gaussian.GetOutputPort())
nerve_iso.ComputeScalarsOff()
nerve_iso.ComputeGradientsOff()
nerve_iso.ComputeNormalsOff()
nerve_iso.SetValue(0, 127.5)
nerve_iso.Update()

nerve_tf = vtkTransformPolyDataFilter()
nerve_tf.SetTransform(slice_transforms["si"])
nerve_tf.SetInputConnection(nerve_iso.GetOutputPort())

nerve_smoother = vtkWindowedSincPolyDataFilter()
nerve_smoother.SetInputConnection(nerve_tf.GetOutputPort())
nerve_smoother.BoundarySmoothingOff()
nerve_smoother.FeatureEdgeSmoothingOff()
nerve_smoother.SetFeatureAngle(60)
nerve_smoother.SetPassBand(0.1)
nerve_smoother.NonManifoldSmoothingOn()
nerve_smoother.NormalizeCoordinatesOff()

nerve_normals = vtkPolyDataNormals()
nerve_normals.SetInputConnection(nerve_smoother.GetOutputPort())
nerve_normals.SetFeatureAngle(60)

nerve_stripper = vtkStripper()
nerve_stripper.SetInputConnection(nerve_normals.GetOutputPort())

nerve_mapper = vtkPolyDataMapper()
nerve_mapper.SetInputConnection(nerve_stripper.GetOutputPort())

nerve_actor = vtkActor()
nerve_actor.SetMapper(nerve_mapper)
nerve_actor.GetProperty().SetOpacity(1.0)
nerve_actor.GetProperty().SetDiffuseColor(color_lut.GetTableValue(12)[:3])
nerve_actor.GetProperty().SetSpecular(0.5)
nerve_actor.GetProperty().SetSpecularPower(10)
renderer.AddActor(nerve_actor)

# ---- skeleton (tissue 13) ----
skeleton_reader = vtkMetaImageReader()
skeleton_reader.SetFileName(str(mhd_files["frogtissue"]))
skeleton_reader.SetDataSpacing(1, 1, 1.5)
skeleton_reader.SetDataOrigin(-250.0, -235.0, 1.5)
skeleton_reader.SetDataExtent(23, 479, 0, 461, 1, 136)
skeleton_reader.Update()

skeleton_threshold = vtkImageThreshold()
skeleton_threshold.ThresholdBetween(13, 13)
skeleton_threshold.SetInValue(255)
skeleton_threshold.SetOutValue(0)
skeleton_threshold.SetInputConnection(skeleton_reader.GetOutputPort())

skeleton_shrinker = vtkImageShrink3D()
skeleton_shrinker.SetInputConnection(skeleton_threshold.GetOutputPort())
skeleton_shrinker.SetShrinkFactors(1, 1, 1)
skeleton_shrinker.AveragingOn()

skeleton_gaussian = vtkImageGaussianSmooth()
skeleton_gaussian.SetStandardDeviation(1.5, 1.5, 1)
skeleton_gaussian.SetRadiusFactors(2, 2, 2)
skeleton_gaussian.SetInputConnection(skeleton_shrinker.GetOutputPort())

skeleton_iso = vtkFlyingEdges3D()
skeleton_iso.SetInputConnection(skeleton_gaussian.GetOutputPort())
skeleton_iso.ComputeScalarsOff()
skeleton_iso.ComputeGradientsOff()
skeleton_iso.ComputeNormalsOff()
skeleton_iso.SetValue(0, 64.5)
skeleton_iso.Update()

skeleton_tf = vtkTransformPolyDataFilter()
skeleton_tf.SetTransform(slice_transforms["si"])
skeleton_tf.SetInputConnection(skeleton_iso.GetOutputPort())

skeleton_smoother = vtkWindowedSincPolyDataFilter()
skeleton_smoother.SetInputConnection(skeleton_tf.GetOutputPort())
skeleton_smoother.BoundarySmoothingOff()
skeleton_smoother.FeatureEdgeSmoothingOff()
skeleton_smoother.SetFeatureAngle(60)
skeleton_smoother.SetPassBand(0.1)
skeleton_smoother.NonManifoldSmoothingOn()
skeleton_smoother.NormalizeCoordinatesOff()

skeleton_normals = vtkPolyDataNormals()
skeleton_normals.SetInputConnection(skeleton_smoother.GetOutputPort())
skeleton_normals.SetFeatureAngle(60)

skeleton_stripper = vtkStripper()
skeleton_stripper.SetInputConnection(skeleton_normals.GetOutputPort())

skeleton_mapper = vtkPolyDataMapper()
skeleton_mapper.SetInputConnection(skeleton_stripper.GetOutputPort())

skeleton_actor = vtkActor()
skeleton_actor.SetMapper(skeleton_mapper)
skeleton_actor.GetProperty().SetOpacity(1.0)
skeleton_actor.GetProperty().SetDiffuseColor(color_lut.GetTableValue(13)[:3])
skeleton_actor.GetProperty().SetSpecular(0.5)
skeleton_actor.GetProperty().SetSpecularPower(10)
renderer.AddActor(skeleton_actor)

# ---- spleen (tissue 14) ----
spleen_reader = vtkMetaImageReader()
spleen_reader.SetFileName(str(mhd_files["frogtissue"]))
spleen_reader.SetDataSpacing(1, 1, 1.5)
spleen_reader.SetDataOrigin(-250.0, -235.0, 67.5)
spleen_reader.SetDataExtent(166, 219, 238, 274, 45, 68)
spleen_reader.Update()

spleen_threshold = vtkImageThreshold()
spleen_threshold.ThresholdBetween(14, 14)
spleen_threshold.SetInValue(255)
spleen_threshold.SetOutValue(0)
spleen_threshold.SetInputConnection(spleen_reader.GetOutputPort())

spleen_shrinker = vtkImageShrink3D()
spleen_shrinker.SetInputConnection(spleen_threshold.GetOutputPort())
spleen_shrinker.SetShrinkFactors(1, 1, 1)
spleen_shrinker.AveragingOn()

spleen_gaussian = vtkImageGaussianSmooth()
spleen_gaussian.SetStandardDeviation(2, 2, 2)
spleen_gaussian.SetRadiusFactors(2, 2, 2)
spleen_gaussian.SetInputConnection(spleen_shrinker.GetOutputPort())

spleen_iso = vtkFlyingEdges3D()
spleen_iso.SetInputConnection(spleen_gaussian.GetOutputPort())
spleen_iso.ComputeScalarsOff()
spleen_iso.ComputeGradientsOff()
spleen_iso.ComputeNormalsOff()
spleen_iso.SetValue(0, 127.5)
spleen_iso.Update()

spleen_tf = vtkTransformPolyDataFilter()
spleen_tf.SetTransform(slice_transforms["si"])
spleen_tf.SetInputConnection(spleen_iso.GetOutputPort())

spleen_smoother = vtkWindowedSincPolyDataFilter()
spleen_smoother.SetInputConnection(spleen_tf.GetOutputPort())
spleen_smoother.BoundarySmoothingOff()
spleen_smoother.FeatureEdgeSmoothingOff()
spleen_smoother.SetFeatureAngle(60)
spleen_smoother.SetPassBand(0.1)
spleen_smoother.NonManifoldSmoothingOn()
spleen_smoother.NormalizeCoordinatesOff()

spleen_normals = vtkPolyDataNormals()
spleen_normals.SetInputConnection(spleen_smoother.GetOutputPort())
spleen_normals.SetFeatureAngle(60)

spleen_stripper = vtkStripper()
spleen_stripper.SetInputConnection(spleen_normals.GetOutputPort())

spleen_mapper = vtkPolyDataMapper()
spleen_mapper.SetInputConnection(spleen_stripper.GetOutputPort())

spleen_actor = vtkActor()
spleen_actor.SetMapper(spleen_mapper)
spleen_actor.GetProperty().SetOpacity(1.0)
spleen_actor.GetProperty().SetDiffuseColor(color_lut.GetTableValue(14)[:3])
spleen_actor.GetProperty().SetSpecular(0.5)
spleen_actor.GetProperty().SetSpecularPower(10)
renderer.AddActor(spleen_actor)

# ---- stomach (tissue 15) ----
stomach_reader = vtkMetaImageReader()
stomach_reader.SetFileName(str(mhd_files["frogtissue"]))
stomach_reader.SetDataSpacing(1, 1, 1.5)
stomach_reader.SetDataOrigin(-250.0, -235.0, 39.0)
stomach_reader.SetDataExtent(143, 365, 172, 311, 26, 119)
stomach_reader.Update()

stomach_threshold = vtkImageThreshold()
stomach_threshold.ThresholdBetween(15, 15)
stomach_threshold.SetInValue(255)
stomach_threshold.SetOutValue(0)
stomach_threshold.SetInputConnection(stomach_reader.GetOutputPort())

stomach_shrinker = vtkImageShrink3D()
stomach_shrinker.SetInputConnection(stomach_threshold.GetOutputPort())
stomach_shrinker.SetShrinkFactors(1, 1, 1)
stomach_shrinker.AveragingOn()

stomach_gaussian = vtkImageGaussianSmooth()
stomach_gaussian.SetStandardDeviation(2, 2, 2)
stomach_gaussian.SetRadiusFactors(2, 2, 2)
stomach_gaussian.SetInputConnection(stomach_shrinker.GetOutputPort())

stomach_iso = vtkFlyingEdges3D()
stomach_iso.SetInputConnection(stomach_gaussian.GetOutputPort())
stomach_iso.ComputeScalarsOff()
stomach_iso.ComputeGradientsOff()
stomach_iso.ComputeNormalsOff()
stomach_iso.SetValue(0, 127.5)
stomach_iso.Update()

stomach_tf = vtkTransformPolyDataFilter()
stomach_tf.SetTransform(slice_transforms["si"])
stomach_tf.SetInputConnection(stomach_iso.GetOutputPort())

stomach_smoother = vtkWindowedSincPolyDataFilter()
stomach_smoother.SetInputConnection(stomach_tf.GetOutputPort())
stomach_smoother.BoundarySmoothingOff()
stomach_smoother.FeatureEdgeSmoothingOff()
stomach_smoother.SetFeatureAngle(60)
stomach_smoother.SetPassBand(0.1)
stomach_smoother.NonManifoldSmoothingOn()
stomach_smoother.NormalizeCoordinatesOff()

stomach_normals = vtkPolyDataNormals()
stomach_normals.SetInputConnection(stomach_smoother.GetOutputPort())
stomach_normals.SetFeatureAngle(60)

stomach_stripper = vtkStripper()
stomach_stripper.SetInputConnection(stomach_normals.GetOutputPort())

stomach_mapper = vtkPolyDataMapper()
stomach_mapper.SetInputConnection(stomach_stripper.GetOutputPort())

stomach_actor = vtkActor()
stomach_actor.SetMapper(stomach_mapper)
stomach_actor.GetProperty().SetOpacity(1.0)
stomach_actor.GetProperty().SetDiffuseColor(color_lut.GetTableValue(15)[:3])
stomach_actor.GetProperty().SetSpecular(0.5)
stomach_actor.GetProperty().SetSpecularPower(10)
renderer.AddActor(stomach_actor)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("froggie surface")
render_window.SetMultiSamples(0)
render_window.SetSize(1024, 1024)

# Scene: configure camera
camera = renderer.GetActiveCamera()
cam_transform = vtkTransform()
cam_transform.SetMatrix(camera.GetModelTransformMatrix())
cam_transform.RotateY(-90)
cam_transform.RotateZ(90)
camera.SetModelTransformMatrix(cam_transform.GetMatrix())
renderer.ResetCamera()

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)
style = vtkInteractorStyleTrackballCamera()
render_window_interactor.SetInteractorStyle(style)

# CameraOrientationWidget: interactive orientation gizmo
cow = vtkCameraOrientationWidget()
cow.SetParentRenderer(renderer)
cow.SetInteractor(render_window_interactor)
cow.On()
cow.EnabledOn()

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
