#!/usr/bin/env python

# Test alternative probing methods on PLOT3D combustor data: default FindCell,
# vtkStaticCellLocator, and vtkCellLocatorStrategy on three separate planes.

import os

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonDataModel import (
    vtkCellLocatorStrategy,
    vtkStaticCellLocator,
)
from vtkmodules.vtkCommonTransforms import vtkTransform
from vtkmodules.vtkFiltersCore import (
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

# Control test size
resolution = 50

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
plane.SetResolution(resolution, resolution)

# --- Plane 1: default FindCell ---
trans_p1 = vtkTransform()
trans_p1.Translate(3.7, 0.0, 28.37)
trans_p1.Scale(5, 5, 5)
trans_p1.RotateY(90)

transform_filter_1 = vtkTransformPolyDataFilter()
transform_filter_1.SetInputConnection(plane.GetOutputPort())
transform_filter_1.SetTransform(trans_p1)

probe_1 = vtkProbeFilter()
probe_1.SetInputConnection(transform_filter_1.GetOutputPort())
probe_1.SetSourceData(output)

contour_1 = vtkContourFilter()
contour_1.SetInputConnection(probe_1.GetOutputPort())
contour_1.GenerateValues(50, output.GetScalarRange())

probe_mapper_1 = vtkPolyDataMapper()
probe_mapper_1.SetInputConnection(contour_1.GetOutputPort())
probe_mapper_1.SetScalarRange(output.GetScalarRange())

probe_1_actor = vtkActor()
probe_1_actor.SetMapper(probe_mapper_1)

outline_filter_1 = vtkOutlineFilter()
outline_filter_1.SetInputConnection(transform_filter_1.GetOutputPort())
outline_mapper_1 = vtkPolyDataMapper()
outline_mapper_1.SetInputConnection(outline_filter_1.GetOutputPort())
outline_actor_1 = vtkActor()
outline_actor_1.SetMapper(outline_mapper_1)
outline_actor_1.GetProperty().SetColor(0, 0, 0)

# --- Plane 2: vtkStaticCellLocator ---
trans_p2 = vtkTransform()
trans_p2.Translate(9.2, 0.0, 31.20)
trans_p2.Scale(5, 5, 5)
trans_p2.RotateY(90)

transform_filter_2 = vtkTransformPolyDataFilter()
transform_filter_2.SetInputConnection(plane.GetOutputPort())
transform_filter_2.SetTransform(trans_p2)

cell_locator = vtkStaticCellLocator()

probe_2 = vtkProbeFilter()
probe_2.SetInputConnection(transform_filter_2.GetOutputPort())
probe_2.SetSourceData(output)
probe_2.SetCellLocatorPrototype(cell_locator)

contour_2 = vtkContourFilter()
contour_2.SetInputConnection(probe_2.GetOutputPort())
contour_2.GenerateValues(50, output.GetScalarRange())

probe_mapper_2 = vtkPolyDataMapper()
probe_mapper_2.SetInputConnection(contour_2.GetOutputPort())
probe_mapper_2.SetScalarRange(output.GetScalarRange())

probe_2_actor = vtkActor()
probe_2_actor.SetMapper(probe_mapper_2)

outline_filter_2 = vtkOutlineFilter()
outline_filter_2.SetInputConnection(transform_filter_2.GetOutputPort())
outline_mapper_2 = vtkPolyDataMapper()
outline_mapper_2.SetInputConnection(outline_filter_2.GetOutputPort())
outline_actor_2 = vtkActor()
outline_actor_2.SetMapper(outline_mapper_2)
outline_actor_2.GetProperty().SetColor(0, 0, 0)

# --- Plane 3: vtkCellLocatorStrategy ---
trans_p3 = vtkTransform()
trans_p3.Translate(13.27, 0.0, 33.30)
trans_p3.Scale(5, 5, 5)
trans_p3.RotateY(90)

transform_filter_3 = vtkTransformPolyDataFilter()
transform_filter_3.SetInputConnection(plane.GetOutputPort())
transform_filter_3.SetTransform(trans_p3)

strategy = vtkCellLocatorStrategy()

probe_3 = vtkProbeFilter()
probe_3.SetInputConnection(transform_filter_3.GetOutputPort())
probe_3.SetSourceData(output)
probe_3.SetFindCellStrategy(strategy)

contour_3 = vtkContourFilter()
contour_3.SetInputConnection(probe_3.GetOutputPort())
contour_3.GenerateValues(50, output.GetScalarRange())

probe_mapper_3 = vtkPolyDataMapper()
probe_mapper_3.SetInputConnection(contour_3.GetOutputPort())
probe_mapper_3.SetScalarRange(output.GetScalarRange())

probe_3_actor = vtkActor()
probe_3_actor.SetMapper(probe_mapper_3)

outline_filter_3 = vtkOutlineFilter()
outline_filter_3.SetInputConnection(transform_filter_3.GetOutputPort())
outline_mapper_3 = vtkPolyDataMapper()
outline_mapper_3.SetInputConnection(outline_filter_3.GetOutputPort())
outline_actor_3 = vtkActor()
outline_actor_3.SetMapper(outline_mapper_3)
outline_actor_3.GetProperty().SetColor(0, 0, 0)

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
renderer.AddActor(probe_1_actor)
renderer.AddActor(probe_2_actor)
renderer.AddActor(probe_3_actor)
renderer.AddActor(outline_actor_1)
renderer.AddActor(outline_actor_2)
renderer.AddActor(outline_actor_3)
renderer.SetBackground(1, 1, 1)

# Window
render_window = vtkRenderWindow()
render_window.SetMultiSamples(0)
render_window.AddRenderer(renderer)
render_window.SetSize(400, 400)
render_window.SetWindowName("probe comb locators")

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
