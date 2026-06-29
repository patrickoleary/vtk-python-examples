#!/usr/bin/env python

# Read a NetCDF CF file with unstructured (p-sided) cells, render cartesian and spherical views.

import os

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersCore import vtkAssignAttribute
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
nc_file = os.path.join(data_dir, "sampleGenGrid3.nc")

# Case 1: Spherical coordinates off (cartesian)
reader_cartesian = vtkNetCDFCFReader()
reader_cartesian.SetFileName(nc_file)
reader_cartesian.UpdateMetaData()
reader_cartesian.SetVariableArrayStatus("sample", 1)
reader_cartesian.SphericalCoordinatesOff()

# Assign field to scalars
aa_cartesian = vtkAssignAttribute()
aa_cartesian.SetInputConnection(reader_cartesian.GetOutputPort())
aa_cartesian.Assign("sample", "SCALARS", "CELL_DATA")

# Extract surface
surface_cartesian = vtkDataSetSurfaceFilter()
surface_cartesian.SetInputConnection(aa_cartesian.GetOutputPort())

mapper_cartesian = vtkPolyDataMapper()
mapper_cartesian.SetInputConnection(surface_cartesian.GetOutputPort())
mapper_cartesian.SetScalarRange(100, 2500)

actor_cartesian = vtkActor()
actor_cartesian.SetMapper(mapper_cartesian)

renderer_0 = vtkRenderer()
renderer_0.AddActor(actor_cartesian)
renderer_0.SetViewport(0.0, 0.0, 0.5, 1.0)

# Case 2: Spherical coordinates on
reader_spherical = vtkNetCDFCFReader()
reader_spherical.SetFileName(nc_file)
reader_spherical.UpdateMetaData()
reader_spherical.SetVariableArrayStatus("sample", 1)
reader_spherical.SphericalCoordinatesOn()

# Assign field to scalars
aa_spherical = vtkAssignAttribute()
aa_spherical.SetInputConnection(reader_spherical.GetOutputPort())
aa_spherical.Assign("sample", "SCALARS", "CELL_DATA")

# Extract surface
surface_spherical = vtkDataSetSurfaceFilter()
surface_spherical.SetInputConnection(aa_spherical.GetOutputPort())

mapper_spherical = vtkPolyDataMapper()
mapper_spherical.SetInputConnection(surface_spherical.GetOutputPort())
mapper_spherical.SetScalarRange(100, 2500)

actor_spherical = vtkActor()
actor_spherical.SetMapper(mapper_spherical)

renderer_1 = vtkRenderer()
renderer_1.AddActor(actor_spherical)
renderer_1.SetViewport(0.5, 0.0, 1.0, 1.0)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer_0)
render_window.AddRenderer(renderer_1)
render_window.SetWindowName("netcdf cf unstructured x array")
render_window.SetMultiSamples(0)
render_window.SetSize(400, 200)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
