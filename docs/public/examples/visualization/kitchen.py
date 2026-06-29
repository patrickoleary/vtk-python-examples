#!/usr/bin/env python

# Visualize air convection in a kitchen using streamlines seeded from a rake.

import os
from pathlib import Path

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkFiltersCore import vtkStructuredGridOutlineFilter
from vtkmodules.vtkFiltersFlowPaths import vtkStreamTracer
from vtkmodules.vtkFiltersGeometry import vtkStructuredGridGeometryFilter
from vtkmodules.vtkFiltersSources import vtkLineSource
from vtkmodules.vtkIOLegacy import vtkStructuredGridReader
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
lamp_black = (0.180, 0.282, 0.231)
burlywood = (0.871, 0.722, 0.529)
sky_blue = (0.529, 0.808, 0.922)
egg_shell = (0.988, 0.914, 0.827)
silver = (0.753, 0.753, 0.753)
furniture = (0.800, 0.800, 0.600)
tomato = (1.000, 0.388, 0.278)
black = (0.0, 0.0, 0.0)

# Data directory
data_dir = Path(os.environ.get("VPE_DATA_DIR", Path(__file__).parent))

# Reader: load the kitchen structured grid
reader = vtkStructuredGridReader()
reader.SetFileName(str(data_dir / "kitchen.vtk"))
reader.Update()

scalar_range = [0.0, 0.0]
max_time = 0.0
if reader.GetOutput().GetPointData().GetScalars():
    reader.GetOutput().GetPointData().GetScalars().GetRange(scalar_range)
if reader.GetOutput().GetPointData().GetVectors():
    max_velocity = reader.GetOutput().GetPointData().GetVectors().GetMaxNorm()
    max_time = 4.0 * reader.GetOutput().GetLength() / max_velocity

# Filter: outline around the data
outline_filter = vtkStructuredGridOutlineFilter()
outline_filter.SetInputConnection(reader.GetOutputPort())

outline_mapper = vtkPolyDataMapper()
outline_mapper.SetInputConnection(outline_filter.GetOutputPort())

outline_actor = vtkActor()
outline_actor.SetMapper(outline_mapper)
outline_actor.GetProperty().SetColor(lamp_black)

# Furniture geometry: 17 surface pieces

furn_geom_0 = vtkStructuredGridGeometryFilter()
furn_geom_0.SetInputConnection(reader.GetOutputPort())
furn_geom_0.SetExtent(27, 27, 14, 18, 0, 11)

furn_mapper_0 = vtkPolyDataMapper()
furn_mapper_0.SetInputConnection(furn_geom_0.GetOutputPort())
furn_mapper_0.ScalarVisibilityOff()

furn_actor_0 = vtkActor()
furn_actor_0.SetMapper(furn_mapper_0)
furn_actor_0.GetProperty().SetColor(burlywood)

furn_geom_1 = vtkStructuredGridGeometryFilter()
furn_geom_1.SetInputConnection(reader.GetOutputPort())
furn_geom_1.SetExtent(0, 0, 9, 18, 6, 12)

furn_mapper_1 = vtkPolyDataMapper()
furn_mapper_1.SetInputConnection(furn_geom_1.GetOutputPort())
furn_mapper_1.ScalarVisibilityOff()

furn_actor_1 = vtkActor()
furn_actor_1.SetMapper(furn_mapper_1)
furn_actor_1.GetProperty().SetColor(sky_blue)
furn_actor_1.GetProperty().SetOpacity(0.6)

furn_geom_2 = vtkStructuredGridGeometryFilter()
furn_geom_2.SetInputConnection(reader.GetOutputPort())
furn_geom_2.SetExtent(5, 12, 23, 23, 6, 12)

furn_mapper_2 = vtkPolyDataMapper()
furn_mapper_2.SetInputConnection(furn_geom_2.GetOutputPort())
furn_mapper_2.ScalarVisibilityOff()

furn_actor_2 = vtkActor()
furn_actor_2.SetMapper(furn_mapper_2)
furn_actor_2.GetProperty().SetColor(sky_blue)
furn_actor_2.GetProperty().SetOpacity(0.6)

furn_geom_3 = vtkStructuredGridGeometryFilter()
furn_geom_3.SetInputConnection(reader.GetOutputPort())
furn_geom_3.SetExtent(17, 17, 0, 11, 0, 6)

furn_mapper_3 = vtkPolyDataMapper()
furn_mapper_3.SetInputConnection(furn_geom_3.GetOutputPort())
furn_mapper_3.ScalarVisibilityOff()

furn_actor_3 = vtkActor()
furn_actor_3.SetMapper(furn_mapper_3)
furn_actor_3.GetProperty().SetColor(egg_shell)

furn_geom_4 = vtkStructuredGridGeometryFilter()
furn_geom_4.SetInputConnection(reader.GetOutputPort())
furn_geom_4.SetExtent(19, 19, 0, 11, 0, 6)

furn_mapper_4 = vtkPolyDataMapper()
furn_mapper_4.SetInputConnection(furn_geom_4.GetOutputPort())
furn_mapper_4.ScalarVisibilityOff()

furn_actor_4 = vtkActor()
furn_actor_4.SetMapper(furn_mapper_4)
furn_actor_4.GetProperty().SetColor(egg_shell)

furn_geom_5 = vtkStructuredGridGeometryFilter()
furn_geom_5.SetInputConnection(reader.GetOutputPort())
furn_geom_5.SetExtent(17, 19, 0, 0, 0, 6)

furn_mapper_5 = vtkPolyDataMapper()
furn_mapper_5.SetInputConnection(furn_geom_5.GetOutputPort())
furn_mapper_5.ScalarVisibilityOff()

furn_actor_5 = vtkActor()
furn_actor_5.SetMapper(furn_mapper_5)
furn_actor_5.GetProperty().SetColor(egg_shell)

furn_geom_6 = vtkStructuredGridGeometryFilter()
furn_geom_6.SetInputConnection(reader.GetOutputPort())
furn_geom_6.SetExtent(17, 19, 11, 11, 0, 6)

furn_mapper_6 = vtkPolyDataMapper()
furn_mapper_6.SetInputConnection(furn_geom_6.GetOutputPort())
furn_mapper_6.ScalarVisibilityOff()

furn_actor_6 = vtkActor()
furn_actor_6.SetMapper(furn_mapper_6)
furn_actor_6.GetProperty().SetColor(egg_shell)

furn_geom_7 = vtkStructuredGridGeometryFilter()
furn_geom_7.SetInputConnection(reader.GetOutputPort())
furn_geom_7.SetExtent(17, 19, 0, 11, 0, 0)

furn_mapper_7 = vtkPolyDataMapper()
furn_mapper_7.SetInputConnection(furn_geom_7.GetOutputPort())
furn_mapper_7.ScalarVisibilityOff()

furn_actor_7 = vtkActor()
furn_actor_7.SetMapper(furn_mapper_7)
furn_actor_7.GetProperty().SetColor(egg_shell)

furn_geom_8 = vtkStructuredGridGeometryFilter()
furn_geom_8.SetInputConnection(reader.GetOutputPort())
furn_geom_8.SetExtent(17, 19, 0, 7, 6, 6)

furn_mapper_8 = vtkPolyDataMapper()
furn_mapper_8.SetInputConnection(furn_geom_8.GetOutputPort())
furn_mapper_8.ScalarVisibilityOff()

furn_actor_8 = vtkActor()
furn_actor_8.SetMapper(furn_mapper_8)
furn_actor_8.GetProperty().SetColor(egg_shell)

furn_geom_9 = vtkStructuredGridGeometryFilter()
furn_geom_9.SetInputConnection(reader.GetOutputPort())
furn_geom_9.SetExtent(17, 19, 9, 11, 6, 6)

furn_mapper_9 = vtkPolyDataMapper()
furn_mapper_9.SetInputConnection(furn_geom_9.GetOutputPort())
furn_mapper_9.ScalarVisibilityOff()

furn_actor_9 = vtkActor()
furn_actor_9.SetMapper(furn_mapper_9)
furn_actor_9.GetProperty().SetColor(egg_shell)

furn_geom_10 = vtkStructuredGridGeometryFilter()
furn_geom_10.SetInputConnection(reader.GetOutputPort())
furn_geom_10.SetExtent(17, 17, 0, 11, 11, 16)

furn_mapper_10 = vtkPolyDataMapper()
furn_mapper_10.SetInputConnection(furn_geom_10.GetOutputPort())
furn_mapper_10.ScalarVisibilityOff()

furn_actor_10 = vtkActor()
furn_actor_10.SetMapper(furn_mapper_10)
furn_actor_10.GetProperty().SetColor(silver)

furn_geom_11 = vtkStructuredGridGeometryFilter()
furn_geom_11.SetInputConnection(reader.GetOutputPort())
furn_geom_11.SetExtent(19, 19, 0, 11, 11, 16)

furn_mapper_11 = vtkPolyDataMapper()
furn_mapper_11.SetInputConnection(furn_geom_11.GetOutputPort())
furn_mapper_11.ScalarVisibilityOff()

furn_actor_11 = vtkActor()
furn_actor_11.SetMapper(furn_mapper_11)
furn_actor_11.GetProperty().SetColor(furniture)

furn_geom_12 = vtkStructuredGridGeometryFilter()
furn_geom_12.SetInputConnection(reader.GetOutputPort())
furn_geom_12.SetExtent(17, 19, 0, 0, 11, 16)

furn_mapper_12 = vtkPolyDataMapper()
furn_mapper_12.SetInputConnection(furn_geom_12.GetOutputPort())
furn_mapper_12.ScalarVisibilityOff()

furn_actor_12 = vtkActor()
furn_actor_12.SetMapper(furn_mapper_12)
furn_actor_12.GetProperty().SetColor(furniture)

furn_geom_13 = vtkStructuredGridGeometryFilter()
furn_geom_13.SetInputConnection(reader.GetOutputPort())
furn_geom_13.SetExtent(17, 19, 11, 11, 11, 16)

furn_mapper_13 = vtkPolyDataMapper()
furn_mapper_13.SetInputConnection(furn_geom_13.GetOutputPort())
furn_mapper_13.ScalarVisibilityOff()

furn_actor_13 = vtkActor()
furn_actor_13.SetMapper(furn_mapper_13)
furn_actor_13.GetProperty().SetColor(furniture)

furn_geom_14 = vtkStructuredGridGeometryFilter()
furn_geom_14.SetInputConnection(reader.GetOutputPort())
furn_geom_14.SetExtent(17, 19, 0, 11, 16, 16)

furn_mapper_14 = vtkPolyDataMapper()
furn_mapper_14.SetInputConnection(furn_geom_14.GetOutputPort())
furn_mapper_14.ScalarVisibilityOff()

furn_actor_14 = vtkActor()
furn_actor_14.SetMapper(furn_mapper_14)
furn_actor_14.GetProperty().SetColor(furniture)

furn_geom_15 = vtkStructuredGridGeometryFilter()
furn_geom_15.SetInputConnection(reader.GetOutputPort())
furn_geom_15.SetExtent(17, 19, 7, 9, 6, 6)

furn_mapper_15 = vtkPolyDataMapper()
furn_mapper_15.SetInputConnection(furn_geom_15.GetOutputPort())
furn_mapper_15.ScalarVisibilityOff()

furn_actor_15 = vtkActor()
furn_actor_15.SetMapper(furn_mapper_15)
furn_actor_15.GetProperty().SetColor(tomato)

furn_geom_16 = vtkStructuredGridGeometryFilter()
furn_geom_16.SetInputConnection(reader.GetOutputPort())
furn_geom_16.SetExtent(17, 19, 7, 9, 11, 11)

furn_mapper_16 = vtkPolyDataMapper()
furn_mapper_16.SetInputConnection(furn_geom_16.GetOutputPort())
furn_mapper_16.ScalarVisibilityOff()

furn_actor_16 = vtkActor()
furn_actor_16.SetMapper(furn_mapper_16)
furn_actor_16.GetProperty().SetColor(furniture)

# Source: seed line (rake) for streamlines
seed_line = vtkLineSource()
seed_line.SetResolution(39)
seed_line.SetPoint1(0.08, 2.50, 0.71)
seed_line.SetPoint2(0.08, 4.50, 0.71)

rake_mapper = vtkPolyDataMapper()
rake_mapper.SetInputConnection(seed_line.GetOutputPort())

rake_actor = vtkActor()
rake_actor.SetMapper(rake_mapper)

# Filter: trace streamlines through the kitchen flow field
streamers = vtkStreamTracer()
streamers.SetInputConnection(reader.GetOutputPort())
streamers.SetSourceConnection(seed_line.GetOutputPort())
streamers.SetMaximumPropagation(max_time)
streamers.SetInitialIntegrationStep(0.5)
streamers.SetMinimumIntegrationStep(0.1)
streamers.SetIntegratorType(2)
streamers.Update()

stream_mapper = vtkPolyDataMapper()
stream_mapper.SetInputConnection(streamers.GetOutputPort())
stream_mapper.SetScalarRange(scalar_range)

stream_actor = vtkActor()
stream_actor.SetMapper(stream_mapper)
stream_actor.GetProperty().SetColor(black)

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.TwoSidedLightingOn()
renderer.AddActor(outline_actor)
renderer.AddActor(furn_actor_0)
renderer.AddActor(furn_actor_1)
renderer.AddActor(furn_actor_2)
renderer.AddActor(furn_actor_3)
renderer.AddActor(furn_actor_4)
renderer.AddActor(furn_actor_5)
renderer.AddActor(furn_actor_6)
renderer.AddActor(furn_actor_7)
renderer.AddActor(furn_actor_8)
renderer.AddActor(furn_actor_9)
renderer.AddActor(furn_actor_10)
renderer.AddActor(furn_actor_11)
renderer.AddActor(furn_actor_12)
renderer.AddActor(furn_actor_13)
renderer.AddActor(furn_actor_14)
renderer.AddActor(furn_actor_15)
renderer.AddActor(furn_actor_16)
renderer.AddActor(rake_actor)
renderer.AddActor(stream_actor)
renderer.SetBackground(slate_gray)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("kitchen")
render_window.SetMultiSamples(0)
render_window.SetSize(640, 512)

# Scene: configure camera
camera = vtkCamera()
renderer.SetActiveCamera(camera)
renderer.ResetCamera()
camera.SetFocalPoint(3.505, 2.505, 1.255)
camera.SetPosition(3.505, 24.6196, 1.255)
camera.SetViewUp(0, 0, 1)
camera.Azimuth(60)
camera.Elevation(30)
camera.Dolly(1.4)
renderer.ResetCameraClippingRange()

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
