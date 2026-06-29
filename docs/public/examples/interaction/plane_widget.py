#!/usr/bin/env python
# Demonstrate vtkPlaneWidget probing PLOT3D data with interactive plane positioning.

import os

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonDataModel import vtkPolyData
from vtkmodules.vtkFiltersCore import vtkProbeFilter, vtkStructuredGridOutlineFilter
from vtkmodules.vtkInteractionWidgets import vtkPlaneWidget
from vtkmodules.vtkIOParallel import vtkMultiBlockPLOT3DReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Source
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

plot3d_reader = vtkMultiBlockPLOT3DReader()
plot3d_reader.SetXYZFileName(os.path.join(data_dir, "combxyz.bin"))
plot3d_reader.SetQFileName(os.path.join(data_dir, "combq.bin"))
plot3d_reader.SetScalarFunctionNumber(100)
plot3d_reader.SetVectorFunctionNumber(202)
plot3d_reader.Update()
plot3d_block0 = plot3d_reader.GetOutput().GetBlock(0)

plane = vtkPolyData()

# Filter
probe = vtkProbeFilter()
probe.SetInputData(plane)
probe.SetSourceData(plot3d_block0)

outline = vtkStructuredGridOutlineFilter()
outline.SetInputData(plot3d_block0)

# Mapper + Actor (probe)
probe_mapper = vtkPolyDataMapper()
probe_mapper.SetInputConnection(probe.GetOutputPort())
scalar_range = plot3d_block0.GetScalarRange()
probe_mapper.SetScalarRange(scalar_range[0], scalar_range[1])

probe_actor = vtkActor()
probe_actor.SetMapper(probe_mapper)
probe_actor.VisibilityOff()

# Mapper + Actor (outline)
outline_mapper = vtkPolyDataMapper()
outline_mapper.SetInputConnection(outline.GetOutputPort())

outline_actor = vtkActor()
outline_actor.SetMapper(outline_mapper)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(probe_actor)
renderer.AddActor(outline_actor)
renderer.SetBackground(0.1, 0.2, 0.4)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("plane widget")
render_window.SetMultiSamples(0)
render_window.SetSize(300, 300)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)


# Callback updates the probe plane and makes the actor visible
def plane_callback(caller, event_string):
    caller.GetPolyData(plane)
    probe_actor.VisibilityOn()


# Widget
plane_widget = vtkPlaneWidget()
plane_widget.SetInteractor(interactor)
plane_widget.SetInputData(plot3d_block0)
plane_widget.NormalToXAxisOn()
plane_widget.SetResolution(20)
plane_widget.SetRepresentationToOutline()
plane_widget.PlaceWidget()
plane_widget.AddObserver("InteractionEvent", plane_callback)
plane_widget.On()

# Scene
renderer.ResetCamera()

interactor.Initialize()
interactor.Start()
