#!/usr/bin/env python

# Generate a ruled stream surface from PLOT3D combustor data using
# vtkRuledSurfaceFilter in PointWalk mode with backward integration.

import os

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonMath import vtkRungeKutta4
from vtkmodules.vtkFiltersCore import vtkStructuredGridOutlineFilter
from vtkmodules.vtkFiltersFlowPaths import vtkStreamTracer
from vtkmodules.vtkFiltersModeling import vtkRuledSurfaceFilter
from vtkmodules.vtkFiltersSources import vtkLineSource
from vtkmodules.vtkIOParallel import vtkMultiBlockPLOT3DReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
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

# Outline
outline = vtkStructuredGridOutlineFilter()
outline.SetInputData(output)

outline_mapper = vtkPolyDataMapper()
outline_mapper.SetInputConnection(outline.GetOutputPort())

outline_actor = vtkActor()
outline_actor.SetMapper(outline_mapper)

# Seed line
seeds = vtkLineSource()
seeds.SetPoint1(15, -5, 32)
seeds.SetPoint2(15, 5, 32)
seeds.SetResolution(10)

# RK4 integrator
integrator = vtkRungeKutta4()

# Stream tracer (backward)
stream_tracer = vtkStreamTracer()
stream_tracer.SetIntegrator(integrator)
stream_tracer.SetInputData(output)
stream_tracer.SetSourceConnection(seeds.GetOutputPort())
stream_tracer.SetMaximumPropagation(100)
stream_tracer.SetInitialIntegrationStep(0.1)
stream_tracer.SetIntegrationDirectionToBackward()

# Ruled surface in PointWalk mode
scalar_surface = vtkRuledSurfaceFilter()
scalar_surface.SetInputConnection(stream_tracer.GetOutputPort())
scalar_surface.SetOffset(0)
scalar_surface.SetOnRatio(2)
scalar_surface.PassLinesOn()
scalar_surface.SetRuledModeToPointWalk()
scalar_surface.SetDistanceFactor(30)

mapper = vtkPolyDataMapper()
mapper.SetInputConnection(scalar_surface.GetOutputPort())

actor = vtkActor()
actor.SetMapper(mapper)

# Seed line actor
seed_mapper = vtkPolyDataMapper()
seed_mapper.SetInputConnection(seeds.GetOutputPort())

seed_actor = vtkActor()
seed_actor.SetMapper(seed_mapper)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(seed_actor)
renderer.AddActor(actor)
renderer.AddActor(outline_actor)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(300, 300)
render_window.SetWindowName("stream surface basic")

# Scene
camera = renderer.GetActiveCamera()
camera.SetClippingRange(3.95297, 50)
camera.SetFocalPoint(8.88908, 0.595038, 29.3342)
camera.SetPosition(-12.3332, 31.7479, 41.2387)
camera.SetViewUp(0.060772, -0.319905, 0.945498)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
