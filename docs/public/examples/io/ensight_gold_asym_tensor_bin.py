#!/usr/bin/env python

# Read EnSight Gold binary fluid domain case, assign R_ns as scalars, and render.

import os

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonDataModel import vtkDataSetAttributes
from vtkmodules.vtkFiltersCore import vtkAssignAttribute
from vtkmodules.vtkFiltersGeometry import vtkDataSetSurfaceFilter
from vtkmodules.vtkIOEnSight import vtkGenericEnSightReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkCompositePolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Source
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Read EnSight case file
ensight_reader = vtkGenericEnSightReader()
ensight_reader.SetCaseFileName(os.path.join(data_dir, "EnSight", "RESULT_FLUID_DOMAIN.case"))
ensight_reader.Update()

# Extract surface
surface_filter = vtkDataSetSurfaceFilter()
surface_filter.SetInputConnection(ensight_reader.GetOutputPort())
surface_filter.Update()

# Assign R_ns as scalars
assign_attribute = vtkAssignAttribute()
assign_attribute.SetInputConnection(surface_filter.GetOutputPort())
assign_attribute.Assign("R_ns", vtkDataSetAttributes.SCALARS, vtkAssignAttribute.CELL_DATA)
assign_attribute.Update()

# Mapper
composite_mapper = vtkCompositePolyDataMapper()
composite_mapper.SetInputConnection(assign_attribute.GetOutputPort())
composite_mapper.SetScalarVisibility(True)
composite_mapper.SetScalarRange(0.001, 0.008)
composite_mapper.UseLookupTableScalarRangeOff()

# Actor
ensight_actor = vtkActor()
ensight_actor.SetMapper(composite_mapper)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(ensight_actor)
renderer.SetBackground(1, 1, 1)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("ensight gold asym tensor bin")
render_window.SetMultiSamples(0)
render_window.SetSize(300, 300)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.ResetCamera()

interactor.Initialize()
interactor.Start()
