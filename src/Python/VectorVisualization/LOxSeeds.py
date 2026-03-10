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

# Four spherical seed positions
seed_centers = [
    [-0.74, 0.0, 0.3],
    [-0.74, 0.0, 1.0],
    [-0.74, 0.0, 2.0],
    [-0.74, 0.0, 3.0],
]

renderers = []

for center in seed_centers:
    # ---- Filter: floor wireframe plane ----
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
    floor_actor.GetProperty().SetColor(black)
    floor_actor.GetProperty().SetLineWidth(2)

    # ---- Filter: post cross-section ----
    post_geom = vtkStructuredGridGeometryFilter()
    post_geom.SetExtent(10, 10, 0, 75, 0, 37)
    post_geom.SetInputData(sg)

    post_mapper = vtkPolyDataMapper()
    post_mapper.SetInputConnection(post_geom.GetOutputPort())
    post_mapper.SetLookupTable(lut)
    post_mapper.SetScalarRange(scalar_range)

    post_actor = vtkActor()
    post_actor.SetMapper(post_mapper)
    post_actor.GetProperty().SetColor(black)

    # ---- Source: spherical seed points ----
    rake = vtkPointSource()
    rake.SetCenter(center)
    rake.SetNumberOfPoints(10)

    # ---- Filter: trace streamlines ----
    streamers = vtkStreamTracer()
    streamers.SetInputConnection(pl3d.GetOutputPort())
    streamers.SetSourceConnection(rake.GetOutputPort())
    streamers.SetMaximumPropagation(250)
    streamers.SetInitialIntegrationStep(0.2)
    streamers.SetMinimumIntegrationStep(0.01)
    streamers.SetIntegratorType(2)
    streamers.Update()

    # ---- Filter: wrap streamlines in tubes ----
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

    # ---- Renderer: one viewport per seed position ----
    ren = vtkRenderer()
    ren.AddActor(floor_actor)
    ren.AddActor(post_actor)
    ren.AddActor(tube_actor)
    ren.SetBackground(slate_gray)
    renderers.append(ren)

# Camera: shared across all viewports
camera = vtkCamera()
camera.SetFocalPoint(0.918037, -0.0779233, 2.69513)
camera.SetPosition(0.840735, -23.6176, 8.50211)
camera.SetViewUp(0.00227904, 0.239501, 0.970893)
camera.SetClippingRange(1, 100)

# Window: 2x2 grid of viewports
render_window = vtkRenderWindow()
render_window.SetWindowName("LOxSeeds")
render_window.SetSize(512, 512)

for row in range(2):
    for col in range(2):
        idx = row * 2 + col
        viewport = [col / 2.0, (1 - row) / 2.0, (col + 1) / 2.0, (2 - row) / 2.0]
        renderers[idx].SetViewport(viewport)
        renderers[idx].SetActiveCamera(camera)
        render_window.AddRenderer(renderers[idx])

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Start()
