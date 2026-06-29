#!/usr/bin/env python

# Compare vtkContour3DLinearGrid on tetra, voxel, and hex meshes
# against standard vtkContourFilter in four viewports.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import vtkPoints
from vtkmodules.vtkCommonDataModel import (
    vtkQuadric,
    vtkStructuredGrid,
)
from vtkmodules.vtkFiltersCore import (
    vtkContour3DLinearGrid,
    vtkContourFilter,
    vtkExtractCells,
)
from vtkmodules.vtkFiltersGeneral import vtkClipVolume
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
interpolate_attr = 1
compute_normals = 1

# Source: sample a quadric function
quadric = vtkQuadric()
quadric.SetCoefficients(0.5, 1, 0.2, 0, 0.1, 0, 0, 0.2, 0, 0)

sample = vtkSampleFunction()
sample.SetSampleDimensions(resolution, resolution, resolution)
sample.SetImplicitFunction(quadric)
sample.ComputeNormalsOn()
sample.Update()

# --- Top-left: tetra contouring ---

# Clip to generate tetrahedra
clip = vtkClipVolume()
clip.SetInputConnection(sample.GetOutputPort())
clip.SetValue(-10.0)
clip.GenerateClippedOutputOff()
clip.Update()

contour_tetra = vtkContour3DLinearGrid()
contour_tetra.SetInputConnection(clip.GetOutputPort())
contour_tetra.SetValue(0, 0.5)
contour_tetra.SetValue(1, 0.9)
contour_tetra.SetMergePoints(0)
contour_tetra.SetSequentialProcessing(0)
contour_tetra.SetInterpolateAttributes(0)
contour_tetra.SetComputeNormals(0)

tetra_mapper = vtkPolyDataMapper()
tetra_mapper.SetInputConnection(contour_tetra.GetOutputPort())
tetra_mapper.ScalarVisibilityOff()

tetra_actor = vtkActor()
tetra_actor.SetMapper(tetra_mapper)
tetra_actor.GetProperty().SetColor(0.8, 0.4, 0.4)

# --- Top-right: voxel contouring ---

extract_voxel = vtkExtractCells()
extract_voxel.SetInputConnection(sample.GetOutputPort())
extract_voxel.AddCellRange(0, sample.GetOutput().GetNumberOfCells())
extract_voxel.Update()

contour_voxel = vtkContour3DLinearGrid()
contour_voxel.SetInputConnection(extract_voxel.GetOutputPort())
contour_voxel.SetValue(0, 0.5)
contour_voxel.SetValue(1, 0.9)
contour_voxel.SetMergePoints(merge_points)
contour_voxel.SetSequentialProcessing(0)
contour_voxel.SetInterpolateAttributes(interpolate_attr)
contour_voxel.SetComputeNormals(compute_normals)

voxel_mapper = vtkPolyDataMapper()
voxel_mapper.SetInputConnection(contour_voxel.GetOutputPort())
voxel_mapper.ScalarVisibilityOff()

voxel_actor = vtkActor()
voxel_actor.SetMapper(voxel_mapper)
voxel_actor.GetProperty().SetColor(0.8, 0.4, 0.4)

# --- Bottom-left: hex contouring ---

# Build a structured grid with hex cells reusing sample scalars
structured_grid = vtkStructuredGrid()
structured_grid.SetDimensions(resolution, resolution, resolution)

hex_points = vtkPoints()
origin = sample.GetOutput().GetOrigin()
spacing = sample.GetOutput().GetSpacing()
for k in range(resolution):
    z = origin[2] + k * spacing[2]
    for j in range(resolution):
        y = origin[1] + j * spacing[1]
        for i in range(resolution):
            x = origin[0] + i * spacing[0]
            hex_points.InsertNextPoint(x, y, z)
structured_grid.SetPoints(hex_points)
structured_grid.GetPointData().SetScalars(sample.GetOutput().GetPointData().GetScalars())
structured_grid.GetPointData().SetVectors(sample.GetOutput().GetPointData().GetVectors())

extract_hex = vtkExtractCells()
extract_hex.SetInputData(structured_grid)
extract_hex.AddCellRange(0, sample.GetOutput().GetNumberOfCells())
extract_hex.Update()

contour_hex = vtkContour3DLinearGrid()
contour_hex.SetInputConnection(extract_hex.GetOutputPort())
contour_hex.SetValue(0, 0.5)
contour_hex.SetMergePoints(merge_points)
contour_hex.SetSequentialProcessing(0)
contour_hex.SetInterpolateAttributes(interpolate_attr)
contour_hex.SetComputeNormals(compute_normals)

hex_mapper = vtkPolyDataMapper()
hex_mapper.SetInputConnection(contour_hex.GetOutputPort())
hex_mapper.ScalarVisibilityOff()

hex_actor = vtkActor()
hex_actor.SetMapper(hex_mapper)
hex_actor.GetProperty().SetColor(0.8, 0.4, 0.4)

# --- Bottom-right: standard contour filter on hexes ---

contour_standard = vtkContourFilter()
contour_standard.SetInputConnection(extract_hex.GetOutputPort())
contour_standard.SetValue(0, 0.5)

standard_mapper = vtkPolyDataMapper()
standard_mapper.SetInputConnection(contour_standard.GetOutputPort())
standard_mapper.ScalarVisibilityOff()

standard_actor = vtkActor()
standard_actor.SetMapper(standard_mapper)
standard_actor.GetProperty().SetColor(0.8, 0.4, 0.4)

# Update and print info
contour_tetra.Update()
contour_voxel.Update()
contour_hex.Update()
contour_standard.Update()

print(f"Tetra: {contour_tetra.GetOutput().GetNumberOfPoints()} pts, {contour_tetra.GetOutput().GetNumberOfCells()} cells")
print(f"Voxel: {contour_voxel.GetOutput().GetNumberOfPoints()} pts, {contour_voxel.GetOutput().GetNumberOfCells()} cells")
print(f"Hex: {contour_hex.GetOutput().GetNumberOfPoints()} pts, {contour_hex.GetOutput().GetNumberOfCells()} cells")
print(f"Standard: {contour_standard.GetOutput().GetNumberOfPoints()} pts, {contour_standard.GetOutput().GetNumberOfCells()} cells")

# Four viewports
renderer_0 = vtkRenderer()
renderer_0.SetViewport(0, 0, 0.5, 0.5)
renderer_0.SetBackground(1, 1, 1)
renderer_0.AddActor(tetra_actor)

renderer_1 = vtkRenderer()
renderer_1.SetViewport(0.5, 0, 1, 0.5)
renderer_1.SetBackground(1, 1, 1)
renderer_1.AddActor(voxel_actor)

renderer_2 = vtkRenderer()
renderer_2.SetViewport(0, 0.5, 0.5, 1)
renderer_2.SetBackground(1, 1, 1)
renderer_2.AddActor(hex_actor)

renderer_3 = vtkRenderer()
renderer_3.SetViewport(0.5, 0.5, 1, 1)
renderer_3.SetBackground(1, 1, 1)
renderer_3.AddActor(standard_actor)

# Window
render_window = vtkRenderWindow()
render_window.SetMultiSamples(0)
render_window.AddRenderer(renderer_0)
render_window.AddRenderer(renderer_1)
render_window.AddRenderer(renderer_2)
render_window.AddRenderer(renderer_3)
render_window.SetWindowName("contour3d lineargrid")

# Scene
renderer_0.ResetCamera()
camera = renderer_0.GetActiveCamera()
renderer_1.SetActiveCamera(camera)
renderer_2.SetActiveCamera(camera)
renderer_3.SetActiveCamera(camera)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
