#!/usr/bin/env python

# Contour a composite (multi-block) dataset using vtkContour3DLinearGrid
# with a vtkSpanSpace scalar tree, including a polydata block that is skipped.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonDataModel import (
    vtkMultiBlockDataSet,
    vtkQuadric,
)
from vtkmodules.vtkCommonExecutionModel import vtkSpanSpace
from vtkmodules.vtkFiltersCore import (
    vtkContour3DLinearGrid,
    vtkExtractCells,
)
from vtkmodules.vtkFiltersModeling import vtkOutlineFilter
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkImagingHybrid import vtkSampleFunction
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkCompositePolyDataMapper,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

resolution = 50
merge_points = 1
interpolate_attr = 0
compute_normals = 0

# Left half of the volume
quadric_left = vtkQuadric()
quadric_left.SetCoefficients(0.5, 1, 0.2, 0, 0.1, 0, 0, 0.2, 0, 0)

sample_left = vtkSampleFunction()
sample_left.SetModelBounds(-1, 0, -1, 1, -1, 1)
sample_left.SetSampleDimensions(int(resolution / 2), resolution, resolution)
sample_left.SetImplicitFunction(quadric_left)
sample_left.ComputeNormalsOn()
sample_left.Update()

# Right half of the volume
quadric_right = vtkQuadric()
quadric_right.SetCoefficients(0.5, 1, 0.2, 0, 0.1, 0, 0, 0.2, 0, 0)

sample_right = vtkSampleFunction()
sample_right.SetModelBounds(0, 1, -1, 1, -1, 1)
sample_right.SetSampleDimensions(int(resolution / 2), resolution, resolution)
sample_right.SetImplicitFunction(quadric_right)
sample_right.ComputeNormalsOn()
sample_right.Update()

# Extract voxel cells from left and right
extract_left = vtkExtractCells()
extract_left.SetInputConnection(sample_left.GetOutputPort())
extract_left.AddCellRange(0, sample_left.GetOutput().GetNumberOfCells())
extract_left.Update()

extract_right = vtkExtractCells()
extract_right.SetInputConnection(sample_right.GetOutputPort())
extract_right.AddCellRange(0, sample_right.GetOutput().GetNumberOfCells())
extract_right.Update()

# Extra polydata block (should be skipped by the contour filter)
sphere = vtkSphereSource()
sphere.SetCenter(1, 0, 0)
sphere.Update()

# Assemble composite dataset
composite = vtkMultiBlockDataSet()
composite.SetBlock(0, extract_left.GetOutput())
composite.SetBlock(1, extract_right.GetOutput())
composite.SetBlock(2, sphere.GetOutput())

# Scalar tree cloned for each composite piece
scalar_tree = vtkSpanSpace()
scalar_tree.SetDataSet(extract_left.GetOutput())
scalar_tree.ComputeResolutionOn()
scalar_tree.SetScalarRange(0.25, 0.75)
scalar_tree.SetComputeScalarRange(0)

# Contour with scalar tree
contour = vtkContour3DLinearGrid()
contour.SetInputData(composite)
contour.SetValue(0, 0.5)
contour.SetMergePoints(merge_points)
contour.SetSequentialProcessing(0)
contour.SetInterpolateAttributes(interpolate_attr)
contour.SetComputeNormals(compute_normals)
contour.UseScalarTreeOn()
contour.SetScalarTree(scalar_tree)

contour_mapper = vtkCompositePolyDataMapper()
contour_mapper.SetInputConnection(contour.GetOutputPort())
contour_mapper.ScalarVisibilityOff()

contour_actor = vtkActor()
contour_actor.SetMapper(contour_mapper)
contour_actor.GetProperty().SetColor(0.8, 0.4, 0.4)

# Outline of the composite
outline_filter = vtkOutlineFilter()
outline_filter.SetInputData(composite)

outline_mapper = vtkPolyDataMapper()
outline_mapper.SetInputConnection(outline_filter.GetOutputPort())

outline_actor = vtkActor()
outline_actor.SetMapper(outline_mapper)
outline_actor.GetProperty().SetColor(0, 0, 0)

contour.Update()
print(f"Contour points: {contour.GetOutput().GetNumberOfPoints()}")
print(f"Contour cells: {contour.GetOutput().GetNumberOfCells()}")

# Renderer
renderer = vtkRenderer()
renderer.SetBackground(1, 1, 1)
renderer.AddActor(contour_actor)
renderer.AddActor(outline_actor)

# Window
render_window = vtkRenderWindow()
render_window.SetSize(200, 200)
render_window.SetMultiSamples(0)
render_window.AddRenderer(renderer)
render_window.SetWindowName("contour3d lineargrid composite input")

# Scene
renderer.ResetCamera()

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
