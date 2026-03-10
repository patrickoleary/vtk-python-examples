#!/usr/bin/env python

# Visualize airflow around a blunt fin using streamlines from a PLOT3D dataset.

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
from vtkmodules.vtkIOParallel import vtkMultiBlockPLOT3DReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
gray = (0.502, 0.502, 0.502)
moccasin = (1.000, 0.894, 0.710)
silver = (0.753, 0.753, 0.753)
black = (0.0, 0.0, 0.0)

# Data directory
data_dir = Path(os.environ.get("VPE_DATA_DIR", Path(__file__).parent))

# Reader: load PLOT3D blunt fin dataset
reader = vtkMultiBlockPLOT3DReader()
reader.SetXYZFileName(str(data_dir / "bluntfinxyz.bin"))
reader.SetQFileName(str(data_dir / "bluntfinq.bin"))
reader.Update()

pd = reader.GetOutput().GetBlock(0)

scalar_range = [0.0, 0.0]
max_time = 0.0
if pd.GetPointData().GetScalars():
    pd.GetPointData().GetScalars().GetRange(scalar_range)
if pd.GetPointData().GetVectors():
    max_velocity = pd.GetPointData().GetVectors().GetMaxNorm()
    max_time = 20.0 * pd.GetLength() / max_velocity

# Filter: structured grid outline
outline_filter = vtkStructuredGridOutlineFilter()
outline_filter.SetInputData(pd)

outline_mapper = vtkPolyDataMapper()
outline_mapper.SetInputConnection(outline_filter.GetOutputPort())

outline_actor = vtkActor()
outline_actor.SetMapper(outline_mapper)
outline_actor.GetProperty().SetColor(moccasin)
outline_actor.GetProperty().SetLineWidth(2.0)

# Filter: wall geometry for context
wall = vtkStructuredGridGeometryFilter()
wall.SetInputData(pd)
wall.SetExtent(0, 100, 0, 100, 0, 0)

wall_mapper = vtkPolyDataMapper()
wall_mapper.SetInputConnection(wall.GetOutputPort())
wall_mapper.ScalarVisibilityOff()

wall_actor = vtkActor()
wall_actor.SetMapper(wall_mapper)
wall_actor.GetProperty().SetColor(silver)

# Filter: fin geometry for context
fin = vtkStructuredGridGeometryFilter()
fin.SetInputData(pd)
fin.SetExtent(0, 100, 0, 0, 0, 100)

fin_mapper = vtkPolyDataMapper()
fin_mapper.SetInputConnection(fin.GetOutputPort())
fin_mapper.ScalarVisibilityOff()

fin_actor = vtkActor()
fin_actor.SetMapper(fin_mapper)
fin_actor.GetProperty().SetColor(silver)

# Source: seed line for streamlines
seed_line = vtkLineSource()
seed_line.SetResolution(25)
seed_line.SetPoint1(-6.36, 0.25, 0.06)
seed_line.SetPoint2(-6.36, 0.25, 5.37)

rake_mapper = vtkPolyDataMapper()
rake_mapper.SetInputConnection(seed_line.GetOutputPort())

rake_actor = vtkActor()
rake_actor.SetMapper(rake_mapper)
rake_actor.GetProperty().SetColor(black)
rake_actor.GetProperty().SetLineWidth(5)

# Filter: trace streamlines through the flow field
streamers = vtkStreamTracer()
streamers.SetInputConnection(reader.GetOutputPort())
streamers.SetSourceConnection(seed_line.GetOutputPort())
streamers.SetMaximumPropagation(max_time)
streamers.SetInitialIntegrationStep(0.2)
streamers.SetMinimumIntegrationStep(0.01)
streamers.SetIntegratorType(2)
streamers.Update()

# Mapper: color streamlines by scalar
stream_mapper = vtkPolyDataMapper()
stream_mapper.SetInputConnection(streamers.GetOutputPort())
stream_mapper.SetScalarRange(scalar_range)

# Actor: display the streamlines
stream_actor = vtkActor()
stream_actor.SetMapper(stream_mapper)

# Renderer: assemble the scene and configure the camera
renderer = vtkRenderer()
renderer.AddActor(outline_actor)
renderer.AddActor(wall_actor)
renderer.AddActor(fin_actor)
renderer.AddActor(rake_actor)
renderer.AddActor(stream_actor)
renderer.SetBackground(gray)
renderer.ResetCamera()
renderer.GetActiveCamera().Elevation(30.0)
renderer.GetActiveCamera().Azimuth(30.0)
renderer.GetActiveCamera().Dolly(1.2)
renderer.ResetCameraClippingRange()

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("BluntStreamlines")
render_window.SetSize(640, 480)

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Start()
