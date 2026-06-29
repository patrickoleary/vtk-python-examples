#!/usr/bin/env python

# Read a NetCDF file using the COARDS convention and render the tos field.

import os

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersCore import (
    vtkAssignAttribute,
    vtkThreshold,
)
from vtkmodules.vtkFiltersGeometry import vtkDataSetSurfaceFilter
from vtkmodules.vtkIONetCDF import vtkNetCDFCFReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Source
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Read the NetCDF file
cf_reader = vtkNetCDFCFReader()
cf_reader.SetFileName(os.path.join(data_dir, "tos_O1_2001-2002.nc"))
cf_reader.UpdateMetaData()
cf_reader.SetVariableArrayStatus("tos", 1)
cf_reader.SetSphericalCoordinates(0)
cf_reader.Update()

# Assign field to scalars
assign_attribute = vtkAssignAttribute()
assign_attribute.SetInputConnection(cf_reader.GetOutputPort())
assign_attribute.Assign("tos", "SCALARS", "POINT_DATA")

# Threshold to remove fill values
threshold_filter = vtkThreshold()
threshold_filter.SetInputConnection(assign_attribute.GetOutputPort())
threshold_filter.SetThresholdFunction(vtkThreshold.THRESHOLD_LOWER)
threshold_filter.SetLowerThreshold(10000.0)

# Extract surface
surface_filter = vtkDataSetSurfaceFilter()
surface_filter.SetInputConnection(threshold_filter.GetOutputPort())

# Mapper
surface_mapper = vtkPolyDataMapper()
surface_mapper.SetInputConnection(surface_filter.GetOutputPort())
surface_mapper.SetScalarRange(270, 310)

# Actor
actor = vtkActor()
actor.SetMapper(surface_mapper)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(actor)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("netcdf reader x array")
render_window.SetMultiSamples(0)
render_window.SetSize(200, 200)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
