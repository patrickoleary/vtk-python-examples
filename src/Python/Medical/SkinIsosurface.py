#!/usr/bin/env python

# Extract and display the skin isosurface from a CT head dataset using
# vtkFlyingEdges3D with an outline for spatial context.

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
    vtkProperty,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
skin_color_rgb = (0.941, 0.722, 0.627)
backface_color_rgb = (1.0, 0.898, 0.784)
black_rgb = (0.0, 0.0, 0.0)
bkg_color_rgb = (0.200, 0.302, 0.400)

# Data directory: defaults to the folder containing this script
data_dir = Path(os.environ.get("VPE_DATA_DIR", Path(__file__).parent))

# Reader: load the CT head volume
reader = vtkMetaImageReader()
reader.SetFileName(str(data_dir / "FullHead.mhd"))

# Filter: extract the skin isosurface at contour value 500
skin_extractor = vtkFlyingEdges3D()
skin_extractor.SetInputConnection(reader.GetOutputPort())
skin_extractor.SetValue(0, 500)

# Mapper: map the skin surface to graphics primitives
skin_mapper = vtkPolyDataMapper()
skin_mapper.SetInputConnection(skin_extractor.GetOutputPort())
skin_mapper.ScalarVisibilityOff()

# Actor: assign the mapped skin geometry with diffuse color and backface
skin_actor = vtkActor()
skin_actor.SetMapper(skin_mapper)
skin_actor.GetProperty().SetDiffuseColor(skin_color_rgb)

back_property = vtkProperty()
back_property.SetDiffuseColor(backface_color_rgb)
skin_actor.SetBackfaceProperty(back_property)

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
renderer.AddActor(skin_actor)
renderer.SetActiveCamera(camera)
renderer.SetBackground(bkg_color_rgb)
renderer.ResetCamera()
camera.Dolly(1.5)
renderer.ResetCameraClippingRange()

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(640, 480)
render_window.SetWindowName("SkinIsosurface")

# Interactor: handle mouse and keyboard events
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
interactor.Initialize()
interactor.Start()
