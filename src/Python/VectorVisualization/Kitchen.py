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

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.TwoSidedLightingOn()
renderer.AddActor(outline_actor)

# Furniture geometry: extent, color, opacity for each surface piece
furniture_specs = [
    ((27, 27, 14, 18, 0, 11), burlywood, 1.0),
    ((0, 0, 9, 18, 6, 12), sky_blue, 0.6),
    ((5, 12, 23, 23, 6, 12), sky_blue, 0.6),
    ((17, 17, 0, 11, 0, 6), egg_shell, 1.0),
    ((19, 19, 0, 11, 0, 6), egg_shell, 1.0),
    ((17, 19, 0, 0, 0, 6), egg_shell, 1.0),
    ((17, 19, 11, 11, 0, 6), egg_shell, 1.0),
    ((17, 19, 0, 11, 0, 0), egg_shell, 1.0),
    ((17, 19, 0, 7, 6, 6), egg_shell, 1.0),
    ((17, 19, 9, 11, 6, 6), egg_shell, 1.0),
    ((17, 17, 0, 11, 11, 16), silver, 1.0),
    ((19, 19, 0, 11, 11, 16), furniture, 1.0),
    ((17, 19, 0, 0, 11, 16), furniture, 1.0),
    ((17, 19, 11, 11, 11, 16), furniture, 1.0),
    ((17, 19, 0, 11, 16, 16), furniture, 1.0),
    ((17, 19, 7, 9, 6, 6), tomato, 1.0),
    ((17, 19, 7, 9, 11, 11), furniture, 1.0),
]

for extent, color, opacity in furniture_specs:
    geom = vtkStructuredGridGeometryFilter()
    geom.SetInputConnection(reader.GetOutputPort())
    geom.SetExtent(*extent)

    mapper = vtkPolyDataMapper()
    mapper.SetInputConnection(geom.GetOutputPort())
    mapper.ScalarVisibilityOff()

    actor = vtkActor()
    actor.SetMapper(mapper)
    actor.GetProperty().SetColor(color)
    if opacity < 1.0:
        actor.GetProperty().SetOpacity(opacity)
    renderer.AddActor(actor)

# Source: seed line (rake) for streamlines
seed_line = vtkLineSource()
seed_line.SetResolution(39)
seed_line.SetPoint1(0.08, 2.50, 0.71)
seed_line.SetPoint2(0.08, 4.50, 0.71)

rake_mapper = vtkPolyDataMapper()
rake_mapper.SetInputConnection(seed_line.GetOutputPort())

rake_actor = vtkActor()
rake_actor.SetMapper(rake_mapper)
renderer.AddActor(rake_actor)

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
renderer.AddActor(stream_actor)

# Camera: configure the viewpoint
renderer.SetBackground(slate_gray)
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

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("Kitchen")
render_window.SetSize(640, 512)

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Start()
