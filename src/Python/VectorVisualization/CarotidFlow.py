#!/usr/bin/env python

# Visualize blood flow in the carotid arteries using streamtubes.

import os
from pathlib import Path

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkCommonCore import vtkLookupTable
from vtkmodules.vtkFiltersCore import (
    vtkContourFilter,
    vtkTubeFilter,
)
from vtkmodules.vtkFiltersFlowPaths import vtkStreamTracer
from vtkmodules.vtkFiltersModeling import vtkOutlineFilter
from vtkmodules.vtkFiltersSources import vtkPointSource
from vtkmodules.vtkIOLegacy import vtkStructuredPointsReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkCamera,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
wheat = (0.961, 0.871, 0.702)
black = (0.0, 0.0, 0.0)

# Data directory
data_dir = Path(os.environ.get("VPE_DATA_DIR", Path(__file__).parent))

# Reader: load carotid artery structured points
reader = vtkStructuredPointsReader()
reader.SetFileName(str(data_dir / "carotid.vtk"))

# Source: seed points for streamlines
psource = vtkPointSource()
psource.SetNumberOfPoints(25)
psource.SetCenter(133.1, 116.3, 5.0)
psource.SetRadius(2.0)

# Filter: trace streamlines through the velocity field
streamers = vtkStreamTracer()
streamers.SetInputConnection(reader.GetOutputPort())
streamers.SetSourceConnection(psource.GetOutputPort())
streamers.SetMaximumPropagation(100.0)
streamers.SetInitialIntegrationStep(0.2)
streamers.SetTerminalSpeed(0.01)
streamers.Update()

scalar_range = streamers.GetOutput().GetPointData().GetScalars().GetRange()

# Filter: wrap streamlines in tubes for better visibility
tubes = vtkTubeFilter()
tubes.SetInputConnection(streamers.GetOutputPort())
tubes.SetRadius(0.3)
tubes.SetNumberOfSides(6)
tubes.SetVaryRadius(0)

# Lookup table: hue-based color mapping
lut = vtkLookupTable()
lut.SetHueRange(0.667, 0.0)
lut.Build()

# Mapper: color streamtubes by scalar
stream_mapper = vtkPolyDataMapper()
stream_mapper.SetInputConnection(tubes.GetOutputPort())
stream_mapper.SetScalarRange(scalar_range)
stream_mapper.SetLookupTable(lut)

# Actor: display the streamtubes
stream_actor = vtkActor()
stream_actor.SetMapper(stream_mapper)

# Filter: speed contour for context
iso = vtkContourFilter()
iso.SetInputConnection(reader.GetOutputPort())
iso.SetValue(0, 175)

iso_mapper = vtkPolyDataMapper()
iso_mapper.SetInputConnection(iso.GetOutputPort())
iso_mapper.ScalarVisibilityOff()

iso_actor = vtkActor()
iso_actor.SetMapper(iso_mapper)
iso_actor.GetProperty().SetRepresentationToWireframe()
iso_actor.GetProperty().SetOpacity(0.25)

# Filter: outline around the data
outline = vtkOutlineFilter()
outline.SetInputConnection(reader.GetOutputPort())

outline_mapper = vtkPolyDataMapper()
outline_mapper.SetInputConnection(outline.GetOutputPort())

outline_actor = vtkActor()
outline_actor.SetMapper(outline_mapper)
outline_actor.GetProperty().SetColor(black)

# Camera: configure the viewpoint
camera = vtkCamera()
camera.SetClippingRange(17.4043, 870.216)
camera.SetFocalPoint(136.71, 104.025, 23)
camera.SetPosition(204.747, 258.939, 63.7925)
camera.SetViewUp(-0.102647, -0.210897, 0.972104)
camera.Zoom(1.2)

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.AddActor(outline_actor)
renderer.AddActor(stream_actor)
renderer.AddActor(iso_actor)
renderer.SetBackground(wheat)
renderer.SetActiveCamera(camera)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("CarotidFlow")
render_window.SetSize(640, 480)

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Start()
