#!/usr/bin/env python

# Connectivity filter to extract the largest region from a noisy isosurface.

import os
from pathlib import Path

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkFiltersCore import vtkPolyDataConnectivityFilter
from vtkmodules.vtkFiltersModeling import vtkOutlineFilter
from vtkmodules.vtkIOGeometry import vtkMCubesReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
raw_sienna = (0.780, 0.380, 0.082)
black = (0.000, 0.000, 0.000)
slate_gray = (0.439, 0.502, 0.565)

# Data file
data_dir = Path(os.environ.get("VPE_DATA_DIR", Path(__file__).parent))
file_name = str(data_dir / "pine_root.tri")

# Reader: load the marching cubes triangulation of a pine root
reader = vtkMCubesReader()
reader.SetFileName(file_name)

# Filter: extract the largest connected region to remove noise
connect = vtkPolyDataConnectivityFilter()
connect.SetInputConnection(reader.GetOutputPort())
connect.SetExtractionModeToLargestRegion()

# Mapper: map the connected isosurface to graphics primitives
iso_mapper = vtkPolyDataMapper()
iso_mapper.SetInputConnection(connect.GetOutputPort())
iso_mapper.ScalarVisibilityOff()

# Actor: display the connected isosurface
iso_actor = vtkActor()
iso_actor.SetMapper(iso_mapper)
iso_actor.GetProperty().SetColor(raw_sienna)

# Filter: bounding outline for spatial context
outline = vtkOutlineFilter()
outline.SetInputConnection(reader.GetOutputPort())

# Mapper: map the outline to graphics primitives
outline_mapper = vtkPolyDataMapper()
outline_mapper.SetInputConnection(outline.GetOutputPort())

# Actor: display the outline
outline_actor = vtkActor()
outline_actor.SetMapper(outline_mapper)
outline_actor.GetProperty().SetColor(black)

# Renderer: assemble the scene and configure the camera
renderer = vtkRenderer()
renderer.AddActor(outline_actor)
renderer.AddActor(iso_actor)
renderer.SetBackground(slate_gray)
cam = renderer.GetActiveCamera()
cam.SetFocalPoint(40.6018, 37.2813, 50.1953)
cam.SetPosition(40.6018, -280.533, 47.0172)
cam.ComputeViewPlaneNormal()
cam.SetClippingRange(26.1073, 1305.36)
cam.SetViewAngle(20.9219)
cam.SetViewUp(0.0, 0.0, 1.0)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("PineRootConnectivity")
render_window.SetSize(512, 512)

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Start()
