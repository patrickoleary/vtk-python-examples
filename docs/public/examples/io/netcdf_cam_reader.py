#!/usr/bin/env python

# Read a NetCDF CAM file with connectivity and render the temperature field.

import os

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersGeometry import vtkGeometryFilter
from vtkmodules.vtkIONetCDF import vtkNetCDFCAMReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Source
data_dir = os.path.join(os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__))), "NetCDF")

# Read the NetCDF CAM file
cam_reader = vtkNetCDFCAMReader()
cam_reader.SetFileName(os.path.join(data_dir, "CAMReaderPoints.nc"))
cam_reader.SetConnectivityFileName(os.path.join(data_dir, "CAMReaderConnectivity.nc"))
cam_reader.Update()

# Convert to polydata
geometry_filter = vtkGeometryFilter()
geometry_filter.SetInputConnection(cam_reader.GetOutputPort())

# Mapper with temperature coloring
geometry_mapper = vtkPolyDataMapper()
geometry_mapper.SetInputConnection(geometry_filter.GetOutputPort())
geometry_mapper.ScalarVisibilityOn()
geometry_mapper.SetColorModeToMapScalars()
geometry_mapper.SetScalarRange(205, 250)
geometry_mapper.SetScalarModeToUsePointFieldData()
geometry_mapper.SelectColorArray("T")

# Actor
actor = vtkActor()
actor.SetMapper(geometry_mapper)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(0, 0, 0)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("netcdf cam reader")
render_window.SetMultiSamples(0)
render_window.SetSize(300, 300)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.ResetCamera(cam_reader.GetOutput().GetBounds())
renderer.GetActiveCamera().Zoom(1.5)

interactor.Initialize()
interactor.Start()
