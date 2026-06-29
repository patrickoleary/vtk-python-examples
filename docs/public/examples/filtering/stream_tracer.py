#!/usr/bin/env python

# Trace streamlines through office airflow data using vtkStreamTracer
# with a Runge-Kutta 4/5 integrator and display as ribbons.

import os

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonMath import vtkRungeKutta45
from vtkmodules.vtkFiltersCore import (
    vtkAssignAttribute,
    vtkStructuredGridOutlineFilter,
)
from vtkmodules.vtkFiltersFlowPaths import vtkStreamTracer
from vtkmodules.vtkFiltersModeling import vtkRibbonFilter
from vtkmodules.vtkIOLegacy import vtkStructuredGridReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Data directory
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Read office airflow data
reader = vtkStructuredGridReader()
reader.SetFileName(os.path.join(data_dir, "office.binary.vtk"))
reader.Update()

# Outline
outline = vtkStructuredGridOutlineFilter()
outline.SetInputConnection(reader.GetOutputPort())

outline_mapper = vtkPolyDataMapper()
outline_mapper.SetInputConnection(outline.GetOutputPort())

outline_actor = vtkActor()
outline_actor.SetMapper(outline_mapper)
outline_actor.GetProperty().SetColor(0, 0, 0)

# Stream tracer with RK45 integrator
rk = vtkRungeKutta45()

streamer = vtkStreamTracer()
streamer.SetInputConnection(reader.GetOutputPort())
streamer.SetStartPosition(0.1, 2.1, 0.5)
streamer.SetMaximumPropagation(500)
streamer.SetIntegrationStepUnit(2)
streamer.SetMinimumIntegrationStep(0.1)
streamer.SetMaximumIntegrationStep(1.0)
streamer.SetInitialIntegrationStep(0.2)
streamer.SetIntegrationDirection(0)
streamer.SetIntegrator(rk)
streamer.SetRotationScale(0.5)
streamer.SetMaximumError(1.0e-8)

aa = vtkAssignAttribute()
aa.SetInputConnection(streamer.GetOutputPort())
aa.Assign("Normals", "NORMALS", "POINT_DATA")

# Ribbon filter
rf = vtkRibbonFilter()
rf.SetInputConnection(aa.GetOutputPort())
rf.SetWidth(0.1)
rf.VaryWidthOff()

stream_mapper = vtkPolyDataMapper()
stream_mapper.SetInputConnection(rf.GetOutputPort())
stream_mapper.SetScalarRange(reader.GetOutput().GetScalarRange())

stream_actor = vtkActor()
stream_actor.SetMapper(stream_mapper)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(outline_actor)
renderer.AddActor(stream_actor)
renderer.SetBackground(0.4, 0.4, 0.5)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(300, 200)
render_window.SetWindowName("stream tracer")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
cam = renderer.GetActiveCamera()
cam.SetPosition(-2.35599, -3.35001, 4.59236)
cam.SetFocalPoint(2.255, 2.255, 1.28413)
cam.SetViewUp(0.311311, 0.279912, 0.908149)
cam.SetClippingRange(1.12294, 16.6226)

interactor.Initialize()
interactor.Start()
