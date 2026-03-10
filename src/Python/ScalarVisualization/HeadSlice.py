#!/usr/bin/env python

# Generate contour lines on a CT head slice using vtkContourFilter.

import os
from pathlib import Path

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkFiltersCore import vtkContourFilter
from vtkmodules.vtkFiltersModeling import vtkOutlineFilter
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
wheat = (0.961, 0.871, 0.702)
slate_gray = (0.439, 0.502, 0.565)

# Data file
data_dir = Path(os.environ.get("VPE_DATA_DIR", Path(__file__).parent))
file_name = str(data_dir / "FullHead.mhd")

# Reader: load the CT head volume
reader = vtkMetaImageReader()
reader.SetFileName(file_name)
reader.Update()

# Filter: extract a single axial slice
extract_voi = vtkExtractVOI()
extract_voi.SetInputConnection(reader.GetOutputPort())
extract_voi.SetVOI(0, 255, 0, 255, 45, 45)

# Filter: generate contour lines on the slice
iso = vtkContourFilter()
iso.SetInputConnection(extract_voi.GetOutputPort())
iso.GenerateValues(12, 500, 1150)

# Mapper: map contour lines to graphics primitives
iso_mapper = vtkPolyDataMapper()
iso_mapper.SetInputConnection(iso.GetOutputPort())
iso_mapper.ScalarVisibilityOff()

# Actor: display the contour lines
iso_actor = vtkActor()
iso_actor.SetMapper(iso_mapper)
iso_actor.GetProperty().SetColor(wheat)

# Filter: bounding outline of the slice
outline = vtkOutlineFilter()
outline.SetInputConnection(extract_voi.GetOutputPort())

# Mapper: map outline to graphics primitives
outline_mapper = vtkPolyDataMapper()
outline_mapper.SetInputConnection(outline.GetOutputPort())

# Actor: display the outline
outline_actor = vtkActor()
outline_actor.SetMapper(outline_mapper)

# Renderer: assemble the scene and configure the camera
renderer = vtkRenderer()
renderer.AddActor(outline_actor)
renderer.AddActor(iso_actor)
renderer.SetBackground(slate_gray)
renderer.ResetCamera()
renderer.GetActiveCamera().Dolly(1.5)
renderer.ResetCameraClippingRange()

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("HeadSlice")
render_window.SetSize(640, 640)

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Start()
