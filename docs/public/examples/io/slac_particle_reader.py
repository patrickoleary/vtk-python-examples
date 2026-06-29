#!/usr/bin/env python

# Read SLAC mesh with field modes and particle data, render both together.

import os

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import vtkLookupTable
from vtkmodules.vtkCommonExecutionModel import vtkStreamingDemandDrivenPipeline
from vtkmodules.vtkFiltersGeometry import vtkCompositeDataGeometryFilter
from vtkmodules.vtkIONetCDF import (
    vtkSLACParticleReader,
    vtkSLACReader,
)
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Source
data_dir = os.path.join(os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__))), "SLAC", "pic-example")

# Read the SLAC mesh and field mode files
mesh_reader = vtkSLACReader()
mesh_reader.SetMeshFileName(os.path.join(data_dir, "mesh.ncdf"))
mesh_reader.AddModeFileName(os.path.join(data_dir, "fields_0.mod"))
mesh_reader.AddModeFileName(os.path.join(data_dir, "fields_1.mod"))
mesh_reader.AddModeFileName(os.path.join(data_dir, "fields_2.mod"))
mesh_reader.AddModeFileName(os.path.join(data_dir, "fields_3.mod"))
mesh_reader.AddModeFileName(os.path.join(data_dir, "fields_4.mod"))
mesh_reader.AddModeFileName(os.path.join(data_dir, "fields_5.mod"))
mesh_reader.AddModeFileName(os.path.join(data_dir, "fields_6.mod"))
mesh_reader.AddModeFileName(os.path.join(data_dir, "fields_7.mod"))
mesh_reader.AddModeFileName(os.path.join(data_dir, "fields_8.mod"))

mesh_reader.ReadInternalVolumeOn()
mesh_reader.ReadExternalSurfaceOff()
mesh_reader.ReadMidpointsOff()

# Extract volume geometry
volume_geometry = vtkCompositeDataGeometryFilter()
volume_geometry.SetInputConnection(mesh_reader.GetOutputPort(vtkSLACReader.VOLUME_OUTPUT))

# Read the particle file
particle_reader = vtkSLACParticleReader()
particle_reader.SetFileName(os.path.join(data_dir, "particles_5.ncdf"))

# Mesh mapper with efield z-component coloring on log scale
mesh_mapper = vtkPolyDataMapper()
mesh_mapper.SetInputConnection(volume_geometry.GetOutputPort())
mesh_mapper.SetScalarModeToUsePointFieldData()
mesh_mapper.ColorByArrayComponent("efield", 2)
mesh_mapper.UseLookupTableScalarRangeOff()
mesh_mapper.SetScalarRange(1.0, 1e+05)

efield_lut = vtkLookupTable()
efield_lut.SetHueRange(0.66667, 0.0)
efield_lut.SetScaleToLog10()
mesh_mapper.SetLookupTable(efield_lut)

mesh_actor = vtkActor()
mesh_actor.SetMapper(mesh_mapper)
mesh_actor.GetProperty().FrontfaceCullingOn()

# Particle mapper
particle_mapper = vtkPolyDataMapper()
particle_mapper.SetInputConnection(particle_reader.GetOutputPort())
particle_mapper.ScalarVisibilityOff()

particle_actor = vtkActor()
particle_actor.SetMapper(particle_mapper)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(mesh_actor)
renderer.AddActor(particle_actor)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("slac particle reader")
render_window.SetMultiSamples(0)
render_window.SetSize(300, 200)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
camera = renderer.GetActiveCamera()
camera.SetPosition(-0.2, 0.05, 0.0)
camera.SetFocalPoint(0.0, 0.05, 0.0)
camera.SetViewUp(0.0, 1.0, 0.0)

render_window.Render()

# Sync mesh time to particle time
particle_time = particle_reader.GetOutput().GetInformation().Get(
    particle_reader.GetOutput().DATA_TIME_STEP())

volume_geometry.UpdateInformation()
volume_geometry.GetOutputInformation(0).Set(
    vtkStreamingDemandDrivenPipeline.UPDATE_TIME_STEP(), particle_time)

interactor.Initialize()
interactor.Start()
