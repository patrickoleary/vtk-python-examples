#!/usr/bin/env python

# Read a VASP tessellation file and render molecules with Voronoi tessellations across four time steps.

import os

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonDataModel import vtkMolecule, vtkPolyData
from vtkmodules.vtkCommonExecutionModel import vtkStreamingDemandDrivenPipeline
from vtkmodules.vtkDomainsChemistry import vtkMoleculeMapper
from vtkmodules.vtkFiltersGeometry import vtkDataSetSurfaceFilter
from vtkmodules.vtkIOChemistry import vtkVASPTessellationReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Source
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Read the VASP tessellation file
vasp_reader = vtkVASPTessellationReader()
vasp_reader.SetFileName(os.path.join(data_dir, "VASP", "NPT_Z_TESSELLATE.out"))
vasp_reader.UpdateInformation()

# Surface filter for the tessellation output (port 1)
surface_filter = vtkDataSetSurfaceFilter()
surface_filter.SetInputConnection(vasp_reader.GetOutputPort(1))

# Get available time steps
out_info = vasp_reader.GetExecutive().GetOutputInformation(0)
times = [out_info.Get(vtkStreamingDemandDrivenPipeline.TIME_STEPS(), i)
         for i in range(out_info.Length(vtkStreamingDemandDrivenPipeline.TIME_STEPS()))]

# Time step 0
vasp_reader.UpdateTimeStep(times[0])
molecule_0 = vtkMolecule()
molecule_0.ShallowCopy(vasp_reader.GetOutput(0))
surface_filter.UpdateTimeStep(times[0])
tessellation_poly_0 = vtkPolyData()
tessellation_poly_0.ShallowCopy(surface_filter.GetOutput(0))

molecule_mapper_0 = vtkMoleculeMapper()
molecule_mapper_0.SetInputData(molecule_0)
molecule_mapper_0.UseBallAndStickSettings()
molecule_mapper_0.RenderLatticeOn()

molecule_actor_0 = vtkActor()
molecule_actor_0.SetMapper(molecule_mapper_0)

tessellation_mapper_0 = vtkPolyDataMapper()
tessellation_mapper_0.SetInputData(tessellation_poly_0)
tessellation_mapper_0.SelectColorArray("Atomic Numbers")
tessellation_mapper_0.SetLookupTable(molecule_mapper_0.GetLookupTable())

tessellation_actor_0 = vtkActor()
tessellation_actor_0.SetMapper(tessellation_mapper_0)
tessellation_actor_0.GetProperty().SetOpacity(0.5)

# Time step 1
vasp_reader.UpdateTimeStep(times[2])
molecule_1 = vtkMolecule()
molecule_1.ShallowCopy(vasp_reader.GetOutput(0))
surface_filter.UpdateTimeStep(times[2])
tessellation_poly_1 = vtkPolyData()
tessellation_poly_1.ShallowCopy(surface_filter.GetOutput(0))

molecule_mapper_1 = vtkMoleculeMapper()
molecule_mapper_1.SetInputData(molecule_1)
molecule_mapper_1.UseBallAndStickSettings()
molecule_mapper_1.RenderLatticeOn()

molecule_actor_1 = vtkActor()
molecule_actor_1.SetMapper(molecule_mapper_1)

tessellation_mapper_1 = vtkPolyDataMapper()
tessellation_mapper_1.SetInputData(tessellation_poly_1)
tessellation_mapper_1.SelectColorArray("Atomic Numbers")
tessellation_mapper_1.SetLookupTable(molecule_mapper_1.GetLookupTable())

tessellation_actor_1 = vtkActor()
tessellation_actor_1.SetMapper(tessellation_mapper_1)
tessellation_actor_1.GetProperty().SetOpacity(0.5)

# Time step 2
vasp_reader.UpdateTimeStep(times[4])
molecule_2 = vtkMolecule()
molecule_2.ShallowCopy(vasp_reader.GetOutput(0))
surface_filter.UpdateTimeStep(times[4])
tessellation_poly_2 = vtkPolyData()
tessellation_poly_2.ShallowCopy(surface_filter.GetOutput(0))

molecule_mapper_2 = vtkMoleculeMapper()
molecule_mapper_2.SetInputData(molecule_2)
molecule_mapper_2.UseBallAndStickSettings()
molecule_mapper_2.RenderLatticeOn()

molecule_actor_2 = vtkActor()
molecule_actor_2.SetMapper(molecule_mapper_2)

tessellation_mapper_2 = vtkPolyDataMapper()
tessellation_mapper_2.SetInputData(tessellation_poly_2)
tessellation_mapper_2.SelectColorArray("Atomic Numbers")
tessellation_mapper_2.SetLookupTable(molecule_mapper_2.GetLookupTable())

tessellation_actor_2 = vtkActor()
tessellation_actor_2.SetMapper(tessellation_mapper_2)
tessellation_actor_2.GetProperty().SetOpacity(0.5)

# Time step 3
vasp_reader.UpdateTimeStep(times[6])
molecule_3 = vtkMolecule()
molecule_3.ShallowCopy(vasp_reader.GetOutput(0))
surface_filter.UpdateTimeStep(times[6])
tessellation_poly_3 = vtkPolyData()
tessellation_poly_3.ShallowCopy(surface_filter.GetOutput(0))

molecule_mapper_3 = vtkMoleculeMapper()
molecule_mapper_3.SetInputData(molecule_3)
molecule_mapper_3.UseBallAndStickSettings()
molecule_mapper_3.RenderLatticeOn()

molecule_actor_3 = vtkActor()
molecule_actor_3.SetMapper(molecule_mapper_3)

tessellation_mapper_3 = vtkPolyDataMapper()
tessellation_mapper_3.SetInputData(tessellation_poly_3)
tessellation_mapper_3.SelectColorArray("Atomic Numbers")
tessellation_mapper_3.SetLookupTable(molecule_mapper_3.GetLookupTable())

tessellation_actor_3 = vtkActor()
tessellation_actor_3.SetMapper(tessellation_mapper_3)
tessellation_actor_3.GetProperty().SetOpacity(0.5)

# Renderers
renderer_0 = vtkRenderer()
renderer_0.SetViewport(0.0, 0.5, 0.5, 1.0)
renderer_0.AddActor(molecule_actor_0)
renderer_0.AddActor(tessellation_actor_0)
renderer_0.SetBackground(0.0, 0.0, 0.0)

renderer_1 = vtkRenderer()
renderer_1.SetViewport(0.5, 0.5, 1.0, 1.0)
renderer_1.AddActor(molecule_actor_1)
renderer_1.AddActor(tessellation_actor_1)
renderer_1.SetBackground(0.0, 0.0, 0.0)

renderer_2 = vtkRenderer()
renderer_2.SetViewport(0.0, 0.0, 0.5, 0.5)
renderer_2.AddActor(molecule_actor_2)
renderer_2.AddActor(tessellation_actor_2)
renderer_2.SetBackground(0.0, 0.0, 0.0)

renderer_3 = vtkRenderer()
renderer_3.SetViewport(0.5, 0.0, 1.0, 0.5)
renderer_3.AddActor(molecule_actor_3)
renderer_3.AddActor(tessellation_actor_3)
renderer_3.SetBackground(0.0, 0.0, 0.0)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer_0)
render_window.AddRenderer(renderer_1)
render_window.AddRenderer(renderer_2)
render_window.AddRenderer(renderer_3)
render_window.SetWindowName("vasp tessellation reader")
render_window.SetMultiSamples(0)
render_window.SetSize(450, 450)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer_0.GetActiveCamera().Dolly(1.5)
renderer_0.ResetCameraClippingRange()
renderer_1.GetActiveCamera().Dolly(1.5)
renderer_1.ResetCameraClippingRange()
renderer_2.GetActiveCamera().Dolly(1.5)
renderer_2.ResetCameraClippingRange()
renderer_3.GetActiveCamera().Dolly(1.5)
renderer_3.ResetCameraClippingRange()

interactor.Initialize()
interactor.Start()
