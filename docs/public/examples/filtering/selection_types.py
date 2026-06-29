#!/usr/bin/env python

# Demonstrate vtkExtractSelection with multiple selection types
# (GLOBALIDS, INDICES, VALUES, THRESHOLDS, LOCATIONS, FRUSTUM)
# on both cell and point data of a 3x3x3 image data cube, arranged
# in a grid layout.

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

# Renderer
renderer = vtkRenderer()

# Selection pipeline
selection = vtkSelection()
selection_node = vtkSelectionNode()
selection.AddNode(selection_node)

extract_selection = vtkExtractSelection()
extract_selection.SetInputData(0, sample_data)
extract_selection.SetInputData(1, selection)
extract_selection.PreserveTopologyOff()

COLORBYCELL = 0
COLORBYPOINT = 1

def show_me(result, x, y, cell_or_point, array):
    copy = result.NewInstance()
    copy.DeepCopy(result)
    mapper = vtkDataSetMapper()
    mapper.SetInputData(copy)
    r = array.GetRange()
    if cell_or_point == COLORBYCELL:
        copy.GetCellData().SetActiveScalars(array.GetName())
        mapper.SetScalarModeToUseCellData()
    else:
        copy.GetPointData().SetActiveScalars(array.GetName())
        mapper.SetScalarModeToUsePointData()
    mapper.SetScalarRange(r[0], r[1])
    actor = vtkActor()
    actor.SetPosition(x * 4, y * 4, 0)
    actor.SetMapper(mapper)
    actor.GetProperty().SetPointSize(6.0)
    renderer.AddActor(actor)

# --- GLOBALIDS on cells ---
selection_node.Initialize()
selection_node.GetProperties().Set(vtkSelectionNode.CONTENT_TYPE(), vtkSelectionNode.GLOBALIDS)
selection_node.SetFieldType(vtkSelectionNode.CELL)
cell_ids = vtkIdTypeArray()
cell_ids.SetNumberOfComponents(1)
cell_ids.SetNumberOfTuples(5)
cell_ids.SetTuple1(0, 9)
cell_ids.SetTuple1(1, 10)
cell_ids.SetTuple1(2, 11)
cell_ids.SetTuple1(3, 36)
cell_ids.SetTuple1(4, 37)
selection_node.SetSelectionList(cell_ids)

extract_selection.Update()
show_me(extract_selection.GetOutput(), 0, 0, COLORBYCELL, cell_forward_ids)

selection_node.GetProperties().Set(vtkSelectionNode.INVERSE(), 1)
extract_selection.Update()
show_me(extract_selection.GetOutput(), 1, 0, COLORBYCELL, cell_forward_ids)

selection_node.GetProperties().Set(vtkSelectionNode.INVERSE(), 0)
extract_selection.PreserveTopologyOn()
extract_selection.Update()
inside_arr = extract_selection.GetOutput().GetCellData().GetArray("vtkInsidedness")
show_me(extract_selection.GetOutput(), 2, 0, COLORBYCELL, inside_arr)

# --- GLOBALIDS on points ---
selection_node.Initialize()
extract_selection.PreserveTopologyOff()
selection_node.GetProperties().Set(vtkSelectionNode.CONTENT_TYPE(), vtkSelectionNode.GLOBALIDS)
selection_node.GetProperties().Set(vtkSelectionNode.FIELD_TYPE(), vtkSelectionNode.POINT)
point_ids = vtkIdTypeArray()
point_ids.SetNumberOfComponents(1)
point_ids.SetNumberOfTuples(5)
point_ids.SetTuple1(0, 9)
point_ids.SetTuple1(1, 10)
point_ids.SetTuple1(2, 11)
point_ids.SetTuple1(3, 73)
point_ids.SetTuple1(4, 74)
selection_node.SetSelectionList(point_ids)

extract_selection.Update()
show_me(extract_selection.GetOutput(), 3, 0, COLORBYPOINT, point_forward_ids)

selection_node.GetProperties().Set(vtkSelectionNode.INVERSE(), 1)
extract_selection.Update()
show_me(extract_selection.GetOutput(), 4, 0, COLORBYPOINT, point_forward_ids)

selection_node.GetProperties().Set(vtkSelectionNode.INVERSE(), 0)
selection_node.GetProperties().Set(vtkSelectionNode.CONTAINING_CELLS(), 1)
extract_selection.Update()
show_me(extract_selection.GetOutput(), 5, 0, COLORBYPOINT, point_forward_ids)

selection_node.GetProperties().Set(vtkSelectionNode.CONTAINING_CELLS(), 0)
extract_selection.PreserveTopologyOn()
extract_selection.Update()
inside_arr = extract_selection.GetOutput().GetPointData().GetArray("vtkInsidedness")
show_me(extract_selection.GetOutput(), 6, 0, COLORBYPOINT, inside_arr)

selection_node.GetProperties().Set(vtkSelectionNode.CONTAINING_CELLS(), 1)
extract_selection.Update()
inside_arr = extract_selection.GetOutput().GetCellData().GetArray("vtkInsidedness")
show_me(extract_selection.GetOutput(), 7, 0, COLORBYCELL, inside_arr)

# --- INDICES on cells ---
selection_node.Initialize()
extract_selection.PreserveTopologyOff()
selection_node.GetProperties().Set(vtkSelectionNode.CONTENT_TYPE(), vtkSelectionNode.INDICES)
selection_node.SetFieldType(vtkSelectionNode.CELL)
cell_ids = vtkIdTypeArray()
cell_ids.SetNumberOfComponents(1)
cell_ids.SetNumberOfTuples(5)
cell_ids.SetTuple1(0, 0)
cell_ids.SetTuple1(1, 1)
cell_ids.SetTuple1(2, 2)
cell_ids.SetTuple1(3, 26)
cell_ids.SetTuple1(4, 27)
selection_node.SetSelectionList(cell_ids)

extract_selection.Update()
show_me(extract_selection.GetOutput(), 0, 1, COLORBYCELL, cell_counter_array)

selection_node.GetProperties().Set(vtkSelectionNode.INVERSE(), 1)
extract_selection.Update()
show_me(extract_selection.GetOutput(), 1, 1, COLORBYCELL, cell_counter_array)

selection_node.GetProperties().Set(vtkSelectionNode.INVERSE(), 0)
extract_selection.PreserveTopologyOn()
extract_selection.Update()
inside_arr = extract_selection.GetOutput().GetCellData().GetArray("vtkInsidedness")
show_me(extract_selection.GetOutput(), 2, 1, COLORBYCELL, inside_arr)

# --- INDICES on points ---
selection_node.Initialize()
extract_selection.PreserveTopologyOff()
selection_node.GetProperties().Set(vtkSelectionNode.CONTENT_TYPE(), vtkSelectionNode.INDICES)
selection_node.GetProperties().Set(vtkSelectionNode.FIELD_TYPE(), vtkSelectionNode.POINT)
point_ids = vtkIdTypeArray()
point_ids.SetNumberOfComponents(1)
point_ids.SetNumberOfTuples(5)
point_ids.SetTuple1(0, 0)
point_ids.SetTuple1(1, 1)
point_ids.SetTuple1(2, 2)
point_ids.SetTuple1(3, 63)
point_ids.SetTuple1(4, 64)
selection_node.SetSelectionList(point_ids)

extract_selection.Update()
show_me(extract_selection.GetOutput(), 3, 1, COLORBYPOINT, point_counter_array)

selection_node.GetProperties().Set(vtkSelectionNode.INVERSE(), 1)
extract_selection.Update()
show_me(extract_selection.GetOutput(), 4, 1, COLORBYPOINT, point_counter_array)

selection_node.GetProperties().Set(vtkSelectionNode.INVERSE(), 0)
selection_node.GetProperties().Set(vtkSelectionNode.CONTAINING_CELLS(), 1)
extract_selection.Update()
show_me(extract_selection.GetOutput(), 5, 1, COLORBYPOINT, point_counter_array)

selection_node.GetProperties().Set(vtkSelectionNode.INVERSE(), 0)
selection_node.GetProperties().Set(vtkSelectionNode.CONTAINING_CELLS(), 0)
extract_selection.PreserveTopologyOn()
extract_selection.Update()
inside_arr = extract_selection.GetOutput().GetPointData().GetArray("vtkInsidedness")
show_me(extract_selection.GetOutput(), 6, 1, COLORBYPOINT, inside_arr)

selection_node.GetProperties().Set(vtkSelectionNode.CONTAINING_CELLS(), 1)
extract_selection.Update()
inside_arr = extract_selection.GetOutput().GetCellData().GetArray("vtkInsidedness")
show_me(extract_selection.GetOutput(), 7, 1, COLORBYCELL, inside_arr)

# --- VALUES on cells ---
selection_node.Initialize()
extract_selection.PreserveTopologyOff()
selection_node.GetProperties().Set(vtkSelectionNode.CONTENT_TYPE(), vtkSelectionNode.VALUES)
selection_node.SetFieldType(vtkSelectionNode.CELL)
cell_ids = vtkIdTypeArray()
cell_ids.SetName("Reverse Cell Ids")
cell_ids.SetNumberOfComponents(1)
cell_ids.SetNumberOfTuples(5)
cell_ids.SetTuple1(0, 9)
cell_ids.SetTuple1(1, 10)
cell_ids.SetTuple1(2, 11)
cell_ids.SetTuple1(3, 36)
cell_ids.SetTuple1(4, 37)
selection_node.SetSelectionList(cell_ids)

extract_selection.Update()
show_me(extract_selection.GetOutput(), 0, 2, COLORBYCELL, cell_reverse_ids)

selection_node.GetProperties().Set(vtkSelectionNode.INVERSE(), 1)
extract_selection.Update()
show_me(extract_selection.GetOutput(), 1, 2, COLORBYCELL, cell_reverse_ids)

selection_node.GetProperties().Set(vtkSelectionNode.INVERSE(), 0)
extract_selection.PreserveTopologyOn()
extract_selection.Update()
inside_arr = extract_selection.GetOutput().GetCellData().GetArray("vtkInsidedness")
show_me(extract_selection.GetOutput(), 2, 2, COLORBYCELL, inside_arr)

# --- VALUES on points ---
selection_node.Initialize()
extract_selection.PreserveTopologyOff()
selection_node.GetProperties().Set(vtkSelectionNode.CONTENT_TYPE(), vtkSelectionNode.VALUES)
selection_node.GetProperties().Set(vtkSelectionNode.FIELD_TYPE(), vtkSelectionNode.POINT)
point_ids = vtkIdTypeArray()
point_ids.SetName("Reverse Point Ids")
point_ids.SetNumberOfComponents(1)
point_ids.SetNumberOfTuples(5)
point_ids.SetTuple1(0, 9)
point_ids.SetTuple1(1, 10)
point_ids.SetTuple1(2, 11)
point_ids.SetTuple1(3, 73)
point_ids.SetTuple1(4, 74)
selection_node.SetSelectionList(point_ids)

extract_selection.Update()
show_me(extract_selection.GetOutput(), 3, 2, COLORBYPOINT, point_reverse_ids)

selection_node.GetProperties().Set(vtkSelectionNode.INVERSE(), 1)
extract_selection.Update()
show_me(extract_selection.GetOutput(), 4, 2, COLORBYPOINT, point_reverse_ids)

selection_node.GetProperties().Set(vtkSelectionNode.INVERSE(), 0)
selection_node.GetProperties().Set(vtkSelectionNode.CONTAINING_CELLS(), 1)
extract_selection.Update()
show_me(extract_selection.GetOutput(), 5, 2, COLORBYPOINT, point_reverse_ids)

selection_node.GetProperties().Set(vtkSelectionNode.INVERSE(), 0)
selection_node.GetProperties().Set(vtkSelectionNode.CONTAINING_CELLS(), 0)
extract_selection.PreserveTopologyOn()
extract_selection.Update()
inside_arr = extract_selection.GetOutput().GetPointData().GetArray("vtkInsidedness")
show_me(extract_selection.GetOutput(), 6, 2, COLORBYPOINT, inside_arr)

selection_node.GetProperties().Set(vtkSelectionNode.CONTAINING_CELLS(), 1)
extract_selection.Update()
inside_arr = extract_selection.GetOutput().GetCellData().GetArray("vtkInsidedness")
show_me(extract_selection.GetOutput(), 7, 2, COLORBYCELL, inside_arr)

# --- THRESHOLDS on cells ---
selection_node.Initialize()
extract_selection.PreserveTopologyOff()
selection_node.GetProperties().Set(vtkSelectionNode.CONTENT_TYPE(), vtkSelectionNode.THRESHOLDS)
selection_node.SetFieldType(vtkSelectionNode.CELL)
cell_thresh = vtkDoubleArray()
cell_thresh.SetNumberOfComponents(2)
cell_thresh.SetNumberOfTuples(1)
cell_thresh.SetComponent(0, 0, 1.9)
cell_thresh.SetComponent(0, 1, 3.1)
selection_node.SetSelectionList(cell_thresh)

extract_selection.Update()
show_me(extract_selection.GetOutput(), 0, 3, COLORBYCELL, cell_x_array)

selection_node.GetProperties().Set(vtkSelectionNode.INVERSE(), 1)
extract_selection.Update()
show_me(extract_selection.GetOutput(), 1, 3, COLORBYCELL, cell_x_array)

selection_node.GetProperties().Set(vtkSelectionNode.INVERSE(), 0)
extract_selection.PreserveTopologyOn()
extract_selection.Update()
inside_arr = extract_selection.GetOutput().GetCellData().GetArray("vtkInsidedness")
show_me(extract_selection.GetOutput(), 2, 3, COLORBYCELL, inside_arr)

# --- THRESHOLDS on points ---
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
show_me(extract_selection.GetOutput(), 3, 3, COLORBYPOINT, point_x_array)

selection_node.GetProperties().Set(vtkSelectionNode.INVERSE(), 1)
extract_selection.Update()
show_me(extract_selection.GetOutput(), 4, 3, COLORBYPOINT, point_x_array)

selection_node.GetProperties().Set(vtkSelectionNode.INVERSE(), 0)
selection_node.GetProperties().Set(vtkSelectionNode.CONTAINING_CELLS(), 1)
extract_selection.Update()
show_me(extract_selection.GetOutput(), 5, 3, COLORBYPOINT, point_x_array)

selection_node.GetProperties().Set(vtkSelectionNode.CONTAINING_CELLS(), 0)
extract_selection.PreserveTopologyOn()
extract_selection.Update()
inside_arr = extract_selection.GetOutput().GetPointData().GetArray("vtkInsidedness")
show_me(extract_selection.GetOutput(), 6, 3, COLORBYPOINT, inside_arr)

selection_node.GetProperties().Set(vtkSelectionNode.CONTAINING_CELLS(), 1)
extract_selection.Update()
inside_arr = extract_selection.GetOutput().GetCellData().GetArray("vtkInsidedness")
show_me(extract_selection.GetOutput(), 7, 3, COLORBYCELL, inside_arr)

# --- LOCATIONS on cells ---
selection_node.Initialize()
extract_selection.PreserveTopologyOff()
selection_node.GetProperties().Set(vtkSelectionNode.CONTENT_TYPE(), vtkSelectionNode.LOCATIONS)
selection_node.SetFieldType(vtkSelectionNode.CELL)
cell_locs = vtkDoubleArray()
cell_locs.SetNumberOfComponents(3)
cell_locs.SetNumberOfTuples(4)
cell_locs.SetTuple3(0, 0.0, 0.99, 0.5)
cell_locs.SetTuple3(1, 2.5, 1.5, 0.5)
cell_locs.SetTuple3(2, 2.5, 2.1, 2.9)
cell_locs.SetTuple3(3, 5.0, 5.0, 5.0)
selection_node.SetSelectionList(cell_locs)

extract_selection.Update()
show_me(extract_selection.GetOutput(), 0, 4, COLORBYCELL, cell_counter_array)

selection_node.GetProperties().Set(vtkSelectionNode.INVERSE(), 1)
extract_selection.Update()
show_me(extract_selection.GetOutput(), 1, 4, COLORBYCELL, cell_counter_array)

selection_node.GetProperties().Set(vtkSelectionNode.INVERSE(), 0)
extract_selection.PreserveTopologyOn()
extract_selection.Update()
inside_arr = extract_selection.GetOutput().GetCellData().GetArray("vtkInsidedness")
show_me(extract_selection.GetOutput(), 2, 4, COLORBYCELL, inside_arr)

# --- LOCATIONS on points ---
selection_node.Initialize()
extract_selection.PreserveTopologyOff()
selection_node.GetProperties().Set(vtkSelectionNode.CONTENT_TYPE(), vtkSelectionNode.LOCATIONS)
selection_node.GetProperties().Set(vtkSelectionNode.FIELD_TYPE(), vtkSelectionNode.POINT)
selection_node.GetProperties().Set(vtkSelectionNode.EPSILON(), 0.3)
point_locs = vtkDoubleArray()
point_locs.SetNumberOfComponents(3)
point_locs.SetNumberOfTuples(3)
point_locs.SetTuple3(0, 0.0, 0.0, 0.29)
point_locs.SetTuple3(1, 1.0, 0.0, 0.31)
point_locs.SetTuple3(2, 1.0, 1.0, 3.1)
selection_node.SetSelectionList(point_locs)

extract_selection.Update()
show_me(extract_selection.GetOutput(), 3, 4, COLORBYPOINT, point_counter_array)

selection_node.GetProperties().Set(vtkSelectionNode.INVERSE(), 1)
extract_selection.Update()
show_me(extract_selection.GetOutput(), 4, 4, COLORBYPOINT, point_counter_array)

selection_node.GetProperties().Set(vtkSelectionNode.INVERSE(), 0)
selection_node.GetProperties().Set(vtkSelectionNode.CONTAINING_CELLS(), 1)
extract_selection.Update()
show_me(extract_selection.GetOutput(), 5, 4, COLORBYPOINT, point_counter_array)

selection_node.GetProperties().Set(vtkSelectionNode.INVERSE(), 0)
selection_node.GetProperties().Set(vtkSelectionNode.CONTAINING_CELLS(), 0)
extract_selection.PreserveTopologyOn()
extract_selection.Update()
inside_arr = extract_selection.GetOutput().GetPointData().GetArray("vtkInsidedness")
show_me(extract_selection.GetOutput(), 6, 4, COLORBYPOINT, inside_arr)

selection_node.GetProperties().Set(vtkSelectionNode.CONTAINING_CELLS(), 1)
extract_selection.Update()
inside_arr = extract_selection.GetOutput().GetCellData().GetArray("vtkInsidedness")
show_me(extract_selection.GetOutput(), 7, 4, COLORBYCELL, inside_arr)

# --- FRUSTUM on cells ---
selection_node.Initialize()
extract_selection.PreserveTopologyOff()
selection_node.GetProperties().Set(vtkSelectionNode.CONTENT_TYPE(), vtkSelectionNode.FRUSTUM)
selection_node.SetFieldType(vtkSelectionNode.CELL)
frust_corners = vtkDoubleArray()
frust_corners.SetNumberOfComponents(4)
frust_corners.SetNumberOfTuples(8)
frust_corners.SetTuple4(0, 0.1, 0.1, 3.1, 0.0)
frust_corners.SetTuple4(1, 0.1, 0.1, 0.1, 0.0)
frust_corners.SetTuple4(2, 0.1, 0.9, 3.1, 0.0)
frust_corners.SetTuple4(3, 0.1, 0.9, 0.1, 0.0)
frust_corners.SetTuple4(4, 0.9, 0.1, 3.1, 0.0)
frust_corners.SetTuple4(5, 0.9, 0.1, 0.1, 0.0)
frust_corners.SetTuple4(6, 0.9, 0.9, 3.1, 0.0)
frust_corners.SetTuple4(7, 0.9, 0.9, 0.1, 0.0)
selection_node.SetSelectionList(frust_corners)

extract_selection.Update()
show_me(extract_selection.GetOutput(), 0, 5, COLORBYCELL, cell_counter_array)

selection_node.GetProperties().Set(vtkSelectionNode.INVERSE(), 1)
extract_selection.Update()
show_me(extract_selection.GetOutput(), 1, 5, COLORBYCELL, cell_counter_array)

selection_node.GetProperties().Set(vtkSelectionNode.INVERSE(), 0)
extract_selection.PreserveTopologyOn()
extract_selection.Update()
inside_arr = extract_selection.GetOutput().GetCellData().GetArray("vtkInsidedness")
show_me(extract_selection.GetOutput(), 2, 5, COLORBYCELL, inside_arr)

# --- FRUSTUM on points ---
selection_node.Initialize()
extract_selection.PreserveTopologyOff()
selection_node.GetProperties().Set(vtkSelectionNode.CONTENT_TYPE(), vtkSelectionNode.FRUSTUM)
selection_node.GetProperties().Set(vtkSelectionNode.FIELD_TYPE(), vtkSelectionNode.POINT)
frust_corners = vtkDoubleArray()
frust_corners.SetNumberOfComponents(4)
frust_corners.SetNumberOfTuples(8)
frust_corners.SetTuple4(0, -0.1, -0.1, 3.1, 0.0)
frust_corners.SetTuple4(1, -0.1, -0.1, -0.1, 0.0)
frust_corners.SetTuple4(2, -0.1, 0.1, 3.1, 0.0)
frust_corners.SetTuple4(3, -0.1, 0.1, -0.1, 0.0)
frust_corners.SetTuple4(4, 0.1, -0.1, 3.1, 0.0)
frust_corners.SetTuple4(5, 0.1, -0.1, -0.1, 0.0)
frust_corners.SetTuple4(6, 0.1, 0.1, 3.1, 0.0)
frust_corners.SetTuple4(7, 0.1, 0.1, -0.1, 0.0)
selection_node.SetSelectionList(frust_corners)

extract_selection.Update()
show_me(extract_selection.GetOutput(), 3, 5, COLORBYPOINT, point_counter_array)

selection_node.GetProperties().Set(vtkSelectionNode.INVERSE(), 1)
extract_selection.Update()
show_me(extract_selection.GetOutput(), 4, 5, COLORBYPOINT, point_counter_array)

selection_node.GetProperties().Set(vtkSelectionNode.INVERSE(), 0)
selection_node.GetProperties().Set(vtkSelectionNode.CONTAINING_CELLS(), 1)
extract_selection.Update()
show_me(extract_selection.GetOutput(), 5, 5, COLORBYPOINT, point_counter_array)

selection_node.GetProperties().Set(vtkSelectionNode.INVERSE(), 0)
selection_node.GetProperties().Set(vtkSelectionNode.CONTAINING_CELLS(), 0)
extract_selection.PreserveTopologyOn()
extract_selection.Update()
inside_arr = extract_selection.GetOutput().GetPointData().GetArray("vtkInsidedness")
show_me(extract_selection.GetOutput(), 6, 5, COLORBYPOINT, inside_arr)

selection_node.GetProperties().Set(vtkSelectionNode.CONTAINING_CELLS(), 1)
extract_selection.Update()
inside_arr = extract_selection.GetOutput().GetCellData().GetArray("vtkInsidedness")
show_me(extract_selection.GetOutput(), 7, 5, COLORBYCELL, inside_arr)

# Window
render_window = vtkRenderWindow()
render_window.SetMultiSamples(0)
render_window.SetSize(600, 600)
render_window.AddRenderer(renderer)
render_window.SetWindowName("selection types")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.ResetCamera()

interactor.Initialize()
interactor.Start()
