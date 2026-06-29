#!/usr/bin/env python

# Demonstrate vtkPolyDataConnectivityFilter with scalar connectivity
# on a slice of PLOT3D combustor data.

import os

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersCore import (
    vtkPolyDataConnectivityFilter,
    vtkStructuredGridOutlineFilter,
)
from vtkmodules.vtkFiltersGeometry import vtkStructuredGridGeometryFilter
from vtkmodules.vtkIOParallel import vtkMultiBlockPLOT3DReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkCamera,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Data directory
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Read PLOT3D combustor data
plot3d_reader = vtkMultiBlockPLOT3DReader()
plot3d_reader.SetXYZFileName(os.path.join(data_dir, "combxyz.bin"))
plot3d_reader.SetQFileName(os.path.join(data_dir, "combq.bin"))
plot3d_reader.SetScalarFunctionNumber(100)
plot3d_reader.SetVectorFunctionNumber(202)
plot3d_reader.Update()
output = plot3d_reader.GetOutput().GetBlock(0)

# Extract a plane and filter by scalar connectivity
plane_1 = vtkStructuredGridGeometryFilter()
plane_1.SetInputData(output)
plane_1.SetExtent(20, 20, 0, 100, 0, 100)

connectivity = vtkPolyDataConnectivityFilter()
connectivity.SetInputConnection(plane_1.GetOutputPort())
connectivity.ScalarConnectivityOn()
connectivity.SetScalarRange(0.19, 0.25)
connectivity.Update()

plane_1_mapper = vtkPolyDataMapper()
plane_1_mapper.SetInputConnection(connectivity.GetOutputPort())
plane_1_mapper.SetScalarRange(output.GetScalarRange())

plane_1_actor = vtkActor()
plane_1_actor.SetMapper(plane_1_mapper)
plane_1_actor.GetProperty().SetOpacity(0.999)

# Outline
outline = vtkStructuredGridOutlineFilter()
outline.SetInputData(output)

outline_mapper = vtkPolyDataMapper()
outline_mapper.SetInputConnection(outline.GetOutputPort())

outline_actor = vtkActor()
outline_actor.SetMapper(outline_mapper)
outline_actor.GetProperty().SetColor(0, 0, 0)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(outline_actor)
renderer.AddActor(plane_1_actor)
renderer.SetBackground(1, 1, 1)

# Window
render_window = vtkRenderWindow()
render_window.SetMultiSamples(0)
render_window.AddRenderer(renderer)
render_window.SetSize(300, 300)
render_window.SetWindowName("poly conn")

# Scene
camera = vtkCamera()
camera.SetClippingRange(14.29, 63.53)
camera.SetFocalPoint(8.58522, 1.58266, 30.6486)
camera.SetPosition(37.6808, -20.1298, 35.4016)
camera.SetViewAngle(30)
camera.SetViewUp(-0.0566235, 0.140504, 0.98846)
renderer.SetActiveCamera(camera)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
