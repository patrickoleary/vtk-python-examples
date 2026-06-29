#!/usr/bin/env python

# Compare three methods of cutting a rectilinear grid: vtkCutter,
# vtkPlaneCutter with sphere tree, and vtkPlaneCutter without tree,
# displayed in three viewports.

import os

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonDataModel import vtkPlane
from vtkmodules.vtkFiltersCore import (
    vtkCutter,
    vtkPlaneCutter,
)
from vtkmodules.vtkFiltersModeling import vtkOutlineFilter
from vtkmodules.vtkIOXML import vtkXMLRectilinearGridReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Data file path (relative to this script)
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Reader: load rectilinear grid
reader = vtkXMLRectilinearGridReader()
reader.SetFileName(os.path.join(data_dir, "cth.vtr"))
reader.Update()

input_data = reader.GetOutput()

# Cut plane centered on the data
plane = vtkPlane()
plane.SetOrigin(input_data.GetCenter())
plane.SetNormal(1, 1, 1)

# Standard cutter
cutter = vtkCutter()
cutter.SetInputData(input_data)
cutter.SetCutFunction(plane)
cutter.Update()

cutter_mapper = vtkPolyDataMapper()
cutter_mapper.SetInputConnection(cutter.GetOutputPort())
cutter_mapper.ScalarVisibilityOff()

cutter_actor = vtkActor()
cutter_actor.SetMapper(cutter_mapper)
cutter_actor.GetProperty().SetColor(1, 1, 1)

# Outline
outline = vtkOutlineFilter()
outline.SetInputData(input_data)

outline_mapper = vtkPolyDataMapper()
outline_mapper.SetInputConnection(outline.GetOutputPort())

outline_actor = vtkActor()
outline_actor.SetMapper(outline_mapper)

# Accelerated plane cutter with sphere tree
plane_cutter = vtkPlaneCutter()
plane_cutter.SetInputData(input_data)
plane_cutter.SetPlane(plane)
plane_cutter.Update()

plane_cutter_mapper = vtkPolyDataMapper()
plane_cutter_mapper.SetInputConnection(plane_cutter.GetOutputPort())
plane_cutter_mapper.ScalarVisibilityOff()

plane_cutter_actor = vtkActor()
plane_cutter_actor.SetMapper(plane_cutter_mapper)
plane_cutter_actor.GetProperty().SetColor(1, 1, 1)

# Accelerated plane cutter without tree
plane_cutter_no_tree = vtkPlaneCutter()
plane_cutter_no_tree.SetInputData(input_data)
plane_cutter_no_tree.SetPlane(plane)
plane_cutter_no_tree.BuildTreeOff()
plane_cutter_no_tree.Update()

plane_cutter_no_tree_mapper = vtkPolyDataMapper()
plane_cutter_no_tree_mapper.SetInputConnection(plane_cutter_no_tree.GetOutputPort())
plane_cutter_no_tree_mapper.ScalarVisibilityOff()

plane_cutter_no_tree_actor = vtkActor()
plane_cutter_no_tree_actor.SetMapper(plane_cutter_no_tree_mapper)
plane_cutter_no_tree_actor.GetProperty().SetColor(1, 1, 1)

# Outline for accelerated cutters
outline_t = vtkOutlineFilter()
outline_t.SetInputData(input_data)

outline_t_mapper = vtkPolyDataMapper()
outline_t_mapper.SetInputConnection(outline_t.GetOutputPort())

outline_t_actor = vtkActor()
outline_t_actor.SetMapper(outline_t_mapper)

# Three viewports
renderer_0 = vtkRenderer()
renderer_0.SetViewport(0, 0, 0.33, 1)
renderer_0.SetBackground(0, 0, 0)
renderer_0.AddActor(outline_actor)
renderer_0.AddActor(cutter_actor)

renderer_1 = vtkRenderer()
renderer_1.SetViewport(0.33, 0, 0.66, 1)
renderer_1.SetBackground(0, 0, 0)
renderer_1.AddActor(outline_t_actor)
renderer_1.AddActor(plane_cutter_actor)

renderer_2 = vtkRenderer()
renderer_2.SetViewport(0.66, 0, 1, 1)
renderer_2.SetBackground(0, 0, 0)
renderer_2.AddActor(outline_t_actor)
renderer_2.AddActor(plane_cutter_no_tree_actor)

# Window
render_window = vtkRenderWindow()
render_window.SetMultiSamples(0)
render_window.AddRenderer(renderer_0)
render_window.AddRenderer(renderer_1)
render_window.AddRenderer(renderer_2)
render_window.SetSize(900, 300)
render_window.SetWindowName("rectilineargrid plane cutter")

# Scene
renderer_0.ResetCamera()
renderer_1.ResetCamera()
renderer_2.ResetCamera()

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
