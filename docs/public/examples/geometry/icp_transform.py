#!/usr/bin/env python
# Demonstrate vtkIterativeClosestPointTransform aligning superquadrics.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonDataModel import vtkIterativeClosestPointTransform
from vtkmodules.vtkFiltersCore import vtkFeatureEdges
from vtkmodules.vtkFiltersSources import vtkSuperquadricSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Superquadric source 1 (target shape).
source_1 = vtkSuperquadricSource()
source_1.ToroidalOff()
source_1.SetThetaResolution(20)
source_1.SetPhiResolution(20)
source_1.SetPhiRoundness(0.3)
source_1.SetThetaRoundness(0.85)
source_1.Update()

# Superquadric source 2.
source_2 = vtkSuperquadricSource()
source_2.ToroidalOff()
source_2.SetThetaResolution(20)
source_2.SetPhiResolution(20)
source_2.SetPhiRoundness(0.7)
source_2.SetThetaRoundness(1.25)
source_2.SetScale(0.7, 0.7, 0.7)
source_2.SetCenter(-0.25, 0.25, 0.0)
source_2.Update()

# Superquadric source 3.
source_3 = vtkSuperquadricSource()
source_3.ToroidalOff()
source_3.SetThetaResolution(20)
source_3.SetPhiResolution(20)
source_3.SetPhiRoundness(1.1)
source_3.SetThetaRoundness(1.65)
source_3.SetScale(0.5, 0.5, 0.5)
source_3.SetCenter(0.4, -0.3, 0.0)
source_3.Update()

# Feature edges for source 1 (used in all three viewports).
feature_edges_1 = vtkFeatureEdges()
feature_edges_1.SetInputConnection(source_1.GetOutputPort())
feature_edges_1.BoundaryEdgesOn()
feature_edges_1.ColoringOff()
feature_edges_1.ManifoldEdgesOff()

# ICP transform: source 2 -> source 1.
icp_2 = vtkIterativeClosestPointTransform()
icp_2.SetSource(source_2.GetOutput())
icp_2.SetTarget(source_1.GetOutput())
icp_2.SetCheckMeanDistance(1)
icp_2.SetMaximumMeanDistance(0.001)
icp_2.SetMaximumNumberOfIterations(30)
icp_2.SetMaximumNumberOfLandmarks(50)

# ICP transform: source 3 -> source 1 (with centroid matching).
icp_3 = vtkIterativeClosestPointTransform()
icp_3.SetSource(source_3.GetOutput())
icp_3.SetTarget(source_1.GetOutput())
icp_3.SetCheckMeanDistance(1)
icp_3.SetMaximumMeanDistance(0.001)
icp_3.SetMaximumNumberOfIterations(30)
icp_3.SetMaximumNumberOfLandmarks(50)
icp_3.StartByMatchingCentroidsOn()

# --- Viewport 0: all three sources, no ICP ---

source_1_mapper_0 = vtkPolyDataMapper()
source_1_mapper_0.SetInputConnection(source_1.GetOutputPort())
source_1_actor_0 = vtkActor()
source_1_actor_0.SetMapper(source_1_mapper_0)
source_1_actor_0.GetProperty().SetOpacity(0.2)

feature_edges_mapper_0 = vtkPolyDataMapper()
feature_edges_mapper_0.SetInputConnection(feature_edges_1.GetOutputPort())
feature_edges_mapper_0.SetResolveCoincidentTopologyToPolygonOffset()
feature_edges_actor_0 = vtkActor()
feature_edges_actor_0.SetMapper(feature_edges_mapper_0)

source_2_mapper_0 = vtkPolyDataMapper()
source_2_mapper_0.SetInputConnection(source_2.GetOutputPort())
source_2_actor_0 = vtkActor()
source_2_actor_0.SetMapper(source_2_mapper_0)
source_2_actor_0.GetProperty().SetColor(0.2, 0.6, 0.1)

source_3_mapper_0 = vtkPolyDataMapper()
source_3_mapper_0.SetInputConnection(source_3.GetOutputPort())
source_3_actor_0 = vtkActor()
source_3_actor_0.SetMapper(source_3_mapper_0)
source_3_actor_0.GetProperty().SetColor(0.1, 0.2, 0.6)

# --- Viewport 1: source 1 + source 2 with ICP ---

source_1_mapper_1 = vtkPolyDataMapper()
source_1_mapper_1.SetInputConnection(source_1.GetOutputPort())
source_1_actor_1 = vtkActor()
source_1_actor_1.SetMapper(source_1_mapper_1)
source_1_actor_1.GetProperty().SetOpacity(0.2)

feature_edges_mapper_1 = vtkPolyDataMapper()
feature_edges_mapper_1.SetInputConnection(feature_edges_1.GetOutputPort())
feature_edges_mapper_1.SetResolveCoincidentTopologyToPolygonOffset()
feature_edges_actor_1 = vtkActor()
feature_edges_actor_1.SetMapper(feature_edges_mapper_1)

source_2_mapper_1 = vtkPolyDataMapper()
source_2_mapper_1.SetInputConnection(source_2.GetOutputPort())
source_2_actor_1 = vtkActor()
source_2_actor_1.SetMapper(source_2_mapper_1)
source_2_actor_1.GetProperty().SetColor(0.2, 0.6, 0.1)
source_2_actor_1.SetUserTransform(icp_2)

# --- Viewport 2: source 1 + source 3 with ICP ---

source_1_mapper_2 = vtkPolyDataMapper()
source_1_mapper_2.SetInputConnection(source_1.GetOutputPort())
source_1_actor_2 = vtkActor()
source_1_actor_2.SetMapper(source_1_mapper_2)
source_1_actor_2.GetProperty().SetOpacity(0.2)

feature_edges_mapper_2 = vtkPolyDataMapper()
feature_edges_mapper_2.SetInputConnection(feature_edges_1.GetOutputPort())
feature_edges_mapper_2.SetResolveCoincidentTopologyToPolygonOffset()
feature_edges_actor_2 = vtkActor()
feature_edges_actor_2.SetMapper(feature_edges_mapper_2)

source_3_mapper_2 = vtkPolyDataMapper()
source_3_mapper_2.SetInputConnection(source_3.GetOutputPort())
source_3_actor_2 = vtkActor()
source_3_actor_2.SetMapper(source_3_mapper_2)
source_3_actor_2.GetProperty().SetColor(0.1, 0.2, 0.6)
source_3_actor_2.SetUserTransform(icp_3)

# --- Renderers ---

renderer_0 = vtkRenderer()
renderer_0.SetViewport(0.0, 0.0, 1.0 / 3.0, 1.0)
renderer_0.SetBackground(0.7, 0.8, 1.0)
renderer_0.AddActor(feature_edges_actor_0)
renderer_0.AddActor(source_1_actor_0)
renderer_0.AddActor(source_2_actor_0)
renderer_0.AddActor(source_3_actor_0)

renderer_1 = vtkRenderer()
renderer_1.SetViewport(1.0 / 3.0, 0.0, 2.0 / 3.0, 1.0)
renderer_1.SetBackground(0.7, 0.8, 1.0)
renderer_1.AddActor(feature_edges_actor_1)
renderer_1.AddActor(source_1_actor_1)
renderer_1.AddActor(source_2_actor_1)

renderer_2 = vtkRenderer()
renderer_2.SetViewport(2.0 / 3.0, 0.0, 1.0, 1.0)
renderer_2.SetBackground(0.7, 0.8, 1.0)
renderer_2.AddActor(feature_edges_actor_2)
renderer_2.AddActor(source_1_actor_2)
renderer_2.AddActor(source_3_actor_2)

render_window = vtkRenderWindow()
render_window.SetSize(400, 100)
render_window.AddRenderer(renderer_0)
render_window.AddRenderer(renderer_1)
render_window.AddRenderer(renderer_2)
render_window.SetWindowName("icp transform")

renderer_0.GetActiveCamera().SetPosition(1.7, 1.4, 1.7)
renderer_1.GetActiveCamera().SetPosition(1.7, 1.4, 1.7)
renderer_2.GetActiveCamera().SetPosition(1.7, 1.4, 1.7)

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
