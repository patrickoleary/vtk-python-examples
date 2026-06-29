#!/usr/bin/env python

# Demonstrate vtkUnstructuredGridToCellGrid converting an Exodus
# unstructured grid to a cell grid, rendering with composite
# cell grid mapper and color series lookup table.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

import os

from vtkmodules.vtkCommonColor import vtkColorSeries
from vtkmodules.vtkCommonDataModel import vtkCellGridSidesQuery
from vtkmodules.vtkCommonExecutionModel import vtkStreamingDemandDrivenPipeline
from vtkmodules.vtkFiltersCellGrid import (
    vtkCellGridComputeSides,
    vtkFiltersCellGrid,
    vtkUnstructuredGridToCellGrid,
)
from vtkmodules.vtkIOIOSS import vtkIOSSReader
from vtkmodules.vtkRenderingCellGrid import vtkRenderingCellGrid
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkCompositeCellGridMapper,
    vtkCompositeDataDisplayAttributes,
    vtkProperty,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Register render responders for DG cells
vtkRenderingCellGrid.RegisterCellsAndResponders()
vtkFiltersCellGrid.RegisterCellsAndResponders()

data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Read Exodus can dataset
reader = vtkIOSSReader()
reader.SetFileName(os.path.join(data_dir, "can.ex2"))
reader.UpdateInformation()
reader.GetSideSetSelection().EnableAllArrays()
reader.GetNodeSetSelection().EnableAllArrays()
reader.Update()

# Set time step
out_info = reader.GetExecutive().GetOutputInformation(0)
out_info.Set(vtkStreamingDemandDrivenPipeline.UPDATE_TIME_STEP(), 0.001)

# Convert unstructured grid to cell grid
converter = vtkUnstructuredGridToCellGrid()
converter.SetInputConnection(reader.GetOutputPort())
converter.Update()

# Compute sides for rendering
compute_sides = vtkCellGridComputeSides()
compute_sides.PreserveRenderableInputsOn()
compute_sides.OmitSidesForRenderableInputsOff()
compute_sides.SetInputConnection(converter.GetOutputPort())
compute_sides.Update()

sides_output = compute_sides.GetOutputDataObject(0)

# Composite cell grid mapper with color series
color_series = vtkColorSeries()
color_series.SetColorSchemeByName("Brewer Qualitative Accent")
lookup_table = color_series.CreateLookupTable(vtkColorSeries.ORDINAL)

mapper = vtkCompositeCellGridMapper()
mapper.SetInputConnection(compute_sides.GetOutputPort())
mapper.SetLookupTable(lookup_table)
mapper.ScalarVisibilityOn()
mapper.ColorByArrayComponent("EQPS", 0)
mapper.SetScalarModeToUseCellFieldData()

display_attributes = vtkCompositeDataDisplayAttributes()
mapper.SetCompositeDataDisplayAttributes(display_attributes)

# Hide some blocks for clearer visualization
display_attributes.SetBlockVisibility(sides_output.GetPartitionedDataSet(1).GetPartitionAsDataObject(0), False)
display_attributes.SetBlockVisibility(sides_output.GetPartitionedDataSet(2).GetPartitionAsDataObject(0), False)
display_attributes.SetBlockVisibility(sides_output.GetPartitionedDataSet(3).GetPartitionAsDataObject(0), False)

actor_prop = vtkProperty()
actor_prop.SetOpacity(1.0)
actor_prop.SetLineWidth(5)
actor_prop.SetPointSize(8)

actor = vtkActor()
actor.SetMapper(mapper)
actor.SetProperty(actor_prop)

# Renderer with gradient background
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(0.5, 0.4, 0.3)
renderer.SetBackground2(0.7, 0.6, 0.5)
renderer.GradientBackgroundOn()

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("unstructuredgrid to cellgrid")

# Scene
bounds = [0, 0, 0, 0, 0, 0]
converter.GetOutputDataObject(0).GetBounds(bounds)
center = [(bounds[0] + bounds[1]) / 2.0, (bounds[2] + bounds[3]) / 2.0, (bounds[4] + bounds[5]) / 2.0]
position = [center[0], bounds[2], center[2]]
camera = renderer.GetActiveCamera()
camera.SetFocalPoint(*center)
camera.SetPosition(*position)
camera.SetViewUp(0.0, 0.0, -1.0)
renderer.ResetCamera()

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
