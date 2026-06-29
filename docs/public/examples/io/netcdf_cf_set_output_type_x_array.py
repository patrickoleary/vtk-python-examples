#!/usr/bin/env python

# Read a NetCDF CF file with four different output types and render each in a quadrant.

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
nc_file = os.path.join(data_dir, "tos_O1_2001-2002.nc")

# Case 1: Image type (bottom-left)
reader_image = vtkNetCDFCFReader()
reader_image.SetFileName(nc_file)
reader_image.SetOutputTypeToImage()
reader_image.UpdateMetaData()
reader_image.SetVariableArrayStatus("tos", 1)
reader_image.SphericalCoordinatesOff()

aa_image = vtkAssignAttribute()
aa_image.SetInputConnection(reader_image.GetOutputPort())
aa_image.Assign("tos", "SCALARS", "POINT_DATA")

thresh_image = vtkThreshold()
thresh_image.SetInputConnection(aa_image.GetOutputPort())
thresh_image.SetThresholdFunction(vtkThreshold.THRESHOLD_LOWER)
thresh_image.SetLowerThreshold(10000.0)

surface_image = vtkDataSetSurfaceFilter()
surface_image.SetInputConnection(thresh_image.GetOutputPort())

mapper_image = vtkPolyDataMapper()
mapper_image.SetInputConnection(surface_image.GetOutputPort())
mapper_image.SetScalarRange(270, 310)

actor_image = vtkActor()
actor_image.SetMapper(mapper_image)

renderer_0 = vtkRenderer()
renderer_0.AddActor(actor_image)
renderer_0.SetViewport(0.0, 0.0, 0.5, 0.5)

# Case 2: Rectilinear type (bottom-right)
reader_rect = vtkNetCDFCFReader()
reader_rect.SetFileName(nc_file)
reader_rect.SetOutputTypeToRectilinear()
reader_rect.UpdateMetaData()
reader_rect.SetVariableArrayStatus("tos", 1)
reader_rect.SphericalCoordinatesOff()

aa_rect = vtkAssignAttribute()
aa_rect.SetInputConnection(reader_rect.GetOutputPort())
aa_rect.Assign("tos", "SCALARS", "POINT_DATA")

thresh_rect = vtkThreshold()
thresh_rect.SetInputConnection(aa_rect.GetOutputPort())
thresh_rect.SetThresholdFunction(vtkThreshold.THRESHOLD_LOWER)
thresh_rect.SetLowerThreshold(10000.0)

surface_rect = vtkDataSetSurfaceFilter()
surface_rect.SetInputConnection(thresh_rect.GetOutputPort())

mapper_rect = vtkPolyDataMapper()
mapper_rect.SetInputConnection(surface_rect.GetOutputPort())
mapper_rect.SetScalarRange(270, 310)

actor_rect = vtkActor()
actor_rect.SetMapper(mapper_rect)

renderer_1 = vtkRenderer()
renderer_1.AddActor(actor_rect)
renderer_1.SetViewport(0.5, 0.0, 1.0, 0.5)

# Case 3: Structured type (top-left)
reader_struct = vtkNetCDFCFReader()
reader_struct.SetFileName(nc_file)
reader_struct.SetOutputTypeToStructured()
reader_struct.UpdateMetaData()
reader_struct.SetVariableArrayStatus("tos", 1)
reader_struct.SphericalCoordinatesOff()

aa_struct = vtkAssignAttribute()
aa_struct.SetInputConnection(reader_struct.GetOutputPort())
aa_struct.Assign("tos", "SCALARS", "POINT_DATA")

thresh_struct = vtkThreshold()
thresh_struct.SetInputConnection(aa_struct.GetOutputPort())
thresh_struct.SetThresholdFunction(vtkThreshold.THRESHOLD_LOWER)
thresh_struct.SetLowerThreshold(10000.0)

surface_struct = vtkDataSetSurfaceFilter()
surface_struct.SetInputConnection(thresh_struct.GetOutputPort())

mapper_struct = vtkPolyDataMapper()
mapper_struct.SetInputConnection(surface_struct.GetOutputPort())
mapper_struct.SetScalarRange(270, 310)

actor_struct = vtkActor()
actor_struct.SetMapper(mapper_struct)

renderer_2 = vtkRenderer()
renderer_2.AddActor(actor_struct)
renderer_2.SetViewport(0.0, 0.5, 0.5, 1.0)

# Case 4: Unstructured type (top-right)
reader_unstruct = vtkNetCDFCFReader()
reader_unstruct.SetFileName(nc_file)
reader_unstruct.SetOutputTypeToUnstructured()
reader_unstruct.UpdateMetaData()
reader_unstruct.SetVariableArrayStatus("tos", 1)
reader_unstruct.SphericalCoordinatesOff()

aa_unstruct = vtkAssignAttribute()
aa_unstruct.SetInputConnection(reader_unstruct.GetOutputPort())
aa_unstruct.Assign("tos", "SCALARS", "POINT_DATA")

thresh_unstruct = vtkThreshold()
thresh_unstruct.SetInputConnection(aa_unstruct.GetOutputPort())
thresh_unstruct.SetThresholdFunction(vtkThreshold.THRESHOLD_LOWER)
thresh_unstruct.SetLowerThreshold(10000.0)

surface_unstruct = vtkDataSetSurfaceFilter()
surface_unstruct.SetInputConnection(thresh_unstruct.GetOutputPort())

mapper_unstruct = vtkPolyDataMapper()
mapper_unstruct.SetInputConnection(surface_unstruct.GetOutputPort())
mapper_unstruct.SetScalarRange(270, 310)

actor_unstruct = vtkActor()
actor_unstruct.SetMapper(mapper_unstruct)

renderer_3 = vtkRenderer()
renderer_3.AddActor(actor_unstruct)
renderer_3.SetViewport(0.5, 0.5, 1.0, 1.0)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer_0)
render_window.AddRenderer(renderer_1)
render_window.AddRenderer(renderer_2)
render_window.AddRenderer(renderer_3)
render_window.SetWindowName("netcdf cf set output type x array")
render_window.SetMultiSamples(0)
render_window.SetSize(400, 400)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
