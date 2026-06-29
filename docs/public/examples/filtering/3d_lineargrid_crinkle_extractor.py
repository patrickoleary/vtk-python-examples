#!/usr/bin/env python

# Compare standard crinkle extraction (vtkExtractGeometry) with
# vtk3DLinearGridCrinkleExtractor across three viewports.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonDataModel import (
    vtkPlane,
    vtkSphere,
)
from vtkmodules.vtkFiltersCore import vtk3DLinearGridCrinkleExtractor
from vtkmodules.vtkFiltersExtraction import vtkExtractGeometry
from vtkmodules.vtkFiltersGeneral import vtkRandomAttributeGenerator
from vtkmodules.vtkFiltersGeometry import vtkGeometryFilter
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

# Source: sample a sphere implicit function across a volume
sphere = vtkSphere()
sphere.SetCenter(0.0, 0.0, 0.0)
sphere.SetRadius(0.25)

sample = vtkSampleFunction()
sample.SetImplicitFunction(sphere)
sample.SetModelBounds(-0.5, 0.5, -0.5, 0.5, -0.5, 0.5)
sample.SetSampleDimensions(resolution, resolution, resolution)
sample.ComputeNormalsOff()
sample.Update()

# Add random cell scalars
random_attr = vtkRandomAttributeGenerator()
random_attr.SetGenerateCellScalars(True)
random_attr.SetInputConnection(sample.GetOutputPort())

# Convert image data to unstructured grid via extraction
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

# --- Left viewport: standard crinkle via vtkExtractGeometry ---

cutter = vtkExtractGeometry()
cutter.SetInputConnection(extract.GetOutputPort())
cutter.SetImplicitFunction(plane)
cutter.ExtractBoundaryCellsOn()
cutter.ExtractOnlyBoundaryCellsOn()

cutter_surface = vtkGeometryFilter()
cutter_surface.SetInputConnection(cutter.GetOutputPort())
cutter_surface.MergingOff()

cutter_mapper = vtkPolyDataMapper()
cutter_mapper.SetInputConnection(cutter_surface.GetOutputPort())

cutter_actor = vtkActor()
cutter_actor.SetMapper(cutter_mapper)
cutter_actor.GetProperty().SetColor(1, 1, 1)

outline_0 = vtkOutlineFilter()
outline_0.SetInputConnection(sample.GetOutputPort())
outline_mapper_0 = vtkPolyDataMapper()
outline_mapper_0.SetInputConnection(outline_0.GetOutputPort())
outline_actor_0 = vtkActor()
outline_actor_0.SetMapper(outline_mapper_0)

# --- Middle viewport: 3DLinearGridCrinkleExtractor with cell data ---

crinkle_1 = vtk3DLinearGridCrinkleExtractor()
crinkle_1.SetInputConnection(extract.GetOutputPort())
crinkle_1.SetImplicitFunction(plane)
crinkle_1.CopyPointDataOff()
crinkle_1.CopyCellDataOn()

crinkle_surface_1 = vtkGeometryFilter()
crinkle_surface_1.SetInputConnection(crinkle_1.GetOutputPort())
crinkle_surface_1.MergingOff()

crinkle_mapper_1 = vtkPolyDataMapper()
crinkle_mapper_1.SetInputConnection(crinkle_surface_1.GetOutputPort())

crinkle_actor_1 = vtkActor()
crinkle_actor_1.SetMapper(crinkle_mapper_1)
crinkle_actor_1.GetProperty().SetColor(1, 1, 1)

outline_1 = vtkOutlineFilter()
outline_1.SetInputConnection(sample.GetOutputPort())
outline_mapper_1 = vtkPolyDataMapper()
outline_mapper_1.SetInputConnection(outline_1.GetOutputPort())
outline_actor_1 = vtkActor()
outline_actor_1.SetMapper(outline_mapper_1)

# --- Right viewport: 3DLinearGridCrinkleExtractor removing unused points ---

crinkle_2 = vtk3DLinearGridCrinkleExtractor()
crinkle_2.SetInputConnection(extract.GetOutputPort())
crinkle_2.SetImplicitFunction(plane)
crinkle_2.RemoveUnusedPointsOn()
crinkle_2.CopyPointDataOn()
crinkle_2.CopyCellDataOn()

crinkle_surface_2 = vtkGeometryFilter()
crinkle_surface_2.SetInputConnection(crinkle_2.GetOutputPort())
crinkle_surface_2.MergingOff()

crinkle_mapper_2 = vtkPolyDataMapper()
crinkle_mapper_2.SetInputConnection(crinkle_surface_2.GetOutputPort())

crinkle_actor_2 = vtkActor()
crinkle_actor_2.SetMapper(crinkle_mapper_2)
crinkle_actor_2.GetProperty().SetColor(1, 1, 1)

outline_2 = vtkOutlineFilter()
outline_2.SetInputConnection(sample.GetOutputPort())
outline_mapper_2 = vtkPolyDataMapper()
outline_mapper_2.SetInputConnection(outline_2.GetOutputPort())
outline_actor_2 = vtkActor()
outline_actor_2.SetMapper(outline_mapper_2)

# Update filters
cutter.Update()
crinkle_1.Update()
crinkle_2.Update()

# Three viewports
renderer_0 = vtkRenderer()
renderer_0.SetViewport(0, 0, 0.333, 1)
renderer_0.AddActor(outline_actor_0)
renderer_0.AddActor(cutter_actor)
renderer_0.SetBackground(0, 0, 0)

renderer_1 = vtkRenderer()
renderer_1.SetViewport(0.333, 0, 0.667, 1)
renderer_1.AddActor(outline_actor_1)
renderer_1.AddActor(crinkle_actor_1)
renderer_1.SetBackground(0, 0, 0)

renderer_2 = vtkRenderer()
renderer_2.SetViewport(0.667, 0, 1, 1)
renderer_2.AddActor(outline_actor_2)
renderer_2.AddActor(crinkle_actor_2)
renderer_2.SetBackground(0, 0, 0)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer_0)
render_window.AddRenderer(renderer_1)
render_window.AddRenderer(renderer_2)
render_window.SetSize(600, 200)
render_window.SetWindowName("3d lineargrid crinkle extractor")

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
