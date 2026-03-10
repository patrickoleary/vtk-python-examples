#!/usr/bin/env python

# Visualize office airflow with a single streamtube whose radius varies by velocity.

import os
from pathlib import Path

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkCommonDataModel import vtkDataObject
from vtkmodules.vtkCommonMath import vtkRungeKutta4
from vtkmodules.vtkFiltersCore import (
    vtkStructuredGridOutlineFilter,
    vtkTubeFilter,
)
from vtkmodules.vtkFiltersFlowPaths import vtkStreamTracer
from vtkmodules.vtkFiltersGeometry import vtkStructuredGridGeometryFilter
from vtkmodules.vtkIOLegacy import vtkDataSetReader
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
table_top = (0.59, 0.427, 0.392)
filing_cabinet = (0.8, 0.8, 0.6)
book_shelf = (0.8, 0.8, 0.6)
window_color = (0.3, 0.3, 0.5)
lamp_black = (0.180, 0.282, 0.231)
black = (0.0, 0.0, 0.0)

# Furniture geometry: (extent, color)
FURNITURE = [
    ((11, 15, 7, 9, 8, 8), table_top),
    ((11, 15, 10, 12, 8, 8), table_top),
    ((15, 15, 7, 9, 0, 8), filing_cabinet),
    ((15, 15, 10, 12, 0, 8), filing_cabinet),
    ((13, 13, 0, 4, 0, 11), book_shelf),
    ((20, 20, 0, 4, 0, 11), book_shelf),
    ((13, 20, 0, 0, 0, 11), book_shelf),
    ((13, 20, 4, 4, 0, 11), book_shelf),
    ((13, 20, 0, 4, 0, 0), book_shelf),
    ((13, 20, 0, 4, 11, 11), book_shelf),
    ((13, 13, 15, 19, 0, 11), book_shelf),
    ((20, 20, 15, 19, 0, 11), book_shelf),
    ((13, 20, 15, 15, 0, 11), book_shelf),
    ((13, 20, 19, 19, 0, 11), book_shelf),
    ((13, 20, 15, 19, 0, 0), book_shelf),
    ((13, 20, 15, 19, 11, 11), book_shelf),
    ((20, 20, 6, 13, 10, 13), window_color),
    ((0, 0, 9, 10, 14, 16), lamp_black),
    ((0, 0, 9, 10, 0, 6), lamp_black),
]

# Data directory
data_dir = Path(os.environ.get("VPE_DATA_DIR", Path(__file__).parent))

# Reader: load office CFD structured grid
reader = vtkDataSetReader()
reader.SetFileName(str(data_dir / "office.binary.vtk"))
reader.Update()

sg = reader.GetStructuredGridOutput()

# Filter: single streamline integrated in both directions using RK4
integ = vtkRungeKutta4()

streamer = vtkStreamTracer()
streamer.SetInputConnection(reader.GetOutputPort())
streamer.SetStartPosition(0.1, 2.1, 0.5)
streamer.SetMaximumPropagation(500)
streamer.SetInitialIntegrationStep(0.05)
streamer.SetIntegrationDirectionToBoth()
streamer.SetIntegrator(integ)

# Filter: tube whose radius varies by vector magnitude (mass flux proxy)
stream_tube = vtkTubeFilter()
stream_tube.SetInputConnection(streamer.GetOutputPort())
stream_tube.SetInputArrayToProcess(1, 0, 0, vtkDataObject.FIELD_ASSOCIATION_POINTS, "vectors")
stream_tube.SetRadius(0.02)
stream_tube.SetNumberOfSides(12)
stream_tube.SetVaryRadiusToVaryRadiusByVector()

tube_mapper = vtkPolyDataMapper()
tube_mapper.SetInputConnection(stream_tube.GetOutputPort())
tube_mapper.SetScalarRange(reader.GetOutput().GetPointData().GetScalars().GetRange())

tube_actor = vtkActor()
tube_actor.SetMapper(tube_mapper)
tube_actor.GetProperty().BackfaceCullingOn()

# Renderer: assemble the scene
renderer = vtkRenderer()

# Furniture geometry from data-driven table
for extent, color in FURNITURE:
    geom = vtkStructuredGridGeometryFilter()
    geom.SetInputData(sg)
    geom.SetExtent(*extent)

    mapper = vtkPolyDataMapper()
    mapper.SetInputConnection(geom.GetOutputPort())
    mapper.ScalarVisibilityOff()

    actor = vtkActor()
    actor.SetMapper(mapper)
    actor.GetProperty().SetColor(color)
    renderer.AddActor(actor)

# Filter: outline around the data
outline = vtkStructuredGridOutlineFilter()
outline.SetInputData(sg)

outline_mapper = vtkPolyDataMapper()
outline_mapper.SetInputConnection(outline.GetOutputPort())

outline_actor = vtkActor()
outline_actor.SetMapper(outline_mapper)
outline_actor.GetProperty().SetColor(black)
renderer.AddActor(outline_actor)

renderer.AddActor(tube_actor)

# Camera: configure the viewpoint
camera = vtkCamera()
camera.SetClippingRange(0.726079, 36.3039)
camera.SetFocalPoint(2.43584, 2.15046, 1.11104)
camera.SetPosition(-4.76183, -10.4426, 3.17203)
camera.ComputeViewPlaneNormal()
camera.SetViewUp(0.0511273, 0.132773, 0.989827)
camera.SetViewAngle(18.604)
camera.Zoom(1.2)

renderer.SetBackground(slate_gray)
renderer.SetActiveCamera(camera)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("OfficeTube")
render_window.SetSize(640, 400)

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Start()
