#!/usr/bin/env python

# Clip an unstructured grid with a plane using vtkClipDataSet.

import os
from pathlib import Path

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkCommonDataModel import vtkPlane
from vtkmodules.vtkCommonTransforms import vtkTransform
from vtkmodules.vtkFiltersGeneral import vtkClipDataSet
from vtkmodules.vtkIOLegacy import vtkUnstructuredGridReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkDataSetMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
orange_rgb = (1.0, 0.647, 0.0)
medium_purple_rgb = (0.576, 0.439, 0.859)
slate_gray_rgb = (0.439, 0.502, 0.565)

# Data: locate the treemesh dataset
data_dir = Path(os.environ.get("VPE_DATA_DIR", Path(__file__).parent))
file_name = str(data_dir / "treemesh.vtk")

# Source: read the unstructured grid
reader = vtkUnstructuredGridReader()
reader.SetFileName(file_name)
reader.Update()

bounds = reader.GetOutput().GetBounds()
center = reader.GetOutput().GetCenter()

# ClipPlane: diagonal clip through the center
clip_plane = vtkPlane()
clip_plane.SetOrigin(center)
clip_plane.SetNormal(0.0, 1.0, 1.0)

# Clipper: clip the unstructured grid (does NOT retain original cells)
clipper = vtkClipDataSet()
clipper.SetClipFunction(clip_plane)
clipper.SetInputData(reader.GetOutput())
clipper.SetValue(0.0)
clipper.GenerateClippedOutputOff()
clipper.Update()

# Clipper (inside-out): generate the clipped output
clipper_inside_out = vtkClipDataSet()
clipper_inside_out.SetClipFunction(clip_plane)
clipper_inside_out.SetInputData(reader.GetOutput())
clipper_inside_out.SetValue(0.0)
clipper_inside_out.InsideOutOn()
clipper_inside_out.GenerateClippedOutputOn()
clipper_inside_out.Update()

# Mapper: inside portion
inside_mapper = vtkDataSetMapper()
inside_mapper.SetInputData(clipper.GetOutput())
inside_mapper.ScalarVisibilityOff()

# Actor: inside portion in yellow
inside_actor = vtkActor()
inside_actor.SetMapper(inside_mapper)
inside_actor.GetProperty().SetDiffuseColor(orange_rgb)
inside_actor.GetProperty().SetAmbient(0.3)
inside_actor.GetProperty().EdgeVisibilityOn()

# Mapper: clipped portion
clipped_mapper = vtkDataSetMapper()
clipped_mapper.SetInputData(clipper_inside_out.GetClippedOutput())
clipped_mapper.ScalarVisibilityOff()

# Actor: clipped portion in red
clipped_actor = vtkActor()
clipped_actor.SetMapper(clipped_mapper)
clipped_actor.GetProperty().SetDiffuseColor(medium_purple_rgb)
clipped_actor.GetProperty().SetAmbient(0.3)
clipped_actor.GetProperty().EdgeVisibilityOn()

# Transform: rotate each half apart to expose the cut faces
inside_transform = vtkTransform()
inside_transform.Translate(center[0], center[1], center[2])
inside_transform.RotateX(-45.0)
inside_transform.Translate(-center[0], -center[1], -center[2])
inside_transform.Translate(0, -(bounds[3] - bounds[2]) * 0.6, 0)
inside_actor.SetUserTransform(inside_transform)

clipped_transform = vtkTransform()
clipped_transform.Translate(center[0], center[1], center[2])
clipped_transform.RotateX(45.0)
clipped_transform.Translate(-center[0], -center[1], -center[2])
clipped_transform.Translate(0, (bounds[3] - bounds[2]) * 0.6, 0)
clipped_actor.SetUserTransform(clipped_transform)

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.AddViewProp(clipped_actor)
renderer.AddViewProp(inside_actor)
renderer.SetBackground(slate_gray_rgb)
renderer.UseHiddenLineRemovalOn()
renderer.ResetCamera()
renderer.GetActiveCamera().Elevation(-30.0)
renderer.GetActiveCamera().Azimuth(40.0)
renderer.GetActiveCamera().Dolly(1.2)
renderer.ResetCameraClippingRange()

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(640, 480)
render_window.SetWindowName("ClipUnstructuredGridWithPlane2")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
