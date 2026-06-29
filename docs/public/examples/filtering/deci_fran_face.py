#!/usr/bin/env python

# Compare vtkDecimatePro with different topology and error accumulation
# settings on a textured face model, shown in four viewports.

import os

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersCore import vtkDecimatePro
from vtkmodules.vtkIOImage import vtkPNGReader
from vtkmodules.vtkIOLegacy import vtkPolyDataReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkCamera,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
    vtkTexture,
)

# Data directory
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Read the face texture
png_reader = vtkPNGReader()
png_reader.SetFileName(os.path.join(data_dir, "fran_cut.png"))
texture = vtkTexture()
texture.SetInputConnection(png_reader.GetOutputPort())
texture.InterpolateOn()

# Read the face geometry
fran = vtkPolyDataReader()
fran.SetFileName(os.path.join(data_dir, "fran_cut.vtk"))

# --- TopologyOn + AccumulateOn ---
deci_on_on = vtkDecimatePro()
deci_on_on.SetInputConnection(fran.GetOutputPort())
deci_on_on.SetTargetReduction(0.95)
deci_on_on.PreserveTopologyOn()
deci_on_on.AccumulateErrorOn()
mapper_on_on = vtkPolyDataMapper()
mapper_on_on.SetInputConnection(deci_on_on.GetOutputPort())
actor_on_on = vtkActor()
actor_on_on.SetMapper(mapper_on_on)
actor_on_on.SetTexture(texture)

# --- TopologyOn + AccumulateOff ---
deci_on_off = vtkDecimatePro()
deci_on_off.SetInputConnection(fran.GetOutputPort())
deci_on_off.SetTargetReduction(0.95)
deci_on_off.PreserveTopologyOn()
deci_on_off.AccumulateErrorOff()
mapper_on_off = vtkPolyDataMapper()
mapper_on_off.SetInputConnection(deci_on_off.GetOutputPort())
actor_on_off = vtkActor()
actor_on_off.SetMapper(mapper_on_off)
actor_on_off.SetTexture(texture)

# --- TopologyOff + AccumulateOn ---
deci_off_on = vtkDecimatePro()
deci_off_on.SetInputConnection(fran.GetOutputPort())
deci_off_on.SetTargetReduction(0.95)
deci_off_on.PreserveTopologyOff()
deci_off_on.AccumulateErrorOn()
mapper_off_on = vtkPolyDataMapper()
mapper_off_on.SetInputConnection(deci_off_on.GetOutputPort())
actor_off_on = vtkActor()
actor_off_on.SetMapper(mapper_off_on)
actor_off_on.SetTexture(texture)

# --- TopologyOff + AccumulateOff ---
deci_off_off = vtkDecimatePro()
deci_off_off.SetInputConnection(fran.GetOutputPort())
deci_off_off.SetTargetReduction(0.95)
deci_off_off.PreserveTopologyOff()
deci_off_off.AccumulateErrorOff()
mapper_off_off = vtkPolyDataMapper()
mapper_off_off.SetInputConnection(deci_off_off.GetOutputPort())
actor_off_off = vtkActor()
actor_off_off.SetMapper(mapper_off_off)
actor_off_off.SetTexture(texture)

# Renderers for four viewports
renderer_0 = vtkRenderer()
renderer_0.SetViewport(0, 0.5, 0.5, 1)
renderer_0.AddActor(actor_on_on)
renderer_0.SetBackground(1, 1, 1)

renderer_1 = vtkRenderer()
renderer_1.SetViewport(0.5, 0.5, 1, 1)
renderer_1.AddActor(actor_on_off)
renderer_1.SetBackground(1, 1, 1)

renderer_2 = vtkRenderer()
renderer_2.SetViewport(0, 0, 0.5, 0.5)
renderer_2.AddActor(actor_off_on)
renderer_2.SetBackground(1, 1, 1)

renderer_3 = vtkRenderer()
renderer_3.SetViewport(0.5, 0, 1, 0.5)
renderer_3.AddActor(actor_off_off)
renderer_3.SetBackground(1, 1, 1)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer_0)
render_window.AddRenderer(renderer_1)
render_window.AddRenderer(renderer_2)
render_window.AddRenderer(renderer_3)
render_window.SetSize(500, 500)
render_window.SetWindowName("deci fran face")

# Scene
camera = vtkCamera()
camera.SetPosition(0.314753, -0.0699988, -0.264225)
camera.SetFocalPoint(0.00188636, -0.136847, -5.84226e-09)
camera.SetViewAngle(30)
camera.SetViewUp(0, 1, 0)

renderer_0.SetActiveCamera(camera)
renderer_1.SetActiveCamera(camera)
renderer_2.SetActiveCamera(camera)
renderer_3.SetActiveCamera(camera)

renderer_0.ResetCameraClippingRange()
renderer_1.ResetCameraClippingRange()
renderer_2.ResetCameraClippingRange()
renderer_3.ResetCameraClippingRange()

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
