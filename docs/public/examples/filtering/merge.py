#!/usr/bin/env python

# Demonstrate vtkMergeFilter by probing PLOT3D combustor data along a line,
# then merging geometry with scalar data for a warp display.

import os

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersCore import (
    vtkMergeFilter,
    vtkProbeFilter,
    vtkStructuredGridOutlineFilter,
    vtkTubeFilter,
)
from vtkmodules.vtkFiltersGeneral import vtkWarpScalar
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
plot3d_reader.SetScalarFunctionNumber(110)
plot3d_reader.SetVectorFunctionNumber(202)
plot3d_reader.Update()
output = plot3d_reader.GetOutput().GetBlock(0)

# Probe along a line through the data
probe_line = vtkLineSource()
probe_line.SetPoint1(1, 1, 29)
probe_line.SetPoint2(16.5, 5, 31.7693)
probe_line.SetResolution(500)

probe = vtkProbeFilter()
probe.SetInputConnection(probe_line.GetOutputPort())
probe.SetSourceData(output)
probe.Update()

# Tube around the probe line for 3D view
probe_tube = vtkTubeFilter()
probe_tube.SetInputData(probe.GetPolyDataOutput())
probe_tube.SetNumberOfSides(5)
probe_tube.SetRadius(0.05)

probe_mapper = vtkPolyDataMapper()
probe_mapper.SetInputConnection(probe_tube.GetOutputPort())
probe_mapper.SetScalarRange(output.GetScalarRange())

probe_actor = vtkActor()
probe_actor.SetMapper(probe_mapper)

# Merge geometry of a flat line with probe scalars for 2D warp display
display_line = vtkLineSource()
display_line.SetPoint1(0, 0, 0)
display_line.SetPoint2(1, 0, 0)
display_line.SetResolution(probe_line.GetResolution())

display_merge = vtkMergeFilter()
display_merge.SetGeometryConnection(display_line.GetOutputPort())
display_merge.SetScalarsData(probe.GetPolyDataOutput())
display_merge.Update()

display_warp = vtkWarpScalar()
display_warp.SetInputData(display_merge.GetPolyDataOutput())
display_warp.SetNormal(0, 1, 0)
display_warp.SetScaleFactor(0.000001)
display_warp.Update()

display_mapper = vtkPolyDataMapper()
display_mapper.SetInputData(display_warp.GetPolyDataOutput())
display_mapper.SetScalarRange(output.GetScalarRange())

display_actor = vtkActor()
display_actor.SetMapper(display_mapper)

# Outline of the structured grid
outline = vtkStructuredGridOutlineFilter()
outline.SetInputData(output)

outline_mapper = vtkPolyDataMapper()
outline_mapper.SetInputConnection(outline.GetOutputPort())

outline_actor = vtkActor()
outline_actor.SetMapper(outline_mapper)
outline_actor.GetProperty().SetColor(0, 0, 0)

# Renderers — top viewport for 3D, bottom strip for 2D plot
renderer_0 = vtkRenderer()
renderer_0.AddActor(outline_actor)
renderer_0.AddActor(probe_actor)
renderer_0.SetBackground(1, 1, 1)
renderer_0.SetViewport(0, 0.25, 1, 1)
renderer_1 = vtkRenderer()
renderer_1.AddActor(display_actor)
renderer_1.SetBackground(0, 0, 0)
renderer_1.SetViewport(0, 0, 1, 0.25)

# Window
render_window = vtkRenderWindow()
render_window.SetMultiSamples(0)
render_window.AddRenderer(renderer_0)
render_window.AddRenderer(renderer_1)
render_window.SetSize(300, 300)
render_window.SetWindowName("merge")

# Scene
renderer_0.ResetCamera()
camera_0 = renderer_0.GetActiveCamera()
camera_0.SetClippingRange(3.95297, 50)
camera_0.SetFocalPoint(8.88908, 0.595038, 29.3342)
camera_0.SetPosition(9.9, -26, 41)
camera_0.SetViewUp(0.060772, -0.319905, 0.945498)
renderer_1.ResetCamera()
camera_1 = renderer_1.GetActiveCamera()
camera_1.ParallelProjectionOn()
camera_1.SetParallelScale(0.15)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
