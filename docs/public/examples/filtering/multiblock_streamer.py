#!/usr/bin/env python

# Stream traces through a multi-block PLOT3D combustor dataset using
# vtkStreamTracer with ribbon visualization colored by density.

import os

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import vtkLookupTable
from vtkmodules.vtkCommonDataModel import (
    vtkMultiBlockDataSet,
    vtkStructuredGrid,
)
from vtkmodules.vtkFiltersCore import (
    vtkAssignAttribute,
    vtkStructuredGridOutlineFilter,
)
from vtkmodules.vtkFiltersExtraction import vtkExtractGrid
from vtkmodules.vtkFiltersFlowPaths import vtkStreamTracer
from vtkmodules.vtkFiltersModeling import vtkRibbonFilter
from vtkmodules.vtkFiltersSources import vtkLineSource
from vtkmodules.vtkIOParallel import vtkMultiBlockPLOT3DReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Data directory
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Read PLOT3D data
plot3d = vtkMultiBlockPLOT3DReader()
plot3d.SetFileName(os.path.join(data_dir, "combxyz.bin"))
plot3d.SetQFileName(os.path.join(data_dir, "combq.bin"))
plot3d.SetBinaryFile(1)
plot3d.SetMultiGrid(0)
plot3d.SetHasByteCount(0)
plot3d.SetIBlanking(0)
plot3d.SetTwoDimensionalGeometry(0)
plot3d.SetForceRead(0)
plot3d.SetByteOrder(0)
plot3d.Update()

output = plot3d.GetOutput().GetBlock(0)

# Outline of the structured grid
outline = vtkStructuredGridOutlineFilter()
outline.SetInputData(output)

outline_mapper = vtkPolyDataMapper()
outline_mapper.SetInputConnection(outline.GetOutputPort())
outline_mapper.UseLookupTableScalarRangeOn()
outline_mapper.SetScalarVisibility(0)
outline_mapper.SetScalarModeToDefault()

outline_actor = vtkActor()
outline_actor.SetMapper(outline_mapper)
outline_actor.GetProperty().SetRepresentationToSurface()
outline_actor.GetProperty().SetInterpolationToGouraud()
outline_actor.GetProperty().SetAmbient(0.15)
outline_actor.GetProperty().SetDiffuse(0.85)
outline_actor.GetProperty().SetSpecular(0.1)
outline_actor.GetProperty().SetSpecularPower(100)
outline_actor.GetProperty().SetSpecularColor(1, 1, 1)
outline_actor.GetProperty().SetColor(1, 1, 1)

# Extract three sub-grids
extract_grid_0 = vtkExtractGrid()
extract_grid_0.SetInputData(output)
extract_grid_0.SetVOI(0, 14, 0, 32, 0, 24)
extract_grid_0.SetSampleRate(1, 1, 1)
extract_grid_0.SetIncludeBoundary(0)
extract_grid_0.Update()

extract_grid_1 = vtkExtractGrid()
extract_grid_1.SetInputData(output)
extract_grid_1.SetVOI(14, 29, 0, 32, 0, 24)
extract_grid_1.SetSampleRate(1, 1, 1)
extract_grid_1.SetIncludeBoundary(0)
extract_grid_1.Update()

extract_grid_2 = vtkExtractGrid()
extract_grid_2.SetInputData(output)
extract_grid_2.SetVOI(29, 56, 0, 32, 0, 24)
extract_grid_2.SetSampleRate(1, 1, 1)
extract_grid_2.SetIncludeBoundary(0)
extract_grid_2.Update()

# Seed line for stream tracer
line_source = vtkLineSource()
line_source.SetPoint1(3.05638, -3.00497, 28.2211)
line_source.SetPoint2(3.05638, 3.95916, 28.2211)
line_source.SetResolution(20)

# Build multi-block dataset from sub-grids
mbds = vtkMultiBlockDataSet()
mbds.SetNumberOfBlocks(3)

sg_0 = vtkStructuredGrid()
sg_0.ShallowCopy(extract_grid_0.GetOutput())
mbds.SetBlock(0, sg_0)

sg_1 = vtkStructuredGrid()
sg_1.ShallowCopy(extract_grid_1.GetOutput())
mbds.SetBlock(1, sg_1)

sg_2 = vtkStructuredGrid()
sg_2.ShallowCopy(extract_grid_2.GetOutput())
mbds.SetBlock(2, sg_2)

# Stream tracer
stream = vtkStreamTracer()
stream.SetInputData(mbds)
stream.SetSourceConnection(line_source.GetOutputPort())
stream.SetIntegrationStepUnit(2)
stream.SetMaximumPropagation(20)
stream.SetInitialIntegrationStep(0.5)
stream.SetIntegrationDirection(0)
stream.SetIntegratorType(0)
stream.SetMaximumNumberOfSteps(2000)
stream.SetTerminalSpeed(1e-12)

# Assign normals attribute
aa = vtkAssignAttribute()
aa.SetInputConnection(stream.GetOutputPort())
aa.Assign("Normals", "NORMALS", "POINT_DATA")

# Ribbon filter
ribbon = vtkRibbonFilter()
ribbon.SetInputConnection(aa.GetOutputPort())
ribbon.SetWidth(0.1)
ribbon.SetAngle(0)
ribbon.SetDefaultNormal(0, 0, 1)
ribbon.SetVaryWidth(0)

# Lookup table
lookup_table = vtkLookupTable()
lookup_table.SetNumberOfTableValues(256)
lookup_table.SetHueRange(0, 0.66667)
lookup_table.SetSaturationRange(1, 1)
lookup_table.SetValueRange(1, 1)
lookup_table.SetTableRange(0.197813, 0.710419)
lookup_table.SetVectorComponent(0)
lookup_table.Build()

# Ribbon mapper
ribbon_mapper = vtkPolyDataMapper()
ribbon_mapper.SetInputConnection(ribbon.GetOutputPort())
ribbon_mapper.UseLookupTableScalarRangeOn()
ribbon_mapper.SetScalarVisibility(1)
ribbon_mapper.SetScalarModeToUsePointFieldData()
ribbon_mapper.SelectColorArray("Density")
ribbon_mapper.SetLookupTable(lookup_table)

ribbon_actor = vtkActor()
ribbon_actor.SetMapper(ribbon_mapper)
ribbon_actor.GetProperty().SetRepresentationToSurface()
ribbon_actor.GetProperty().SetInterpolationToGouraud()
ribbon_actor.GetProperty().SetAmbient(0.15)
ribbon_actor.GetProperty().SetDiffuse(0.85)
ribbon_actor.GetProperty().SetSpecular(0)
ribbon_actor.GetProperty().SetSpecularPower(1)
ribbon_actor.GetProperty().SetSpecularColor(1, 1, 1)

# Renderer
renderer = vtkRenderer()
renderer.SetBackground(0.33, 0.35, 0.43)
renderer.AddActor(outline_actor)
renderer.AddActor(ribbon_actor)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(400, 400)
render_window.SetWindowName("multiblock streamer")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
