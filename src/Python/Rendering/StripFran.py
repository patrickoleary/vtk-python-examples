#!/usr/bin/env python

# Compare triangle-strip versus unstructured mesh rendering on the Fran
# face dataset, showing every other polygon in a side-by-side view.

import os
from pathlib import Path

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkFiltersCore import (
    vtkDecimatePro,
    vtkMaskPolyData,
    vtkStripper,
)
from vtkmodules.vtkIOLegacy import vtkPolyDataReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkCamera,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
flesh = (1.0, 0.808, 0.678)
wheat = (0.961, 0.871, 0.702)
papaya_whip = (1.0, 0.937, 0.835)

# Data directory
data_dir = Path(os.environ.get("VPE_DATA_DIR", Path(__file__).parent))

# Reader: load the Fran face scan
reader = vtkPolyDataReader()
reader.SetFileName(str(data_dir / "fran_cut.vtk"))

# ---------- left viewport: triangle-stripped mesh ----------
# Filter: convert triangles to strips for efficient rendering
stripper = vtkStripper()
stripper.SetInputConnection(reader.GetOutputPort())

# Filter: display every other strip
stripper_mask = vtkMaskPolyData()
stripper_mask.SetInputConnection(stripper.GetOutputPort())
stripper_mask.SetOnRatio(2)

# Mapper: map stripped polygon data
stripper_mapper = vtkPolyDataMapper()
stripper_mapper.SetInputConnection(stripper_mask.GetOutputPort())

# Actor: stripped face mesh
stripper_actor = vtkActor()
stripper_actor.SetMapper(stripper_mapper)
stripper_actor.GetProperty().SetColor(flesh)

# ---------- right viewport: decimated unstructured mesh ----------
# Filter: decimate the mesh to 30% of original polygons
decimate = vtkDecimatePro()
decimate.SetInputConnection(reader.GetOutputPort())
decimate.SetTargetReduction(0.7)
decimate.PreserveTopologyOn()

# Filter: display every other polygon
mask = vtkMaskPolyData()
mask.SetInputConnection(decimate.GetOutputPort())
mask.SetOnRatio(2)

# Mapper: map decimated polygon data
decimated_mapper = vtkPolyDataMapper()
decimated_mapper.SetInputConnection(mask.GetOutputPort())

# Actor: decimated face mesh
decimated_actor = vtkActor()
decimated_actor.SetMapper(decimated_mapper)
decimated_actor.GetProperty().SetColor(flesh)

# Renderer: left viewport — stripped mesh
renderer_left = vtkRenderer()
renderer_left.AddActor(stripper_actor)
renderer_left.SetBackground(wheat)
renderer_left.SetViewport(0.0, 0.0, 0.5, 1.0)

# Renderer: right viewport — decimated mesh
renderer_right = vtkRenderer()
renderer_right.AddActor(decimated_actor)
renderer_right.SetBackground(papaya_whip)
renderer_right.SetViewport(0.5, 0.0, 1.0, 1.0)

# Camera: shared between both viewports
camera = vtkCamera()
camera.SetFocalPoint(0, 0, 0)
camera.SetPosition(1, 0, 0)
camera.SetViewUp(0, 1, 0)
renderer_left.SetActiveCamera(camera)
renderer_right.SetActiveCamera(camera)
renderer_left.ResetCamera()
camera.Azimuth(30)
camera.Elevation(30)
camera.Dolly(1.4)
renderer_left.ResetCameraClippingRange()

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer_left)
render_window.AddRenderer(renderer_right)
render_window.SetSize(1024, 640)
render_window.SetWindowName("StripFran")

# Interactor: handle mouse and keyboard events
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window.Render()
interactor.Start()
