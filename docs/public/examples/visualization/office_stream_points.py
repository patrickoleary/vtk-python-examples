#!/usr/bin/env python

# Visualize office airflow using streamlines seeded near the inlet.

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
from vtkmodules.vtkFiltersSources import vtkPointSource
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

# Data directory
data_dir = Path(os.environ.get("VPE_DATA_DIR", Path(__file__).parent))

# Reader: load office CFD structured grid
reader = vtkDataSetReader()
reader.SetFileName(str(data_dir / "office.binary.vtk"))

sg = reader.GetStructuredGridOutput()

# Furniture geometry: 19 surface pieces

furn_geom_0 = vtkStructuredGridGeometryFilter()
furn_geom_0.SetInputData(sg)
furn_geom_0.SetExtent(11, 15, 7, 9, 8, 8)

furn_mapper_0 = vtkPolyDataMapper()
furn_mapper_0.SetInputConnection(furn_geom_0.GetOutputPort())
furn_mapper_0.ScalarVisibilityOff()

furn_actor_0 = vtkActor()
furn_actor_0.SetMapper(furn_mapper_0)
furn_actor_0.GetProperty().SetColor(table_top)

furn_geom_1 = vtkStructuredGridGeometryFilter()
furn_geom_1.SetInputData(sg)
furn_geom_1.SetExtent(11, 15, 10, 12, 8, 8)

furn_mapper_1 = vtkPolyDataMapper()
furn_mapper_1.SetInputConnection(furn_geom_1.GetOutputPort())
furn_mapper_1.ScalarVisibilityOff()

furn_actor_1 = vtkActor()
furn_actor_1.SetMapper(furn_mapper_1)
furn_actor_1.GetProperty().SetColor(table_top)

furn_geom_2 = vtkStructuredGridGeometryFilter()
furn_geom_2.SetInputData(sg)
furn_geom_2.SetExtent(15, 15, 7, 9, 0, 8)

furn_mapper_2 = vtkPolyDataMapper()
furn_mapper_2.SetInputConnection(furn_geom_2.GetOutputPort())
furn_mapper_2.ScalarVisibilityOff()

furn_actor_2 = vtkActor()
furn_actor_2.SetMapper(furn_mapper_2)
furn_actor_2.GetProperty().SetColor(filing_cabinet)

furn_geom_3 = vtkStructuredGridGeometryFilter()
furn_geom_3.SetInputData(sg)
furn_geom_3.SetExtent(15, 15, 10, 12, 0, 8)

furn_mapper_3 = vtkPolyDataMapper()
furn_mapper_3.SetInputConnection(furn_geom_3.GetOutputPort())
furn_mapper_3.ScalarVisibilityOff()

furn_actor_3 = vtkActor()
furn_actor_3.SetMapper(furn_mapper_3)
furn_actor_3.GetProperty().SetColor(filing_cabinet)

furn_geom_4 = vtkStructuredGridGeometryFilter()
furn_geom_4.SetInputData(sg)
furn_geom_4.SetExtent(13, 13, 0, 4, 0, 11)

furn_mapper_4 = vtkPolyDataMapper()
furn_mapper_4.SetInputConnection(furn_geom_4.GetOutputPort())
furn_mapper_4.ScalarVisibilityOff()

furn_actor_4 = vtkActor()
furn_actor_4.SetMapper(furn_mapper_4)
furn_actor_4.GetProperty().SetColor(book_shelf)

furn_geom_5 = vtkStructuredGridGeometryFilter()
furn_geom_5.SetInputData(sg)
furn_geom_5.SetExtent(20, 20, 0, 4, 0, 11)

furn_mapper_5 = vtkPolyDataMapper()
furn_mapper_5.SetInputConnection(furn_geom_5.GetOutputPort())
furn_mapper_5.ScalarVisibilityOff()

furn_actor_5 = vtkActor()
furn_actor_5.SetMapper(furn_mapper_5)
furn_actor_5.GetProperty().SetColor(book_shelf)

furn_geom_6 = vtkStructuredGridGeometryFilter()
furn_geom_6.SetInputData(sg)
furn_geom_6.SetExtent(13, 20, 0, 0, 0, 11)

furn_mapper_6 = vtkPolyDataMapper()
furn_mapper_6.SetInputConnection(furn_geom_6.GetOutputPort())
furn_mapper_6.ScalarVisibilityOff()

furn_actor_6 = vtkActor()
furn_actor_6.SetMapper(furn_mapper_6)
furn_actor_6.GetProperty().SetColor(book_shelf)

furn_geom_7 = vtkStructuredGridGeometryFilter()
furn_geom_7.SetInputData(sg)
furn_geom_7.SetExtent(13, 20, 4, 4, 0, 11)

furn_mapper_7 = vtkPolyDataMapper()
furn_mapper_7.SetInputConnection(furn_geom_7.GetOutputPort())
furn_mapper_7.ScalarVisibilityOff()

furn_actor_7 = vtkActor()
furn_actor_7.SetMapper(furn_mapper_7)
furn_actor_7.GetProperty().SetColor(book_shelf)

furn_geom_8 = vtkStructuredGridGeometryFilter()
furn_geom_8.SetInputData(sg)
furn_geom_8.SetExtent(13, 20, 0, 4, 0, 0)

furn_mapper_8 = vtkPolyDataMapper()
furn_mapper_8.SetInputConnection(furn_geom_8.GetOutputPort())
furn_mapper_8.ScalarVisibilityOff()

furn_actor_8 = vtkActor()
furn_actor_8.SetMapper(furn_mapper_8)
furn_actor_8.GetProperty().SetColor(book_shelf)

furn_geom_9 = vtkStructuredGridGeometryFilter()
furn_geom_9.SetInputData(sg)
furn_geom_9.SetExtent(13, 20, 0, 4, 11, 11)

furn_mapper_9 = vtkPolyDataMapper()
furn_mapper_9.SetInputConnection(furn_geom_9.GetOutputPort())
furn_mapper_9.ScalarVisibilityOff()

furn_actor_9 = vtkActor()
furn_actor_9.SetMapper(furn_mapper_9)
furn_actor_9.GetProperty().SetColor(book_shelf)

furn_geom_10 = vtkStructuredGridGeometryFilter()
furn_geom_10.SetInputData(sg)
furn_geom_10.SetExtent(13, 13, 15, 19, 0, 11)

furn_mapper_10 = vtkPolyDataMapper()
furn_mapper_10.SetInputConnection(furn_geom_10.GetOutputPort())
furn_mapper_10.ScalarVisibilityOff()

furn_actor_10 = vtkActor()
furn_actor_10.SetMapper(furn_mapper_10)
furn_actor_10.GetProperty().SetColor(book_shelf)

furn_geom_11 = vtkStructuredGridGeometryFilter()
furn_geom_11.SetInputData(sg)
furn_geom_11.SetExtent(20, 20, 15, 19, 0, 11)

furn_mapper_11 = vtkPolyDataMapper()
furn_mapper_11.SetInputConnection(furn_geom_11.GetOutputPort())
furn_mapper_11.ScalarVisibilityOff()

furn_actor_11 = vtkActor()
furn_actor_11.SetMapper(furn_mapper_11)
furn_actor_11.GetProperty().SetColor(book_shelf)

furn_geom_12 = vtkStructuredGridGeometryFilter()
furn_geom_12.SetInputData(sg)
furn_geom_12.SetExtent(13, 20, 15, 15, 0, 11)

furn_mapper_12 = vtkPolyDataMapper()
furn_mapper_12.SetInputConnection(furn_geom_12.GetOutputPort())
furn_mapper_12.ScalarVisibilityOff()

furn_actor_12 = vtkActor()
furn_actor_12.SetMapper(furn_mapper_12)
furn_actor_12.GetProperty().SetColor(book_shelf)

furn_geom_13 = vtkStructuredGridGeometryFilter()
furn_geom_13.SetInputData(sg)
furn_geom_13.SetExtent(13, 20, 19, 19, 0, 11)

furn_mapper_13 = vtkPolyDataMapper()
furn_mapper_13.SetInputConnection(furn_geom_13.GetOutputPort())
furn_mapper_13.ScalarVisibilityOff()

furn_actor_13 = vtkActor()
furn_actor_13.SetMapper(furn_mapper_13)
furn_actor_13.GetProperty().SetColor(book_shelf)

furn_geom_14 = vtkStructuredGridGeometryFilter()
furn_geom_14.SetInputData(sg)
furn_geom_14.SetExtent(13, 20, 15, 19, 0, 0)

furn_mapper_14 = vtkPolyDataMapper()
furn_mapper_14.SetInputConnection(furn_geom_14.GetOutputPort())
furn_mapper_14.ScalarVisibilityOff()

furn_actor_14 = vtkActor()
furn_actor_14.SetMapper(furn_mapper_14)
furn_actor_14.GetProperty().SetColor(book_shelf)

furn_geom_15 = vtkStructuredGridGeometryFilter()
furn_geom_15.SetInputData(sg)
furn_geom_15.SetExtent(13, 20, 15, 19, 11, 11)

furn_mapper_15 = vtkPolyDataMapper()
furn_mapper_15.SetInputConnection(furn_geom_15.GetOutputPort())
furn_mapper_15.ScalarVisibilityOff()

furn_actor_15 = vtkActor()
furn_actor_15.SetMapper(furn_mapper_15)
furn_actor_15.GetProperty().SetColor(book_shelf)

furn_geom_16 = vtkStructuredGridGeometryFilter()
furn_geom_16.SetInputData(sg)
furn_geom_16.SetExtent(20, 20, 6, 13, 10, 13)

furn_mapper_16 = vtkPolyDataMapper()
furn_mapper_16.SetInputConnection(furn_geom_16.GetOutputPort())
furn_mapper_16.ScalarVisibilityOff()

furn_actor_16 = vtkActor()
furn_actor_16.SetMapper(furn_mapper_16)
furn_actor_16.GetProperty().SetColor(window_color)

furn_geom_17 = vtkStructuredGridGeometryFilter()
furn_geom_17.SetInputData(sg)
furn_geom_17.SetExtent(0, 0, 9, 10, 14, 16)

furn_mapper_17 = vtkPolyDataMapper()
furn_mapper_17.SetInputConnection(furn_geom_17.GetOutputPort())
furn_mapper_17.ScalarVisibilityOff()

furn_actor_17 = vtkActor()
furn_actor_17.SetMapper(furn_mapper_17)
furn_actor_17.GetProperty().SetColor(lamp_black)

furn_geom_18 = vtkStructuredGridGeometryFilter()
furn_geom_18.SetInputData(sg)
furn_geom_18.SetExtent(0, 0, 9, 10, 0, 6)

furn_mapper_18 = vtkPolyDataMapper()
furn_mapper_18.SetInputConnection(furn_geom_18.GetOutputPort())
furn_mapper_18.ScalarVisibilityOff()

furn_actor_18 = vtkActor()
furn_actor_18.SetMapper(furn_mapper_18)
furn_actor_18.GetProperty().SetColor(lamp_black)

# Filter: outline around the data
outline = vtkStructuredGridOutlineFilter()
outline.SetInputData(sg)

outline_mapper = vtkPolyDataMapper()
outline_mapper.SetInputConnection(outline.GetOutputPort())

outline_actor = vtkActor()
outline_actor.SetMapper(outline_mapper)
outline_actor.GetProperty().SetColor(black)

# Source: seed points for streamlines near the inlet (center 0)
seeds = vtkPointSource()
seeds.SetRadius(0.075)
seeds.SetCenter(0.0, 2.1, 0.5)
seeds.SetNumberOfPoints(25)

# Filter: trace streamlines through the flow field
streamers = vtkStreamTracer()
streamers.SetInputConnection(reader.GetOutputPort())
streamers.SetSourceConnection(seeds.GetOutputPort())
streamers.SetMaximumPropagation(500)
streamers.SetMinimumIntegrationStep(0.1)
streamers.SetMaximumIntegrationStep(1.0)
streamers.SetInitialIntegrationStep(0.2)
streamers.SetIntegratorType(2)
streamers.Update()

# Mapper: color streamlines by scalar
stream_mapper = vtkPolyDataMapper()
stream_mapper.SetInputConnection(streamers.GetOutputPort())
stream_mapper.SetScalarRange(reader.GetOutput().GetPointData().GetScalars().GetRange())

stream_actor = vtkActor()
stream_actor.SetMapper(stream_mapper)

# Renderer: assemble the scene
renderer = vtkRenderer()
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
renderer.AddActor(furn_actor_17)
renderer.AddActor(furn_actor_18)
renderer.AddActor(outline_actor)
renderer.AddActor(stream_actor)
renderer.SetBackground(slate_gray)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("office stream points")
render_window.SetMultiSamples(0)
render_window.SetSize(640, 400)

# Scene: configure camera
camera = vtkCamera()
camera.SetClippingRange(0.726079, 36.3039)
camera.SetFocalPoint(2.43584, 2.15046, 1.11104)
camera.SetPosition(-4.76183, -10.4426, 3.17203)
camera.ComputeViewPlaneNormal()
camera.SetViewUp(0.0511273, 0.132773, 0.989827)
camera.SetViewAngle(18.604)
camera.Zoom(1.2)
renderer.SetActiveCamera(camera)

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
