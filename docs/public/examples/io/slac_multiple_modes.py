#!/usr/bin/env python

# Read SLAC pillbox data with multiple modes, set phase shifts and frequency scales, render efield.

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
data_dir = os.path.join(os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__))), "SLAC", "pillbox")

# Read the SLAC mesh and mode files
slac_reader = vtkSLACReader()
slac_reader.SetMeshFileName(os.path.join(data_dir, "Pillbox3TenDSlice.ncdf"))
slac_reader.AddModeFileName(os.path.join(data_dir, "omega3p.l0.m0000.1.3138186e+09.mod"))
slac_reader.AddModeFileName(os.path.join(data_dir, "omega3p.l0.m0001.1.3138187e+09.mod"))
slac_reader.AddModeFileName(os.path.join(data_dir, "omega3p.l0.m0002.1.3138189e+09.mod"))

slac_reader.ReadInternalVolumeOff()
slac_reader.ReadExternalSurfaceOn()
slac_reader.ReadMidpointsOff()

slac_reader.UpdateInformation()

# Get the time period from the surface output
out_info = slac_reader.GetExecutive().GetOutputInformation(vtkSLACReader.SURFACE_OUTPUT)
time_range = out_info.Get(vtkStreamingDemandDrivenPipeline.TIME_RANGE())
period = time_range[1]

# Set phase shifts and frequency scales
slac_reader.ResetPhaseShifts()
slac_reader.SetPhaseShift(1, 0.5 * period)
slac_reader.SetPhaseShift(2, 0.5 * period)

slac_reader.ResetFrequencyScales()
slac_reader.SetFrequencyScale(0, 0.75)
slac_reader.SetFrequencyScale(1, 1.5)

# Extract surface geometry
surface_geometry = vtkCompositeDataGeometryFilter()
surface_geometry.SetInputConnection(slac_reader.GetOutputPort(vtkSLACReader.SURFACE_OUTPUT))

# Mapper with efield z-component coloring
efield_mapper = vtkPolyDataMapper()
efield_mapper.SetInputConnection(surface_geometry.GetOutputPort())
efield_mapper.SetScalarModeToUsePointFieldData()
efield_mapper.ColorByArrayComponent("efield", 2)
efield_mapper.UseLookupTableScalarRangeOff()
efield_mapper.SetScalarRange(-240, 240)

efield_lut = vtkLookupTable()
efield_lut.SetHueRange(0.66667, 0.0)
efield_mapper.SetLookupTable(efield_lut)

# Actor
actor = vtkActor()
actor.SetMapper(efield_mapper)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(actor)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("slac multiple modes")
render_window.SetMultiSamples(0)
render_window.SetSize(600, 150)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
camera = renderer.GetActiveCamera()
camera.SetPosition(-0.75, 0.0, 0.0)
camera.SetFocalPoint(0.0, 0.0, 0.0)
camera.SetViewUp(0.0, 1.0, 0.0)

render_window.Render()

# Offset the phase by updating time
surface_geometry.UpdateInformation()
surface_geometry.GetOutputInformation(0).Set(
    vtkStreamingDemandDrivenPipeline.UPDATE_TIME_STEP(), 0.5 * period)

interactor.Initialize()
interactor.Start()
