#!/usr/bin/env python

# Compare vtkContour3DLinearGrid with and without a vtkSpanSpace scalar tree,
# and against standard vtkContourFilter, in two viewports.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import vtkFloatArray
from vtkmodules.vtkCommonDataModel import (
    vtkDataObject,
    vtkQuadric,
    vtkUnstructuredGrid,
)
from vtkmodules.vtkCommonExecutionModel import vtkSpanSpace
from vtkmodules.vtkFiltersCore import (
    vtkContour3DLinearGrid,
    vtkContourFilter,
    vtkExtractCells,
)
from vtkmodules.vtkImagingHybrid import vtkSampleFunction
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

resolution = 50
merge_points = 1
interpolate_attr = 0
compute_normals = 0

# Source: sample a quadric function
quadric = vtkQuadric()
quadric.SetCoefficients(0.5, 1, 0.2, 0, 0.1, 0, 0, 0.2, 0, 0)

sample = vtkSampleFunction()
sample.SetSampleDimensions(resolution, resolution, resolution)
sample.SetImplicitFunction(quadric)
sample.ComputeNormalsOn()
sample.Update()

# Extract voxel cells
extract = vtkExtractCells()
extract.SetInputConnection(sample.GetOutputPort())
extract.AddCellRange(0, sample.GetOutput().GetNumberOfCells())
extract.Update()

# Deep copy to add a zeros array
grid = vtkUnstructuredGrid()
grid.DeepCopy(extract.GetOutput())

zeros = vtkFloatArray()
zeros.SetNumberOfTuples(grid.GetNumberOfPoints())
zeros.Fill(0.0)
zeros.SetName("zeros")
grid.GetPointData().AddArray(zeros)

# Scalar tree
scalar_tree = vtkSpanSpace()
scalar_tree.SetDataSet(grid)
scalar_tree.SetNumberOfCellsPerBucket(1)

# Contour without scalar tree
contour_no_tree = vtkContour3DLinearGrid()
contour_no_tree.SetInputData(grid)
contour_no_tree.SetValue(0, 0.5)
contour_no_tree.SetValue(1, 0.75)
contour_no_tree.SetMergePoints(merge_points)
contour_no_tree.SetSequentialProcessing(0)
contour_no_tree.SetInterpolateAttributes(interpolate_attr)
contour_no_tree.SetComputeNormals(compute_normals)
contour_no_tree.UseScalarTreeOff()

contour_no_tree_mapper = vtkPolyDataMapper()
contour_no_tree_mapper.SetInputConnection(contour_no_tree.GetOutputPort())
contour_no_tree_mapper.ScalarVisibilityOff()

contour_no_tree_actor = vtkActor()
contour_no_tree_actor.SetMapper(contour_no_tree_mapper)
contour_no_tree_actor.GetProperty().SetColor(0.8, 0.4, 0.4)

# Standard contour filter for comparison
contour_standard = vtkContourFilter()
contour_standard.SetInputConnection(extract.GetOutputPort())
contour_standard.SetValue(0, 0.5)
contour_standard.SetValue(1, 0.75)

contour_standard_mapper = vtkPolyDataMapper()
contour_standard_mapper.SetInputConnection(contour_standard.GetOutputPort())
contour_standard_mapper.ScalarVisibilityOff()

contour_standard_actor = vtkActor()
contour_standard_actor.SetMapper(contour_standard_mapper)
contour_standard_actor.GetProperty().SetColor(0.8, 0.4, 0.4)

# Update and print info
contour_no_tree.Update()
contour_standard.Update()

print(f"3D linear (no tree): {contour_no_tree.GetOutput().GetNumberOfPoints()} pts, {contour_no_tree.GetOutput().GetNumberOfCells()} cells")
print(f"Standard contour: {contour_standard.GetOutput().GetNumberOfPoints()} pts, {contour_standard.GetOutput().GetNumberOfCells()} cells")

# Two viewports
renderer_0 = vtkRenderer()
renderer_0.SetViewport(0, 0, 0.5, 1)
renderer_0.SetBackground(1, 1, 1)
renderer_0.AddActor(contour_no_tree_actor)

renderer_1 = vtkRenderer()
renderer_1.SetViewport(0.5, 0, 1, 1)
renderer_1.SetBackground(1, 1, 1)
renderer_1.AddActor(contour_standard_actor)

# Window
render_window = vtkRenderWindow()
render_window.SetSize(400, 200)
render_window.SetMultiSamples(0)
render_window.AddRenderer(renderer_0)
render_window.AddRenderer(renderer_1)
render_window.SetWindowName("contour3d lineargrid scalar tree")

# Scene
renderer_0.ResetCamera()
renderer_1.SetActiveCamera(renderer_0.GetActiveCamera())

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
