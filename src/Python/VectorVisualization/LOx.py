#!/usr/bin/env python

# Visualize LOx post flow with streamtubes seeded from the computational grid.

import os
from pathlib import Path

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkCommonCore import vtkLookupTable
from vtkmodules.vtkFiltersCore import (
    vtkStructuredGridOutlineFilter,
    vtkTubeFilter,
)
from vtkmodules.vtkFiltersFlowPaths import vtkStreamTracer
from vtkmodules.vtkFiltersGeometry import vtkStructuredGridGeometryFilter
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
beige = (0.961, 0.961, 0.863)

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

# Filter: floor wireframe plane
floor_geom = vtkStructuredGridGeometryFilter()
floor_geom.SetExtent(0, 37, 0, 75, 0, 0)
floor_geom.SetInputData(sg)
floor_geom.Update()

floor_mapper = vtkPolyDataMapper()
floor_mapper.SetInputConnection(floor_geom.GetOutputPort())
floor_mapper.ScalarVisibilityOff()
floor_mapper.SetLookupTable(lut)

floor_actor = vtkActor()
floor_actor.SetMapper(floor_mapper)
floor_actor.GetProperty().SetRepresentationToWireframe()
floor_actor.GetProperty().SetColor(beige)
floor_actor.GetProperty().SetLineWidth(2)

# Filter: post cross-section
post_geom = vtkStructuredGridGeometryFilter()
post_geom.SetExtent(10, 10, 0, 75, 0, 37)
post_geom.SetInputData(sg)

post_mapper = vtkPolyDataMapper()
post_mapper.SetInputConnection(post_geom.GetOutputPort())
post_mapper.SetLookupTable(lut)
post_mapper.SetScalarRange(scalar_range)

post_actor = vtkActor()
post_actor.SetMapper(post_mapper)
post_actor.GetProperty().SetColor(beige)

# Source: seed points from computational grid in front of the post
seeds_geom = vtkStructuredGridGeometryFilter()
seeds_geom.SetExtent(10, 10, 37, 39, 1, 27)
seeds_geom.SetInputData(sg)

# Filter: trace streamlines through the flow field
streamers = vtkStreamTracer()
streamers.SetInputConnection(pl3d.GetOutputPort())
streamers.SetSourceConnection(seeds_geom.GetOutputPort())
streamers.SetMaximumPropagation(250)
streamers.SetInitialIntegrationStep(0.2)
streamers.SetMinimumIntegrationStep(0.01)
streamers.SetIntegratorType(2)
streamers.Update()

# Filter: wrap streamlines in tubes
tubes = vtkTubeFilter()
tubes.SetInputConnection(streamers.GetOutputPort())
tubes.SetNumberOfSides(8)
tubes.SetRadius(0.08)
tubes.SetVaryRadius(0)

tube_mapper = vtkPolyDataMapper()
tube_mapper.SetInputConnection(tubes.GetOutputPort())
tube_mapper.SetScalarRange(scalar_range)

tube_actor = vtkActor()
tube_actor.SetMapper(tube_mapper)

# Filter: outline around the data
outline = vtkStructuredGridOutlineFilter()
outline.SetInputData(sg)

outline_mapper = vtkPolyDataMapper()
outline_mapper.SetInputConnection(outline.GetOutputPort())

outline_actor = vtkActor()
outline_actor.SetMapper(outline_mapper)
outline_actor.GetProperty().SetColor(beige)

# Camera: configure the viewpoint
camera = vtkCamera()
camera.SetFocalPoint(2.47736, -0.150024, 2.42361)
camera.SetPosition(1.57547, -13.4601, 5.47872)
camera.SetViewUp(0.00653193, 0.617865, 0.786257)
camera.SetClippingRange(1, 100)

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.AddActor(outline_actor)
renderer.AddActor(floor_actor)
renderer.AddActor(post_actor)
renderer.AddActor(tube_actor)
renderer.SetBackground(slate_gray)
renderer.SetActiveCamera(camera)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("LOx")
render_window.SetSize(640, 480)

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Start()
