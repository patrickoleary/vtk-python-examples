#!/usr/bin/env python

# Read a directory of DICOM files and browse slices interactively with
# mouse wheel or Up/Down keys.  Uses the standard VTK pipeline with
# vtkImageActor, parallel projection, and a custom
# vtkInteractorStyleImage subclass for slice navigation.

import os
from pathlib import Path

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkIOImage import vtkDICOMImageReader
from vtkmodules.vtkInteractionStyle import vtkInteractorStyleImage
from vtkmodules.vtkRenderingCore import (
    vtkActor2D,
    vtkImageActor,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
    vtkTextMapper,
    vtkTextProperty,
)

# Colors (normalized RGB)
background_rgb = (0.200, 0.302, 0.400)

# Data directory: defaults to the folder containing this script
data_dir = Path(os.environ.get("VPE_DATA_DIR", Path(__file__).parent))


# Custom interactor style: scroll through DICOM slices with mouse wheel
# or Up/Down keys and update the slice status text overlay.
# Subclassing vtkInteractorStyleImage is required to intercept these events.
class SliceInteractorStyle(vtkInteractorStyleImage):
    def __init__(self, image_actor, status_mapper, min_slice, max_slice,
                 renderer, render_window):
        super().__init__()
        self.image_actor = image_actor
        self.status_mapper = status_mapper
        self.min_slice = min_slice
        self.max_slice = max_slice
        self.slice = min_slice
        self.total = max_slice - min_slice + 1
        self.xy_extent = image_actor.GetInput().GetExtent()[:4]
        self.renderer = renderer
        self.render_window = render_window
        self.AddObserver("KeyPressEvent", self._on_key)
        self.AddObserver("MouseWheelForwardEvent", lambda o, e: self._move(1))
        self.AddObserver("MouseWheelBackwardEvent", lambda o, e: self._move(-1))

    def _move(self, delta):
        self.slice = max(self.min_slice, min(self.max_slice, self.slice + delta))
        self.image_actor.SetDisplayExtent(
            *self.xy_extent, self.slice, self.slice)
        self.status_mapper.SetInput(
            f"Slice {self.slice - self.min_slice + 1}/{self.total}")
        self.renderer.ResetCamera()
        self.render_window.Render()

    def _on_key(self, obj, event):
        key = self.GetInteractor().GetKeySym()
        if key == "Up":
            self._move(1)
        elif key == "Down":
            self._move(-1)


# Reader: load all DICOM files from the brain/ directory
reader = vtkDICOMImageReader()
reader.SetDirectoryName(str(data_dir / "brain"))
reader.Update()

# Determine slice range from the data extent (Z axis)
extent = reader.GetOutput().GetExtent()
min_slice = extent[4]
max_slice = extent[5]

# Actor: display the image as a 2D texture, starting at the first slice
actor = vtkImageActor()
actor.GetMapper().SetInputConnection(reader.GetOutputPort())
actor.SetDisplayExtent(extent[0], extent[1], extent[2], extent[3],
                       min_slice, min_slice)
scalar_range = reader.GetOutput().GetScalarRange()
actor.GetProperty().SetColorWindow(scalar_range[1] - scalar_range[0])
actor.GetProperty().SetColorLevel((scalar_range[1] + scalar_range[0]) / 2.0)

# Slice status text overlay (bottom-left)
slice_text_prop = vtkTextProperty()
slice_text_prop.SetFontFamilyToCourier()
slice_text_prop.SetFontSize(20)
slice_text_prop.SetVerticalJustificationToBottom()
slice_text_prop.SetJustificationToLeft()

slice_text_mapper = vtkTextMapper()
slice_text_mapper.SetInput(f"Slice 1/{max_slice - min_slice + 1}")
slice_text_mapper.SetTextProperty(slice_text_prop)

slice_text_actor = vtkActor2D()
slice_text_actor.SetMapper(slice_text_mapper)
slice_text_actor.SetPosition(15, 10)

# Usage hint text overlay (top-left)
usage_text_prop = vtkTextProperty()
usage_text_prop.SetFontFamilyToCourier()
usage_text_prop.SetFontSize(14)
usage_text_prop.SetVerticalJustificationToTop()
usage_text_prop.SetJustificationToLeft()

usage_text_mapper = vtkTextMapper()
usage_text_mapper.SetInput(
    "Slice with mouse wheel\n  or Up/Down-Key\n"
    "- Zoom with pressed right\n  mouse button while dragging")
usage_text_mapper.SetTextProperty(usage_text_prop)

usage_text_actor = vtkActor2D()
usage_text_actor.SetMapper(usage_text_mapper)
usage_text_actor.GetPositionCoordinate().SetCoordinateSystemToNormalizedDisplay()
usage_text_actor.GetPositionCoordinate().SetValue(0.05, 0.95)

# Renderer: assemble the scene and configure the camera
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.AddViewProp(slice_text_actor)
renderer.AddViewProp(usage_text_actor)
renderer.SetBackground(background_rgb)
renderer.ResetCamera()
renderer.GetActiveCamera().ParallelProjectionOn()

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(800, 800)
render_window.SetWindowName("ReadDICOMSeriesApp")

# Interactor: custom slice-browsing style with 2D image interaction
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)
slice_style = SliceInteractorStyle(
    actor, slice_text_mapper, min_slice, max_slice, renderer, render_window)
render_window_interactor.SetInteractorStyle(slice_style)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
