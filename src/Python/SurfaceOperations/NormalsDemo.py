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

renderers = []
for i in range(3):
    if i == 0:
        normals_filter.ComputePointNormalsOff()
    elif i == 1:
        normals_filter.ComputePointNormalsOn()
        normals_filter.SplittingOff()
    else:
        normals_filter.ComputePointNormalsOn()
        normals_filter.SplittingOn()

    normals_filter.Update()

    normals_copy = vtkPolyData()
    normals_copy.DeepCopy(normals_filter.GetOutput())

    # ---- Mapper: map the normal-processed mesh ----
    mapper = vtkPolyDataMapper()
    mapper.SetInputData(normals_copy)
    mapper.ScalarVisibilityOff()

    # ---- Actor: display with Peacock blue surface ----
    actor = vtkActor()
    actor.SetMapper(mapper)
    actor.GetProperty().SetDiffuseColor(peacock)
    actor.GetProperty().SetDiffuse(0.7)
    actor.GetProperty().SetSpecularPower(20)
    actor.GetProperty().SetSpecular(0.5)

    # ---- Renderer: one viewport per normal mode ----
    ren = vtkRenderer()
    ren.SetViewport(viewports[i])
    ren.SetBackground(bkg_colors[i])
    ren.SetActiveCamera(camera)
    ren.AddActor(actor)
    renderers.append(ren)

# Camera: configure the shared camera
camera.SetFocalPoint(0, 0, 0)
camera.SetPosition(1, 0, 0)
camera.SetViewUp(0, 0, -1)
renderers[0].ResetCamera()
camera.Azimuth(120)
camera.Elevation(30)
camera.Dolly(1.1)
renderers[0].ResetCameraClippingRange()

# Window: display the three-panel comparison
render_window = vtkRenderWindow()
for ren in renderers:
    render_window.AddRenderer(ren)
render_window.SetWindowName("NormalsDemo")
render_window.SetSize(900, 300)

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Start()
