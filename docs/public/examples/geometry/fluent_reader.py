#!/usr/bin/env python

# Read a Fluent case file and render pressure field.

import os

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersExtraction import vtkExtractBlock
from vtkmodules.vtkFiltersGeometry import vtkGeometryFilter
from vtkmodules.vtkIOGeometry import vtkFLUENTReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkCompositePolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Source
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Read Fluent case file
fluent_reader = vtkFLUENTReader()
fluent_reader.SetFileName(os.path.join(data_dir, "room.cas"))
fluent_reader.EnableAllCellArrays()

# Extract block
extract_block = vtkExtractBlock()
extract_block.AddIndex(1)
extract_block.SetInputConnection(fluent_reader.GetOutputPort())

# Geometry
geometry_filter = vtkGeometryFilter()
geometry_filter.SetInputConnection(extract_block.GetOutputPort())

# Mapper
composite_mapper = vtkCompositePolyDataMapper()
composite_mapper.SetInputConnection(geometry_filter.GetOutputPort())
composite_mapper.SetScalarModeToUseCellFieldData()
composite_mapper.SelectColorArray("PRESSURE")
composite_mapper.SetScalarRange(-31, 44)

# Actor
fluent_actor = vtkActor()
fluent_actor.SetMapper(composite_mapper)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(fluent_actor)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("fluent reader")
render_window.SetMultiSamples(0)
render_window.SetSize(300, 300)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
camera = renderer.GetActiveCamera()
camera.SetPosition(2, 2, 11)
camera.SetFocalPoint(2, 2, 0)
camera.SetViewUp(0, 1, 0)
camera.SetViewAngle(30)
renderer.ResetCameraClippingRange()

interactor.Initialize()
interactor.Start()
