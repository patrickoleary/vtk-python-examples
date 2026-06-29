#!/usr/bin/env python

# Probe PLOT3D combustor data with three transformed planes, then
# isocontour the probed results. Uses vtkAppendPolyData to merge planes.

import os

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonTransforms import vtkTransform
from vtkmodules.vtkFiltersCore import (
    vtkAppendPolyData,
    vtkContourFilter,
    vtkProbeFilter,
    vtkStructuredGridOutlineFilter,
)
from vtkmodules.vtkFiltersGeneral import vtkTransformPolyDataFilter
from vtkmodules.vtkFiltersModeling import vtkOutlineFilter
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

# Read PLOT3D combustor data
plot3d_reader = vtkMultiBlockPLOT3DReader()
plot3d_reader.SetXYZFileName(os.path.join(data_dir, "combxyz.bin"))
plot3d_reader.SetQFileName(os.path.join(data_dir, "combq.bin"))
plot3d_reader.SetScalarFunctionNumber(100)
plot3d_reader.SetVectorFunctionNumber(202)
plot3d_reader.Update()
output = plot3d_reader.GetOutput().GetBlock(0)

# Shared plane source
plane = vtkPlaneSource()
plane.SetResolution(50, 50)

# --- Plane 1 ---
trans_p1 = vtkTransform()
trans_p1.Translate(3.7, 0.0, 28.37)
trans_p1.Scale(5, 5, 5)
trans_p1.RotateY(90)

transform_filter_1 = vtkTransformPolyDataFilter()
transform_filter_1.SetInputConnection(plane.GetOutputPort())
transform_filter_1.SetTransform(trans_p1)

outline_filter_1 = vtkOutlineFilter()
outline_filter_1.SetInputConnection(transform_filter_1.GetOutputPort())
outline_mapper_1 = vtkPolyDataMapper()
outline_mapper_1.SetInputConnection(outline_filter_1.GetOutputPort())
outline_actor_1 = vtkActor()
outline_actor_1.SetMapper(outline_mapper_1)
outline_actor_1.GetProperty().SetColor(0, 0, 0)

# --- Plane 2 ---
trans_p2 = vtkTransform()
trans_p2.Translate(9.2, 0.0, 31.20)
trans_p2.Scale(5, 5, 5)
trans_p2.RotateY(90)

transform_filter_2 = vtkTransformPolyDataFilter()
transform_filter_2.SetInputConnection(plane.GetOutputPort())
transform_filter_2.SetTransform(trans_p2)

outline_filter_2 = vtkOutlineFilter()
outline_filter_2.SetInputConnection(transform_filter_2.GetOutputPort())
outline_mapper_2 = vtkPolyDataMapper()
outline_mapper_2.SetInputConnection(outline_filter_2.GetOutputPort())
outline_actor_2 = vtkActor()
outline_actor_2.SetMapper(outline_mapper_2)
outline_actor_2.GetProperty().SetColor(0, 0, 0)

# --- Plane 3 ---
trans_p3 = vtkTransform()
trans_p3.Translate(13.27, 0.0, 33.30)
trans_p3.Scale(5, 5, 5)
trans_p3.RotateY(90)

transform_filter_3 = vtkTransformPolyDataFilter()
transform_filter_3.SetInputConnection(plane.GetOutputPort())
transform_filter_3.SetTransform(trans_p3)

outline_filter_3 = vtkOutlineFilter()
outline_filter_3.SetInputConnection(transform_filter_3.GetOutputPort())
outline_mapper_3 = vtkPolyDataMapper()
outline_mapper_3.SetInputConnection(outline_filter_3.GetOutputPort())
outline_actor_3 = vtkActor()
outline_actor_3.SetMapper(outline_mapper_3)
outline_actor_3.GetProperty().SetColor(0, 0, 0)

# Append all three planes and probe
append_filter = vtkAppendPolyData()
append_filter.AddInputConnection(transform_filter_1.GetOutputPort())
append_filter.AddInputConnection(transform_filter_2.GetOutputPort())
append_filter.AddInputConnection(transform_filter_3.GetOutputPort())

probe_filter = vtkProbeFilter()
probe_filter.SetInputConnection(append_filter.GetOutputPort())
probe_filter.SetSourceData(output)

# Isocontour the probed data
contour = vtkContourFilter()
contour.SetInputConnection(probe_filter.GetOutputPort())
contour.GenerateValues(50, output.GetScalarRange())

contour_mapper = vtkPolyDataMapper()
contour_mapper.SetInputConnection(contour.GetOutputPort())
contour_mapper.SetScalarRange(output.GetScalarRange())

plane_actor = vtkActor()
plane_actor.SetMapper(contour_mapper)

# Outline of the structured grid
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
renderer.AddActor(plane_actor)
renderer.AddActor(outline_actor_1)
renderer.AddActor(outline_actor_2)
renderer.AddActor(outline_actor_3)
renderer.SetBackground(1, 1, 1)

# Window
render_window = vtkRenderWindow()
render_window.SetMultiSamples(0)
render_window.AddRenderer(renderer)
render_window.SetSize(400, 400)
render_window.SetWindowName("probe comb")

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
