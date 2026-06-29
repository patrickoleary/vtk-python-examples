#!/usr/bin/env python

# Read EnSight Gold rigid body (veh) case file at a specific time step and render.

import os

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonExecutionModel import vtkStreamingDemandDrivenPipeline
from vtkmodules.vtkFiltersGeometry import vtkGeometryFilter
from vtkmodules.vtkIOEnSight import vtkGenericEnSightReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkCompositePolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Source
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Read EnSight case file
ensight_reader = vtkGenericEnSightReader()
ensight_reader.SetCaseFileName(os.path.join(data_dir, "EnSight", "veh.case"))
ensight_reader.UpdateInformation()

# Verify time steps
out_info = ensight_reader.GetOutputInformation(0)
num_steps = out_info.Length(vtkStreamingDemandDrivenPipeline.TIME_STEPS())
assert num_steps == 21, f"Expected 21 time steps, got {num_steps}"

# Set time step
out_info.Set(vtkStreamingDemandDrivenPipeline.UPDATE_TIME_STEP(), 36.0)
ensight_reader.Update()

# Extract geometry
geometry_filter = vtkGeometryFilter()
geometry_filter.SetInputConnection(ensight_reader.GetOutputPort())

# Mapper
composite_mapper = vtkCompositePolyDataMapper()
composite_mapper.SetInputConnection(geometry_filter.GetOutputPort())
composite_mapper.SetColorModeToMapScalars()
composite_mapper.SetScalarModeToUseCellFieldData()
composite_mapper.ColorByArrayComponent("evect", 0)

# Actor
ensight_actor = vtkActor()
ensight_actor.SetMapper(composite_mapper)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(ensight_actor)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("ensight gold rigid body")
render_window.SetMultiSamples(0)
render_window.SetSize(300, 300)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
camera = renderer.GetActiveCamera()
camera.SetFocalPoint(1.5, 0, -6.5)
camera.SetPosition(26.4, 2.7, 1.4)
camera.SetViewUp(-0.1, 1.0, -0.02)

interactor.Initialize()
interactor.Start()
