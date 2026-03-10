#!/usr/bin/env python

# Display a JPEG image as a background layer behind a 3D superquadric
# using two renderers on separate layers.

import os
from pathlib import Path

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkFiltersSources import vtkSuperquadricSource
from vtkmodules.vtkIOImage import vtkJPEGReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkImageActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
navajo_white_rgb = (1.0, 0.871, 0.678)

# Data directory: defaults to the folder containing this script
data_dir = Path(os.environ.get("VPE_DATA_DIR", Path(__file__).parent))

# Reader: load the JPEG background image
jpeg_reader = vtkJPEGReader()
jpeg_reader.SetFileName(str(data_dir / "Gourds2.jpg"))
jpeg_reader.Update()
image_data = jpeg_reader.GetOutput()

# Background actor: display the image as a 2D background
image_actor = vtkImageActor()
image_actor.SetInputData(image_data)

# Background renderer: layer 0, non-interactive
background_renderer = vtkRenderer()
background_renderer.SetLayer(0)
background_renderer.InteractiveOff()
background_renderer.AddActor(image_actor)

# Source: generate a superquadric for the foreground scene
superquadric_source = vtkSuperquadricSource()
superquadric_source.SetPhiRoundness(1.1)
superquadric_source.SetThetaRoundness(0.2)

# Mapper: map polygon data to graphics primitives
superquadric_mapper = vtkPolyDataMapper()
superquadric_mapper.SetInputConnection(superquadric_source.GetOutputPort())

# Actor: assign the mapped geometry
superquadric_actor = vtkActor()
superquadric_actor.SetMapper(superquadric_mapper)
superquadric_actor.GetProperty().SetColor(navajo_white_rgb)

# Scene renderer: layer 1, interactive foreground
scene_renderer = vtkRenderer()
scene_renderer.SetLayer(1)
scene_renderer.AddActor(superquadric_actor)

# Window: two-layer rendering with background image and foreground geometry
render_window = vtkRenderWindow()
render_window.SetNumberOfLayers(2)
render_window.AddRenderer(background_renderer)
render_window.AddRenderer(scene_renderer)
render_window.SetWindowName("BackgroundImage")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Render once to position the background camera
render_window.Render()

# Camera: fit the background image to fill the background renderer
origin = image_data.GetOrigin()
spacing = image_data.GetSpacing()
extent = image_data.GetExtent()

camera = background_renderer.GetActiveCamera()
camera.ParallelProjectionOn()

xc = origin[0] + 0.5 * (extent[0] + extent[1]) * spacing[0]
yc = origin[1] + 0.5 * (extent[2] + extent[3]) * spacing[1]
yd = (extent[3] - extent[2] + 1) * spacing[1]
d = camera.GetDistance()
camera.SetParallelScale(0.5 * yd)
camera.SetFocalPoint(xc, yc, 0.0)
camera.SetPosition(xc, yc, d)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
