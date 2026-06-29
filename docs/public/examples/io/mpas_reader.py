#!/usr/bin/env python

# Read an MPAS NetCDF file in multiple modes and render kinetic energy with different projections.

import os

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonDataModel import vtkPlane
from vtkmodules.vtkCommonExecutionModel import vtkStreamingDemandDrivenPipeline
from vtkmodules.vtkFiltersExtraction import vtkExtractGeometry
from vtkmodules.vtkFiltersGeometry import vtkGeometryFilter
from vtkmodules.vtkIONetCDF import vtkMPASReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Source
data_dir = os.path.join(os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__))), "NetCDF")

# Config 0: no lat-lon projection, no multilayer, vertical level 0
mpas_reader_0 = vtkMPASReader()
mpas_reader_0.SetFileName(os.path.join(data_dir, "MPASReader.nc"))

geometry_filter_0 = vtkGeometryFilter()
geometry_filter_0.SetInputConnection(mpas_reader_0.GetOutputPort())
geometry_filter_0.UpdateInformation()
executive_0 = geometry_filter_0.GetExecutive()
input_vector_0 = executive_0.GetInputInformation(0)
input_vector_0.GetInformationObject(0).Set(
    vtkStreamingDemandDrivenPipeline.UPDATE_TIME_STEP(), 0.0)

mpas_reader_0.Update()
mpas_reader_0.EnableAllCellArrays()
mpas_reader_0.EnableAllPointArrays()
mpas_reader_0.SetProjectLatLon(False)
mpas_reader_0.SetShowMultilayerView(False)
mpas_reader_0.SetLayerThickness(1000000)
mpas_reader_0.SetVerticalLevel(0)
mpas_reader_0.Update()

geometry_mapper_0 = vtkPolyDataMapper()
geometry_mapper_0.SetInputConnection(geometry_filter_0.GetOutputPort())
geometry_mapper_0.ScalarVisibilityOn()
geometry_mapper_0.SetColorModeToMapScalars()
geometry_mapper_0.SetScalarRange(0.0116, 199.9)
geometry_mapper_0.SetScalarModeToUsePointFieldData()
geometry_mapper_0.SelectColorArray("ke")

actor_0 = vtkActor()
actor_0.SetMapper(geometry_mapper_0)

# Config 1: lat-lon projection, no multilayer, vertical level 1
mpas_reader_1 = vtkMPASReader()
mpas_reader_1.SetFileName(os.path.join(data_dir, "MPASReader.nc"))

geometry_filter_1 = vtkGeometryFilter()
geometry_filter_1.SetInputConnection(mpas_reader_1.GetOutputPort())
geometry_filter_1.UpdateInformation()
executive_1 = geometry_filter_1.GetExecutive()
input_vector_1 = executive_1.GetInputInformation(0)
input_vector_1.GetInformationObject(0).Set(
    vtkStreamingDemandDrivenPipeline.UPDATE_TIME_STEP(), 0.0)

mpas_reader_1.Update()
mpas_reader_1.EnableAllCellArrays()
mpas_reader_1.EnableAllPointArrays()
mpas_reader_1.SetProjectLatLon(True)
mpas_reader_1.SetShowMultilayerView(False)
mpas_reader_1.SetLayerThickness(1000000)
mpas_reader_1.SetVerticalLevel(1)
mpas_reader_1.Update()

geometry_mapper_1 = vtkPolyDataMapper()
geometry_mapper_1.SetInputConnection(geometry_filter_1.GetOutputPort())
geometry_mapper_1.ScalarVisibilityOn()
geometry_mapper_1.SetColorModeToMapScalars()
geometry_mapper_1.SetScalarRange(0.0116, 199.9)
geometry_mapper_1.SetScalarModeToUsePointFieldData()
geometry_mapper_1.SelectColorArray("ke")

actor_1 = vtkActor()
actor_1.SetMapper(geometry_mapper_1)
actor_1.SetScale(30000)
actor_1.AddPosition(4370000, 0, 0)

# Config 2: no lat-lon projection, multilayer, vertical level 2
mpas_reader_2 = vtkMPASReader()
mpas_reader_2.SetFileName(os.path.join(data_dir, "MPASReader.nc"))

clip_plane_2 = vtkPlane()
clip_plane_2.SetOrigin(0.0, 0.0, 0.0)
clip_plane_2.SetNormal(-0.866, 0.0, 0.5)

extract_geometry_2 = vtkExtractGeometry()
extract_geometry_2.SetInputConnection(mpas_reader_2.GetOutputPort())
extract_geometry_2.SetImplicitFunction(clip_plane_2)

geometry_filter_2 = vtkGeometryFilter()
geometry_filter_2.SetInputConnection(extract_geometry_2.GetOutputPort())
geometry_filter_2.UpdateInformation()
executive_2 = geometry_filter_2.GetExecutive()
input_vector_2 = executive_2.GetInputInformation(0)
input_vector_2.GetInformationObject(0).Set(
    vtkStreamingDemandDrivenPipeline.UPDATE_TIME_STEP(), 0.0)

mpas_reader_2.Update()
mpas_reader_2.EnableAllCellArrays()
mpas_reader_2.EnableAllPointArrays()
mpas_reader_2.SetProjectLatLon(False)
mpas_reader_2.SetShowMultilayerView(True)
mpas_reader_2.SetLayerThickness(1000000)
mpas_reader_2.SetVerticalLevel(2)
mpas_reader_2.Update()

geometry_mapper_2 = vtkPolyDataMapper()
geometry_mapper_2.SetInputConnection(geometry_filter_2.GetOutputPort())
geometry_mapper_2.ScalarVisibilityOn()
geometry_mapper_2.SetColorModeToMapScalars()
geometry_mapper_2.SetScalarRange(0.0116, 199.9)
geometry_mapper_2.SetScalarModeToUsePointFieldData()
geometry_mapper_2.SelectColorArray("ke")

actor_2 = vtkActor()
actor_2.SetMapper(geometry_mapper_2)
actor_2.AddPosition(-10000000, 0, 0)

# Config 3: lat-lon projection, multilayer, vertical level 3
mpas_reader_3 = vtkMPASReader()
mpas_reader_3.SetFileName(os.path.join(data_dir, "MPASReader.nc"))

clip_plane_3 = vtkPlane()
clip_plane_3.SetOrigin(0.0, 0.0, 0.0)
clip_plane_3.SetNormal(-0.866, 0.0, 0.5)

extract_geometry_3 = vtkExtractGeometry()
extract_geometry_3.SetInputConnection(mpas_reader_3.GetOutputPort())
extract_geometry_3.SetImplicitFunction(clip_plane_3)

geometry_filter_3 = vtkGeometryFilter()
geometry_filter_3.SetInputConnection(extract_geometry_3.GetOutputPort())
geometry_filter_3.UpdateInformation()
executive_3 = geometry_filter_3.GetExecutive()
input_vector_3 = executive_3.GetInputInformation(0)
input_vector_3.GetInformationObject(0).Set(
    vtkStreamingDemandDrivenPipeline.UPDATE_TIME_STEP(), 0.0)

mpas_reader_3.Update()
mpas_reader_3.EnableAllCellArrays()
mpas_reader_3.EnableAllPointArrays()
mpas_reader_3.SetProjectLatLon(True)
mpas_reader_3.SetShowMultilayerView(True)
mpas_reader_3.SetLayerThickness(1000000)
mpas_reader_3.SetVerticalLevel(3)
mpas_reader_3.Update()

geometry_mapper_3 = vtkPolyDataMapper()
geometry_mapper_3.SetInputConnection(geometry_filter_3.GetOutputPort())
geometry_mapper_3.ScalarVisibilityOn()
geometry_mapper_3.SetColorModeToMapScalars()
geometry_mapper_3.SetScalarRange(0.0116, 199.9)
geometry_mapper_3.SetScalarModeToUsePointFieldData()
geometry_mapper_3.SelectColorArray("ke")

actor_3 = vtkActor()
actor_3.SetMapper(geometry_mapper_3)
actor_3.SetScale(30000)
actor_3.AddPosition(4370000, 0, 0)
actor_3.AddPosition(-10000000, 0, 0)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(actor_0)
renderer.AddActor(actor_1)
renderer.AddActor(actor_2)
renderer.AddActor(actor_3)
renderer.SetBackground(0, 0, 0)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("mpas reader")
render_window.SetMultiSamples(0)
render_window.SetSize(350, 300)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.ResetCamera(-14000000, 12370000, -6370000, 16370000, -6370000, 6370000)
renderer.GetActiveCamera().Zoom(2)

interactor.Initialize()
interactor.Start()
