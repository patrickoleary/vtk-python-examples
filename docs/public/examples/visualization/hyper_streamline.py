#!/usr/bin/env python

# Visualize tensor fields using hyperstreamlines seeded at four corner points.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkFiltersGeneral import vtkHyperStreamline
from vtkmodules.vtkFiltersGeometry import vtkImageDataGeometryFilter
from vtkmodules.vtkFiltersModeling import vtkOutlineFilter
from vtkmodules.vtkFiltersSources import vtkConeSource
from vtkmodules.vtkImagingHybrid import vtkPointLoad
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkCamera,
    vtkLogLookupTable,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
slate_gray = (0.439, 0.502, 0.565)
black = (0.0, 0.0, 0.0)
tomato = (1.000, 0.388, 0.278)

# Source: generate a tensor field from a simulated point load
pt_load = vtkPointLoad()
pt_load.SetLoadValue(100.0)
pt_load.SetSampleDimensions(20, 20, 20)
pt_load.ComputeEffectiveStressOn()
pt_load.SetModelBounds(-10, 10, -10, 10, -10, 10)
pt_load.Update()

scalar_range = pt_load.GetOutput().GetScalarRange()

# Lookup table: logarithmic color mapping
lut = vtkLogLookupTable()
lut.SetHueRange(0.6667, 0.0)

# Filter/Mapper/Actor: hyperstreamline seeded at (9, 9, -9)
hs_0 = vtkHyperStreamline()
hs_0.SetInputData(pt_load.GetOutput())
hs_0.SetStartPosition(9, 9, -9)
hs_0.IntegrateMinorEigenvector()
hs_0.SetMaximumPropagationDistance(18.0)
hs_0.SetIntegrationStepLength(0.1)
hs_0.SetStepLength(0.01)
hs_0.SetRadius(0.25)
hs_0.SetNumberOfSides(18)
hs_0.SetIntegrationDirectionToIntegrateBothDirections()
hs_0.Update()

hs_mapper_0 = vtkPolyDataMapper()
hs_mapper_0.SetInputConnection(hs_0.GetOutputPort())
hs_mapper_0.SetLookupTable(lut)
hs_mapper_0.SetScalarRange(scalar_range)

hs_actor_0 = vtkActor()
hs_actor_0.SetMapper(hs_mapper_0)

# Filter/Mapper/Actor: hyperstreamline seeded at (-9, -9, -9)
hs_1 = vtkHyperStreamline()
hs_1.SetInputData(pt_load.GetOutput())
hs_1.SetStartPosition(-9, -9, -9)
hs_1.IntegrateMinorEigenvector()
hs_1.SetMaximumPropagationDistance(18.0)
hs_1.SetIntegrationStepLength(0.1)
hs_1.SetStepLength(0.01)
hs_1.SetRadius(0.25)
hs_1.SetNumberOfSides(18)
hs_1.SetIntegrationDirectionToIntegrateBothDirections()
hs_1.Update()

hs_mapper_1 = vtkPolyDataMapper()
hs_mapper_1.SetInputConnection(hs_1.GetOutputPort())
hs_mapper_1.SetLookupTable(lut)
hs_mapper_1.SetScalarRange(scalar_range)

hs_actor_1 = vtkActor()
hs_actor_1.SetMapper(hs_mapper_1)

# Filter/Mapper/Actor: hyperstreamline seeded at (9, -9, -9)
hs_2 = vtkHyperStreamline()
hs_2.SetInputData(pt_load.GetOutput())
hs_2.SetStartPosition(9, -9, -9)
hs_2.IntegrateMinorEigenvector()
hs_2.SetMaximumPropagationDistance(18.0)
hs_2.SetIntegrationStepLength(0.1)
hs_2.SetStepLength(0.01)
hs_2.SetRadius(0.25)
hs_2.SetNumberOfSides(18)
hs_2.SetIntegrationDirectionToIntegrateBothDirections()
hs_2.Update()

hs_mapper_2 = vtkPolyDataMapper()
hs_mapper_2.SetInputConnection(hs_2.GetOutputPort())
hs_mapper_2.SetLookupTable(lut)
hs_mapper_2.SetScalarRange(scalar_range)

hs_actor_2 = vtkActor()
hs_actor_2.SetMapper(hs_mapper_2)

# Filter/Mapper/Actor: hyperstreamline seeded at (-9, 9, -9)
hs_3 = vtkHyperStreamline()
hs_3.SetInputData(pt_load.GetOutput())
hs_3.SetStartPosition(-9, 9, -9)
hs_3.IntegrateMinorEigenvector()
hs_3.SetMaximumPropagationDistance(18.0)
hs_3.SetIntegrationStepLength(0.1)
hs_3.SetStepLength(0.01)
hs_3.SetRadius(0.25)
hs_3.SetNumberOfSides(18)
hs_3.SetIntegrationDirectionToIntegrateBothDirections()
hs_3.Update()

hs_mapper_3 = vtkPolyDataMapper()
hs_mapper_3.SetInputConnection(hs_3.GetOutputPort())
hs_mapper_3.SetLookupTable(lut)
hs_mapper_3.SetScalarRange(scalar_range)

hs_actor_3 = vtkActor()
hs_actor_3.SetMapper(hs_mapper_3)

# Filter: extract a mid-plane slice for context
plane_filter = vtkImageDataGeometryFilter()
plane_filter.SetInputData(pt_load.GetOutput())
plane_filter.SetExtent(0, 100, 0, 100, 0, 0)
plane_filter.Update()

plane_mapper = vtkPolyDataMapper()
plane_mapper.SetInputConnection(plane_filter.GetOutputPort())
plane_mapper.SetScalarRange(plane_filter.GetOutput().GetScalarRange())

plane_actor = vtkActor()
plane_actor.SetMapper(plane_mapper)

# Filter: outline around the data volume
outline = vtkOutlineFilter()
outline.SetInputData(pt_load.GetOutput())

outline_mapper = vtkPolyDataMapper()
outline_mapper.SetInputConnection(outline.GetOutputPort())

outline_actor = vtkActor()
outline_actor.SetMapper(outline_mapper)
outline_actor.GetProperty().SetColor(black)

# Source: cone indicating the application of the load
cone_source = vtkConeSource()
cone_source.SetRadius(0.5)
cone_source.SetHeight(2)

cone_mapper = vtkPolyDataMapper()
cone_mapper.SetInputConnection(cone_source.GetOutputPort())

cone_actor = vtkActor()
cone_actor.SetMapper(cone_mapper)
cone_actor.SetPosition(0, 0, 11)
cone_actor.RotateY(90)
cone_actor.GetProperty().SetColor(tomato)

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.AddActor(hs_actor_0)
renderer.AddActor(hs_actor_1)
renderer.AddActor(hs_actor_2)
renderer.AddActor(hs_actor_3)
renderer.AddActor(plane_actor)
renderer.AddActor(outline_actor)
renderer.AddActor(cone_actor)
renderer.SetBackground(slate_gray)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("hyper streamline")
render_window.SetMultiSamples(0)
render_window.SetSize(640, 480)

# Scene: configure camera
camera = vtkCamera()
camera.SetFocalPoint(0.113766, -1.13665, -1.01919)
camera.SetPosition(-29.4886, -63.1488, 26.5807)
camera.SetViewAngle(24.4617)
camera.SetViewUp(0.17138, 0.331163, 0.927879)
camera.SetClippingRange(1, 100)
renderer.SetActiveCamera(camera)

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
