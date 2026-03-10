#!/usr/bin/env python

# Crop a sub-volume from a 3D medical dataset (FullHead.mhd) using
# vtkExtractVOI and render the result with vtkFlyingEdges3D.

import os
from pathlib import Path

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkFiltersCore import vtkFlyingEdges3D
from vtkmodules.vtkIOImage import vtkMetaImageReader
from vtkmodules.vtkImagingCore import vtkExtractVOI
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
wheat_rgb = (0.961, 0.871, 0.702)
slate_gray_background_rgb = (0.439, 0.502, 0.565)

# Data directory: defaults to the folder containing this script
data_dir = Path(os.environ.get("VPE_DATA_DIR", Path(__file__).parent))

# Reader: load the 3D medical volume
reader = vtkMetaImageReader()
reader.SetFileName(str(data_dir / "FullHead.mhd"))
reader.Update()

# Filter: extract a sub-volume (VOI) covering the central region
# The full volume is 256x256x94; crop to the center 128x128x60
extract = vtkExtractVOI()
extract.SetInputConnection(reader.GetOutputPort())
extract.SetVOI(64, 192, 64, 192, 17, 77)
extract.SetSampleRate(1, 1, 1)

# Filter: extract an iso-surface from the cropped sub-volume
flying_edges = vtkFlyingEdges3D()
flying_edges.SetInputConnection(extract.GetOutputPort())
flying_edges.SetValue(0, 500)
flying_edges.ComputeNormalsOn()

# Mapper: map the iso-surface polydata to graphics primitives
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(flying_edges.GetOutputPort())
mapper.ScalarVisibilityOff()

# Actor: assign the mapped geometry
actor = vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetDiffuseColor(wheat_rgb)
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
render_window.SetWindowName("ImageExtractVOI")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
