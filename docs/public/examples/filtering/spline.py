#!/usr/bin/env python

# Demonstrate vtkSplineFilter on stream traces through PLOT3D combustor
# data, displaying spline-smoothed ribbons colored by scalar field.

import os

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonDataModel import vtkDataObject
from vtkmodules.vtkCommonMath import vtkRungeKutta4
from vtkmodules.vtkFiltersCore import vtkStructuredGridOutlineFilter
from vtkmodules.vtkFiltersFlowPaths import vtkStreamTracer
from vtkmodules.vtkFiltersGeneral import vtkSplineFilter
from vtkmodules.vtkFiltersModeling import vtkRibbonFilter
from vtkmodules.vtkFiltersSources import vtkPlaneSource
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

# Read PLOT3D data
pl3d = vtkMultiBlockPLOT3DReader()
pl3d.SetXYZFileName(os.path.join(data_dir, "combxyz.bin"))
pl3d.SetQFileName(os.path.join(data_dir, "combq.bin"))
pl3d.SetScalarFunctionNumber(100)
pl3d.SetVectorFunctionNumber(202)
pl3d.Update()
output = pl3d.GetOutput().GetBlock(0)

# Seed plane for stream tracer
ps = vtkPlaneSource()
ps.SetXResolution(4)
ps.SetYResolution(4)
ps.SetOrigin(2, -2, 26)
ps.SetPoint1(2, 2, 26)
ps.SetPoint2(2, -2, 32)

ps_mapper = vtkPolyDataMapper()
ps_mapper.SetInputConnection(ps.GetOutputPort())

ps_actor = vtkActor()
ps_actor.SetMapper(ps_mapper)
ps_actor.GetProperty().SetRepresentationToWireframe()

# Stream tracer with RK4
rk4 = vtkRungeKutta4()

streamer = vtkStreamTracer()
streamer.SetInputData(output)
streamer.SetSourceData(ps.GetOutput())
streamer.SetMaximumPropagation(100)
streamer.SetInitialIntegrationStep(0.2)
streamer.SetIntegrationDirectionToForward()
streamer.SetComputeVorticity(1)
streamer.SetIntegrator(rk4)

# Spline filter to smooth the stream lines
sf = vtkSplineFilter()
sf.SetInputConnection(streamer.GetOutputPort())
sf.SetSubdivideToLength()
sf.SetLength(0.15)

# Ribbon filter for visualization
rf = vtkRibbonFilter()
rf.SetInputConnection(sf.GetOutputPort())
rf.SetInputArrayToProcess(1, 0, 0, vtkDataObject.FIELD_ASSOCIATION_POINTS, "Normals")
rf.SetWidth(0.1)
rf.SetWidthFactor(5)

stream_mapper = vtkPolyDataMapper()
stream_mapper.SetInputConnection(rf.GetOutputPort())
stream_mapper.SetScalarRange(output.GetScalarRange())

streamline_actor = vtkActor()
streamline_actor.SetMapper(stream_mapper)

# Outline of the structured grid
outline = vtkStructuredGridOutlineFilter()
outline.SetInputData(output)

outline_mapper = vtkPolyDataMapper()
outline_mapper.SetInputConnection(outline.GetOutputPort())

outline_actor = vtkActor()
outline_actor.SetMapper(outline_mapper)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(ps_actor)
renderer.AddActor(outline_actor)
renderer.AddActor(streamline_actor)
renderer.SetBackground(0.1, 0.2, 0.4)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(300, 300)
render_window.SetWindowName("spline")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
cam = renderer.GetActiveCamera()
cam.SetClippingRange(3.95297, 50)
cam.SetFocalPoint(9.71821, 0.458166, 29.3999)
cam.SetPosition(2.7439, -37.3196, 38.7167)
cam.SetViewUp(-0.16123, 0.264271, 0.950876)

interactor.Initialize()
interactor.Start()
