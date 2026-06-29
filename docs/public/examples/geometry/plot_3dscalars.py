#!/usr/bin/env python

# Display all Plot3D scalar functions in a 5x2 grid of renderers.

import os

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersGeometry import vtkStructuredGridGeometryFilter
from vtkmodules.vtkIOParallel import vtkMultiBlockPLOT3DReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkCamera,
    vtkLight,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Source
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

camera = vtkCamera()
light = vtkLight()

# Source - Density (100)
density_reader = vtkMultiBlockPLOT3DReader()
density_reader.SetXYZFileName(os.path.join(data_dir, "bluntfinxyz.bin"))
density_reader.SetQFileName(os.path.join(data_dir, "bluntfinq.bin"))
density_reader.SetScalarFunctionNumber(100)
density_reader.Update()
density_output = density_reader.GetOutput().GetBlock(0)

density_geometry = vtkStructuredGridGeometryFilter()
density_geometry.SetInputData(density_output)
density_geometry.SetExtent(25, 25, 0, 100, 0, 100)

density_mapper = vtkPolyDataMapper()
density_mapper.SetInputConnection(density_geometry.GetOutputPort())
density_mapper.SetScalarRange(density_output.GetPointData().GetScalars().GetRange())

density_actor = vtkActor()
density_actor.SetMapper(density_mapper)

# Source - Pressure (110)
pressure_reader = vtkMultiBlockPLOT3DReader()
pressure_reader.SetXYZFileName(os.path.join(data_dir, "bluntfinxyz.bin"))
pressure_reader.SetQFileName(os.path.join(data_dir, "bluntfinq.bin"))
pressure_reader.SetScalarFunctionNumber(110)
pressure_reader.Update()
pressure_output = pressure_reader.GetOutput().GetBlock(0)

pressure_geometry = vtkStructuredGridGeometryFilter()
pressure_geometry.SetInputData(pressure_output)
pressure_geometry.SetExtent(25, 25, 0, 100, 0, 100)

pressure_mapper = vtkPolyDataMapper()
pressure_mapper.SetInputConnection(pressure_geometry.GetOutputPort())
pressure_mapper.SetScalarRange(pressure_output.GetPointData().GetScalars().GetRange())

pressure_actor = vtkActor()
pressure_actor.SetMapper(pressure_mapper)

# Source - Temperature (120)
temperature_reader = vtkMultiBlockPLOT3DReader()
temperature_reader.SetXYZFileName(os.path.join(data_dir, "bluntfinxyz.bin"))
temperature_reader.SetQFileName(os.path.join(data_dir, "bluntfinq.bin"))
temperature_reader.SetScalarFunctionNumber(120)
temperature_reader.Update()
temperature_output = temperature_reader.GetOutput().GetBlock(0)

temperature_geometry = vtkStructuredGridGeometryFilter()
temperature_geometry.SetInputData(temperature_output)
temperature_geometry.SetExtent(25, 25, 0, 100, 0, 100)

temperature_mapper = vtkPolyDataMapper()
temperature_mapper.SetInputConnection(temperature_geometry.GetOutputPort())
temperature_mapper.SetScalarRange(temperature_output.GetPointData().GetScalars().GetRange())

temperature_actor = vtkActor()
temperature_actor.SetMapper(temperature_mapper)

# Source - Enthalpy (130)
enthalpy_reader = vtkMultiBlockPLOT3DReader()
enthalpy_reader.SetXYZFileName(os.path.join(data_dir, "bluntfinxyz.bin"))
enthalpy_reader.SetQFileName(os.path.join(data_dir, "bluntfinq.bin"))
enthalpy_reader.SetScalarFunctionNumber(130)
enthalpy_reader.Update()
enthalpy_output = enthalpy_reader.GetOutput().GetBlock(0)

enthalpy_geometry = vtkStructuredGridGeometryFilter()
enthalpy_geometry.SetInputData(enthalpy_output)
enthalpy_geometry.SetExtent(25, 25, 0, 100, 0, 100)

enthalpy_mapper = vtkPolyDataMapper()
enthalpy_mapper.SetInputConnection(enthalpy_geometry.GetOutputPort())
enthalpy_mapper.SetScalarRange(enthalpy_output.GetPointData().GetScalars().GetRange())

enthalpy_actor = vtkActor()
enthalpy_actor.SetMapper(enthalpy_mapper)

# Source - Internal Energy (140)
internal_energy_reader = vtkMultiBlockPLOT3DReader()
internal_energy_reader.SetXYZFileName(os.path.join(data_dir, "bluntfinxyz.bin"))
internal_energy_reader.SetQFileName(os.path.join(data_dir, "bluntfinq.bin"))
internal_energy_reader.SetScalarFunctionNumber(140)
internal_energy_reader.Update()
internal_energy_output = internal_energy_reader.GetOutput().GetBlock(0)

internal_energy_geometry = vtkStructuredGridGeometryFilter()
internal_energy_geometry.SetInputData(internal_energy_output)
internal_energy_geometry.SetExtent(25, 25, 0, 100, 0, 100)

internal_energy_mapper = vtkPolyDataMapper()
internal_energy_mapper.SetInputConnection(internal_energy_geometry.GetOutputPort())
internal_energy_mapper.SetScalarRange(internal_energy_output.GetPointData().GetScalars().GetRange())

internal_energy_actor = vtkActor()
internal_energy_actor.SetMapper(internal_energy_mapper)

# Source - Kinetic Energy (144)
kinetic_energy_reader = vtkMultiBlockPLOT3DReader()
kinetic_energy_reader.SetXYZFileName(os.path.join(data_dir, "bluntfinxyz.bin"))
kinetic_energy_reader.SetQFileName(os.path.join(data_dir, "bluntfinq.bin"))
kinetic_energy_reader.SetScalarFunctionNumber(144)
kinetic_energy_reader.Update()
kinetic_energy_output = kinetic_energy_reader.GetOutput().GetBlock(0)

kinetic_energy_geometry = vtkStructuredGridGeometryFilter()
kinetic_energy_geometry.SetInputData(kinetic_energy_output)
kinetic_energy_geometry.SetExtent(25, 25, 0, 100, 0, 100)

kinetic_energy_mapper = vtkPolyDataMapper()
kinetic_energy_mapper.SetInputConnection(kinetic_energy_geometry.GetOutputPort())
kinetic_energy_mapper.SetScalarRange(kinetic_energy_output.GetPointData().GetScalars().GetRange())

kinetic_energy_actor = vtkActor()
kinetic_energy_actor.SetMapper(kinetic_energy_mapper)

# Source - Velocity Magnitude (153)
velocity_magnitude_reader = vtkMultiBlockPLOT3DReader()
velocity_magnitude_reader.SetXYZFileName(os.path.join(data_dir, "bluntfinxyz.bin"))
velocity_magnitude_reader.SetQFileName(os.path.join(data_dir, "bluntfinq.bin"))
velocity_magnitude_reader.SetScalarFunctionNumber(153)
velocity_magnitude_reader.Update()
velocity_magnitude_output = velocity_magnitude_reader.GetOutput().GetBlock(0)

velocity_magnitude_geometry = vtkStructuredGridGeometryFilter()
velocity_magnitude_geometry.SetInputData(velocity_magnitude_output)
velocity_magnitude_geometry.SetExtent(25, 25, 0, 100, 0, 100)

velocity_magnitude_mapper = vtkPolyDataMapper()
velocity_magnitude_mapper.SetInputConnection(velocity_magnitude_geometry.GetOutputPort())
velocity_magnitude_mapper.SetScalarRange(velocity_magnitude_output.GetPointData().GetScalars().GetRange())

velocity_magnitude_actor = vtkActor()
velocity_magnitude_actor.SetMapper(velocity_magnitude_mapper)

# Source - Stagnation Energy (163)
stagnation_energy_reader = vtkMultiBlockPLOT3DReader()
stagnation_energy_reader.SetXYZFileName(os.path.join(data_dir, "bluntfinxyz.bin"))
stagnation_energy_reader.SetQFileName(os.path.join(data_dir, "bluntfinq.bin"))
stagnation_energy_reader.SetScalarFunctionNumber(163)
stagnation_energy_reader.Update()
stagnation_energy_output = stagnation_energy_reader.GetOutput().GetBlock(0)

stagnation_energy_geometry = vtkStructuredGridGeometryFilter()
stagnation_energy_geometry.SetInputData(stagnation_energy_output)
stagnation_energy_geometry.SetExtent(25, 25, 0, 100, 0, 100)

stagnation_energy_mapper = vtkPolyDataMapper()
stagnation_energy_mapper.SetInputConnection(stagnation_energy_geometry.GetOutputPort())
stagnation_energy_mapper.SetScalarRange(stagnation_energy_output.GetPointData().GetScalars().GetRange())

stagnation_energy_actor = vtkActor()
stagnation_energy_actor.SetMapper(stagnation_energy_mapper)

# Source - Entropy (170)
entropy_reader = vtkMultiBlockPLOT3DReader()
entropy_reader.SetXYZFileName(os.path.join(data_dir, "bluntfinxyz.bin"))
entropy_reader.SetQFileName(os.path.join(data_dir, "bluntfinq.bin"))
entropy_reader.SetScalarFunctionNumber(170)
entropy_reader.Update()
entropy_output = entropy_reader.GetOutput().GetBlock(0)

entropy_geometry = vtkStructuredGridGeometryFilter()
entropy_geometry.SetInputData(entropy_output)
entropy_geometry.SetExtent(25, 25, 0, 100, 0, 100)

entropy_mapper = vtkPolyDataMapper()
entropy_mapper.SetInputConnection(entropy_geometry.GetOutputPort())
entropy_mapper.SetScalarRange(entropy_output.GetPointData().GetScalars().GetRange())

entropy_actor = vtkActor()
entropy_actor.SetMapper(entropy_mapper)

# Source - Swirl (184)
swirl_reader = vtkMultiBlockPLOT3DReader()
swirl_reader.SetXYZFileName(os.path.join(data_dir, "bluntfinxyz.bin"))
swirl_reader.SetQFileName(os.path.join(data_dir, "bluntfinq.bin"))
swirl_reader.SetScalarFunctionNumber(184)
swirl_reader.Update()
swirl_output = swirl_reader.GetOutput().GetBlock(0)

swirl_geometry = vtkStructuredGridGeometryFilter()
swirl_geometry.SetInputData(swirl_output)
swirl_geometry.SetExtent(25, 25, 0, 100, 0, 100)

swirl_mapper = vtkPolyDataMapper()
swirl_mapper.SetInputConnection(swirl_geometry.GetOutputPort())
swirl_mapper.SetScalarRange(swirl_output.GetPointData().GetScalars().GetRange())

swirl_actor = vtkActor()
swirl_actor.SetMapper(swirl_mapper)

# Renderers - Row 1 (bottom)
density_renderer = vtkRenderer()
density_renderer.SetActiveCamera(camera)
density_renderer.AddLight(light)
density_renderer.AddActor(density_actor)
density_renderer.SetViewport(0.0, 0.0, 0.2, 0.5)

pressure_renderer = vtkRenderer()
pressure_renderer.SetActiveCamera(camera)
pressure_renderer.AddLight(light)
pressure_renderer.AddActor(pressure_actor)
pressure_renderer.SetViewport(0.2, 0.0, 0.4, 0.5)

temperature_renderer = vtkRenderer()
temperature_renderer.SetActiveCamera(camera)
temperature_renderer.AddLight(light)
temperature_renderer.AddActor(temperature_actor)
temperature_renderer.SetViewport(0.4, 0.0, 0.6, 0.5)

enthalpy_renderer = vtkRenderer()
enthalpy_renderer.SetActiveCamera(camera)
enthalpy_renderer.AddLight(light)
enthalpy_renderer.AddActor(enthalpy_actor)
enthalpy_renderer.SetViewport(0.6, 0.0, 0.8, 0.5)

internal_energy_renderer = vtkRenderer()
internal_energy_renderer.SetActiveCamera(camera)
internal_energy_renderer.AddLight(light)
internal_energy_renderer.AddActor(internal_energy_actor)
internal_energy_renderer.SetViewport(0.8, 0.0, 1.0, 0.5)

# Renderers - Row 2 (top)
kinetic_energy_renderer = vtkRenderer()
kinetic_energy_renderer.SetActiveCamera(camera)
kinetic_energy_renderer.AddLight(light)
kinetic_energy_renderer.AddActor(kinetic_energy_actor)
kinetic_energy_renderer.SetViewport(0.0, 0.5, 0.2, 1.0)

velocity_magnitude_renderer = vtkRenderer()
velocity_magnitude_renderer.SetActiveCamera(camera)
velocity_magnitude_renderer.AddLight(light)
velocity_magnitude_renderer.AddActor(velocity_magnitude_actor)
velocity_magnitude_renderer.SetViewport(0.2, 0.5, 0.4, 1.0)

stagnation_energy_renderer = vtkRenderer()
stagnation_energy_renderer.SetActiveCamera(camera)
stagnation_energy_renderer.AddLight(light)
stagnation_energy_renderer.AddActor(stagnation_energy_actor)
stagnation_energy_renderer.SetViewport(0.4, 0.5, 0.6, 1.0)

entropy_renderer = vtkRenderer()
entropy_renderer.SetActiveCamera(camera)
entropy_renderer.AddLight(light)
entropy_renderer.AddActor(entropy_actor)
entropy_renderer.SetViewport(0.6, 0.5, 0.8, 1.0)

swirl_renderer = vtkRenderer()
swirl_renderer.SetActiveCamera(camera)
swirl_renderer.AddLight(light)
swirl_renderer.AddActor(swirl_actor)
swirl_renderer.SetViewport(0.8, 0.5, 1.0, 1.0)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(density_renderer)
render_window.AddRenderer(pressure_renderer)
render_window.AddRenderer(temperature_renderer)
render_window.AddRenderer(enthalpy_renderer)
render_window.AddRenderer(internal_energy_renderer)
render_window.AddRenderer(kinetic_energy_renderer)
render_window.AddRenderer(velocity_magnitude_renderer)
render_window.AddRenderer(stagnation_energy_renderer)
render_window.AddRenderer(entropy_renderer)
render_window.AddRenderer(swirl_renderer)
render_window.SetWindowName("plot 3dscalars")
render_window.SetMultiSamples(0)
render_window.SetSize(600, 180)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
camera.SetViewUp(0, 1, 0)
camera.SetFocalPoint(0, 0, 0)
camera.SetPosition(1, 0, 0)
density_renderer.ResetCamera()
camera.Dolly(1.25)

density_renderer.ResetCameraClippingRange()
pressure_renderer.ResetCameraClippingRange()
temperature_renderer.ResetCameraClippingRange()
enthalpy_renderer.ResetCameraClippingRange()
internal_energy_renderer.ResetCameraClippingRange()
kinetic_energy_renderer.ResetCameraClippingRange()
velocity_magnitude_renderer.ResetCameraClippingRange()
stagnation_energy_renderer.ResetCameraClippingRange()
entropy_renderer.ResetCameraClippingRange()
swirl_renderer.ResetCameraClippingRange()

light.SetPosition(camera.GetPosition())
light.SetFocalPoint(camera.GetFocalPoint())

interactor.Initialize()
interactor.Start()
