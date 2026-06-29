#!/usr/bin/env python

# Read WindBlade data and render field, blade, and ground geometry.

import os

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import vtkFloatArray
from vtkmodules.vtkCommonExecutionModel import vtkStreamingDemandDrivenPipeline
from vtkmodules.vtkFiltersGeometry import vtkGeometryFilter
from vtkmodules.vtkIOGeometry import vtkWindBladeReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Source
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Read WindBlade data
wind_reader = vtkWindBladeReader()
wind_reader.SetFilename(os.path.join(data_dir, "WindBladeReader", "test1_topo.wind"))

# Convert field to polydata
field_geometry = vtkGeometryFilter()
field_geometry.SetInputConnection(wind_reader.GetOutputPort(0))

# Convert blade to polydata
blade_geometry = vtkGeometryFilter()
blade_geometry.SetInputConnection(wind_reader.GetOutputPort(1))

# Convert ground to polydata
ground_geometry = vtkGeometryFilter()
ground_geometry.SetInputConnection(wind_reader.GetOutputPort(2))

# Set time request
field_geometry.UpdateInformation()
executive = field_geometry.GetExecutive()
input_vector = executive.GetInputInformation(0)
input_vector.GetInformationObject(0).Set(
    vtkStreamingDemandDrivenPipeline.UPDATE_TIME_STEP(), 10.0)

blade_geometry.UpdateInformation()
executive = blade_geometry.GetExecutive()
input_vector = executive.GetInputInformation(0)
input_vector.GetInformationObject(0).Set(
    vtkStreamingDemandDrivenPipeline.UPDATE_TIME_STEP(), 10.0)

wind_reader.Update()
blade_geometry.Update()
ground_geometry.Update()

# Add color arrays to blade and ground
blade_output = blade_geometry.GetOutput()
blade_color = vtkFloatArray()
blade_color.SetNumberOfTuples(blade_output.GetNumberOfPoints())
for i in range(blade_output.GetNumberOfPoints()):
    blade_color.SetValue(i, 1.0)
blade_color.SetName("Density")
blade_output.GetPointData().AddArray(blade_color)
blade_output.GetPointData().SetScalars(blade_color)

ground_output = ground_geometry.GetOutput()
ground_color = vtkFloatArray()
ground_color.SetNumberOfTuples(ground_output.GetNumberOfPoints())
for i in range(ground_output.GetNumberOfPoints()):
    ground_color.SetValue(i, 1.0)
ground_color.SetName("Density")
ground_output.GetPointData().AddArray(ground_color)
ground_output.GetPointData().SetScalars(ground_color)

# Field mapper
field_mapper = vtkPolyDataMapper()
field_mapper.SetInputConnection(field_geometry.GetOutputPort())
field_mapper.ScalarVisibilityOn()
field_mapper.SetColorModeToMapScalars()
field_mapper.SetScalarRange(0.964, 1.0065)
field_mapper.SetScalarModeToUsePointFieldData()
field_mapper.SelectColorArray("Density")

# Blade mapper
blade_mapper = vtkPolyDataMapper()
blade_mapper.SetInputConnection(blade_geometry.GetOutputPort())
blade_mapper.ScalarVisibilityOn()

# Ground mapper
ground_mapper = vtkPolyDataMapper()
ground_mapper.SetInputConnection(ground_geometry.GetOutputPort())
ground_mapper.ScalarVisibilityOn()

# Field actor
field_actor = vtkActor()
field_actor.SetMapper(field_mapper)

# Blade actor
blade_actor = vtkActor()
blade_actor.SetMapper(blade_mapper)
position = blade_actor.GetPosition()
blade_actor.RotateZ(90)
blade_actor.SetPosition(position[0] + 100, position[1] + 100, position[2] - 150)

# Ground actor
ground_actor = vtkActor()
ground_actor.SetMapper(ground_mapper)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(field_actor)
renderer.AddActor(blade_actor)
renderer.AddActor(ground_actor)
renderer.SetBackground(1, 1, 1)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("wind blade reader")
render_window.SetMultiSamples(0)
render_window.SetSize(300, 300)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
bounds = list(wind_reader.GetFieldOutput().GetBounds())
bounds[2] -= 150
renderer.ResetCamera(bounds)
renderer.GetActiveCamera().Elevation(-90)
renderer.GetActiveCamera().SetViewUp(0, 0, 1)
renderer.GetActiveCamera().Zoom(1.2)
renderer.ResetCameraClippingRange()

interactor.Initialize()
interactor.Start()
