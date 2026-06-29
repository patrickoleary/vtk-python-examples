#!/usr/bin/env python

# Compare vtkCutter, vtkPlaneCutter, and vtk3DLinearGridPlaneCutter
# on a sampled sphere volume across three viewports.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonDataModel import (
    vtkPlane,
    vtkSphere,
)
from vtkmodules.vtkFiltersCore import (
    vtk3DLinearGridPlaneCutter,
    vtkCutter,
    vtkPlaneCutter,
)
from vtkmodules.vtkFiltersExtraction import vtkExtractGeometry
from vtkmodules.vtkFiltersGeneral import vtkRandomAttributeGenerator
from vtkmodules.vtkFiltersModeling import vtkOutlineFilter
from vtkmodules.vtkImagingHybrid import vtkSampleFunction
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkCompositePolyDataMapper,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

resolution = 50

# Source: sample a sphere implicit function across a volume
sphere = vtkSphere()
sphere.SetCenter(0.0, 0.0, 0.0)
sphere.SetRadius(0.25)

sample = vtkSampleFunction()
sample.SetImplicitFunction(sphere)
sample.SetModelBounds(-0.5, 0.5, -0.5, 0.5, -0.5, 0.5)
sample.SetSampleDimensions(resolution, resolution, resolution)
sample.Update()

# Add random cell scalars
random_attr = vtkRandomAttributeGenerator()
random_attr.SetGenerateCellScalars(True)
random_attr.SetInputConnection(sample.GetOutputPort())

# Convert image data to unstructured grid
extraction_sphere = vtkSphere()
extraction_sphere.SetRadius(100)
extraction_sphere.SetCenter(0, 0, 0)
extract = vtkExtractGeometry()
extract.SetImplicitFunction(extraction_sphere)
extract.SetInputConnection(random_attr.GetOutputPort())
extract.Update()

# Cut plane
plane = vtkPlane()
plane.SetOrigin(0, 0, 0)
plane.SetNormal(1, 1, 1)

# --- Left viewport: vtkCutter ---

cutter = vtkCutter()
cutter.SetInputConnection(extract.GetOutputPort())
cutter.SetCutFunction(plane)

cutter_mapper = vtkCompositePolyDataMapper()
cutter_mapper.SetInputConnection(cutter.GetOutputPort())

cutter_actor = vtkActor()
cutter_actor.SetMapper(cutter_mapper)
cutter_actor.GetProperty().SetColor(1, 1, 1)

outline_0 = vtkOutlineFilter()
outline_0.SetInputConnection(sample.GetOutputPort())
outline_mapper_0 = vtkPolyDataMapper()
outline_mapper_0.SetInputConnection(outline_0.GetOutputPort())
outline_actor_0 = vtkActor()
outline_actor_0.SetMapper(outline_mapper_0)

# --- Middle viewport: vtkPlaneCutter ---

plane_cutter = vtkPlaneCutter()
plane_cutter.SetInputConnection(extract.GetOutputPort())
plane_cutter.SetPlane(plane)
plane_cutter.BuildTreeOff()

plane_cutter_mapper = vtkPolyDataMapper()
plane_cutter_mapper.SetInputConnection(plane_cutter.GetOutputPort())

plane_cutter_actor = vtkActor()
plane_cutter_actor.SetMapper(plane_cutter_mapper)
plane_cutter_actor.GetProperty().SetColor(1, 1, 1)

outline_1 = vtkOutlineFilter()
outline_1.SetInputConnection(sample.GetOutputPort())
outline_mapper_1 = vtkPolyDataMapper()
outline_mapper_1.SetInputConnection(outline_1.GetOutputPort())
outline_actor_1 = vtkActor()
outline_actor_1.SetMapper(outline_mapper_1)

# --- Right viewport: vtk3DLinearGridPlaneCutter ---

linear_cutter = vtk3DLinearGridPlaneCutter()
linear_cutter.SetInputConnection(extract.GetOutputPort())
linear_cutter.SetPlane(plane)
linear_cutter.ComputeNormalsOff()
linear_cutter.MergePointsOff()
linear_cutter.InterpolateAttributesOn()

linear_cutter_mapper = vtkPolyDataMapper()
linear_cutter_mapper.SetInputConnection(linear_cutter.GetOutputPort())

linear_cutter_actor = vtkActor()
linear_cutter_actor.SetMapper(linear_cutter_mapper)
linear_cutter_actor.GetProperty().SetColor(1, 1, 1)

outline_2 = vtkOutlineFilter()
outline_2.SetInputConnection(sample.GetOutputPort())
outline_mapper_2 = vtkPolyDataMapper()
outline_mapper_2.SetInputConnection(outline_2.GetOutputPort())
outline_actor_2 = vtkActor()
outline_actor_2.SetMapper(outline_mapper_2)

# Three viewports
renderer_0 = vtkRenderer()
renderer_0.SetViewport(0, 0, 0.33, 1)
renderer_0.AddActor(outline_actor_0)
renderer_0.AddActor(cutter_actor)
renderer_0.SetBackground(0, 0, 0)

renderer_1 = vtkRenderer()
renderer_1.SetViewport(0.33, 0, 0.67, 1)
renderer_1.AddActor(outline_actor_1)
renderer_1.AddActor(plane_cutter_actor)
renderer_1.SetBackground(0, 0, 0)

renderer_2 = vtkRenderer()
renderer_2.SetViewport(0.67, 0, 1, 1)
renderer_2.AddActor(outline_actor_2)
renderer_2.AddActor(linear_cutter_actor)
renderer_2.SetBackground(0, 0, 0)

# Window
render_window = vtkRenderWindow()
render_window.SetMultiSamples(0)
render_window.AddRenderer(renderer_0)
render_window.AddRenderer(renderer_1)
render_window.AddRenderer(renderer_2)
render_window.SetSize(400, 200)
render_window.SetWindowName("3d lineargrid plane cutter")

# Scene
renderer_0.ResetCamera()
camera = renderer_0.GetActiveCamera()
renderer_1.SetActiveCamera(camera)
renderer_2.SetActiveCamera(camera)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
