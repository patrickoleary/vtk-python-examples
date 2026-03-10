#!/usr/bin/env python

# Clip an unstructured grid with a plane using vtkTableBasedClipDataSet.

import os
from pathlib import Path

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkCommonDataModel import vtkPlane
from vtkmodules.vtkCommonTransforms import vtkTransform
from vtkmodules.vtkFiltersGeneral import vtkTableBasedClipDataSet
from vtkmodules.vtkIOLegacy import vtkUnstructuredGridReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkDataSetMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
gold_rgb = (1.0, 0.843, 0.0)
steel_blue_rgb = (0.275, 0.510, 0.706)
wheat_rgb = (0.961, 0.871, 0.702)

# Data: locate the treemesh dataset
data_dir = Path(os.environ.get("VPE_DATA_DIR", Path(__file__).parent))
file_name = str(data_dir / "treemesh.vtk")

# Source: read the unstructured grid
reader = vtkUnstructuredGridReader()
reader.SetFileName(file_name)
reader.Update()

bounds = reader.GetOutput().GetBounds()
center = reader.GetOutput().GetCenter()

# ClipPlane: vertical clip through the center (x-axis normal)
clip_plane = vtkPlane()
clip_plane.SetOrigin(center)
clip_plane.SetNormal(1.0, 0.0, 0.0)

# Clipper: clip the unstructured grid (retains original unclipped cells)
clipper = vtkTableBasedClipDataSet()
clipper.SetClipFunction(clip_plane)
clipper.SetInputData(reader.GetOutput())
clipper.SetValue(0.0)
clipper.GenerateClippedOutputOn()
clipper.Update()

# Mapper: inside (retained) portion
inside_mapper = vtkDataSetMapper()
inside_mapper.SetInputData(clipper.GetOutput())
inside_mapper.ScalarVisibilityOff()

# Actor: inside portion in yellow
inside_actor = vtkActor()
inside_actor.SetMapper(inside_mapper)
inside_actor.GetProperty().SetDiffuseColor(gold_rgb)
inside_actor.GetProperty().SetAmbient(0.3)
inside_actor.GetProperty().EdgeVisibilityOn()

# Mapper: clipped portion
clipped_mapper = vtkDataSetMapper()
clipped_mapper.SetInputData(clipper.GetClippedOutput())
clipped_mapper.ScalarVisibilityOff()

# Actor: clipped portion in red
clipped_actor = vtkActor()
clipped_actor.SetMapper(clipped_mapper)
clipped_actor.GetProperty().SetDiffuseColor(steel_blue_rgb)
clipped_actor.GetProperty().SetAmbient(0.3)
clipped_actor.GetProperty().EdgeVisibilityOn()

# Transform: separate the two halves along the x-axis
inside_transform = vtkTransform()
inside_transform.Translate(-(bounds[1] - bounds[0]) * 0.6, 0, 0)
inside_actor.SetUserTransform(inside_transform)

clipped_transform = vtkTransform()
clipped_transform.Translate((bounds[1] - bounds[0]) * 0.6, 0, 0)
clipped_actor.SetUserTransform(clipped_transform)

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.AddViewProp(clipped_actor)
renderer.AddViewProp(inside_actor)
renderer.SetBackground(wheat_rgb)
renderer.UseHiddenLineRemovalOn()
renderer.ResetCamera()
renderer.GetActiveCamera().Elevation(20.0)
renderer.GetActiveCamera().Azimuth(10.0)
renderer.GetActiveCamera().Dolly(1.4)
renderer.ResetCameraClippingRange()

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(640, 480)
render_window.SetWindowName("ClipUnstructuredGridWithPlane")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
