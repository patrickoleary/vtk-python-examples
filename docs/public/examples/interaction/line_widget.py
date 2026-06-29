#!/usr/bin/env python
# Demonstrate vtkLineWidget seeding streamlines on PLOT3D data with ribbon visualization.

import os

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonDataModel import vtkPolyData
from vtkmodules.vtkCommonMath import vtkRungeKutta4
from vtkmodules.vtkFiltersCore import vtkStructuredGridOutlineFilter
from vtkmodules.vtkFiltersFlowPaths import vtkStreamTracer
from vtkmodules.vtkFiltersModeling import vtkRibbonFilter
from vtkmodules.vtkIOParallel import vtkMultiBlockPLOT3DReader
from vtkmodules.vtkInteractionWidgets import vtkLineWidget
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Source: PLOT3D data
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

plot3d_reader = vtkMultiBlockPLOT3DReader()
plot3d_reader.SetXYZFileName(os.path.join(data_dir, "combxyz.bin"))
plot3d_reader.SetQFileName(os.path.join(data_dir, "combq.bin"))
plot3d_reader.SetScalarFunctionNumber(100)
plot3d_reader.SetVectorFunctionNumber(202)
plot3d_reader.Update()
plot3d_block0 = plot3d_reader.GetOutput().GetBlock(0)

seeds = vtkPolyData()

# Filters
integrator = vtkRungeKutta4()

streamer = vtkStreamTracer()
streamer.SetInputData(plot3d_block0)
streamer.SetSourceData(seeds)
streamer.SetMaximumPropagation(100)
streamer.SetInitialIntegrationStep(0.2)
streamer.SetIntegrationDirectionToForward()
streamer.SetComputeVorticity(True)
streamer.SetIntegrator(integrator)

ribbon_filter = vtkRibbonFilter()
ribbon_filter.SetInputConnection(streamer.GetOutputPort())
ribbon_filter.SetInputArrayToProcess(1, 0, 0, 0, "Normals")
ribbon_filter.SetWidth(0.1)
ribbon_filter.SetWidthFactor(5)

outline = vtkStructuredGridOutlineFilter()
outline.SetInputData(plot3d_block0)

# Mapper + Actor
stream_mapper = vtkPolyDataMapper()
stream_mapper.SetInputConnection(ribbon_filter.GetOutputPort())
scalar_range = plot3d_block0.GetScalarRange()
stream_mapper.SetScalarRange(scalar_range[0], scalar_range[1])

streamline_actor = vtkActor()
streamline_actor.SetMapper(stream_mapper)
streamline_actor.VisibilityOff()

outline_mapper = vtkPolyDataMapper()
outline_mapper.SetInputConnection(outline.GetOutputPort())

outline_actor = vtkActor()
outline_actor.SetMapper(outline_mapper)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(streamline_actor)
renderer.AddActor(outline_actor)
renderer.SetBackground(0.1, 0.2, 0.4)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("line widget")
render_window.SetMultiSamples(0)
render_window.SetSize(300, 300)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)


# Callback updates seed points and makes streamline visible
def line_callback(caller, event_string):
    caller.GetPolyData(seeds)
    streamline_actor.VisibilityOn()


# Widget
line_widget = vtkLineWidget()
line_widget.SetInteractor(interactor)
line_widget.SetInputData(plot3d_block0)
line_widget.SetAlignToYAxis()
line_widget.PlaceWidget()
line_widget.GetPolyData(seeds)
line_widget.AddObserver("InteractionEvent", line_callback)
line_widget.On()

# Scene
renderer.ResetCamera()

interactor.Initialize()
interactor.Start()
