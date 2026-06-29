#!/usr/bin/env python

# Demonstrate vtkExtractSelection with THRESHOLDS selection type
# on both cell and point data of a 3x3x3 image data cube.
# Shows select, inverse, preserve topology, and containing cells variants.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import (
    VTK_FLOAT,
    vtkDoubleArray,
    vtkFloatArray,
    vtkIdTypeArray,
)
from vtkmodules.vtkCommonDataModel import (
    vtkImageData,
    vtkSelection,
    vtkSelectionNode,
)
from vtkmodules.vtkFiltersExtraction import vtkExtractSelection
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkDataSetMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

XCELLS = 3
YCELLS = 3
ZCELLS = 3

# Create sample image data with known structure and arrays
sample_data = vtkImageData()
sample_data.SetSpacing(1.0, 1.0, 1.0)
sample_data.SetOrigin(0.0, 0.0, 0.0)
sample_data.SetDimensions(XCELLS + 1, YCELLS + 1, ZCELLS + 1)
sample_data.AllocateScalars(VTK_FLOAT, 1)

# Point arrays
point_counter_array = vtkIdTypeArray()
point_counter_array.SetNumberOfComponents(1)
point_counter_array.SetName("Point Counter")
sample_data.GetPointData().AddArray(point_counter_array)

point_forward_ids = vtkIdTypeArray()
point_forward_ids.SetNumberOfComponents(1)
point_forward_ids.SetName("Forward Point Ids")
sample_data.GetPointData().AddArray(point_forward_ids)

point_reverse_ids = vtkIdTypeArray()
point_reverse_ids.SetNumberOfComponents(1)
point_reverse_ids.SetName("Reverse Point Ids")
sample_data.GetPointData().AddArray(point_reverse_ids)

point_x_array = vtkFloatArray()
point_x_array.SetNumberOfComponents(1)
point_x_array.SetName("Point X")
sample_data.GetPointData().AddArray(point_x_array)

point_y_array = vtkFloatArray()
point_y_array.SetNumberOfComponents(1)
point_y_array.SetName("Point Y")
sample_data.GetPointData().AddArray(point_y_array)

point_z_array = vtkFloatArray()
point_z_array.SetNumberOfComponents(1)
point_z_array.SetName("Point Z")
sample_data.GetPointData().AddArray(point_z_array)

point_count = 0
for i in range(ZCELLS + 1):
    for j in range(YCELLS + 1):
        for k in range(XCELLS + 1):
            point_counter_array.InsertNextValue(point_count)
            id_f = point_count + 10
            id_r = (XCELLS + 1) * (YCELLS + 1) * (ZCELLS + 1) - 1 - point_count + 10
            point_forward_ids.InsertNextValue(id_f)
            point_reverse_ids.InsertNextValue(id_r)
            point_count += 1
            point_x_array.InsertNextValue(float(k))
            point_y_array.InsertNextValue(float(j))
            point_z_array.InsertNextValue(float(i))

# Cell arrays
cell_counter_array = vtkIdTypeArray()
cell_counter_array.SetNumberOfComponents(1)
cell_counter_array.SetName("Cell Count")
sample_data.GetCellData().AddArray(cell_counter_array)

cell_forward_ids = vtkIdTypeArray()
cell_forward_ids.SetNumberOfComponents(1)
cell_forward_ids.SetName("Forward Cell Ids")
sample_data.GetCellData().AddArray(cell_forward_ids)

cell_reverse_ids = vtkIdTypeArray()
cell_reverse_ids.SetNumberOfComponents(1)
cell_reverse_ids.SetName("Reverse Cell Ids")
sample_data.GetCellData().AddArray(cell_reverse_ids)

cell_x_array = vtkDoubleArray()
cell_x_array.SetNumberOfComponents(1)
cell_x_array.SetName("Cell X")
sample_data.GetCellData().AddArray(cell_x_array)

cell_y_array = vtkDoubleArray()
cell_y_array.SetNumberOfComponents(1)
cell_y_array.SetName("Cell Y")
sample_data.GetCellData().AddArray(cell_y_array)

cell_z_array = vtkDoubleArray()
cell_z_array.SetNumberOfComponents(1)
cell_z_array.SetName("Cell Z")
sample_data.GetCellData().AddArray(cell_z_array)

cell_count = 0
for i in range(ZCELLS):
    for j in range(YCELLS):
        for k in range(XCELLS):
            cell_counter_array.InsertNextValue(cell_count)
            id_f = cell_count + 10
            id_r = XCELLS * YCELLS * ZCELLS - 1 - cell_count + 10
            cell_forward_ids.InsertNextValue(id_f)
            cell_reverse_ids.InsertNextValue(id_r)
            cell_count += 1
            cell_x_array.InsertNextValue(k + 0.5)
            cell_y_array.InsertNextValue(j + 0.5)
            cell_z_array.InsertNextValue(i + 0.5)

sample_data.GetPointData().SetGlobalIds(point_forward_ids)
sample_data.GetPointData().SetScalars(point_x_array)
sample_data.GetCellData().SetGlobalIds(cell_forward_ids)
sample_data.GetCellData().SetScalars(cell_x_array)

# Selection pipeline
selection = vtkSelection()
selection_node = vtkSelectionNode()
selection.AddNode(selection_node)

extract_selection = vtkExtractSelection()
extract_selection.SetInputData(0, sample_data)
extract_selection.SetInputData(1, selection)
extract_selection.PreserveTopologyOff()

# --- THRESHOLDS on cells: select ---
selection_node.Initialize()
selection_node.GetProperties().Set(vtkSelectionNode.CONTENT_TYPE(), vtkSelectionNode.THRESHOLDS)
selection_node.SetFieldType(vtkSelectionNode.CELL)
cell_thresh = vtkDoubleArray()
cell_thresh.SetNumberOfComponents(2)
cell_thresh.SetNumberOfTuples(1)
cell_thresh.SetComponent(0, 0, 1.9)
cell_thresh.SetComponent(0, 1, 3.1)
selection_node.SetSelectionList(cell_thresh)

extract_selection.Update()
cell_select_copy = extract_selection.GetOutput().NewInstance()
cell_select_copy.DeepCopy(extract_selection.GetOutput())

# --- THRESHOLDS on cells: inverse ---
selection_node.GetProperties().Set(vtkSelectionNode.INVERSE(), 1)
extract_selection.Update()
cell_inverse_copy = extract_selection.GetOutput().NewInstance()
cell_inverse_copy.DeepCopy(extract_selection.GetOutput())

# --- THRESHOLDS on cells: preserve topology ---
selection_node.GetProperties().Set(vtkSelectionNode.INVERSE(), 0)
extract_selection.PreserveTopologyOn()
extract_selection.Update()
cell_topo_insidedness = extract_selection.GetOutput().GetCellData().GetArray("vtkInsidedness")
cell_topo_copy = extract_selection.GetOutput().NewInstance()
cell_topo_copy.DeepCopy(extract_selection.GetOutput())

# --- THRESHOLDS on points: select ---
selection_node.Initialize()
extract_selection.PreserveTopologyOff()
selection_node.GetProperties().Set(vtkSelectionNode.CONTENT_TYPE(), vtkSelectionNode.THRESHOLDS)
selection_node.GetProperties().Set(vtkSelectionNode.FIELD_TYPE(), vtkSelectionNode.POINT)
point_thresh = vtkDoubleArray()
point_thresh.SetNumberOfComponents(2)
point_thresh.SetNumberOfTuples(1)
point_thresh.SetComponent(0, 0, 0.9)
point_thresh.SetComponent(0, 1, 1.1)
selection_node.SetSelectionList(point_thresh)

extract_selection.Update()
point_select_copy = extract_selection.GetOutput().NewInstance()
point_select_copy.DeepCopy(extract_selection.GetOutput())

# --- THRESHOLDS on points: inverse ---
selection_node.GetProperties().Set(vtkSelectionNode.INVERSE(), 1)
extract_selection.Update()
point_inverse_copy = extract_selection.GetOutput().NewInstance()
point_inverse_copy.DeepCopy(extract_selection.GetOutput())

# --- THRESHOLDS on points: containing cells ---
selection_node.GetProperties().Set(vtkSelectionNode.INVERSE(), 0)
selection_node.GetProperties().Set(vtkSelectionNode.CONTAINING_CELLS(), 1)
extract_selection.Update()
point_containing_copy = extract_selection.GetOutput().NewInstance()
point_containing_copy.DeepCopy(extract_selection.GetOutput())

# --- THRESHOLDS on points: preserve topology ---
selection_node.GetProperties().Set(vtkSelectionNode.CONTAINING_CELLS(), 0)
extract_selection.PreserveTopologyOn()
extract_selection.Update()
point_topo_insidedness = extract_selection.GetOutput().GetPointData().GetArray("vtkInsidedness")
point_topo_copy = extract_selection.GetOutput().NewInstance()
point_topo_copy.DeepCopy(extract_selection.GetOutput())

# --- THRESHOLDS on points: preserve topology + containing cells ---
selection_node.GetProperties().Set(vtkSelectionNode.CONTAINING_CELLS(), 1)
extract_selection.Update()
point_topo_contain_insidedness = extract_selection.GetOutput().GetCellData().GetArray("vtkInsidedness")
point_topo_contain_copy = extract_selection.GetOutput().NewInstance()
point_topo_contain_copy.DeepCopy(extract_selection.GetOutput())

# Mapper — cell select
cell_select_mapper = vtkDataSetMapper()
cell_select_mapper.SetInputData(cell_select_copy)
cell_select_copy.GetCellData().SetActiveScalars(cell_x_array.GetName())
cell_select_mapper.SetScalarModeToUseCellData()
cell_select_mapper.SetScalarRange(cell_x_array.GetRange())

# Mapper — cell inverse
cell_inverse_mapper = vtkDataSetMapper()
cell_inverse_mapper.SetInputData(cell_inverse_copy)
cell_inverse_copy.GetCellData().SetActiveScalars(cell_x_array.GetName())
cell_inverse_mapper.SetScalarModeToUseCellData()
cell_inverse_mapper.SetScalarRange(cell_x_array.GetRange())

# Mapper — cell topology
cell_topo_mapper = vtkDataSetMapper()
cell_topo_mapper.SetInputData(cell_topo_copy)
cell_topo_copy.GetCellData().SetActiveScalars("vtkInsidedness")
cell_topo_mapper.SetScalarModeToUseCellData()
cell_topo_mapper.SetScalarRange(cell_topo_insidedness.GetRange())

# Mapper — point select
point_select_mapper = vtkDataSetMapper()
point_select_mapper.SetInputData(point_select_copy)
point_select_copy.GetPointData().SetActiveScalars(point_x_array.GetName())
point_select_mapper.SetScalarModeToUsePointData()
point_select_mapper.SetScalarRange(point_x_array.GetRange())

# Mapper — point inverse
point_inverse_mapper = vtkDataSetMapper()
point_inverse_mapper.SetInputData(point_inverse_copy)
point_inverse_copy.GetPointData().SetActiveScalars(point_x_array.GetName())
point_inverse_mapper.SetScalarModeToUsePointData()
point_inverse_mapper.SetScalarRange(point_x_array.GetRange())

# Mapper — point containing cells
point_containing_mapper = vtkDataSetMapper()
point_containing_mapper.SetInputData(point_containing_copy)
point_containing_copy.GetPointData().SetActiveScalars(point_x_array.GetName())
point_containing_mapper.SetScalarModeToUsePointData()
point_containing_mapper.SetScalarRange(point_x_array.GetRange())

# Mapper — point topology
point_topo_mapper = vtkDataSetMapper()
point_topo_mapper.SetInputData(point_topo_copy)
point_topo_copy.GetPointData().SetActiveScalars("vtkInsidedness")
point_topo_mapper.SetScalarModeToUsePointData()
point_topo_mapper.SetScalarRange(point_topo_insidedness.GetRange())

# Mapper — point topology + containing
point_topo_contain_mapper = vtkDataSetMapper()
point_topo_contain_mapper.SetInputData(point_topo_contain_copy)
point_topo_contain_copy.GetCellData().SetActiveScalars("vtkInsidedness")
point_topo_contain_mapper.SetScalarModeToUseCellData()
point_topo_contain_mapper.SetScalarRange(point_topo_contain_insidedness.GetRange())

# Actor — cell select
cell_select_actor = vtkActor()
cell_select_actor.SetPosition(0, 0, 0)
cell_select_actor.SetMapper(cell_select_mapper)
cell_select_actor.GetProperty().SetPointSize(6.0)

# Actor — cell inverse
cell_inverse_actor = vtkActor()
cell_inverse_actor.SetPosition(4, 0, 0)
cell_inverse_actor.SetMapper(cell_inverse_mapper)
cell_inverse_actor.GetProperty().SetPointSize(6.0)

# Actor — cell topology
cell_topo_actor = vtkActor()
cell_topo_actor.SetPosition(8, 0, 0)
cell_topo_actor.SetMapper(cell_topo_mapper)
cell_topo_actor.GetProperty().SetPointSize(6.0)

# Actor — point select
point_select_actor = vtkActor()
point_select_actor.SetPosition(12, 0, 0)
point_select_actor.SetMapper(point_select_mapper)
point_select_actor.GetProperty().SetPointSize(6.0)

# Actor — point inverse
point_inverse_actor = vtkActor()
point_inverse_actor.SetPosition(16, 0, 0)
point_inverse_actor.SetMapper(point_inverse_mapper)
point_inverse_actor.GetProperty().SetPointSize(6.0)

# Actor — point containing cells
point_containing_actor = vtkActor()
point_containing_actor.SetPosition(20, 0, 0)
point_containing_actor.SetMapper(point_containing_mapper)
point_containing_actor.GetProperty().SetPointSize(6.0)

# Actor — point topology
point_topo_actor = vtkActor()
point_topo_actor.SetPosition(24, 0, 0)
point_topo_actor.SetMapper(point_topo_mapper)
point_topo_actor.GetProperty().SetPointSize(6.0)

# Actor — point topology + containing
point_topo_contain_actor = vtkActor()
point_topo_contain_actor.SetPosition(28, 0, 0)
point_topo_contain_actor.SetMapper(point_topo_contain_mapper)
point_topo_contain_actor.GetProperty().SetPointSize(6.0)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(cell_select_actor)
renderer.AddActor(cell_inverse_actor)
renderer.AddActor(cell_topo_actor)
renderer.AddActor(point_select_actor)
renderer.AddActor(point_inverse_actor)
renderer.AddActor(point_containing_actor)
renderer.AddActor(point_topo_actor)
renderer.AddActor(point_topo_contain_actor)

# Window
render_window = vtkRenderWindow()
render_window.SetMultiSamples(0)
render_window.SetSize(600, 300)
render_window.AddRenderer(renderer)
render_window.SetWindowName("extraction thresholds")

# Scene
renderer.ResetCamera()

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
