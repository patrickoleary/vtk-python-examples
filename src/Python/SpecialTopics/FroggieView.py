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

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.SetBackground(paraview_bkg_rgb)

# Build a tissue actor for each tissue, with opacity slider
slider_widgets = {}
left_pos_y = 0.275
left_step = 1.0 / 9
right_pos_y = 0.05
right_step = 1.0 / 9
slider_count = 0

for tissue in tissue_names:
    # ---- Reader: load the preprocessed VTK polydata ----
    reader = vtkPolyDataReader()
    reader.SetFileName(vtk_files[tissue])
    reader.Update()

    # ---- Transform: orient according to slice order, then scale for VTK view ----
    trans = vtkTransform()
    trans.DeepCopy(slice_transforms[tissue_orientation[tissue]])
    trans.Scale(1, -1, -1)

    tf = vtkTransformPolyDataFilter()
    tf.SetInputConnection(reader.GetOutputPort())
    tf.SetTransform(trans)

    # ---- PolyDataNormals: recompute normals after transform ----
    normals = vtkPolyDataNormals()
    normals.SetInputConnection(tf.GetOutputPort())
    normals.SetFeatureAngle(60.0)

    # ---- Mapper: map polygon data to graphics primitives ----
    mapper = vtkPolyDataMapper()
    mapper.SetInputConnection(normals.GetOutputPort())

    # ---- Actor: assign the mapped geometry ----
    actor = vtkActor()
    actor.SetMapper(mapper)
    actor.GetProperty().SetOpacity(tissue_opacity[tissue])
    actor.GetProperty().SetDiffuseColor(color_lut.GetTableValue(tissue_indices[tissue])[:3])
    actor.GetProperty().SetSpecular(0.2)
    actor.GetProperty().SetSpecularPower(10)
    renderer.AddActor(actor)

    # ---- SliderWidget: opacity control for this tissue ----
    slider_rep = vtkSliderRepresentation2D()
    slider_rep.SetMinimumValue(0.0)
    slider_rep.SetMaximumValue(1.0)
    slider_rep.SetValue(tissue_opacity[tissue])
    slider_rep.SetTitleText(tissue)
    slider_rep.SetTubeWidth(0.004)
    slider_rep.SetSliderLength(0.015)
    slider_rep.SetSliderWidth(0.008)
    slider_rep.SetEndCapLength(0.008)
    slider_rep.SetEndCapWidth(0.02)
    slider_rep.SetTitleHeight(0.02)
    slider_rep.SetLabelHeight(0.02)

    if slider_count < 7:
        x0, x1, y = 0.02, 0.18, left_pos_y
        left_pos_y += left_step
    else:
        x0, x1, y = 0.82, 0.98, right_pos_y
        right_pos_y += right_step

    slider_rep.GetPoint1Coordinate().SetCoordinateSystemToNormalizedDisplay()
    slider_rep.GetPoint1Coordinate().SetValue(x0, y)
    slider_rep.GetPoint2Coordinate().SetCoordinateSystemToNormalizedDisplay()
    slider_rep.GetPoint2Coordinate().SetValue(x1, y)

    slider_rep.GetTubeProperty().SetColor(black_rgb)
    slider_rep.GetCapProperty().SetColor(indigo_rgb)
    slider_rep.GetSliderProperty().SetColor(burlywood_rgb)
    slider_rep.GetSelectedProperty().SetColor(lime_rgb)
    slider_rep.GetLabelProperty().SetColor(dark_slate_gray_rgb)
    idx = tissue_indices[tissue]
    if 0 <= idx < 16:
        slider_rep.GetTitleProperty().SetColor(color_lut.GetTableValue(idx)[:3])
        slider_rep.GetTitleProperty().ShadowOff()
    else:
        slider_rep.GetTitleProperty().SetColor(black_rgb)

    sw = vtkSliderWidget()
    sw.SetRepresentation(slider_rep)
    sw.SetAnimationModeToAnimate()

    actor_prop = actor.GetProperty()
    sw.AddObserver(vtkCommand.InteractionEvent,
                   lambda caller, ev, prop=actor_prop: prop.SetOpacity(
                       caller.GetRepresentation().GetValue()))

    slider_widgets[tissue] = sw
    slider_count += 1

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
cow.Off()
cow.EnabledOff()

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.SetSize(1024 + 400, 1024)
render_window.SetWindowName("FroggieView")
render_window.AddRenderer(renderer)

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)
style = vtkInteractorStyleTrackballCamera()
render_window_interactor.SetInteractorStyle(style)

# Enable slider widgets
for sw in slider_widgets.values():
    sw.SetInteractor(render_window_interactor)
    sw.EnabledOn()

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
