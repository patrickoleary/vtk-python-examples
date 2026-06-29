#!/usr/bin/env python

# Compare three methods of cutting a structured grid: vtkCutter,
# vtkPlaneCutter with sphere tree, and vtkPlaneCutter without tree,
# displayed in three viewports.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonDataModel import (
    vtkPlane,
    vtkSphere,
)
from vtkmodules.vtkFiltersCore import (
    vtkCutter,
    vtkPlaneCutter,
)
from vtkmodules.vtkFiltersGeneral import vtkImageDataToPointSet
from vtkmodules.vtkFiltersModeling import vtkOutlineFilter
from vtkmodules.vtkImagingHybrid import vtkSampleFunction
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

resolution = 50

# Source: sample a sphere implicit function
sphere = vtkSphere()
sphere.SetCenter(0.0, 0.0, 0.0)
sphere.SetRadius(0.25)

sample = vtkSampleFunction()
sample.SetImplicitFunction(sphere)
sample.SetModelBounds(-0.5, 0.5, -0.5, 0.5, -0.5, 0.5)
sample.SetSampleDimensions(resolution, resolution, resolution)
sample.Update()

# Convert image data to structured grid
convert = vtkImageDataToPointSet()
convert.SetInputConnection(sample.GetOutputPort())
convert.Update()

input_data = convert.GetOutput()

# Cut plane
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
outline_tree = vtkOutlineFilter()
outline_tree.SetInputData(input_data)

outline_tree_mapper = vtkPolyDataMapper()
outline_tree_mapper.SetInputConnection(outline_tree.GetOutputPort())

outline_tree_actor = vtkActor()
outline_tree_actor.SetMapper(outline_tree_mapper)

# Three viewports
renderer_0 = vtkRenderer()
renderer_0.SetViewport(0, 0, 0.33, 1)
renderer_0.SetBackground(0, 0, 0)
renderer_0.AddActor(outline_actor)
renderer_0.AddActor(cutter_actor)

renderer_1 = vtkRenderer()
renderer_1.SetViewport(0.33, 0, 0.66, 1)
renderer_1.SetBackground(0, 0, 0)
renderer_1.AddActor(outline_tree_actor)
renderer_1.AddActor(plane_cutter_actor)

renderer_2 = vtkRenderer()
renderer_2.SetViewport(0.66, 0, 1, 1)
renderer_2.SetBackground(0, 0, 0)
renderer_2.AddActor(outline_tree_actor)
renderer_2.AddActor(plane_cutter_no_tree_actor)

# Window
render_window = vtkRenderWindow()
render_window.SetMultiSamples(0)
render_window.AddRenderer(renderer_0)
render_window.AddRenderer(renderer_1)
render_window.AddRenderer(renderer_2)
render_window.SetSize(900, 300)
render_window.SetWindowName("structuredgrid plane cutter")

# Scene
renderer_0.ResetCamera()
renderer_1.ResetCamera()
renderer_2.ResetCamera()

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
