#!/usr/bin/env python

# Compare three sphere cutting methods: vtkCutter, vtkPlaneCutter, and
# vtkPolyDataPlaneCutter in three viewports.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonDataModel import vtkPlane
from vtkmodules.vtkFiltersCore import (
    vtkCutter,
    vtkPlaneCutter,
    vtkPolyDataPlaneCutter,
)
from vtkmodules.vtkFiltersModeling import vtkOutlineFilter
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

resolution = 50

# Source: sphere
sphere = vtkSphereSource()
sphere.SetCenter(0.0, 0.0, 0.0)
sphere.SetRadius(0.25)
sphere.SetPhiResolution(resolution)
sphere.SetThetaResolution(2 * resolution)
sphere.Update()

# Cut plane
plane = vtkPlane()
plane.SetOrigin(0, 0, 0)
plane.SetNormal(1, 1, 1)

# Standard cutter
cutter = vtkCutter()
cutter.SetInputConnection(sphere.GetOutputPort())
cutter.SetCutFunction(plane)

cutter_mapper = vtkPolyDataMapper()
cutter_mapper.SetInputConnection(cutter.GetOutputPort())
cutter_mapper.ScalarVisibilityOff()

cutter_actor = vtkActor()
cutter_actor.SetMapper(cutter_mapper)
cutter_actor.GetProperty().SetColor(1, 1, 1)
cutter_actor.GetProperty().SetInterpolationToFlat()

# Outline for standard cutter
outline = vtkOutlineFilter()
outline.SetInputConnection(sphere.GetOutputPort())

outline_mapper = vtkPolyDataMapper()
outline_mapper.SetInputConnection(outline.GetOutputPort())

outline_actor = vtkActor()
outline_actor.SetMapper(outline_mapper)

# Accelerated plane cutter (sphere tree)
plane_cutter = vtkPlaneCutter()
plane_cutter.SetInputConnection(sphere.GetOutputPort())
plane_cutter.SetPlane(plane)

plane_cutter_mapper = vtkPolyDataMapper()
plane_cutter_mapper.SetInputConnection(plane_cutter.GetOutputPort())
plane_cutter_mapper.ScalarVisibilityOff()

plane_cutter_actor = vtkActor()
plane_cutter_actor.SetMapper(plane_cutter_mapper)
plane_cutter_actor.GetProperty().SetColor(1, 1, 1)
plane_cutter_actor.GetProperty().SetInterpolationToFlat()

# Specialized polydata plane cutter
pd_cutter = vtkPolyDataPlaneCutter()
pd_cutter.SetInputConnection(sphere.GetOutputPort())
pd_cutter.SetPlane(plane)
pd_cutter.SetBatchSize(10)

pd_cutter_mapper = vtkPolyDataMapper()
pd_cutter_mapper.SetInputConnection(pd_cutter.GetOutputPort())
pd_cutter_mapper.ScalarVisibilityOff()

pd_cutter_actor = vtkActor()
pd_cutter_actor.SetMapper(pd_cutter_mapper)
pd_cutter_actor.GetProperty().SetColor(1, 1, 1)
pd_cutter_actor.GetProperty().SetInterpolationToFlat()

# Outline for accelerated cutters
outline_t = vtkOutlineFilter()
outline_t.SetInputConnection(sphere.GetOutputPort())

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
renderer_2.AddActor(pd_cutter_actor)

# Window
render_window = vtkRenderWindow()
render_window.SetMultiSamples(0)
render_window.AddRenderer(renderer_0)
render_window.AddRenderer(renderer_1)
render_window.AddRenderer(renderer_2)
render_window.SetSize(900, 300)
render_window.SetWindowName("polydata plane cutter")

# Scene
renderer_0.ResetCamera()
renderer_1.ResetCamera()
renderer_2.ResetCamera()

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
