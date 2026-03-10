#!/usr/bin/env python

# Frog brain: unsmoothed iso-surface (left) vs. smoothed (right).

import os
from pathlib import Path

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkFiltersCore import (
    vtkFlyingEdges3D,
    vtkPolyDataNormals,
    vtkStripper,
    vtkWindowedSincPolyDataFilter,
)
from vtkmodules.vtkIOImage import vtkMetaImageReader
from vtkmodules.vtkImagingCore import vtkImageThreshold
from vtkmodules.vtkImagingGeneral import vtkImageGaussianSmooth
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
beige_rgb = (0.961, 0.961, 0.863)
light_steel_blue_rgb = (0.690, 0.769, 0.871)

# Data: locate the frogtissue segmentation volume
data_dir = Path(os.environ.get("VPE_DATA_DIR", Path(__file__).parent))
file_name = str(data_dir / "Frog" / "frogtissue.mhd")

# Brain tissue label = 2
tissue = 2
brain_color = beige_rgb

# ---------- Left viewport: unsmoothed iso-surface ----------

# Reader: load the segmented frog tissue volume
reader_left = vtkMetaImageReader()
reader_left.SetFileName(file_name)
reader_left.Update()

# ImageThreshold: isolate the brain tissue label
threshold_left = vtkImageThreshold()
threshold_left.ThresholdBetween(tissue, tissue)
threshold_left.SetInValue(255)
threshold_left.SetOutValue(0)
threshold_left.SetInputConnection(reader_left.GetOutputPort())

# FlyingEdges3D: extract the iso-surface at 63.5
iso_left = vtkFlyingEdges3D()
iso_left.SetInputConnection(threshold_left.GetOutputPort())
iso_left.ComputeScalarsOff()
iso_left.ComputeGradientsOff()
iso_left.ComputeNormalsOn()
iso_left.SetValue(0, 63.5)

# Stripper: create triangle strips for faster rendering
stripper_left = vtkStripper()
stripper_left.SetInputConnection(iso_left.GetOutputPort())

# Mapper: map polygon data to graphics primitives
mapper_left = vtkPolyDataMapper()
mapper_left.SetInputConnection(stripper_left.GetOutputPort())

# Actor: assign the mapped geometry (unsmoothed brain)
actor_left = vtkActor()
actor_left.SetMapper(mapper_left)
actor_left.GetProperty().SetDiffuseColor(brain_color)

# ---------- Right viewport: smoothed iso-surface ----------

# Reader: load the segmented frog tissue volume
reader_right = vtkMetaImageReader()
reader_right.SetFileName(file_name)
reader_right.Update()

# ImageThreshold: isolate the brain tissue label
threshold_right = vtkImageThreshold()
threshold_right.ThresholdBetween(tissue, tissue)
threshold_right.SetInValue(255)
threshold_right.SetOutValue(0)
threshold_right.SetInputConnection(reader_right.GetOutputPort())

# ImageGaussianSmooth: blur the thresholded volume before contouring
gaussian = vtkImageGaussianSmooth()
gaussian.SetStandardDeviations(2.0, 2.0, 2.0)
gaussian.SetRadiusFactors(1, 1, 1)
gaussian.SetInputConnection(threshold_right.GetOutputPort())

# FlyingEdges3D: extract the iso-surface at 127.5 (smoothed)
iso_right = vtkFlyingEdges3D()
iso_right.SetInputConnection(gaussian.GetOutputPort())
iso_right.ComputeScalarsOff()
iso_right.ComputeGradientsOff()
iso_right.ComputeNormalsOff()
iso_right.SetValue(0, 127.5)

# WindowedSincPolyDataFilter: smooth the mesh geometry
smoother = vtkWindowedSincPolyDataFilter()
smoother.SetInputConnection(iso_right.GetOutputPort())
smoother.SetNumberOfIterations(20)
smoother.BoundarySmoothingOff()
smoother.FeatureEdgeSmoothingOff()
smoother.SetFeatureAngle(60.0)
smoother.SetPassBand(0.001)
smoother.NonManifoldSmoothingOn()
smoother.NormalizeCoordinatesOff()
smoother.Update()

# PolyDataNormals: recompute normals after smoothing
normals_right = vtkPolyDataNormals()
normals_right.SetInputConnection(smoother.GetOutputPort())
normals_right.SetFeatureAngle(60.0)

# Stripper: create triangle strips for faster rendering
stripper_right = vtkStripper()
stripper_right.SetInputConnection(normals_right.GetOutputPort())

# Mapper: map polygon data to graphics primitives
mapper_right = vtkPolyDataMapper()
mapper_right.SetInputConnection(stripper_right.GetOutputPort())

# Actor: assign the mapped geometry (smoothed brain)
actor_right = vtkActor()
actor_right.SetMapper(mapper_right)
actor_right.GetProperty().SetDiffuseColor(brain_color)
actor_right.GetProperty().SetDiffuse(1.0)
actor_right.GetProperty().SetSpecular(0.5)
actor_right.GetProperty().SetSpecularPower(100)

# ---------- Renderers and window ----------

# Renderer: unsmoothed (left viewport)
renderer_left = vtkRenderer()
renderer_left.SetViewport(0, 0, 0.5, 1)
renderer_left.AddActor(actor_left)
renderer_left.SetBackground(light_steel_blue_rgb)

# Renderer: smoothed (right viewport, shared camera)
renderer_right = vtkRenderer()
renderer_right.SetViewport(0.5, 0, 1, 1)
renderer_right.AddActor(actor_right)
renderer_right.SetBackground(light_steel_blue_rgb)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.SetSize(640, 480)
render_window.SetWindowName("FrogBrain")
render_window.AddRenderer(renderer_left)
render_window.AddRenderer(renderer_right)

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

renderer_left.ResetCamera()
renderer_left.GetActiveCamera().SetViewUp(-1, 0, 0)
renderer_left.GetActiveCamera().Azimuth(180)
renderer_left.ResetCameraClippingRange()
renderer_right.SetActiveCamera(renderer_left.GetActiveCamera())

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
