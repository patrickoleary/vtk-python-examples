#!/usr/bin/env python

# Demonstrate vtkExpandMarkedElements expanding marked cells across
# a multi-block sphere dataset, removing intermediate layers and seed.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import vtkSignedCharArray
from vtkmodules.vtkCommonDataModel import (
    vtkDataObject,
    vtkMultiBlockDataSet,
)
from vtkmodules.vtkFiltersExtraction import vtkExpandMarkedElements
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkCompositePolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Build multi-block dataset of 3 sphere parts
multi_block = vtkMultiBlockDataSet()

# Block 0.
sphere_0 = vtkSphereSource()
sphere_0.SetPhiResolution(6)
sphere_0.SetThetaResolution(6)
sphere_0.SetStartTheta(0.0)
sphere_0.SetEndTheta(120.0)
sphere_0.Update()
block_data_0 = sphere_0.GetOutput()
selected_cells_0 = vtkSignedCharArray()
selected_cells_0.SetName("MarkedCells")
selected_cells_0.SetNumberOfTuples(block_data_0.GetNumberOfCells())
selected_cells_0.FillComponent(0, 0)
selected_cells_0.SetComponent(20, 0, 1)
block_data_0.GetCellData().AddArray(selected_cells_0)
multi_block.SetBlock(0, block_data_0)

# Block 1.
sphere_1 = vtkSphereSource()
sphere_1.SetPhiResolution(6)
sphere_1.SetThetaResolution(6)
sphere_1.SetStartTheta(120.0)
sphere_1.SetEndTheta(240.0)
sphere_1.Update()
block_data_1 = sphere_1.GetOutput()
selected_cells_1 = vtkSignedCharArray()
selected_cells_1.SetName("MarkedCells")
selected_cells_1.SetNumberOfTuples(block_data_1.GetNumberOfCells())
selected_cells_1.FillComponent(0, 0)
selected_cells_1.SetComponent(20, 0, 1)
block_data_1.GetCellData().AddArray(selected_cells_1)
multi_block.SetBlock(1, block_data_1)

# Block 2.
sphere_2 = vtkSphereSource()
sphere_2.SetPhiResolution(6)
sphere_2.SetThetaResolution(6)
sphere_2.SetStartTheta(240.0)
sphere_2.SetEndTheta(360.0)
sphere_2.Update()
block_data_2 = sphere_2.GetOutput()
selected_cells_2 = vtkSignedCharArray()
selected_cells_2.SetName("MarkedCells")
selected_cells_2.SetNumberOfTuples(block_data_2.GetNumberOfCells())
selected_cells_2.FillComponent(0, 0)
selected_cells_2.SetComponent(20, 0, 1)
block_data_2.GetCellData().AddArray(selected_cells_2)
multi_block.SetBlock(2, block_data_2)

# Expand marked elements
expand_filter = vtkExpandMarkedElements()
expand_filter.SetInputDataObject(multi_block)
expand_filter.SetInputArrayToProcess(
    0, 0, 0, vtkDataObject.FIELD_ASSOCIATION_CELLS, "MarkedCells")
expand_filter.RemoveIntermediateLayersOn()
expand_filter.RemoveSeedOn()
expand_filter.SetNumberOfLayers(3)

# Composite mapper colored by MarkedCells
mapper = vtkCompositePolyDataMapper()
mapper.SetInputConnection(expand_filter.GetOutputPort())
mapper.SetScalarModeToUseCellFieldData()
mapper.SelectColorArray("MarkedCells")

actor = vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().EdgeVisibilityOn()

# Renderer
renderer = vtkRenderer()
renderer.AddActor(actor)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("expand marked elements")

# Scene
renderer.ResetCamera()

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
