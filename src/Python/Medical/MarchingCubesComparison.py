#!/usr/bin/env python

# Compare vtkFlyingEdges3D and vtkMarchingCubes side by side on a CT head
# dataset.  Both extract the skin isosurface at the same contour value; the
# left viewport shows FlyingEdges3D and the right shows MarchingCubes.

import os
from pathlib import Path

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkFiltersCore import vtkFlyingEdges3D, vtkMarchingCubes
from vtkmodules.vtkIOImage import vtkMetaImageReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkCamera,
    vtkPolyDataMapper,
    vtkProperty,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
    vtkTextActor,
)

# Colors (normalized RGB)
skin_color_rgb = (0.941, 0.722, 0.627)
backface_color_rgb = (1.0, 0.898, 0.784)
bkg_color_rgb = (0.200, 0.302, 0.400)
white_rgb = (1.0, 1.0, 1.0)

# Data directory: defaults to the folder containing this script
data_dir = Path(os.environ.get("VPE_DATA_DIR", Path(__file__).parent))

# Reader: load the CT head volume
reader = vtkMetaImageReader()
reader.SetFileName(str(data_dir / "FullHead.mhd"))

# FlyingEdges3D: extract skin isosurface (left viewport)
flying_edges = vtkFlyingEdges3D()
flying_edges.SetInputConnection(reader.GetOutputPort())
flying_edges.SetValue(0, 500)

fe_mapper = vtkPolyDataMapper()
fe_mapper.SetInputConnection(flying_edges.GetOutputPort())
fe_mapper.ScalarVisibilityOff()

fe_actor = vtkActor()
fe_actor.SetMapper(fe_mapper)
fe_actor.GetProperty().SetDiffuseColor(skin_color_rgb)

fe_back = vtkProperty()
fe_back.SetDiffuseColor(backface_color_rgb)
fe_actor.SetBackfaceProperty(fe_back)

# MarchingCubes: extract skin isosurface (right viewport)
marching_cubes = vtkMarchingCubes()
marching_cubes.SetInputConnection(reader.GetOutputPort())
marching_cubes.SetValue(0, 500)

mc_mapper = vtkPolyDataMapper()
mc_mapper.SetInputConnection(marching_cubes.GetOutputPort())
mc_mapper.ScalarVisibilityOff()

mc_actor = vtkActor()
mc_actor.SetMapper(mc_mapper)
mc_actor.GetProperty().SetDiffuseColor(skin_color_rgb)

mc_back = vtkProperty()
mc_back.SetDiffuseColor(backface_color_rgb)
mc_actor.SetBackfaceProperty(mc_back)

# Camera: shared view direction for both renderers
camera = vtkCamera()
camera.SetViewUp(0, 0, -1)
camera.SetPosition(0, -1, 0)
camera.SetFocalPoint(0, 0, 0)
camera.ComputeViewPlaneNormal()
camera.Azimuth(30.0)
camera.Elevation(30.0)

# Left renderer: FlyingEdges3D
left_renderer = vtkRenderer()
left_renderer.SetViewport(0.0, 0.0, 0.5, 1.0)
left_renderer.AddActor(fe_actor)
left_renderer.SetActiveCamera(camera)
left_renderer.SetBackground(bkg_color_rgb)
left_renderer.ResetCamera()
camera.Dolly(1.5)
left_renderer.ResetCameraClippingRange()

fe_label = vtkTextActor()
fe_label.SetInput("FlyingEdges3D")
fe_label.GetTextProperty().SetFontSize(20)
fe_label.GetTextProperty().SetColor(white_rgb)
fe_label.SetPosition(10, 10)
left_renderer.AddViewProp(fe_label)

# Right renderer: MarchingCubes (shares the same camera)
right_renderer = vtkRenderer()
right_renderer.SetViewport(0.5, 0.0, 1.0, 1.0)
right_renderer.AddActor(mc_actor)
right_renderer.SetActiveCamera(camera)
right_renderer.SetBackground(bkg_color_rgb)
right_renderer.ResetCameraClippingRange()

mc_label = vtkTextActor()
mc_label.SetInput("MarchingCubes")
mc_label.GetTextProperty().SetFontSize(20)
mc_label.GetTextProperty().SetColor(white_rgb)
mc_label.SetPosition(10, 10)
right_renderer.AddViewProp(mc_label)

# Window: display both renderers side by side
render_window = vtkRenderWindow()
render_window.AddRenderer(left_renderer)
render_window.AddRenderer(right_renderer)
render_window.SetSize(1280, 480)
render_window.SetWindowName("MarchingCubesComparison")

# Interactor: handle mouse and keyboard events
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
interactor.Initialize()
interactor.Start()
