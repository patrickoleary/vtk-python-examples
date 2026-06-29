#!/usr/bin/env python

# Probe PLOT3D combustor data using a cut plane, and display with
# a wireframe comparison plane and outline.

import os

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonDataModel import vtkPlane
from vtkmodules.vtkFiltersCore import (
    vtkCutter,
    vtkProbeFilter,
    vtkStructuredGridOutlineFilter,
)
from vtkmodules.vtkFiltersGeometry import vtkStructuredGridGeometryFilter
from vtkmodules.vtkIOParallel import vtkMultiBlockPLOT3DReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkDataSetMapper,
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

# Cut the data with an angled plane
plane = vtkPlane()
plane.SetOrigin(output.GetCenter())
plane.SetNormal(-0.287, 0, 0.9579)

plane_cut = vtkCutter()
plane_cut.SetInputData(output)
plane_cut.SetCutFunction(plane)

# Probe the cut surface against the source data
probe_filter = vtkProbeFilter()
probe_filter.SetInputConnection(plane_cut.GetOutputPort())
probe_filter.SetSourceData(output)

cut_mapper = vtkDataSetMapper()
cut_mapper.SetInputConnection(probe_filter.GetOutputPort())
cut_mapper.SetScalarRange(output.GetPointData().GetScalars().GetRange())

cut_actor = vtkActor()
cut_actor.SetMapper(cut_mapper)

# Extract a comparison plane at z=9
comp_plane = vtkStructuredGridGeometryFilter()
comp_plane.SetInputData(output)
comp_plane.SetExtent(0, 100, 0, 100, 9, 9)

comp_mapper = vtkPolyDataMapper()
comp_mapper.SetInputConnection(comp_plane.GetOutputPort())
comp_mapper.ScalarVisibilityOff()

comp_actor = vtkActor()
comp_actor.SetMapper(comp_mapper)
comp_actor.GetProperty().SetRepresentationToWireframe()
comp_actor.GetProperty().SetColor(0, 0, 0)

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
renderer.AddActor(comp_actor)
renderer.AddActor(cut_actor)
renderer.SetBackground(1, 1, 1)

# Window
render_window = vtkRenderWindow()
render_window.SetMultiSamples(0)
render_window.AddRenderer(renderer)
render_window.SetSize(400, 300)
render_window.SetWindowName("probe")

# Scene
camera = renderer.GetActiveCamera()
camera.SetClippingRange(11.1034, 59.5328)
camera.SetFocalPoint(9.71821, 0.458166, 29.3999)
camera.SetPosition(-2.95748, -26.7271, 44.5309)
camera.SetViewUp(0.0184785, 0.479657, 0.877262)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
