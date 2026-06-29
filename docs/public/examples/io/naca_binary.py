#!/usr/bin/env python

# Read EnSight Gold binary NACA case file with lookup table and render.

import os

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import vtkLookupTable
from vtkmodules.vtkFiltersGeometry import vtkGeometryFilter
from vtkmodules.vtkIOEnSight import vtkEnSightGoldBinaryReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkCompositePolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Source
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Read EnSight Gold binary case file
ensight_reader = vtkEnSightGoldBinaryReader()
ensight_reader.SetCaseFileName(os.path.join(data_dir, "EnSight", "naca.bin.case"))
ensight_reader.SetTimeValue(3)

# Lookup table
lookup_table = vtkLookupTable()
lookup_table.SetHueRange(0.667, 0.0)
lookup_table.SetTableRange(0.636, 1.34)

# Extract geometry
geometry_filter = vtkGeometryFilter()
geometry_filter.SetInputConnection(ensight_reader.GetOutputPort())

# Mapper
composite_mapper = vtkCompositePolyDataMapper()
composite_mapper.SetInputConnection(geometry_filter.GetOutputPort())

# Actor
ensight_actor = vtkActor()
ensight_actor.SetMapper(composite_mapper)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(ensight_actor)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("naca binary")
render_window.SetMultiSamples(0)
render_window.SetSize(400, 400)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.ResetCamera()
camera = renderer.GetActiveCamera()
camera.SetFocalPoint(0, 0, 0)
camera.ParallelProjectionOff()
camera.Zoom(70)
camera.SetViewAngle(1.0)

interactor.Initialize()
interactor.Start()
