#!/usr/bin/env python

# Interactively seed streamline ribbons in the combustor using two line widgets.

import os
from pathlib import Path

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
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

# Colors (normalized RGB)
silver = (0.753, 0.753, 0.753)
black = (0.0, 0.0, 0.0)

# Data directory
data_dir = Path(os.environ.get("VPE_DATA_DIR", Path(__file__).parent))

num_streamlines = 25

# Reader: load PLOT3D combustor dataset
pl3d = vtkMultiBlockPLOT3DReader()
pl3d.SetXYZFileName(str(data_dir / "combxyz.bin"))
pl3d.SetQFileName(str(data_dir / "combq.bin"))
pl3d.SetScalarFunctionNumber(100)
pl3d.SetVectorFunctionNumber(202)
pl3d.Update()

sg = pl3d.GetOutput().GetBlock(0)
scalar_range = sg.GetScalarRange()

# Renderer: assemble the scene
renderer = vtkRenderer()

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("StreamlinesWithLineWidget")
render_window.SetSize(512, 512)

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Seed containers for the two line widgets
seeds1 = vtkPolyData()
seeds2 = vtkPolyData()
streamline_actor1 = vtkActor()
streamline_actor2 = vtkActor()


class EnableActorCallback:
    def __init__(self, actor):
        self.actor = actor

    def __call__(self, caller, ev):
        self.actor.VisibilityOn()


class GenerateStreamlinesCallback:
    def __init__(self, poly_data, ren_win):
        self.poly_data = poly_data
        self.ren_win = ren_win

    def __call__(self, caller, ev):
        caller.GetPolyData(self.poly_data)
        self.ren_win.Render()


# Widget 1: line widget seeding streamlines (press 'i' to activate)
line_widget1 = vtkLineWidget()
line_widget1.SetResolution(num_streamlines)
line_widget1.SetInputData(sg)
line_widget1.GetPolyData(seeds1)
line_widget1.SetAlignToNone()
line_widget1.SetPoint1(0.974678, 5.073630, 31.217961)
line_widget1.SetPoint2(0.457544, -4.995921, 31.080175)
line_widget1.ClampToBoundsOn()
line_widget1.PlaceWidget()
line_widget1.SetInteractor(render_window_interactor)
line_widget1.AddObserver("StartInteractionEvent", EnableActorCallback(streamline_actor1))
line_widget1.AddObserver("InteractionEvent", GenerateStreamlinesCallback(seeds1, render_window))

# Widget 2: second line widget (press 'L' to activate)
line_widget2 = vtkLineWidget()
line_widget2.SetResolution(num_streamlines)
line_widget2.SetInputData(sg)
line_widget2.GetPolyData(seeds2)
line_widget2.SetKeyPressActivationValue("L")
line_widget2.SetAlignToZAxis()
line_widget2.ClampToBoundsOn()
line_widget2.PlaceWidget()
line_widget2.SetInteractor(render_window_interactor)
line_widget2.AddObserver("StartInteractionEvent", EnableActorCallback(streamline_actor2))
line_widget2.AddObserver("InteractionEvent", GenerateStreamlinesCallback(seeds2, render_window))

# Filter: streamline ribbon pipeline 1
rk4 = vtkRungeKutta4()

streamer1 = vtkStreamTracer()
streamer1.SetInputData(sg)
streamer1.SetSourceData(seeds1)
streamer1.SetMaximumPropagation(100)
streamer1.SetInitialIntegrationStep(0.2)
streamer1.SetIntegrationDirectionToForward()
streamer1.SetComputeVorticity(1)
streamer1.SetIntegrator(rk4)

ribbon1 = vtkRibbonFilter()
ribbon1.SetInputConnection(streamer1.GetOutputPort())
ribbon1.SetWidth(0.1)
ribbon1.SetWidthFactor(5)

stream_mapper1 = vtkPolyDataMapper()
stream_mapper1.SetInputConnection(ribbon1.GetOutputPort())
stream_mapper1.SetScalarRange(scalar_range)

streamline_actor1.SetMapper(stream_mapper1)
streamline_actor1.VisibilityOff()

# Filter: streamline ribbon pipeline 2
streamer2 = vtkStreamTracer()
streamer2.SetInputData(sg)
streamer2.SetSourceData(seeds2)
streamer2.SetMaximumPropagation(100)
streamer2.SetInitialIntegrationStep(0.2)
streamer2.SetIntegrationDirectionToForward()
streamer2.SetComputeVorticity(1)
streamer2.SetIntegrator(rk4)

ribbon2 = vtkRibbonFilter()
ribbon2.SetInputConnection(streamer2.GetOutputPort())
ribbon2.SetWidth(0.1)
ribbon2.SetWidthFactor(5)

stream_mapper2 = vtkPolyDataMapper()
stream_mapper2.SetInputConnection(ribbon2.GetOutputPort())
stream_mapper2.SetScalarRange(scalar_range)

streamline_actor2.SetMapper(stream_mapper2)
streamline_actor2.VisibilityOff()

# Filter: outline around the data
outline = vtkStructuredGridOutlineFilter()
outline.SetInputData(sg)

outline_mapper = vtkPolyDataMapper()
outline_mapper.SetInputConnection(outline.GetOutputPort())

outline_actor = vtkActor()
outline_actor.SetMapper(outline_mapper)
outline_actor.GetProperty().SetColor(black)

renderer.AddActor(outline_actor)
renderer.AddActor(streamline_actor1)
renderer.AddActor(streamline_actor2)
renderer.SetBackground(silver)

# Seed streamlines from widget 1's initial line position
line_widget1.GetPolyData(seeds1)
streamline_actor1.VisibilityOn()
if not os.environ.get("VTK_DEFAULT_RENDER_WINDOW_OFFSCREEN"):
    line_widget1.EnabledOn()

cam = renderer.GetActiveCamera()
cam.SetClippingRange(14.216207, 68.382915)
cam.SetFocalPoint(9.718210, 0.458166, 29.399900)
cam.SetPosition(-15.827551, -16.997463, 54.003120)
cam.SetViewUp(0.616076, 0.179428, 0.766979)

# Launch the interactive visualization
render_window_interactor.Start()
