#!/usr/bin/env python

# Compare streamtubes from four spherical seed positions around the LOx post.

import os
from pathlib import Path

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkCommonCore import vtkLookupTable
from vtkmodules.vtkFiltersCore import vtkTubeFilter
from vtkmodules.vtkFiltersFlowPaths import vtkStreamTracer
from vtkmodules.vtkFiltersGeometry import vtkStructuredGridGeometryFilter
from vtkmodules.vtkFiltersSources import vtkPointSource
from vtkmodules.vtkIOParallel import vtkMultiBlockPLOT3DReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkCamera,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
slate_gray = (0.439, 0.502, 0.565)
black = (0.0, 0.0, 0.0)

# Data directory
data_dir = Path(os.environ.get("VPE_DATA_DIR", Path(__file__).parent))

# Reader: load PLOT3D LOx post dataset
pl3d = vtkMultiBlockPLOT3DReader()
pl3d.AutoDetectFormatOn()
pl3d.SetXYZFileName(str(data_dir / "postxyz.bin"))
pl3d.SetQFileName(str(data_dir / "postq.bin"))
pl3d.SetScalarFunctionNumber(153)
pl3d.SetVectorFunctionNumber(200)
pl3d.Update()

sg = pl3d.GetOutput().GetBlock(0)
scalar_range = sg.GetScalarRange()

# Lookup table: blue to red
lut = vtkLookupTable()
lut.SetHueRange(0.667, 0.0)

# ---- Viewport 0: seed center (-0.74, 0.0, 0.3) ----
floor_geom_0 = vtkStructuredGridGeometryFilter()
floor_geom_0.SetExtent(0, 37, 0, 75, 0, 0)
floor_geom_0.SetInputData(sg)
floor_geom_0.Update()

floor_mapper_0 = vtkPolyDataMapper()
floor_mapper_0.SetInputConnection(floor_geom_0.GetOutputPort())
floor_mapper_0.ScalarVisibilityOff()
floor_mapper_0.SetLookupTable(lut)

floor_actor_0 = vtkActor()
floor_actor_0.SetMapper(floor_mapper_0)
floor_actor_0.GetProperty().SetRepresentationToWireframe()
floor_actor_0.GetProperty().SetColor(black)
floor_actor_0.GetProperty().SetLineWidth(2)

post_geom_0 = vtkStructuredGridGeometryFilter()
post_geom_0.SetExtent(10, 10, 0, 75, 0, 37)
post_geom_0.SetInputData(sg)

post_mapper_0 = vtkPolyDataMapper()
post_mapper_0.SetInputConnection(post_geom_0.GetOutputPort())
post_mapper_0.SetLookupTable(lut)
post_mapper_0.SetScalarRange(scalar_range)

post_actor_0 = vtkActor()
post_actor_0.SetMapper(post_mapper_0)
post_actor_0.GetProperty().SetColor(black)

rake_0 = vtkPointSource()
rake_0.SetCenter(-0.74, 0.0, 0.3)
rake_0.SetNumberOfPoints(10)

streamers_0 = vtkStreamTracer()
streamers_0.SetInputConnection(pl3d.GetOutputPort())
streamers_0.SetSourceConnection(rake_0.GetOutputPort())
streamers_0.SetMaximumPropagation(250)
streamers_0.SetInitialIntegrationStep(0.2)
streamers_0.SetMinimumIntegrationStep(0.01)
streamers_0.SetIntegratorType(2)
streamers_0.Update()

tubes_0 = vtkTubeFilter()
tubes_0.SetInputConnection(streamers_0.GetOutputPort())
tubes_0.SetNumberOfSides(8)
tubes_0.SetRadius(0.08)
tubes_0.SetVaryRadius(0)

tube_mapper_0 = vtkPolyDataMapper()
tube_mapper_0.SetInputConnection(tubes_0.GetOutputPort())
tube_mapper_0.SetScalarRange(scalar_range)

tube_actor_0 = vtkActor()
tube_actor_0.SetMapper(tube_mapper_0)

renderer_0 = vtkRenderer()
renderer_0.AddActor(floor_actor_0)
renderer_0.AddActor(post_actor_0)
renderer_0.AddActor(tube_actor_0)
renderer_0.SetBackground(slate_gray)
renderer_0.SetViewport(0.0, 0.5, 0.5, 1.0)

# ---- Viewport 1: seed center (-0.74, 0.0, 1.0) ----
floor_geom_1 = vtkStructuredGridGeometryFilter()
floor_geom_1.SetExtent(0, 37, 0, 75, 0, 0)
floor_geom_1.SetInputData(sg)
floor_geom_1.Update()

floor_mapper_1 = vtkPolyDataMapper()
floor_mapper_1.SetInputConnection(floor_geom_1.GetOutputPort())
floor_mapper_1.ScalarVisibilityOff()
floor_mapper_1.SetLookupTable(lut)

floor_actor_1 = vtkActor()
floor_actor_1.SetMapper(floor_mapper_1)
floor_actor_1.GetProperty().SetRepresentationToWireframe()
floor_actor_1.GetProperty().SetColor(black)
floor_actor_1.GetProperty().SetLineWidth(2)

post_geom_1 = vtkStructuredGridGeometryFilter()
post_geom_1.SetExtent(10, 10, 0, 75, 0, 37)
post_geom_1.SetInputData(sg)

post_mapper_1 = vtkPolyDataMapper()
post_mapper_1.SetInputConnection(post_geom_1.GetOutputPort())
post_mapper_1.SetLookupTable(lut)
post_mapper_1.SetScalarRange(scalar_range)

post_actor_1 = vtkActor()
post_actor_1.SetMapper(post_mapper_1)
post_actor_1.GetProperty().SetColor(black)

rake_1 = vtkPointSource()
rake_1.SetCenter(-0.74, 0.0, 1.0)
rake_1.SetNumberOfPoints(10)

streamers_1 = vtkStreamTracer()
streamers_1.SetInputConnection(pl3d.GetOutputPort())
streamers_1.SetSourceConnection(rake_1.GetOutputPort())
streamers_1.SetMaximumPropagation(250)
streamers_1.SetInitialIntegrationStep(0.2)
streamers_1.SetMinimumIntegrationStep(0.01)
streamers_1.SetIntegratorType(2)
streamers_1.Update()

tubes_1 = vtkTubeFilter()
tubes_1.SetInputConnection(streamers_1.GetOutputPort())
tubes_1.SetNumberOfSides(8)
tubes_1.SetRadius(0.08)
tubes_1.SetVaryRadius(0)

tube_mapper_1 = vtkPolyDataMapper()
tube_mapper_1.SetInputConnection(tubes_1.GetOutputPort())
tube_mapper_1.SetScalarRange(scalar_range)

tube_actor_1 = vtkActor()
tube_actor_1.SetMapper(tube_mapper_1)

renderer_1 = vtkRenderer()
renderer_1.AddActor(floor_actor_1)
renderer_1.AddActor(post_actor_1)
renderer_1.AddActor(tube_actor_1)
renderer_1.SetBackground(slate_gray)
renderer_1.SetViewport(0.5, 0.5, 1.0, 1.0)

# ---- Viewport 2: seed center (-0.74, 0.0, 2.0) ----
floor_geom_2 = vtkStructuredGridGeometryFilter()
floor_geom_2.SetExtent(0, 37, 0, 75, 0, 0)
floor_geom_2.SetInputData(sg)
floor_geom_2.Update()

floor_mapper_2 = vtkPolyDataMapper()
floor_mapper_2.SetInputConnection(floor_geom_2.GetOutputPort())
floor_mapper_2.ScalarVisibilityOff()
floor_mapper_2.SetLookupTable(lut)

floor_actor_2 = vtkActor()
floor_actor_2.SetMapper(floor_mapper_2)
floor_actor_2.GetProperty().SetRepresentationToWireframe()
floor_actor_2.GetProperty().SetColor(black)
floor_actor_2.GetProperty().SetLineWidth(2)

post_geom_2 = vtkStructuredGridGeometryFilter()
post_geom_2.SetExtent(10, 10, 0, 75, 0, 37)
post_geom_2.SetInputData(sg)

post_mapper_2 = vtkPolyDataMapper()
post_mapper_2.SetInputConnection(post_geom_2.GetOutputPort())
post_mapper_2.SetLookupTable(lut)
post_mapper_2.SetScalarRange(scalar_range)

post_actor_2 = vtkActor()
post_actor_2.SetMapper(post_mapper_2)
post_actor_2.GetProperty().SetColor(black)

rake_2 = vtkPointSource()
rake_2.SetCenter(-0.74, 0.0, 2.0)
rake_2.SetNumberOfPoints(10)

streamers_2 = vtkStreamTracer()
streamers_2.SetInputConnection(pl3d.GetOutputPort())
streamers_2.SetSourceConnection(rake_2.GetOutputPort())
streamers_2.SetMaximumPropagation(250)
streamers_2.SetInitialIntegrationStep(0.2)
streamers_2.SetMinimumIntegrationStep(0.01)
streamers_2.SetIntegratorType(2)
streamers_2.Update()

tubes_2 = vtkTubeFilter()
tubes_2.SetInputConnection(streamers_2.GetOutputPort())
tubes_2.SetNumberOfSides(8)
tubes_2.SetRadius(0.08)
tubes_2.SetVaryRadius(0)

tube_mapper_2 = vtkPolyDataMapper()
tube_mapper_2.SetInputConnection(tubes_2.GetOutputPort())
tube_mapper_2.SetScalarRange(scalar_range)

tube_actor_2 = vtkActor()
tube_actor_2.SetMapper(tube_mapper_2)

renderer_2 = vtkRenderer()
renderer_2.AddActor(floor_actor_2)
renderer_2.AddActor(post_actor_2)
renderer_2.AddActor(tube_actor_2)
renderer_2.SetBackground(slate_gray)
renderer_2.SetViewport(0.0, 0.0, 0.5, 0.5)

# ---- Viewport 3: seed center (-0.74, 0.0, 3.0) ----
floor_geom_3 = vtkStructuredGridGeometryFilter()
floor_geom_3.SetExtent(0, 37, 0, 75, 0, 0)
floor_geom_3.SetInputData(sg)
floor_geom_3.Update()

floor_mapper_3 = vtkPolyDataMapper()
floor_mapper_3.SetInputConnection(floor_geom_3.GetOutputPort())
floor_mapper_3.ScalarVisibilityOff()
floor_mapper_3.SetLookupTable(lut)

floor_actor_3 = vtkActor()
floor_actor_3.SetMapper(floor_mapper_3)
floor_actor_3.GetProperty().SetRepresentationToWireframe()
floor_actor_3.GetProperty().SetColor(black)
floor_actor_3.GetProperty().SetLineWidth(2)

post_geom_3 = vtkStructuredGridGeometryFilter()
post_geom_3.SetExtent(10, 10, 0, 75, 0, 37)
post_geom_3.SetInputData(sg)

post_mapper_3 = vtkPolyDataMapper()
post_mapper_3.SetInputConnection(post_geom_3.GetOutputPort())
post_mapper_3.SetLookupTable(lut)
post_mapper_3.SetScalarRange(scalar_range)

post_actor_3 = vtkActor()
post_actor_3.SetMapper(post_mapper_3)
post_actor_3.GetProperty().SetColor(black)

rake_3 = vtkPointSource()
rake_3.SetCenter(-0.74, 0.0, 3.0)
rake_3.SetNumberOfPoints(10)

streamers_3 = vtkStreamTracer()
streamers_3.SetInputConnection(pl3d.GetOutputPort())
streamers_3.SetSourceConnection(rake_3.GetOutputPort())
streamers_3.SetMaximumPropagation(250)
streamers_3.SetInitialIntegrationStep(0.2)
streamers_3.SetMinimumIntegrationStep(0.01)
streamers_3.SetIntegratorType(2)
streamers_3.Update()

tubes_3 = vtkTubeFilter()
tubes_3.SetInputConnection(streamers_3.GetOutputPort())
tubes_3.SetNumberOfSides(8)
tubes_3.SetRadius(0.08)
tubes_3.SetVaryRadius(0)

tube_mapper_3 = vtkPolyDataMapper()
tube_mapper_3.SetInputConnection(tubes_3.GetOutputPort())
tube_mapper_3.SetScalarRange(scalar_range)

tube_actor_3 = vtkActor()
tube_actor_3.SetMapper(tube_mapper_3)

renderer_3 = vtkRenderer()
renderer_3.AddActor(floor_actor_3)
renderer_3.AddActor(post_actor_3)
renderer_3.AddActor(tube_actor_3)
renderer_3.SetBackground(slate_gray)
renderer_3.SetViewport(0.5, 0.0, 1.0, 0.5)

# Window: 2x2 grid of viewports
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer_0)
render_window.AddRenderer(renderer_1)
render_window.AddRenderer(renderer_2)
render_window.AddRenderer(renderer_3)
render_window.SetWindowName("l ox seeds")
render_window.SetMultiSamples(0)
render_window.SetSize(512, 512)

# Scene: shared camera across all viewports
camera = vtkCamera()
camera.SetFocalPoint(0.918037, -0.0779233, 2.69513)
camera.SetPosition(0.840735, -23.6176, 8.50211)
camera.SetViewUp(0.00227904, 0.239501, 0.970893)
camera.SetClippingRange(1, 100)
renderer_0.SetActiveCamera(camera)
renderer_1.SetActiveCamera(camera)
renderer_2.SetActiveCamera(camera)
renderer_3.SetActiveCamera(camera)

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
