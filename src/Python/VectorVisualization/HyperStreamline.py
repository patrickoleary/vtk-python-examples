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

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.SetBackground(slate_gray)

# Filter/Mapper/Actor: four hyperstreamlines seeded at cube corners
seed_points = [(9, 9, -9), (-9, -9, -9), (9, -9, -9), (-9, 9, -9)]
for seed in seed_points:
    # ---- Filter: integrate hyperstreamline along minor eigenvector ----
    hs = vtkHyperStreamline()
    hs.SetInputData(pt_load.GetOutput())
    hs.SetStartPosition(seed[0], seed[1], seed[2])
    hs.IntegrateMinorEigenvector()
    hs.SetMaximumPropagationDistance(18.0)
    hs.SetIntegrationStepLength(0.1)
    hs.SetStepLength(0.01)
    hs.SetRadius(0.25)
    hs.SetNumberOfSides(18)
    hs.SetIntegrationDirectionToIntegrateBothDirections()
    hs.Update()

    # ---- Mapper/Actor: display the hyperstreamline ----
    hs_mapper = vtkPolyDataMapper()
    hs_mapper.SetInputConnection(hs.GetOutputPort())
    hs_mapper.SetLookupTable(lut)
    hs_mapper.SetScalarRange(scalar_range)

    hs_actor = vtkActor()
    hs_actor.SetMapper(hs_mapper)
    renderer.AddActor(hs_actor)

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
renderer.AddActor(plane_actor)

# Filter: outline around the data volume
outline = vtkOutlineFilter()
outline.SetInputData(pt_load.GetOutput())

outline_mapper = vtkPolyDataMapper()
outline_mapper.SetInputConnection(outline.GetOutputPort())

outline_actor = vtkActor()
outline_actor.SetMapper(outline_mapper)
outline_actor.GetProperty().SetColor(black)
renderer.AddActor(outline_actor)

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
renderer.AddActor(cone_actor)

# Camera: configure the viewpoint
camera = vtkCamera()
camera.SetFocalPoint(0.113766, -1.13665, -1.01919)
camera.SetPosition(-29.4886, -63.1488, 26.5807)
camera.SetViewAngle(24.4617)
camera.SetViewUp(0.17138, 0.331163, 0.927879)
camera.SetClippingRange(1, 100)
renderer.SetActiveCamera(camera)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("HyperStreamline")
render_window.SetSize(640, 480)

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Start()
