#!/usr/bin/env python

# Clip a medical CT slice using vtkClipDataSet with an outline.

import os

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersGeneral import vtkClipDataSet
from vtkmodules.vtkFiltersModeling import vtkOutlineFilter
from vtkmodules.vtkIOImage import vtkVolume16Reader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkDataSetMapper,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Data directory
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Read CT head data
v16 = vtkVolume16Reader()
v16.SetDataDimensions(64, 64)
v16.GetOutput().SetOrigin(0.0, 0.0, 0.0)
v16.SetDataByteOrderToLittleEndian()
v16.SetFilePrefix(os.path.join(data_dir, "headsq", "quarter"))
v16.SetImageRange(45, 45)
v16.SetDataSpacing(3.2, 3.2, 1.5)
v16.Update()

# Clip the pixel data
clip = vtkClipDataSet()
clip.SetInputConnection(v16.GetOutputPort())
clip.SetValue(1000)

clip_mapper = vtkDataSetMapper()
clip_mapper.SetInputConnection(clip.GetOutputPort())
clip_mapper.ScalarVisibilityOff()

clip_actor = vtkActor()
clip_actor.SetMapper(clip_mapper)

# Outline around the data
outline = vtkOutlineFilter()
outline.SetInputConnection(v16.GetOutputPort())

outline_mapper = vtkPolyDataMapper()
outline_mapper.SetInputConnection(outline.GetOutputPort())

outline_actor = vtkActor()
outline_actor.SetMapper(outline_mapper)
outline_actor.VisibilityOff()

# Renderer
renderer = vtkRenderer()
renderer.AddActor(outline_actor)
renderer.AddActor(clip_actor)
renderer.SetBackground(0, 0, 0)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(200, 200)
render_window.SetWindowName("clip image")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
