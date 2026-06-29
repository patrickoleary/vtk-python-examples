#!/usr/bin/env python

# Clip EnSight elements data with a plane using vtkTableBasedClipDataSet
# and visualize the clipped unstructured grid.

import os

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonDataModel import vtkPlane
from vtkmodules.vtkFiltersGeneral import vtkTableBasedClipDataSet
from vtkmodules.vtkIOEnSight import vtkEnSightGoldReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkDataSetMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Data directory
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Read EnSight elements data
reader = vtkEnSightGoldReader()
reader.SetCaseFileName(os.path.join(data_dir, "EnSight", "elements.case"))
reader.Update()

# Clip with a plane
plane = vtkPlane()
plane.SetOrigin(3.5, 3.5, 0.5)
plane.SetNormal(0, 0, 1)

clipper = vtkTableBasedClipDataSet()
clipper.SetInputConnection(reader.GetOutputPort())
clipper.SetClipFunction(plane)
clipper.SetInsideOut(1)
clipper.Update()

data = clipper.GetOutputDataObject(0).GetBlock(0)

mapper = vtkDataSetMapper()
mapper.SetInputData(data)

actor = vtkActor()
actor.SetMapper(mapper)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(0.1, 0.2, 0.4)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(400, 400)
render_window.SetWindowName("table based clip")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
camera = renderer.GetActiveCamera()
camera.SetPosition(-7.9, 9.7, 14.6)
camera.SetFocalPoint(3.5, 3.5, 0.5)
camera.SetViewUp(0.08, 0.93, -0.34)
renderer.ResetCameraClippingRange()

interactor.Initialize()
interactor.Start()
