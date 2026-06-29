#!/usr/bin/env python

# Read SLAC 9-cell cavity data with quadratic (midpoint) elements and render bfield.

import os

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import vtkLookupTable
from vtkmodules.vtkCommonExecutionModel import vtkStreamingDemandDrivenPipeline
from vtkmodules.vtkFiltersGeometry import vtkCompositeDataGeometryFilter
from vtkmodules.vtkIONetCDF import vtkSLACReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Source
data_dir = os.path.join(os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__))), "SLAC", "ll-9cell-f523")

# Read the SLAC mesh and mode file
slac_reader = vtkSLACReader()
slac_reader.SetMeshFileName(os.path.join(data_dir, "ll-9cell-f523.ncdf"))
slac_reader.AddModeFileName(os.path.join(data_dir, "mode0.l0.R2.457036E+09I2.778314E+04.m3"))

slac_reader.ReadInternalVolumeOff()
slac_reader.ReadExternalSurfaceOn()
slac_reader.ReadMidpointsOn()

# Extract surface geometry
surface_geometry = vtkCompositeDataGeometryFilter()
surface_geometry.SetInputConnection(slac_reader.GetOutputPort(vtkSLACReader.SURFACE_OUTPUT))

# Mapper with bfield y-component coloring
bfield_mapper = vtkPolyDataMapper()
bfield_mapper.SetInputConnection(surface_geometry.GetOutputPort())
bfield_mapper.SetScalarModeToUsePointFieldData()
bfield_mapper.ColorByArrayComponent("bfield", 1)
bfield_mapper.UseLookupTableScalarRangeOff()
bfield_mapper.SetScalarRange(-1e-08, 1e-08)

bfield_lut = vtkLookupTable()
bfield_lut.SetHueRange(0.66667, 0.0)
bfield_mapper.SetLookupTable(bfield_lut)

# Actor
actor = vtkActor()
actor.SetMapper(bfield_mapper)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(actor)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("slac reader quadratic")
render_window.SetMultiSamples(0)
render_window.SetSize(600, 150)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
camera = renderer.GetActiveCamera()
camera.SetPosition(-0.75, 0.0, 0.7)
camera.SetFocalPoint(0.0, 0.0, 0.7)
camera.SetViewUp(0.0, 1.0, 0.0)

render_window.Render()

# Update time to test periodic mode interpolation
surface_geometry.UpdateInformation()
surface_geometry.GetOutputInformation(0).Set(
    vtkStreamingDemandDrivenPipeline.UPDATE_TIME_STEP(), 3e-10)

interactor.Initialize()
interactor.Start()
