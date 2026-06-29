#!/usr/bin/env python

# Cut a composite dataset (multi-block and partitioned) with
# vtkPlaneCutter, comparing results in two viewports.

import os

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonDataModel import vtkPlane
from vtkmodules.vtkFiltersCore import (
    vtkConvertToMultiBlockDataSet,
    vtkPlaneCutter,
)
from vtkmodules.vtkIOIOSS import vtkIOSSReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkCompositePolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Data file path (relative to this script)
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Reader: load Exodus II file
reader = vtkIOSSReader()
reader.SetFileName(os.path.join(data_dir, "can.ex2"))
reader.Update()

# Convert to multi-block dataset
mb_converter = vtkConvertToMultiBlockDataSet()
mb_converter.SetInputConnection(reader.GetOutputPort())

# Cut plane
plane = vtkPlane()
plane.SetOrigin(0, 0, 0)
plane.SetNormal(1, 1, 1)

# Cut the multi-block dataset
cut_0 = vtkPlaneCutter()
cut_0.SetInputConnection(mb_converter.GetOutputPort())
cut_0.SetPlane(plane)
cut_0.ComputeNormalsOff()

cutter_mapper_0 = vtkCompositePolyDataMapper()
cutter_mapper_0.SetInputConnection(cut_0.GetOutputPort())
cutter_mapper_0.ScalarVisibilityOff()

cutter_actor_0 = vtkActor()
cutter_actor_0.SetMapper(cutter_mapper_0)
cutter_actor_0.GetProperty().SetColor(1, 1, 1)

# Cut the partitioned dataset directly
cut_1 = vtkPlaneCutter()
cut_1.SetInputConnection(reader.GetOutputPort())
cut_1.SetPlane(plane)
cut_1.ComputeNormalsOff()

cutter_mapper_1 = vtkCompositePolyDataMapper()
cutter_mapper_1.SetInputConnection(cut_1.GetOutputPort())
cutter_mapper_1.ScalarVisibilityOff()

cutter_actor_1 = vtkActor()
cutter_actor_1.SetMapper(cutter_mapper_1)
cutter_actor_1.GetProperty().SetColor(1, 1, 1)

# Two viewports
renderer_0 = vtkRenderer()
renderer_0.SetViewport(0, 0, 0.5, 1)
renderer_0.AddActor(cutter_actor_0)
renderer_0.SetBackground(0, 0, 0)

renderer_1 = vtkRenderer()
renderer_1.SetViewport(0.5, 0, 1, 1)
renderer_1.AddActor(cutter_actor_1)
renderer_1.SetBackground(0, 0, 0)

# Window
render_window = vtkRenderWindow()
render_window.SetMultiSamples(0)
render_window.AddRenderer(renderer_0)
render_window.AddRenderer(renderer_1)
render_window.SetSize(600, 300)
render_window.SetWindowName("composite dataset plane cutter")

# Scene
renderer_0.ResetCamera()
renderer_1.ResetCamera()

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
