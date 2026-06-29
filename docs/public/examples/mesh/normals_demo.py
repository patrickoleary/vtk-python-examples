#!/usr/bin/env python

# Surface normal generation comparison: faceted, shared normals, and split normals.

import os
from pathlib import Path

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkCommonDataModel import vtkPolyData
from vtkmodules.vtkFiltersCore import vtkPolyDataNormals
from vtkmodules.vtkIOGeometry import vtkSTLReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkCamera,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
peacock = (0.200, 0.631, 0.788)
cornsilk = (1.000, 0.973, 0.863)
navajo_white = (1.000, 0.871, 0.678)
tan_color = (0.824, 0.706, 0.549)

# Data file
data_dir = Path(os.environ.get("VPE_DATA_DIR", Path(__file__).parent))
file_name = str(data_dir / "42400-IDGH.stl")

# Reader: load the STL mesh
reader = vtkSTLReader()
reader.SetFileName(file_name)
reader.Update()
poly_data = reader.GetOutput()

# Shared camera across all three viewports
camera = vtkCamera()

# Background colors for left, center, right viewports
bkg_colors = [cornsilk, navajo_white, tan_color]
viewports = [(0.0, 0.0, 1.0 / 3.0, 1.0),
             (1.0 / 3.0, 0.0, 2.0 / 3.0, 1.0),
             (2.0 / 3.0, 0.0, 1.0, 1.0)]

# Normal filter configured differently for each viewport
normals_filter = vtkPolyDataNormals()
normals_filter.SetInputData(poly_data)
normals_filter.SetFeatureAngle(30.0)

# --- Viewport 0: faceted (no point normals) ---
normals_filter.ComputePointNormalsOff()
normals_filter.Update()

normals_copy_0 = vtkPolyData()
normals_copy_0.DeepCopy(normals_filter.GetOutput())

mapper_0 = vtkPolyDataMapper()
mapper_0.SetInputData(normals_copy_0)
mapper_0.ScalarVisibilityOff()

actor_0 = vtkActor()
actor_0.SetMapper(mapper_0)
actor_0.GetProperty().SetDiffuseColor(peacock)
actor_0.GetProperty().SetDiffuse(0.7)
actor_0.GetProperty().SetSpecularPower(20)
actor_0.GetProperty().SetSpecular(0.5)

ren_0 = vtkRenderer()
ren_0.SetViewport(0.0, 0.0, 1.0 / 3.0, 1.0)
ren_0.SetBackground(cornsilk)
ren_0.SetActiveCamera(camera)
ren_0.AddActor(actor_0)

# --- Viewport 1: shared normals (no splitting) ---
normals_filter.ComputePointNormalsOn()
normals_filter.SplittingOff()
normals_filter.Update()

normals_copy_1 = vtkPolyData()
normals_copy_1.DeepCopy(normals_filter.GetOutput())

mapper_1 = vtkPolyDataMapper()
mapper_1.SetInputData(normals_copy_1)
mapper_1.ScalarVisibilityOff()

actor_1 = vtkActor()
actor_1.SetMapper(mapper_1)
actor_1.GetProperty().SetDiffuseColor(peacock)
actor_1.GetProperty().SetDiffuse(0.7)
actor_1.GetProperty().SetSpecularPower(20)
actor_1.GetProperty().SetSpecular(0.5)

ren_1 = vtkRenderer()
ren_1.SetViewport(1.0 / 3.0, 0.0, 2.0 / 3.0, 1.0)
ren_1.SetBackground(navajo_white)
ren_1.SetActiveCamera(camera)
ren_1.AddActor(actor_1)

# --- Viewport 2: split normals ---
normals_filter.ComputePointNormalsOn()
normals_filter.SplittingOn()
normals_filter.Update()

normals_copy_2 = vtkPolyData()
normals_copy_2.DeepCopy(normals_filter.GetOutput())

mapper_2 = vtkPolyDataMapper()
mapper_2.SetInputData(normals_copy_2)
mapper_2.ScalarVisibilityOff()

actor_2 = vtkActor()
actor_2.SetMapper(mapper_2)
actor_2.GetProperty().SetDiffuseColor(peacock)
actor_2.GetProperty().SetDiffuse(0.7)
actor_2.GetProperty().SetSpecularPower(20)
actor_2.GetProperty().SetSpecular(0.5)

ren_2 = vtkRenderer()
ren_2.SetViewport(2.0 / 3.0, 0.0, 1.0, 1.0)
ren_2.SetBackground(tan_color)
ren_2.SetActiveCamera(camera)
ren_2.AddActor(actor_2)

# Window: display the three-panel comparison
render_window = vtkRenderWindow()
render_window.AddRenderer(ren_0)
render_window.AddRenderer(ren_1)
render_window.AddRenderer(ren_2)
render_window.SetWindowName("normals demo")
render_window.SetMultiSamples(0)
render_window.SetSize(900, 300)

# Scene: configure the shared camera
camera.SetFocalPoint(0, 0, 0)
camera.SetPosition(1, 0, 0)
camera.SetViewUp(0, 0, -1)
ren_0.ResetCamera()
camera.Azimuth(120)
camera.Elevation(30)
camera.Dolly(1.1)
ren_0.ResetCameraClippingRange()

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
