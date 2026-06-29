#!/usr/bin/env python

# Demonstrate vtkOutlineFilter with composite dataset input, showing
# four outline styles: Root, Leafs, RootAndLeafs, and SpecifiedIndex
# in a four-viewport layout.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonDataModel import vtkMultiBlockDataSet, vtkQuadric
from vtkmodules.vtkFiltersCore import vtkExtractCells
from vtkmodules.vtkFiltersModeling import vtkOutlineFilter
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkImagingHybrid import vtkSampleFunction
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

resolution = 50

# Left quadric sample
quadric_l = vtkQuadric()
quadric_l.SetCoefficients([0.5, 1, 0.2, 0, 0.1, 0, 0, 0.2, 0, 0])
sample_l = vtkSampleFunction()
sample_l.SetModelBounds(-1, 0, -1, 1, -1, 1)
sample_l.SetSampleDimensions(int(resolution / 2), resolution, resolution)
sample_l.SetImplicitFunction(quadric_l)
sample_l.ComputeNormalsOn()
sample_l.Update()

# Right quadric sample
quadric_r = vtkQuadric()
quadric_r.SetCoefficients([0.5, 1, 0.2, 0, 0.1, 0, 0, 0.2, 0, 0])
sample_r = vtkSampleFunction()
sample_r.SetModelBounds(0, 1, -1, 1, -1, 1)
sample_r.SetSampleDimensions(int(resolution / 2), resolution, resolution)
sample_r.SetImplicitFunction(quadric_r)
sample_r.ComputeNormalsOn()
sample_r.Update()

# Extract voxel cells
extract_l = vtkExtractCells()
extract_l.SetInputConnection(sample_l.GetOutputPort())
extract_l.AddCellRange(0, sample_l.GetOutput().GetNumberOfCells())
extract_l.Update()

extract_r = vtkExtractCells()
extract_r.SetInputConnection(sample_r.GetOutputPort())
extract_r.AddCellRange(0, sample_r.GetOutput().GetNumberOfCells())
extract_r.Update()

# Sphere for extra polydata block
sphere = vtkSphereSource()
sphere.SetCenter(1, 0, 0)
sphere.Update()

# Composite dataset
composite = vtkMultiBlockDataSet()
composite.SetBlock(0, extract_l.GetOutput())
composite.SetBlock(1, extract_r.GetOutput())
composite.SetBlock(2, sphere.GetOutput())

# Outline around everything (Root style with faces)
outline_filter = vtkOutlineFilter()
outline_filter.SetInputData(composite)
outline_filter.SetCompositeStyleToRoot()
outline_filter.GenerateFacesOn()

outline_mapper = vtkPolyDataMapper()
outline_mapper.SetInputConnection(outline_filter.GetOutputPort())

outline_actor = vtkActor()
outline_actor.SetMapper(outline_mapper)
outline_actor.GetProperty().SetColor(1, 0, 0)

# Outline around composite pieces (Leafs style)
composite_outline_filter = vtkOutlineFilter()
composite_outline_filter.SetInputData(composite)
composite_outline_filter.SetCompositeStyleToLeafs()

composite_outline_mapper = vtkPolyDataMapper()
composite_outline_mapper.SetInputConnection(composite_outline_filter.GetOutputPort())

composite_outline_actor = vtkActor()
composite_outline_actor.SetMapper(composite_outline_mapper)
composite_outline_actor.GetProperty().SetColor(0, 0, 0)

# Outline around root and leafs
outline_filter_2 = vtkOutlineFilter()
outline_filter_2.SetInputData(composite)
outline_filter_2.SetCompositeStyleToRootAndLeafs()

outline_mapper_2 = vtkPolyDataMapper()
outline_mapper_2.SetInputConnection(outline_filter_2.GetOutputPort())

outline_actor_2 = vtkActor()
outline_actor_2.SetMapper(outline_mapper_2)
outline_actor_2.GetProperty().SetColor(0, 0, 1)

# Outline around specified index with faces
outline_filter_3 = vtkOutlineFilter()
outline_filter_3.SetInputData(composite)
outline_filter_3.SetCompositeStyleToSpecifiedIndex()
outline_filter_3.AddIndex(3)
outline_filter_3.GenerateFacesOn()

outline_mapper_3 = vtkPolyDataMapper()
outline_mapper_3.SetInputConnection(outline_filter_3.GetOutputPort())

outline_actor_3 = vtkActor()
outline_actor_3.SetMapper(outline_mapper_3)
outline_actor_3.GetProperty().SetColor(0, 1, 0)

# Four renderers sharing a camera
renderer_0 = vtkRenderer()
renderer_0.SetBackground(1, 1, 1)
renderer_0.SetViewport(0, 0, 0.25, 1)
renderer_0.AddActor(outline_actor)

camera = renderer_0.GetActiveCamera()

renderer_1 = vtkRenderer()
renderer_1.SetBackground(1, 1, 1)
renderer_1.SetViewport(0.25, 0, 0.5, 1)
renderer_1.SetActiveCamera(camera)
renderer_1.AddActor(composite_outline_actor)

renderer_2 = vtkRenderer()
renderer_2.SetBackground(1, 1, 1)
renderer_2.SetViewport(0.5, 0, 0.75, 1)
renderer_2.SetActiveCamera(camera)
renderer_2.AddActor(outline_actor_2)

renderer_3 = vtkRenderer()
renderer_3.SetBackground(1, 1, 1)
renderer_3.SetViewport(0.75, 0, 1, 1)
renderer_3.SetActiveCamera(camera)
renderer_3.AddActor(outline_actor_3)

# Window
render_window = vtkRenderWindow()
render_window.SetSize(600, 150)
render_window.SetMultiSamples(0)
render_window.AddRenderer(renderer_0)
render_window.AddRenderer(renderer_1)
render_window.AddRenderer(renderer_2)
render_window.AddRenderer(renderer_3)
render_window.SetWindowName("outline filter")

# Scene
renderer_0.ResetCamera()

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
