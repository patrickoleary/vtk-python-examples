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
from vtkmodules.vtkImagingMorphological import vtkImageIslandRemoval2D
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

# Build a tissue actor for each tissue and add to the renderer
for name in tissue_names:
    tissue = tissue_params[name]
    pixel_size = tissue["pixel_size"]
    spacing = tissue["spacing"]
    start_slice = tissue["start_slice"]
    data_spacing = [pixel_size, pixel_size, spacing]
    columns = tissue["columns"]
    rows = tissue["rows"]
    data_origin = [-(columns / 2.0) * pixel_size, -(rows / 2.0) * pixel_size, start_slice * spacing]
    voi = [
        tissue["start_column"], tissue["end_column"],
        tissue["start_row"], tissue["end_row"],
        tissue["start_slice"], tissue["end_slice"],
    ]
    tmp = voi[2]
    voi[2] = rows - voi[3] - 1
    voi[3] = rows - tmp - 1

    fn = mhd_files["frog"] if name == "skin" else mhd_files["frogtissue"]

    # ---- Reader: load the volume data ----
    reader = vtkMetaImageReader()
    reader.SetFileName(str(fn))
    reader.SetDataSpacing(data_spacing)
    reader.SetDataOrigin(data_origin)
    reader.SetDataExtent(voi)
    reader.Update()

    last_connection = reader

    if name != "skin":
        # ---- IslandRemoval: remove small isolated regions ----
        if tissue["island_replace"] >= 0:
            island_remover = vtkImageIslandRemoval2D()
            island_remover.SetAreaThreshold(tissue["island_area"])
            island_remover.SetIslandValue(tissue["island_replace"])
            island_remover.SetReplaceValue(tissue["tissue"])
            island_remover.SetInput(last_connection.GetOutput())
            island_remover.Update()
            last_connection = island_remover

        # ---- ImageThreshold: isolate the tissue label ----
        select_tissue = vtkImageThreshold()
        select_tissue.ThresholdBetween(tissue["tissue"], tissue["tissue"])
        select_tissue.SetInValue(255)
        select_tissue.SetOutValue(0)
        select_tissue.SetInputConnection(last_connection.GetOutputPort())
        last_connection = select_tissue

    # ---- ImageShrink3D: downsample the volume ----
    sample_rate = [tissue["sample_rate_column"], tissue["sample_rate_row"], tissue["sample_rate_slice"]]
    shrinker = vtkImageShrink3D()
    shrinker.SetInputConnection(last_connection.GetOutputPort())
    shrinker.SetShrinkFactors(sample_rate)
    shrinker.AveragingOn()
    last_connection = shrinker

    # ---- ImageGaussianSmooth: blur the volume before contouring ----
    gsd = [
        tissue["gaussian_standard_deviation_column"],
        tissue["gaussian_standard_deviation_row"],
        tissue["gaussian_standard_deviation_slice"],
    ]
    if not all(v == 0 for v in gsd):
        grf = [
            tissue["gaussian_radius_factor_column"],
            tissue["gaussian_radius_factor_row"],
            tissue["gaussian_radius_factor_slice"],
        ]
        gaussian = vtkImageGaussianSmooth()
        gaussian.SetStandardDeviation(*gsd)
        gaussian.SetRadiusFactors(*grf)
        gaussian.SetInputConnection(shrinker.GetOutputPort())
        last_connection = gaussian

    # ---- FlyingEdges3D: extract the iso-surface ----
    iso_value = tissue["value"]
    iso_surface = vtkFlyingEdges3D()
    iso_surface.SetInputConnection(last_connection.GetOutputPort())
    iso_surface.ComputeScalarsOff()
    iso_surface.ComputeGradientsOff()
    iso_surface.ComputeNormalsOff()
    iso_surface.SetValue(0, iso_value)
    iso_surface.Update()

    # ---- TransformPolyDataFilter: orient according to slice order ----
    transform = slice_transforms[tissue["slice_order"]]
    tf = vtkTransformPolyDataFilter()
    tf.SetTransform(transform)
    tf.SetInputConnection(iso_surface.GetOutputPort())
    last_connection = tf

    # ---- WindowedSincPolyDataFilter: smooth the mesh ----
    smooth_iterations = tissue["smooth_iterations"]
    if smooth_iterations != 0:
        smoother = vtkWindowedSincPolyDataFilter()
        smoother.SetInputConnection(last_connection.GetOutputPort())
        smoother.BoundarySmoothingOff()
        smoother.FeatureEdgeSmoothingOff()
        smoother.SetFeatureAngle(tissue["smooth_angle"])
        smoother.SetPassBand(tissue["smooth_factor"])
        smoother.NonManifoldSmoothingOn()
        smoother.NormalizeCoordinatesOff()
        last_connection = smoother

    # ---- PolyDataNormals: recompute normals ----
    normals = vtkPolyDataNormals()
    normals.SetInputConnection(last_connection.GetOutputPort())
    normals.SetFeatureAngle(tissue["feature_angle"])

    # ---- Stripper: create triangle strips ----
    stripper = vtkStripper()
    stripper.SetInputConnection(normals.GetOutputPort())

    # ---- Mapper: map polygon data to graphics primitives ----
    mapper = vtkPolyDataMapper()
    mapper.SetInputConnection(stripper.GetOutputPort())

    # ---- Actor: assign the mapped geometry ----
    actor = vtkActor()
    actor.SetMapper(mapper)
    actor.GetProperty().SetOpacity(tissue["opacity"])
    actor.GetProperty().SetDiffuseColor(color_lut.GetTableValue(tissue["tissue"])[:3])
    actor.GetProperty().SetSpecular(0.5)
    actor.GetProperty().SetSpecularPower(10)
    renderer.AddActor(actor)

# Camera: default posterior view (looking down, superior faces top of screen)
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
cow.On()
cow.EnabledOn()

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.SetSize(1024, 1024)
render_window.SetWindowName("FroggieSurface")
render_window.AddRenderer(renderer)

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)
style = vtkInteractorStyleTrackballCamera()
render_window_interactor.SetInteractorStyle(style)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
