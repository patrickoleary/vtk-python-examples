#!/usr/bin/env python

# Compare contour filters with different scalar tree strategies
# (no tree, vtkSimpleScalarTree, vtkSpanSpace) on an Exodus II dataset,
# displayed in two viewports.

import os

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonExecutionModel import (
    vtkSimpleScalarTree,
    vtkSpanSpace,
)
from vtkmodules.vtkFiltersCore import vtkContourFilter
from vtkmodules.vtkFiltersModeling import vtkOutlineFilter
from vtkmodules.vtkIOExodus import vtkExodusIIReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkCompositePolyDataMapper,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Data file path (relative to this script)
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Reader: load Exodus II file
reader = vtkExodusIIReader()
reader.SetFileName(os.path.join(data_dir, "disk_out_ref.ex2"))
reader.SetPointResultArrayStatus("Temp", 1)
reader.Update()

input_data = reader.GetOutput().GetBlock(0).GetBlock(0)

# Scalar trees
simple_tree = vtkSimpleScalarTree()
simple_tree.SetBranchingFactor(3)

span_tree = vtkSpanSpace()
span_tree.SetResolution(100)

# Non-threaded contour filter with span space tree
contour = vtkContourFilter()
contour.SetInputData(input_data)
contour.UseScalarTreeOn()
contour.SetScalarTree(span_tree)
contour.SetValue(0, 350)
contour.SetInputArrayToProcess(0, 0, 0, 0, "Temp")
contour.GenerateTrianglesOff()
contour.Update()

contour_mapper = vtkPolyDataMapper()
contour_mapper.SetInputConnection(contour.GetOutputPort())
contour_mapper.ScalarVisibilityOff()

contour_actor = vtkActor()
contour_actor.SetMapper(contour_mapper)
contour_actor.GetProperty().SetColor(1, 1, 1)

outline = vtkOutlineFilter()
outline.SetInputData(input_data)

outline_mapper = vtkPolyDataMapper()
outline_mapper.SetInputConnection(outline.GetOutputPort())

outline_actor = vtkActor()
outline_actor.SetMapper(outline_mapper)

# Threaded contour filter with simple scalar tree
contour_t = vtkContourFilter()
contour_t.SetInputData(input_data)
contour_t.UseScalarTreeOn()
contour_t.SetScalarTree(simple_tree)
contour_t.SetValue(0, 350)
contour_t.SetInputArrayToProcess(0, 0, 0, 0, "Temp")
contour_t.GenerateTrianglesOff()
contour_t.Update()

contour_t_mapper = vtkCompositePolyDataMapper()
contour_t_mapper.SetInputConnection(contour_t.GetOutputPort())
contour_t_mapper.ScalarVisibilityOff()

contour_t_actor = vtkActor()
contour_t_actor.SetMapper(contour_t_mapper)
contour_t_actor.GetProperty().SetColor(1, 1, 1)

outline_t = vtkOutlineFilter()
outline_t.SetInputData(input_data)

outline_t_mapper = vtkPolyDataMapper()
outline_t_mapper.SetInputConnection(outline_t.GetOutputPort())

outline_t_actor = vtkActor()
outline_t_actor.SetMapper(outline_t_mapper)

# Two viewports
renderer_0 = vtkRenderer()
renderer_0.SetViewport(0, 0, 0.5, 1)
renderer_0.SetBackground(0, 0, 0)
renderer_0.AddActor(outline_actor)
renderer_0.AddActor(contour_actor)

renderer_1 = vtkRenderer()
renderer_1.SetViewport(0.5, 0, 1, 1)
renderer_1.SetBackground(0, 0, 0)
renderer_1.AddActor(outline_t_actor)
renderer_1.AddActor(contour_t_actor)

# Window
render_window = vtkRenderWindow()
render_window.SetMultiSamples(0)
render_window.AddRenderer(renderer_0)
render_window.AddRenderer(renderer_1)
render_window.SetSize(600, 300)
render_window.SetWindowName("scalar trees")

# Scene
renderer_0.ResetCamera()
renderer_1.ResetCamera()

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
