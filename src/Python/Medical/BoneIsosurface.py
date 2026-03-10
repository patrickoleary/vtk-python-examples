#!/usr/bin/env python

# Extract and display the bone isosurface from a CT head dataset using
# vtkFlyingEdges3D at contour value 1150, with an outline for context.

import os
from pathlib import Path

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkFiltersCore import vtkFlyingEdges3D
from vtkmodules.vtkFiltersModeling import vtkOutlineFilter
from vtkmodules.vtkIOImage import vtkMetaImageReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkCamera,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
ivory_rgb = (1.0, 1.0, 0.941)
black_rgb = (0.0, 0.0, 0.0)
dark_slate_gray_rgb = (0.184, 0.310, 0.310)

# Data directory: defaults to the folder containing this script
data_dir = Path(os.environ.get("VPE_DATA_DIR", Path(__file__).parent))

# Reader: load the CT head volume
reader = vtkMetaImageReader()
reader.SetFileName(str(data_dir / "FullHead.mhd"))

# Filter: extract the bone isosurface at contour value 1150
bone_extractor = vtkFlyingEdges3D()
bone_extractor.SetInputConnection(reader.GetOutputPort())
bone_extractor.SetValue(0, 1150)

# Mapper: map the bone surface to graphics primitives
bone_mapper = vtkPolyDataMapper()
bone_mapper.SetInputConnection(bone_extractor.GetOutputPort())
bone_mapper.ScalarVisibilityOff()

# Actor: assign the mapped bone geometry
bone_actor = vtkActor()
bone_actor.SetMapper(bone_mapper)
bone_actor.GetProperty().SetDiffuseColor(ivory_rgb)
bone_actor.GetProperty().SetSpecular(0.3)
bone_actor.GetProperty().SetSpecularPower(20)

# Outline: provide spatial context around the volume
outline_filter = vtkOutlineFilter()
outline_filter.SetInputConnection(reader.GetOutputPort())

outline_mapper = vtkPolyDataMapper()
outline_mapper.SetInputConnection(outline_filter.GetOutputPort())

outline_actor = vtkActor()
outline_actor.SetMapper(outline_mapper)
outline_actor.GetProperty().SetColor(black_rgb)

# Camera: set up an initial view direction
camera = vtkCamera()
camera.SetViewUp(0, 0, -1)
camera.SetPosition(0, -1, 0)
camera.SetFocalPoint(0, 0, 0)
camera.ComputeViewPlaneNormal()
camera.Azimuth(30.0)
camera.Elevation(30.0)

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.AddActor(outline_actor)
renderer.AddActor(bone_actor)
renderer.SetActiveCamera(camera)
renderer.SetBackground(dark_slate_gray_rgb)
renderer.ResetCamera()
camera.Dolly(1.5)
renderer.ResetCameraClippingRange()

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(640, 480)
render_window.SetWindowName("BoneIsosurface")

# Interactor: handle mouse and keyboard events
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
interactor.Initialize()
interactor.Start()
