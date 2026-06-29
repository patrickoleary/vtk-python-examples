#!/usr/bin/env python

# Demonstrate vtkExtractSelection with multiple selection nodes using
# frustum, indices, locations, and threshold selections combined on
# a 15x15x15 image data cube.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import (
    VTK_DOUBLE,
    vtkDoubleArray,
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

XCELLS = 15
YCELLS = 15
ZCELLS = 15

# Create sample image data
sample_data = vtkImageData()
sample_data.SetSpacing(1.0, 1.0, 1.0)
sample_data.SetOrigin(0.0, 0.0, 0.0)
sample_data.SetDimensions(XCELLS + 1, YCELLS + 1, ZCELLS + 1)
sample_data.AllocateScalars(VTK_DOUBLE, 1)

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

point_x_array = vtkDoubleArray()
point_x_array.SetNumberOfComponents(1)
point_x_array.SetName("Point X")
sample_data.GetPointData().AddArray(point_x_array)

point_y_array = vtkDoubleArray()
point_y_array.SetNumberOfComponents(1)
point_y_array.SetName("Point Y")
sample_data.GetPointData().AddArray(point_y_array)

point_z_array = vtkDoubleArray()
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

# Build multi-node selection
selection = vtkSelection()

# Node 1: frustum selection on cells
sel_1 = vtkSelectionNode()
sel_1.SetContentType(vtkSelectionNode.FRUSTUM)
sel_1.SetFieldType(vtkSelectionNode.CELL)
frust_corners = vtkDoubleArray()
frust_corners.SetNumberOfComponents(4)
frust_corners.SetNumberOfTuples(8)
frust_corners.SetTuple4(0, 0.1, 2.5, 9.5, 0.0)
frust_corners.SetTuple4(1, 0.1, 2.5, 2.5, 0.0)
frust_corners.SetTuple4(2, 0.1, 9.5, 9.5, 0.0)
frust_corners.SetTuple4(3, 0.1, 9.5, 2.5, 0.0)
frust_corners.SetTuple4(4, 8.2, 3.2, 4.3, 0.0)
frust_corners.SetTuple4(5, 8.2, 3.2, 3.2, 0.0)
frust_corners.SetTuple4(6, 8.2, 4.3, 4.3, 0.0)
frust_corners.SetTuple4(7, 8.2, 4.3, 3.2, 0.0)
sel_1.SetSelectionList(frust_corners)
selection.AddNode(sel_1)

# Node 2: second frustum selection on cells
sel_2 = vtkSelectionNode()
sel_2.SetContentType(vtkSelectionNode.FRUSTUM)
sel_2.SetFieldType(vtkSelectionNode.CELL)
frust_corners_2 = vtkDoubleArray()
frust_corners_2.SetNumberOfComponents(4)
frust_corners_2.SetNumberOfTuples(8)
frust_corners_2.SetTuple4(0, 0.1, 3.7, 3.1, 0.0)
frust_corners_2.SetTuple4(1, 0.1, 3.7, 0.1, 0.0)
frust_corners_2.SetTuple4(2, 7.3, 8.9, 3.1, 0.0)
frust_corners_2.SetTuple4(3, 7.3, 8.9, 0.1, 0.0)
frust_corners_2.SetTuple4(4, 2.5, 3.7, 3.1, 0.0)
frust_corners_2.SetTuple4(5, 2.5, 3.7, 0.1, 0.0)
frust_corners_2.SetTuple4(6, 9.4, 8.9, 3.1, 0.0)
frust_corners_2.SetTuple4(7, 9.4, 8.9, 0.1, 0.0)
sel_2.SetSelectionList(frust_corners_2)
selection.AddNode(sel_2)

# Node 3: index-based selection on cells
sel_3 = vtkSelectionNode()
sel_3.SetContentType(vtkSelectionNode.INDICES)
sel_3.SetFieldType(vtkSelectionNode.CELL)
ids = vtkIdTypeArray()
ids.SetNumberOfTuples(20)
for i in range(20):
    ids.SetValue(i, i)
sel_3.SetSelectionList(ids)
selection.AddNode(sel_3)

# Node 4: location-based selection on cells
sel_4 = vtkSelectionNode()
sel_4.SetContentType(vtkSelectionNode.LOCATIONS)
sel_4.SetFieldType(vtkSelectionNode.CELL)
locations = vtkDoubleArray()
locations.SetNumberOfComponents(3)
locations.SetNumberOfTuples(XCELLS)
for i in range(XCELLS):
    val = i + 0.5
    locations.SetTuple3(i, val, val, val)
sel_4.SetSelectionList(locations)
selection.AddNode(sel_4)

# Node 5: threshold-based selection on cells with connected layers
sel_5 = vtkSelectionNode()
sel_5.SetContentType(vtkSelectionNode.THRESHOLDS)
sel_5.SetFieldType(vtkSelectionNode.CELL)
thresholds = vtkIdTypeArray()
thresholds.SetName("Cell Count")
thresholds.SetNumberOfComponents(2)
thresholds.SetNumberOfTuples(2)
thresholds.SetTuple2(0, 3350, 4000)
thresholds.SetTuple2(1, 2000, 2010)
sel_5.SetSelectionList(thresholds)
sel_5.GetProperties().Set(vtkSelectionNode.CONNECTED_LAYERS(), 3)
sel_5.GetProperties().Set(vtkSelectionNode.CONNECTED_LAYERS_REMOVE_SEED(), 1)
sel_5.GetProperties().Set(vtkSelectionNode.CONNECTED_LAYERS_REMOVE_INTERMEDIATE_LAYERS(), 1)
selection.AddNode(sel_5)

# Extract selection
extract_selection = vtkExtractSelection()
extract_selection.SetInputData(0, sample_data)
extract_selection.SetInputData(1, selection)
extract_selection.PreserveTopologyOff()
extract_selection.Update()

# Show result
# Renderer
renderer = vtkRenderer()

# Display extraction result colored by cell data
result_copy = extract_selection.GetOutput().NewInstance()
result_copy.DeepCopy(extract_selection.GetOutput())
color_array = sample_data.GetCellData().GetArray(0)
result_copy.GetCellData().SetActiveScalars(color_array.GetName())
mapper = vtkDataSetMapper()
mapper.SetInputData(result_copy)
mapper.SetScalarModeToUseCellData()
scalar_range = color_array.GetRange()
mapper.SetScalarRange(scalar_range[0], scalar_range[1])
actor = vtkActor()
actor.SetPosition(0, 0, 0)
actor.SetMapper(mapper)
actor.GetProperty().SetPointSize(6.0)
renderer.AddActor(actor)

# Window
render_window = vtkRenderWindow()
render_window.SetMultiSamples(0)
render_window.SetSize(600, 600)
render_window.AddRenderer(renderer)
render_window.SetWindowName("extraction expression")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.ResetCamera()

interactor.Initialize()
interactor.Start()
