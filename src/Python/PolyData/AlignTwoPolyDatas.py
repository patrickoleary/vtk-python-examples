#!/usr/bin/env python

# Align two polydata meshes (cow.vtp → cowHead.vtp) using OBB-based landmark
# alignment followed by Iterative Closest Point refinement.

import math
import os
from pathlib import Path

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkCommonCore import (
    VTK_DOUBLE_MAX,
    vtkPoints,
)
from vtkmodules.vtkCommonDataModel import (
    vtkIterativeClosestPointTransform,
    vtkPolyData,
)
from vtkmodules.vtkCommonTransforms import (
    vtkLandmarkTransform,
    vtkTransform,
)
from vtkmodules.vtkFiltersGeneral import (
    vtkOBBTree,
    vtkTransformPolyDataFilter,
)
from vtkmodules.vtkFiltersModeling import vtkHausdorffDistancePointSetFilter
from vtkmodules.vtkIOXML import vtkXMLPolyDataReader
from vtkmodules.vtkInteractionWidgets import vtkCameraOrientationWidget
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkDataSetMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
white_rgb = (1.000, 1.000, 1.000)
tomato_rgb = (1.000, 0.388, 0.278)
sea_green_light_rgb = (0.125, 0.698, 0.667)

# Data files
data_dir = Path(os.environ.get("VPE_DATA_DIR", Path(__file__).parent))
src_file = str(data_dir / "cow.vtp")
tgt_file = str(data_dir / "cowHead.vtp")

# Reader: source mesh
src_reader = vtkXMLPolyDataReader()
src_reader.SetFileName(src_file)
src_reader.Update()
source_polydata = src_reader.GetOutput()

# Keep a copy of the original source
original_source_polydata = vtkPolyData()
original_source_polydata.DeepCopy(source_polydata)

# Reader: target mesh
tgt_reader = vtkXMLPolyDataReader()
tgt_reader.SetFileName(tgt_file)
tgt_reader.Update()
target_polydata = tgt_reader.GetOutput()

# --- Hausdorff distance before any alignment ---
distance = vtkHausdorffDistancePointSetFilter()
distance.SetInputData(0, target_polydata)
distance.SetInputData(1, source_polydata)
distance.Update()
distance_before_align = (
    distance.GetOutput(0).GetFieldData().GetArray("HausdorffDistance").GetComponent(0, 0)
)

# --- OBB-based alignment ---
# Build OBB trees for source and target
source_obb_tree = vtkOBBTree()
source_obb_tree.SetDataSet(source_polydata)
source_obb_tree.SetMaxLevel(1)
source_obb_tree.BuildLocator()

target_obb_tree = vtkOBBTree()
target_obb_tree.SetDataSet(target_polydata)
target_obb_tree.SetMaxLevel(1)
target_obb_tree.BuildLocator()

source_landmarks = vtkPolyData()
source_obb_tree.GenerateRepresentation(0, source_landmarks)

target_landmarks = vtkPolyData()
target_obb_tree.GenerateRepresentation(0, target_landmarks)

# Try rotations about X, Y, Z to find the best OBB alignment
obb_lm_transform = vtkLandmarkTransform()
obb_lm_transform.SetModeToSimilarity()
obb_lm_transform.SetTargetLandmarks(target_landmarks.GetPoints())

best_obb_distance = VTK_DOUBLE_MAX
best_obb_points = vtkPoints()

hausdorff = vtkHausdorffDistancePointSetFilter()
test_transform = vtkTransform()
test_transform_pd = vtkTransformPolyDataFilter()
obb_lm = vtkLandmarkTransform()
obb_lm.SetModeToSimilarity()
obb_lm.SetTargetLandmarks(target_landmarks.GetPoints())
obb_lm_pd = vtkTransformPolyDataFilter()

source_center = source_landmarks.GetCenter()

for axis in ("X", "Y", "Z"):
    for i in range(4):
        angle = 90.0 * i
        test_transform.Identity()
        test_transform.Translate(source_center[0], source_center[1], source_center[2])
        if axis == "X":
            test_transform.RotateX(angle)
        elif axis == "Y":
            test_transform.RotateY(angle)
        else:
            test_transform.RotateZ(angle)
        test_transform.Translate(-source_center[0], -source_center[1], -source_center[2])

        test_transform_pd.SetTransform(test_transform)
        test_transform_pd.SetInputData(source_landmarks)
        test_transform_pd.Update()

        obb_lm.SetSourceLandmarks(test_transform_pd.GetOutput().GetPoints())
        obb_lm.Modified()

        obb_lm_pd.SetInputData(source_polydata)
        obb_lm_pd.SetTransform(obb_lm)
        obb_lm_pd.Update()

        hausdorff.SetInputData(0, target_polydata)
        hausdorff.SetInputData(1, obb_lm_pd.GetOutput())
        hausdorff.Update()

        test_dist = (
            hausdorff.GetOutput(0).GetFieldData().GetArray("HausdorffDistance").GetComponent(0, 0)
        )
        if test_dist < best_obb_distance:
            best_obb_distance = test_dist
            best_obb_points.DeepCopy(test_transform_pd.GetOutput().GetPoints())

# Apply the best OBB alignment
obb_lm_transform.SetSourceLandmarks(best_obb_points)
obb_lm_transform.Modified()

obb_transform_pd = vtkTransformPolyDataFilter()
obb_transform_pd.SetInputData(source_polydata)
obb_transform_pd.SetTransform(obb_lm_transform)
obb_transform_pd.Update()
source_polydata.DeepCopy(obb_transform_pd.GetOutput())

# Hausdorff distance after OBB alignment
distance.SetInputData(0, target_polydata)
distance.SetInputData(1, source_polydata)
distance.Modified()
distance.Update()
distance_after_align = (
    distance.GetOutput(0).GetFieldData().GetArray("HausdorffDistance").GetComponent(0, 0)
)

best_distance = min(distance_before_align, distance_after_align)
if distance_after_align > distance_before_align:
    source_polydata.DeepCopy(original_source_polydata)

# --- ICP refinement ---
icp = vtkIterativeClosestPointTransform()
icp.SetSource(source_polydata)
icp.SetTarget(target_polydata)
icp.GetLandmarkTransform().SetModeToRigidBody()
icp.SetMaximumNumberOfLandmarks(100)
icp.SetMaximumMeanDistance(0.00001)
icp.SetMaximumNumberOfIterations(500)
icp.CheckMeanDistanceOn()
icp.StartByMatchingCentroidsOn()
icp.Update()
icp_mean_distance = icp.GetMeanDistance()

icp_transform_pd = vtkTransformPolyDataFilter()
icp_transform_pd.SetInputData(source_polydata)
icp_transform_pd.SetTransform(icp)
icp_transform_pd.Update()

distance.SetInputData(0, target_polydata)
distance.SetInputData(1, icp_transform_pd.GetOutput())
distance.Update()
distance_after_icp = (
    distance.GetOutput(0).GetFieldData().GetArray("HausdorffDistance").GetComponent(0, 0)
)

if not (math.isnan(icp_mean_distance) or math.isinf(icp_mean_distance)):
    if distance_after_icp < best_distance:
        best_distance = distance_after_icp

print(f"Before aligning:        {distance_before_align:0.5f}")
print(f"After OBB alignment:    {distance_after_align:0.5f}")
print(f"After ICP refinement:   {distance_after_icp:0.5f}")
print(f"Best distance:          {best_distance:0.5f}")

# Mapper & Actor: aligned source (translucent white)
source_mapper = vtkDataSetMapper()
if best_distance == distance_before_align:
    source_mapper.SetInputData(original_source_polydata)
elif best_distance == distance_after_align:
    source_mapper.SetInputData(source_polydata)
else:
    source_mapper.SetInputConnection(icp_transform_pd.GetOutputPort())
source_mapper.ScalarVisibilityOff()

source_actor = vtkActor()
source_actor.SetMapper(source_mapper)
source_actor.GetProperty().SetOpacity(0.6)
source_actor.GetProperty().SetDiffuseColor(white_rgb)

# Mapper & Actor: target (tomato)
target_mapper = vtkDataSetMapper()
target_mapper.SetInputData(target_polydata)
target_mapper.ScalarVisibilityOff()

target_actor = vtkActor()
target_actor.SetMapper(target_mapper)
target_actor.GetProperty().SetDiffuseColor(tomato_rgb)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(source_actor)
renderer.AddActor(target_actor)
renderer.SetBackground(sea_green_light_rgb)
renderer.UseHiddenLineRemovalOn()

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(640, 480)
render_window.SetWindowName("AlignTwoPolyDatas")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Camera orientation widget
cam_orient = vtkCameraOrientationWidget()
cam_orient.SetParentRenderer(renderer)
cam_orient.On()

# Launch the interactive visualization
render_window.Render()
render_window_interactor.Start()
