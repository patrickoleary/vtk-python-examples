#!/usr/bin/env python

# Extract an iso-surface from a 3D medical volume (FullHead.mhd) using
# vtkFlyingEdges3D, the GPU-accelerated successor to vtkMarchingCubes.

import os
from pathlib import Path

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkFiltersCore import vtkFlyingEdges3D
from vtkmodules.vtkIOImage import vtkMetaImageReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
misty_rose_rgb = (1.0, 0.894, 0.882)
slate_gray_background_rgb = (0.439, 0.502, 0.565)

# Data directory: defaults to the folder containing this script
data_dir = Path(os.environ.get("VPE_DATA_DIR", Path(__file__).parent))

# Reader: load the 3D medical volume
reader = vtkMetaImageReader()
reader.SetFileName(str(data_dir / "FullHead.mhd"))
reader.Update()

# Filter: extract an iso-surface at scalar value 500 (skin boundary)
flying_edges = vtkFlyingEdges3D()
flying_edges.SetInputConnection(reader.GetOutputPort())
flying_edges.SetValue(0, 500)
flying_edges.ComputeNormalsOn()
flying_edges.ComputeGradientsOff()

# Mapper: map the iso-surface polydata to graphics primitives
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(flying_edges.GetOutputPort())
mapper.ScalarVisibilityOff()

# Actor: assign the mapped geometry
actor = vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetDiffuseColor(misty_rose_rgb)
actor.GetProperty().SetSpecular(0.3)
actor.GetProperty().SetSpecularPower(20)

# Renderer: assemble the scene and configure the camera
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(slate_gray_background_rgb)
renderer.ResetCamera()
renderer.GetActiveCamera().Azimuth(30)
renderer.GetActiveCamera().Elevation(20)
renderer.ResetCameraClippingRange()

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(640, 480)
render_window.SetWindowName("ImageMarchingCubes")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
