#!/usr/bin/env python

# Read an Exodus DG cell grid file with IOSS, compute sides, and render with CellGrid mapper.

import os

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkIOExodus  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonExecutionModel import vtkStreamingDemandDrivenPipeline
from vtkmodules.vtkFiltersCellGrid import (
    vtkCellGridComputeSides,
    vtkFiltersCellGrid,
)
from vtkmodules.vtkIOIOSS import vtkIOSSCellGridReader
from vtkmodules.vtkInteractionWidgets import vtkCameraOrientationWidget
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

# Source
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Read the Exodus DG file
cell_grid_reader = vtkIOSSCellGridReader()
cell_grid_reader.SetFileName(os.path.join(data_dir, "can.exdg"))
cell_grid_reader.UpdateInformation()
cell_grid_reader.Update()

# Set time step
out_info = cell_grid_reader.GetExecutive().GetOutputInformation(0)
out_info.Set(vtkStreamingDemandDrivenPipeline.UPDATE_TIME_STEP(), 0.001)

# Compute sides for rendering
compute_sides = vtkCellGridComputeSides()
compute_sides.PreserveRenderableInputsOn()
compute_sides.OmitSidesForRenderableInputsOff()
compute_sides.SetInputConnection(cell_grid_reader.GetOutputPort())
compute_sides.Update()

output_data = compute_sides.GetOutputDataObject(0)

# Mapper with composite display attributes
cell_grid_mapper = vtkCompositeCellGridMapper()
display_attributes = vtkCompositeDataDisplayAttributes()
cell_grid_mapper.SetCompositeDataDisplayAttributes(display_attributes)

# Hide some partitions
display_attributes.SetBlockVisibility(output_data.GetPartitionedDataSet(1).GetPartitionAsDataObject(0), False)
display_attributes.SetBlockVisibility(output_data.GetPartitionedDataSet(2).GetPartitionAsDataObject(0), False)
display_attributes.SetBlockVisibility(output_data.GetPartitionedDataSet(3).GetPartitionAsDataObject(0), False)

cell_grid_mapper.SetInputConnection(compute_sides.GetOutputPort())
cell_grid_mapper.ScalarVisibilityOn()
cell_grid_mapper.ColorByArrayComponent("EQPS", 0)
cell_grid_mapper.SetScalarModeToUseCellFieldData()

# Actor
actor = vtkActor()
actor.SetMapper(cell_grid_mapper)
actor_property = vtkProperty()
actor_property.SetOpacity(1.0)
actor_property.SetLineWidth(5)
actor_property.SetPointSize(8)
actor.SetProperty(actor_property)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(0.5, 0.4, 0.3)
renderer.SetBackground2(0.7, 0.6, 0.5)
renderer.GradientBackgroundOn()

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("ioss cellgrid reader")
render_window.SetMultiSamples(0)
render_window.SetSize(300, 300)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Camera orientation widget
camera_widget = vtkCameraOrientationWidget()
camera_widget.SetParentRenderer(renderer)
camera_widget.On()

# Scene
bounds = [0, 0, 0, 0, 0, 0]
output_data.GetBounds(bounds)
center = [(bounds[0] + bounds[1]) / 2.0, (bounds[2] + bounds[3]) / 2.0, (bounds[4] + bounds[5]) / 2.0]
position = [center[0], bounds[2], center[2]]
camera = renderer.GetActiveCamera()
camera.SetFocalPoint(*center)
camera.SetPosition(*position)
camera.SetViewUp(0.0, 0.0, -1.0)
renderer.ResetCamera()

interactor.Initialize()
interactor.Start()
