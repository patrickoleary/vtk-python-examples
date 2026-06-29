#!/usr/bin/env python

# Read a NetCDF POP file and render the DYE01 scalar field on a rectilinear grid.

import os

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersGeometry import vtkGeometryFilter
from vtkmodules.vtkIONetCDF import vtkNetCDFPOPReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Source
data_dir = os.path.join(os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__))), "NetCDF")

# Read the NetCDF POP file
pop_reader = vtkNetCDFPOPReader()
pop_reader.SetFileName(os.path.join(data_dir, "test.pop.nc"))
pop_reader.SetStride(2, 3, 4)
pop_reader.Update()

# Set active scalars
output_grid = pop_reader.GetOutput()
output_grid.GetPointData().SetScalars(output_grid.GetPointData().GetArray("DYE01"))

# Geometry filter
geometry_filter = vtkGeometryFilter()
geometry_filter.SetInputConnection(pop_reader.GetOutputPort())

# Mapper
geometry_mapper = vtkPolyDataMapper()
geometry_mapper.SetInputConnection(geometry_filter.GetOutputPort())
geometry_mapper.ScalarVisibilityOn()

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
render_window.SetWindowName("netcdf pop reader")
render_window.SetMultiSamples(0)
render_window.SetSize(300, 300)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.ResetCamera(output_grid.GetBounds())
renderer.GetActiveCamera().Zoom(8)

interactor.Initialize()
interactor.Start()
