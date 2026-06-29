#!/usr/bin/env python

# Read a NetCDF UGRID file, verify cell and point data, and render the unstructured grid.

import os

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersGeometry import vtkGeometryFilter
from vtkmodules.vtkIONetCDF import vtkNetCDFUGRIDReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkDataSetMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Source
data_dir = os.path.join(os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__))), "NetCDF")

# Read the UGRID file
ugrid_reader = vtkNetCDFUGRIDReader()
ugrid_reader.SetFileName(os.path.join(data_dir, "ugrid.nc"))
ugrid_reader.SetReplaceFillValueWithNan(True)
ugrid_reader.UpdateTimeStep(31.0)

output_grid = ugrid_reader.GetOutput()

# Geometry filter for rendering
geometry_filter = vtkGeometryFilter()
geometry_filter.SetInputConnection(ugrid_reader.GetOutputPort())

# Mapper
geometry_mapper = vtkDataSetMapper()
geometry_mapper.SetInputConnection(geometry_filter.GetOutputPort())
geometry_mapper.ScalarVisibilityOn()

# Actor
actor = vtkActor()
actor.SetMapper(geometry_mapper)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(0.2, 0.3, 0.4)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("netcdf ugrid reader")
render_window.SetMultiSamples(0)
render_window.SetSize(300, 300)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.ResetCamera()

interactor.Initialize()
interactor.Start()
