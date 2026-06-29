#!/usr/bin/env python
# Demonstrate vtkSeedWidget with 2D point handle representation on a medical image slice.

import os

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import vtkCommand, vtkLookupTable
from vtkmodules.vtkImagingCore import vtkImageMapToColors
from vtkmodules.vtkInteractionWidgets import (
    vtkPointHandleRepresentation2D,
    vtkSeedRepresentation,
    vtkSeedWidget,
)
from vtkmodules.vtkIOImage import vtkVolume16Reader
from vtkmodules.vtkRenderingCore import (
    vtkImageActor,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Source
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))
file_prefix = os.path.join(data_dir, "headsq", "quarter")

bw_lut = vtkLookupTable()
bw_lut.SetTableRange(0, 2000)
bw_lut.SetSaturationRange(0, 0)
bw_lut.SetHueRange(0, 0)
bw_lut.SetValueRange(0, 1)
bw_lut.Build()

volume_reader = vtkVolume16Reader()
volume_reader.SetDataDimensions(64, 64)
volume_reader.SetDataByteOrderToLittleEndian()
volume_reader.SetFilePrefix(file_prefix)
volume_reader.SetImageRange(1, 93)
volume_reader.SetDataSpacing(3.2, 3.2, 1.5)

# Filter
sagittal_colors = vtkImageMapToColors()
sagittal_colors.SetInputConnection(volume_reader.GetOutputPort())
sagittal_colors.SetLookupTable(bw_lut)

# Actor
sagittal = vtkImageActor()
sagittal.GetMapper().SetInputConnection(sagittal_colors.GetOutputPort())
sagittal.SetDisplayExtent(32, 32, 0, 63, 0, 92)
sagittal.RotateY(90)
sagittal.RotateX(90)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(sagittal)
renderer.SetBackground(0.1, 0.2, 0.4)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("seed widget2d handles")
render_window.SetMultiSamples(0)
render_window.SetSize(300, 300)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)


# Callback for seed widget events.
def seed_callback(caller, event):
    if event == "CursorChangedEvent":
        print("cursor changed")
    else:
        print("point placed")


# Widget
handle_rep = vtkPointHandleRepresentation2D()
handle_rep.GetProperty().SetColor(1, 0, 0)

seed_rep = vtkSeedRepresentation()
seed_rep.SetHandleRepresentation(handle_rep)

seed_widget = vtkSeedWidget()
seed_widget.SetInteractor(interactor)
seed_widget.SetRepresentation(seed_rep)
seed_widget.AddObserver(vtkCommand.PlacePointEvent, seed_callback)
seed_widget.AddObserver(vtkCommand.CursorChangedEvent, seed_callback)
seed_widget.On()

# Scene
renderer.ResetCamera()

interactor.Initialize()
interactor.Start()
