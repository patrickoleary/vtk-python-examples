#!/usr/bin/env python

# Read Plot3D meta file with time steps and render a scalar plane.

import os

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonExecutionModel import vtkStreamingDemandDrivenPipeline
from vtkmodules.vtkFiltersGeometry import vtkStructuredGridGeometryFilter
from vtkmodules.vtkIOParallel import vtkPlot3DMetaReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkCamera,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Source
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Read Plot3D meta file
meta_reader = vtkPlot3DMetaReader()
meta_reader.SetFileName(os.path.join(data_dir, "test.p3d"))

meta_reader.UpdateInformation()
output_info = meta_reader.GetOutputInformation(0)
num_steps = output_info.Length(vtkStreamingDemandDrivenPipeline.TIME_STEPS())
assert num_steps == 2, f"Wrong number of time steps: {num_steps}, expected 2"

# Read at time step 3.5
output_info.Set(vtkStreamingDemandDrivenPipeline.UPDATE_TIME_STEP(), 3.5)
meta_reader.Update()

# Read at time step 4.5
output_info.Set(vtkStreamingDemandDrivenPipeline.UPDATE_TIME_STEP(), 4.5)
meta_reader.Update()

output = meta_reader.GetOutput().GetBlock(0)

# Extract plane
geometry_filter = vtkStructuredGridGeometryFilter()
geometry_filter.SetInputData(output)
geometry_filter.SetExtent(25, 25, 0, 100, 0, 100)

# Mapper
poly_mapper = vtkPolyDataMapper()
poly_mapper.SetInputConnection(geometry_filter.GetOutputPort())
poly_mapper.SetScalarRange(output.GetPointData().GetScalars().GetRange())

# Actor
plane_actor = vtkActor()
plane_actor.SetMapper(poly_mapper)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(plane_actor)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("plot3d meta")
render_window.SetMultiSamples(0)
render_window.SetSize(400, 300)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
camera = vtkCamera()
renderer.SetActiveCamera(camera)
camera.SetViewUp(0, 1, 0)
camera.SetFocalPoint(0, 0, 0)
camera.SetPosition(1, 0, 0)
renderer.ResetCamera()
camera.Dolly(1.25)
renderer.ResetCameraClippingRange()

interactor.Initialize()
interactor.Start()
