#!/usr/bin/env python

# Write an image dataset to NetCDF CF format, read it back, and render the elevation data.

import os
import tempfile

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import vtkLookupTable
from vtkmodules.vtkCommonDataModel import vtkUniformGrid
from vtkmodules.vtkFiltersGeometry import vtkDataSetSurfaceFilter
from vtkmodules.vtkIONetCDF import (
    vtkNetCDFCFReader,
    vtkNetCDFCFWriter,
)
from vtkmodules.vtkIOXML import vtkXMLImageDataReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Source
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Read source image data
xml_reader = vtkXMLImageDataReader()
xml_reader.SetFileName(os.path.join(data_dir, "okanagan.vti"))
xml_reader.Update()

# Write to NetCDF CF format in a temp directory
temp_dir = tempfile.mkdtemp()
nc_file = os.path.join(temp_dir, "okanagan.nc")

netcdf_writer = vtkNetCDFCFWriter()
netcdf_writer.SetFileName(nc_file)
netcdf_writer.SetInputConnection(xml_reader.GetOutputPort())
netcdf_writer.AddGridMappingAttribute("grid_mapping_name", "lambert_conformal_conic")
netcdf_writer.AddGridMappingAttribute("standard_parallel", 49)
netcdf_writer.AddGridMappingAttribute("longitude_of_central_meridian", -95)
netcdf_writer.AddGridMappingAttribute("latitude_of_projection_origin", 49)
netcdf_writer.SetFillValue(-9999)
netcdf_writer.SetAttributeType(0)  # POINT
netcdf_writer.FillBlankedAttributesOn()
netcdf_writer.Write()

# Read the NetCDF CF file back
netcdf_reader = vtkNetCDFCFReader()
netcdf_reader.SetFileName(nc_file)
netcdf_reader.SphericalCoordinatesOff()
netcdf_reader.SetDimensions("(z, y, x)")
netcdf_reader.Update()

output_data = netcdf_reader.GetOutput()
uniform_grid = vtkUniformGrid()
uniform_grid.ShallowCopy(output_data)

# Extract surface
surface_filter = vtkDataSetSurfaceFilter()
surface_filter.SetInputData(uniform_grid)

# Lookup table
elevation_lut = vtkLookupTable()
elevation_lut.SetHueRange(0.6, 0)
elevation_lut.SetSaturationRange(1.0, 0)
elevation_lut.SetValueRange(0.5, 1)
elevation_lut.SetTableRange(-200, 125)

# Mapper
surface_mapper = vtkPolyDataMapper()
surface_mapper.SetLookupTable(elevation_lut)
surface_mapper.SetInputConnection(surface_filter.GetOutputPort())
surface_mapper.ScalarVisibilityOn()
surface_mapper.SetColorModeToMapScalars()
surface_mapper.SetScalarRange(34, 125)
surface_mapper.SetScalarModeToUsePointFieldData()
surface_mapper.SelectColorArray("National_units")

# Actor
actor = vtkActor()
actor.SetMapper(surface_mapper)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(0, 0, 0)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("netcdf cf writer")
render_window.SetMultiSamples(0)
render_window.SetSize(300, 300)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.ResetCamera(xml_reader.GetOutput().GetBounds())
camera = renderer.GetActiveCamera()
camera.Azimuth(180)
camera.Zoom(1.6)

interactor.Initialize()
interactor.Start()

# Clean up temp file
os.remove(nc_file)
os.rmdir(temp_dir)
